from typing import Dict, Any, Tuple
from app.database.types import AutopilotActionType, AutopilotPolicyDecision, AutopilotActionStatus

class AutopilotPolicyEngine:
    """
    Governance policy engine evaluating risk levels and approval criteria for automated AI actions.
    """

    @staticmethod
    def evaluate_action(
        action_type: AutopilotActionType,
        payload: Dict[str, Any]
    ) -> Tuple[AutopilotPolicyDecision, AutopilotActionStatus, bool, str]:
        """
        Evaluate proposed action and return (policy_decision, action_status, requires_human_review, risk_level).
        """
        # 1. Low Risk Actions -> Auto-approved
        if action_type in [AutopilotActionType.grant_badge_nft, AutopilotActionType.add_game_xp]:
            return (
                AutopilotPolicyDecision.auto_approved,
                AutopilotActionStatus.queued,
                False,
                "low"
            )

        # 2. Moderate Risk Actions -> Manual Admin Review required
        elif action_type in [AutopilotActionType.book_counseling_appointment, AutopilotActionType.create_escalation_ticket]:
            return (
                AutopilotPolicyDecision.needs_review,
                AutopilotActionStatus.pending_review,
                True,
                "moderate"
            )

        # 3. High Risk Actions -> Blocked by default
        elif action_type in [AutopilotActionType.export_clinical_data, AutopilotActionType.modify_token_balance]:
            return (
                AutopilotPolicyDecision.blocked,
                AutopilotActionStatus.rejected,
                False,
                "high"
            )

        else:
            return (
                AutopilotPolicyDecision.blocked,
                AutopilotActionStatus.rejected,
                False,
                "high"
            )

policy_engine = AutopilotPolicyEngine()
