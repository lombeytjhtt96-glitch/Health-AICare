from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Literal, Set

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# Blockchain imports removed
from app.models import BadgeTemplate, PendingBadgeGrant, User, UserBadge
from app.domains.mental_health.models import Conversation, JournalEntry, PlayerWellnessState
from app.schemas.user import EarnedBadgeInfo

logger = logging.getLogger(__name__)

# Dual-chain minting variables removed


LET_THERE_BE_BADGE_BADGE_ID = 1
TRIPLE_THREAT_OF_THOUGHTS_BADGE_ID = 2
SEVEN_DAYS_A_WEEK_BADGE_ID = 3
TWO_WEEKS_NOTICE_YOU_GAVE_TO_NEGATIVITY_BADGE_ID = 4
FULL_MOON_POSITIVITY_BADGE_ID = 5
QUARTER_CENTURY_OF_JOURNALING_BADGE_ID = 6
UNLEASH_THE_WORDS_BADGE_ID = 7
BESTIES_BADGE_ID = 8

AchievementAction = Literal[
    "manual_sync",
    "journal_saved",
    "quest_completed",
    "wellness_state_updated",
]


@dataclass(frozen=True)
class BadgeRule:
    badge_id: int
    reason: str
    trigger_actions: Set[AchievementAction]
    min_activity_days: int | None = None
    min_streak: int | None = None
    min_journal_count: int | None = None
    # Badge 7: longest single journal entry must reach this word count
    min_word_count: int | None = None
    # Badge 8: highest number of exchanges in any single conversation session
    min_chat_session_messages: int | None = None


DEFAULT_BADGE_RULES: tuple[BadgeRule, ...] = (
    BadgeRule(
        badge_id=LET_THERE_BE_BADGE_BADGE_ID,
        reason="First activity",
        trigger_actions={"manual_sync", "journal_saved", "quest_completed"},
        min_activity_days=1,
    ),
    BadgeRule(
        badge_id=TRIPLE_THREAT_OF_THOUGHTS_BADGE_ID,
        reason="3 days of activity",
        trigger_actions={"manual_sync", "journal_saved", "quest_completed"},
        min_activity_days=3,
    ),
    BadgeRule(
        badge_id=SEVEN_DAYS_A_WEEK_BADGE_ID,
        reason="7-day streak",
        trigger_actions={"manual_sync", "quest_completed", "wellness_state_updated"},
        min_streak=7,
    ),
    BadgeRule(
        badge_id=TWO_WEEKS_NOTICE_YOU_GAVE_TO_NEGATIVITY_BADGE_ID,
        reason="14-day streak",
        trigger_actions={"manual_sync", "quest_completed", "wellness_state_updated"},
        min_streak=14,
    ),
    BadgeRule(
        badge_id=FULL_MOON_POSITIVITY_BADGE_ID,
        reason="30-day streak",
        trigger_actions={"manual_sync", "quest_completed", "wellness_state_updated"},
        min_streak=30,
    ),
    BadgeRule(
        badge_id=QUARTER_CENTURY_OF_JOURNALING_BADGE_ID,
        reason="25 journal entries",
        trigger_actions={"manual_sync", "journal_saved"},
        min_journal_count=25,
    ),
    BadgeRule(
        badge_id=UNLEASH_THE_WORDS_BADGE_ID,
        reason="Journal entry longer than 500 words",
        trigger_actions={"manual_sync", "journal_saved"},
        min_word_count=500,
    ),
    BadgeRule(
        badge_id=BESTIES_BADGE_ID,
        reason="100 messages in a single chat session",
        # No real-time chat trigger exists yet; manual_sync provides the catch-up path.
        trigger_actions={"manual_sync"},
        min_chat_session_messages=100,
    ),
)


@dataclass(frozen=True)
class AchievementMetrics:
    current_streak: int
    journal_count: int
    total_activity_days: int
    # Highest word count across any single journal entry (for badge 7)
    max_entry_word_count: int
    # Highest exchange count in any single conversation session (for badge 8)
    max_chat_session_messages: int


async def _load_achievement_metrics(db: AsyncSession, user: User) -> AchievementMetrics:
    current_streak = (
        await db.execute(
            select(User.current_streak).where(User.id == user.id)
        )
    ).scalar() or 0

    journal_count = (
        await db.execute(
            select(func.count(JournalEntry.id)).filter(JournalEntry.user_id == user.id)
        )
    ).scalar() or 0

    total_activity_days = (
        await db.execute(
            select(func.count(func.distinct(JournalEntry.entry_date))).filter(
                JournalEntry.user_id == user.id
            )
        )
    ).scalar() or 0

    wellness_streak = (
        await db.execute(
            select(PlayerWellnessState.current_streak).where(PlayerWellnessState.user_id == user.id)
        )
    ).scalar() or 0
    current_streak = max(current_streak, int(wellness_streak or 0))

    # Max word count across any single journal entry (badge 7 criterion)
    max_entry_word_count = (
        await db.execute(
            select(func.coalesce(func.max(JournalEntry.word_count), 0)).filter(
                JournalEntry.user_id == user.id
            )
        )
    ).scalar() or 0

    # Max exchanges in any single conversation session (badge 8 criterion).
    # Each Conversation row represents one user-assistant exchange, grouped by session_id.
    session_counts_sq = (
        select(func.count(Conversation.id).label("msg_count"))
        .filter(Conversation.user_id == user.id)
        .group_by(Conversation.session_id)
        .subquery()
    )
    max_chat_session_messages = (
        await db.execute(
            select(func.coalesce(func.max(session_counts_sq.c.msg_count), 0))
        )
    ).scalar() or 0

    return AchievementMetrics(
        current_streak=current_streak,
        journal_count=int(journal_count),
        total_activity_days=int(total_activity_days),
        max_entry_word_count=int(max_entry_word_count),
        max_chat_session_messages=int(max_chat_session_messages),
    )


def _qualifies(rule: BadgeRule, metrics: AchievementMetrics) -> bool:
    if rule.min_activity_days is not None and metrics.total_activity_days < rule.min_activity_days:
        return False
    if rule.min_streak is not None and metrics.current_streak < rule.min_streak:
        return False
    if rule.min_journal_count is not None and metrics.journal_count < rule.min_journal_count:
        return False
    if rule.min_word_count is not None and metrics.max_entry_word_count < rule.min_word_count:
        return False
    if rule.min_chat_session_messages is not None and metrics.max_chat_session_messages < rule.min_chat_session_messages:
        return False
    return True


def _rules_for_action(action: AchievementAction) -> List[BadgeRule]:
    return [rule for rule in DEFAULT_BADGE_RULES if action in rule.trigger_actions]


def _criteria_qualifies(criteria: Dict[str, Any], metrics: AchievementMetrics) -> bool:
    if not criteria:
        return False

    min_activity_days_raw = criteria.get("min_activity_days")
    min_streak_raw = criteria.get("min_streak")
    min_journal_count_raw = criteria.get("min_journal_count")

    min_activity_days = int(min_activity_days_raw) if min_activity_days_raw is not None else None
    min_streak = int(min_streak_raw) if min_streak_raw is not None else None
    min_journal_count = int(min_journal_count_raw) if min_journal_count_raw is not None else None

    if min_activity_days is not None and metrics.total_activity_days < min_activity_days:
        return False
    if min_streak is not None and metrics.current_streak < min_streak:
        return False
    if min_journal_count is not None and metrics.journal_count < min_journal_count:
        return False

    # Admin templates can also specify word-count or chat-session thresholds
    min_word_count_raw = criteria.get("min_word_count")
    min_chat_session_messages_raw = criteria.get("min_chat_session_messages")
    min_word_count = int(min_word_count_raw) if min_word_count_raw is not None else None
    min_chat_session_messages = int(min_chat_session_messages_raw) if min_chat_session_messages_raw is not None else None

    if min_word_count is not None and metrics.max_entry_word_count < min_word_count:
        return False
    if min_chat_session_messages is not None and metrics.max_chat_session_messages < min_chat_session_messages:
        return False

    return True


async def trigger_achievement_check(
    db: AsyncSession,
    user: User,
    *,
    action: AchievementAction,
    fail_on_config_error: bool = False,
) -> List[EarnedBadgeInfo]:
    """Evaluate and award badges relevant to a specific user action locally."""
    import uuid
    candidate_rules = _rules_for_action(action)
    metrics = await _load_achievement_metrics(db, user)

    awarded_badges_res = await db.execute(
        select(UserBadge.badge_id, UserBadge.chain_id).filter(UserBadge.user_id == user.id)
    )
    awarded_badges: Set[tuple[int, int]] = {(int(row[0]), int(row[1])) for row in awarded_badges_res.all()}

    template_stmt = (
        select(BadgeTemplate)
        .where(
            BadgeTemplate.auto_award_enabled.is_(True),
            BadgeTemplate.status == "PUBLISHED",
            BadgeTemplate.auto_award_action == action,
        )
        .order_by(BadgeTemplate.created_at.asc())
    )
    admin_templates = list((await db.execute(template_stmt)).scalars().all())

    if not candidate_rules and not admin_templates:
        return []

    badges_to_add_to_db: List[Dict[str, Any]] = []

    # Local award path: uses chain ID 97 (BSC Testnet / fallback chain) with mock tx hash
    for rule in candidate_rules:
        if _qualifies(rule, metrics):
            chain_id = 97
            badge_key = (rule.badge_id, chain_id)
            if badge_key not in awarded_badges:
                awarded_badges.add(badge_key)
                badges_to_add_to_db.append({
                    "badge_id": rule.badge_id,
                    "chain_id": chain_id,
                    "contract_address": "0x0000000000000000000000000000000000000000",
                    "tx_hash": f"local-tx-{rule.badge_id}-{uuid.uuid4()}",
                })
                logger.info("Badge %s awarded locally for user %s (%s)", rule.badge_id, user.id, rule.reason)

    for template in admin_templates:
        criteria = template.auto_award_criteria or {}
        if not isinstance(criteria, dict):
            logger.warning(
                "Skipping auto-award template %s: criteria must be a JSON object.",
                template.id,
            )
            continue
        if not _criteria_qualifies(criteria, metrics):
            continue

        template_chain_id = int(template.chain_id)
        badge_key = (int(template.token_id), template_chain_id)
        if badge_key not in awarded_badges:
            awarded_badges.add(badge_key)
            badges_to_add_to_db.append({
                "badge_id": int(template.token_id),
                "chain_id": template_chain_id,
                "contract_address": "0x0000000000000000000000000000000000000000",
                "tx_hash": f"local-tx-{template.token_id}-{uuid.uuid4()}",
            })
            logger.info("Admin template badge %s awarded locally for user %s", template.token_id, user.id)

    if not badges_to_add_to_db:
        return []

    current_time = datetime.now()
    newly_awarded_badges: List[EarnedBadgeInfo] = []
    for badge_info in badges_to_add_to_db:
        new_award = UserBadge(
            user_id=user.id,
            badge_id=badge_info["badge_id"],
            contract_address=badge_info["contract_address"],
            transaction_hash=badge_info["tx_hash"],
            chain_id=badge_info["chain_id"],
            awarded_at=current_time,
        )
        db.add(new_award)
        newly_awarded_badges.append(
            EarnedBadgeInfo(
                badge_id=badge_info["badge_id"],
                awarded_at=current_time,
                transaction_hash=badge_info["tx_hash"],
                contract_address=badge_info["contract_address"],
            )
        )

    # Pending grants loop removed since badges are immediately saved to the DB

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        logger.info(
            "Concurrent badge insert detected for user %s; awards likely already persisted.",
            user.id,
        )
        return []
    except Exception:
        await db.rollback()
        raise

    logger.info(
        "Saved %s new badge awards for user %s (action=%s)",
        len(newly_awarded_badges),
        user.id,
        action,
    )
    return newly_awarded_badges


async def sync_user_achievements(
    db: AsyncSession,
    user: User,
    *,
    fail_on_config_error: bool = True,
) -> List[EarnedBadgeInfo]:
    """Manual sync path that evaluates all rule groups."""
    return await trigger_achievement_check(
        db,
        user,
        action="manual_sync",
        fail_on_config_error=fail_on_config_error,
    )


async def drain_pending_grants(db: AsyncSession, user: User) -> List[EarnedBadgeInfo]:
    """Retroactively mint all pending badge grants - DEACTIVATED"""
    return []
