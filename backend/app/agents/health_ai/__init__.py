"""
Health-AI - The Meta-Agent

Health-AI (愛佳) is the unified AI consciousness of Health-AICare Support.
She orchestrates all four Safety Agent Suite agents based on user role and intent.

Architecture:
- Meta-agent that coordinates STA, TCA, CMA, and IA
- Role-based routing (user, counselor, admin)
- LangGraph-powered orchestration with direct invocation (agentic pattern)
- Unified personality across all interactions

Name meaning:
- 愛 (Ai) = Love, affection
- 佳 (Ka) = Excellent, beautiful

⚠️ IMPORTANT: Use the cached agent singleton, NOT per-request compilation!
  from app.agents.health_ai_orchestrator_graph import get_health_ai_agent
  health-ai = get_health_ai_agent()  # compiled once at startup, reused per request
  result = await health-ai.ainvoke(state, config={"configurable": {"thread_id": "...", "db": db}})
"""

# ✅ REMOVED: Legacy HealthAIOrchestrator - use health_ai_orchestrator_graph.py instead
from .identity import HEALTH_AI_IDENTITY, HEALTH_AI_SYSTEM_PROMPTS, HEALTH_AI_GREETINGS, HEALTH_AI_CAPABILITIES
from .state import AikaState, AikaResponseMetadata
from .tools import get_health_ai_tools, execute_tool_call

__all__ = [
    # ❌ DEPRECATED: "HealthAIOrchestrator" - Use create_health_ai_agent_with_checkpointing instead
    "HEALTH_AI_IDENTITY",
    "HEALTH_AI_SYSTEM_PROMPTS",
    "HEALTH_AI_GREETINGS",
    "HEALTH_AI_CAPABILITIES",
    "AikaState",
    "AikaResponseMetadata",
    "get_health_ai_tools",
    "execute_tool_call",
]
