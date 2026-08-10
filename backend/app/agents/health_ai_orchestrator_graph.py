"""Unified HealthAI Orchestrator Graph - LangGraph with HealthAI as First Decision Node.

This module is the assembly point for the unified HealthAI orchestrator.  All
node logic, prompt construction, routing, and background tasks now live in
dedicated sub-modules under ``app/agents/health_ai/``.  This file only wires those
pieces together into a LangGraph ``StateGraph`` and exposes the two public
factory functions below.

Real-time Graph Architecture:
    START -> health_ai_decision_node
                 |
                 |--[high/critical]--> parallel_crisis (SDA/CMA escalation path)
                 |                           |
                 |--[moderate]-----> execute_sca (TCA only)
                 |                           |
                 |--[analytics]----> execute_ia  |
                 |                      |       |
                 '--[direct]---> END    '-------'--> synthesize --> END

Safety Triage Agent (STA) - Post-Conversation Background Task:
    STA does NOT participate in the real-time graph.  It runs separately:
    - Automatically triggered via asyncio.create_task() when a conversation ends.
    - Manually triggerable via the trigger_conversation_analysis tool.
    - Performs deep clinical analysis: risk trend, PHQ-9/GAD-7/DASS-21 screening,
      psychologist report, and CMA referral recommendation.
    - Results persisted to ConversationRiskAssessment and ScreeningProfile tables.

Sub-module map:
    health_ai/constants.py        Static data — crisis keywords, smalltalk vocab.
    health_ai/message_classifier.py  Pure classification helpers.
    health_ai/prompt_builder.py   Prompt construction helpers.
    health_ai/decision_node.py    health_ai_decision_node — first orchestrator node.
    health_ai/background_tasks.py Fire-and-forget STA analysis + screening update.
    health_ai/subgraph_nodes.py   TCA, CMA, IA, synthesize node implementations.
    health_ai/routing.py          Conditional edge functions for the graph.
"""
from __future__ import annotations

import logging
from typing import Any, Optional, TYPE_CHECKING

from langgraph.graph import StateGraph, END

from app.agents.graph_state import HealthAIOrchestratorState

# ---------------------------------------------------------------------------
# Re-export extracted nodes and utilities so external import paths remain
# stable.  Any code that does ``from app.agents.health_ai_orchestrator_graph import
# health_ai_decision_node`` (or any other name below) will continue to work.
# ---------------------------------------------------------------------------
from app.agents.health_ai.decision_node import health_ai_decision_node
from app.agents.health_ai.background_tasks import trigger_sta_conversation_analysis_background
from app.agents.health_ai.message_classifier import (
    detect_crisis_keywords as _detect_crisis_keywords,
    is_smalltalk_message as _is_smalltalk_message,
)
from app.agents.health_ai.prompt_builder import (
    normalize_role as _normalize_user_role,
    format_personal_memory_block as _format_personal_memory_block,
)
from app.agents.health_ai.subgraph_nodes import (
    _AsyncInvokable,
    parallel_crisis_node,
    execute_sca_subgraph,
    execute_sda_subgraph,
    execute_ia_subgraph,
    synthesize_final_response,
    execute_sta_subgraph,
)
from app.agents.health_ai.routing import (
    should_invoke_agents,
    ROUTE_CRISIS_PARALLEL,
    ROUTE_TCA,
    ROUTE_IA,
    ROUTE_END,
)

# Lazy TYPE_CHECKING imports kept for IDE/type-checker support only.
if TYPE_CHECKING:
    from app.agents.sta.sta_graph import create_sta_graph
    from app.agents.tca.tca_graph import get_tca_graph
    from app.agents.cma.cma_graph import get_cma_graph
    from app.agents.ia.ia_graph import get_ia_graph

logger = logging.getLogger(__name__)


# ============================================================================
# MODULE-LEVEL AGENT SINGLETON
# Compiled once at FastAPI startup (lifespan) and reused across all requests.
# This avoids re-compiling the graph (and re-binding db sessions) on every
# HTTP request, which was the previous per-request pattern.
# ============================================================================

_compiled_agent: Any = None


def set_health_ai_agent(agent: Any) -> None:
    """Store the app-lifetime compiled HealthAI agent.

    Called exactly once from the FastAPI lifespan handler after the database
    and checkpointer have been initialised.  Subsequent requests retrieve the
    cached agent via ``get_health_ai_agent()`` and inject the per-request
    ``db`` session via ``config["configurable"]["db"]``.
    """
    global _compiled_agent
    _compiled_agent = agent
    logger.info(
        "HealthAI agent singleton registered: %s",
        type(agent).__name__,
    )


def get_health_ai_agent() -> Any:
    """Return the cached compiled HealthAI agent.

    Returns ``None`` before the FastAPI lifespan has completed startup.
    Call sites should guard against this (requests arriving before startup
    are extremely unlikely but possible under heavy load during cold start).
    """
    return _compiled_agent


# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================

def create_health_ai_unified_graph() -> StateGraph:
    """Assemble and return the uncompiled HealthAI orchestrator StateGraph.

    Graph structure::

        START
          |
          +-- health_ai_decision --+-- [cma]   --> parallel_crisis --> synthesize --> END
                              |-- [tca]   --> execute_sca     --> synthesize --> END
                              |-- [ia]    --> execute_ia       --> synthesize --> END
                              '--[direct]                                     --> END

    STA is NOT a node in this graph.  It runs as a fire-and-forget background
    task (trigger_sta_conversation_analysis_background) when a conversation
    ends, or can be triggered manually via the trigger_conversation_analysis
    tool.  execute_sda (CMA) is not registered as a standalone node; it is
    invoked exclusively inside parallel_crisis_node.

    ``db`` is no longer bound at compile time.  Each node receives it at
    invocation time via ``config["configurable"]["db"]``, which allows this
    compiled graph to be shared across all requests.

    Returns:
        Uncompiled StateGraph ready to be compiled with ``.compile()``.
    """
    workflow = StateGraph(HealthAIOrchestratorState)

    # Nodes accept (state, config) — db is injected via config["configurable"],
    # so no functools.partial binding is needed here.
    workflow.add_node("health_ai_decision", health_ai_decision_node)
    workflow.add_node("parallel_crisis", parallel_crisis_node)
    workflow.add_node("execute_sca", execute_sca_subgraph)
    workflow.add_node("execute_ia", execute_ia_subgraph)
    workflow.add_node("synthesize", synthesize_final_response)

    # Entry point
    workflow.set_entry_point("health_ai_decision")

    # Conditional fan-out after the decision node
    workflow.add_conditional_edges(
        "health_ai_decision",
        should_invoke_agents,
        {
            ROUTE_CRISIS_PARALLEL: "parallel_crisis",
            ROUTE_TCA: "execute_sca",
            ROUTE_IA: "execute_ia",
            ROUTE_END: END,
        },
    )

    # All non-direct paths converge at synthesize, then exit.
    workflow.add_edge("execute_sca", "synthesize")
    workflow.add_edge("parallel_crisis", "synthesize")
    workflow.add_edge("execute_ia", "synthesize")
    workflow.add_edge("synthesize", END)

    logger.info("Unified HealthAI orchestrator graph created.")

    return workflow


def create_health_ai_agent_with_checkpointing(
    checkpointer: Optional[Any] = None,
) -> Any:
    """Compile the HealthAI agent with optional conversation-persistent checkpointing.

    Intended to be called **once** at FastAPI startup (via the lifespan handler)
    and stored as ``app.state.health_ai_agent`` or via ``set_health_ai_agent()``.
    Subsequent requests retrieve the compiled agent with ``get_health_ai_agent()``
    and inject the per-request ``db`` session through LangGraph's config::

        result = await health_ai_agent.ainvoke(
            initial_state,
            config={
                "configurable": {
                    "thread_id": f"user_{uid}_session_{sid}",
                    "db": db,               # <-- injected here, not at compile time
                }
            },
        )

    Example — in-memory (testing / dev)::

        from langgraph.checkpoint.memory import MemorySaver
        health_ai = create_health_ai_agent_with_checkpointing(MemorySaver())

    Example — Postgres (production)::

        health_ai = create_health_ai_agent_with_checkpointing(get_langgraph_checkpointer())

    Args:
        checkpointer: Optional LangGraph checkpointer.  When ``None``, a
                      stateless (no conversation memory) graph is returned.

    Returns:
        CompiledGraph ready for direct invocation.
    """
    workflow = create_health_ai_unified_graph()

    if checkpointer:
        logger.info(
            "HealthAI agent compiled WITH checkpointing: %s",
            type(checkpointer).__name__,
        )
        return workflow.compile(checkpointer=checkpointer)

    logger.warning("HealthAI agent compiled WITHOUT checkpointing (stateless).")
    return workflow.compile()


# Public alias for app router/test import compatibility
health_ai_graph = create_health_ai_agent_with_checkpointing()

