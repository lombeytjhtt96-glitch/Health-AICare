"""HealthAI orchestrator - conditional routing functions.

LangGraph evaluates these functions after each node to decide which edge to
follow.  They are kept deliberately thin: each one reads a small number of
state fields, traces the chosen edge, and returns a LangGraph route key.

No external I/O is performed - the only side effect is a call to
execution_tracker.trigger_edge, which records the routing decision for
observability dashboards.

Public API (actively wired in the graph):
    should_invoke_agents    Conditional edge after 'health_ai_decision'.

Legacy (not wired — retained for manual tooling only):
    should_route_to_sca     Post-STA routing; STA is now background-only.
"""
from __future__ import annotations

import logging

from app.agents.execution_tracker import execution_tracker
from app.agents.graph_state import HealthAIOrchestratorState

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Route-key constants — kept here so callers that build the graph's
# ``conditional_edge`` mapping can import them instead of using plain strings.
# ---------------------------------------------------------------------------

ROUTE_CRISIS_PARALLEL = "invoke_crisis_parallel"
ROUTE_TCA = "invoke_tca"
ROUTE_IA = "invoke_ia"
ROUTE_END = "end"

ROUTE_SDA = "route_sda"
ROUTE_SCA = "invoke_sca"
ROUTE_SYNTHESIZE = "synthesize"


def should_invoke_agents(state: HealthAIOrchestratorState) -> str:
    """Conditional edge executed after the health_ai_decision node.

    Reads the routing fields set by the decision node and returns the
    LangGraph route key that selects the next node.

    Route keys (see module-level constants):
    - ROUTE_CRISIS_PARALLEL: high/critical risk — route to SDA/CMA escalation.
    - ROUTE_TCA: moderate risk or structured-support request — TCA only.
    - ROUTE_IA: analytics query from admin or counselor — Insights Agent.
    - ROUTE_END: direct HealthAI response, no sub-agent involvement.

    Priority:
    1. 'next_step' field (set explicitly by decision_node._compute_routing).
    2. 'immediate_risk_level' field (safety-first override).
    3. Ambiguous needs_agents=True with no valid next_step -> safe end.

    Args:
        state: Orchestrator state after health_ai_decision_node ran.

    Returns:
        One of the ROUTE_* string constants defined at the top of this module.
    """
    execution_id = state.get("execution_id")
    next_step = str(state.get("next_step") or "end").lower()
    needs_agents: bool = bool(state.get("needs_agents", False))

    def _trace(edge: str) -> None:
        if execution_id:
            execution_tracker.trigger_edge(
                execution_id, edge, condition_result=True
            )

    # --- Explicit next_step from decision node (highest priority) ---
    if next_step == "cma":
        _trace("health_ai::decision->parallel_crisis")
        logger.warning(
            "Routing after HealthAI: CRISIS ESCALATION (SDA/CMA) risk=%s",
            state.get("immediate_risk_level"),
        )
        return ROUTE_CRISIS_PARALLEL

    if next_step == "tca":
        _trace("health_ai::decision->tca")
        logger.info("Routing after HealthAI: TCA (Support)")
        return ROUTE_TCA

    if next_step == "ia":
        _trace("health_ai::decision->ia")
        logger.info("Routing after HealthAI: IA (Analytics)")
        return ROUTE_IA

    # --- Fallback: resolve ambiguous needs_agents=True via risk level ---
    if needs_agents:
        immediate_risk = str(state.get("immediate_risk_level") or "none")

        if immediate_risk in {"high", "critical"}:
            _trace("health_ai::decision->parallel_crisis")
            return ROUTE_CRISIS_PARALLEL

        if immediate_risk == "moderate":
            _trace("health_ai::decision->tca")
            return ROUTE_TCA

        user_role = str(state.get("user_role", "")).lower()
        if (
            state.get("intent") == "analytics_query"
            and user_role in {"admin", "counselor"}
        ):
            _trace("health_ai::decision->ia")
            return ROUTE_IA

        # needs_agents=True but no valid routing signal — end safely.
        _trace("health_ai::decision->end")
        logger.warning(
            "Ambiguous needs_agents=True without valid route; ending safely."
        )
        return ROUTE_END

    # --- Direct HealthAI response ---
    _trace("health_ai::decision->end")
    logger.info("Routing after HealthAI: Direct Response")
    return ROUTE_END


def should_route_to_sca(state: HealthAIOrchestratorState) -> str:
    """Conditional edge executed after the legacy STA sub-graph node.

    .. deprecated::
        ``execute_sta_subgraph`` is no longer wired in the active graph — STA
        runs exclusively as a background post-conversation task.  This function
        is retained so counselors/admins can re-introduce an inline STA path in
        future without losing the routing logic, and for integration tests that
        exercise the legacy node manually.

        It is NOT re-exported from ``health_ai_orchestrator_graph`` to keep the
        public API surface clean.

    Returns:
        ROUTE_SDA:        High/critical severity — escalate to CMA.
        ROUTE_SCA:        Moderate with TCA recommendation.
        ROUTE_SYNTHESIZE: Low/moderate without intervention — go to synthesis.
    """
    execution_id = state.get("execution_id")
    severity = str(state.get("severity") or "low")
    next_step = str(state.get("next_step") or "end")

    def _trace(edge: str) -> None:
        if execution_id:
            execution_tracker.trigger_edge(
                execution_id, edge, condition_result=True
            )

    if severity in {"high", "critical"}:
        _trace("health_ai::sta->sda")
        logger.info(
            "STA routing: severity=%s → CMA (crisis escalation)", severity
        )
        return ROUTE_SDA

    if next_step == "tca":
        _trace("health_ai::sta->sca")
        logger.info(
            "STA routing: severity=%s, next_step=tca → TCA (support)", severity
        )
        return ROUTE_SCA

    _trace("health_ai::sta->synthesize")
    logger.info(
        "STA routing: severity=%s, next_step=%s → Synthesize",
        severity,
        next_step,
    )
    return ROUTE_SYNTHESIZE
