"""Static constants used across Health-AI agent modules.

Isolated here so that both ``message_classifier`` and the orchestrator graph
can import them without pulling in any heavy dependencies or risking circular
imports.  All values are immutable — do not modify at runtime.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Crisis detection vocabulary (Indonesian + English)
# ---------------------------------------------------------------------------
# Checked against every incoming message in O(n·k) time.  Keep the list
# purposefully conservative: false positives trigger unnecessary CMA escalation.
CRISIS_KEYWORDS: tuple[str, ...] = (
    "suicide",
    "bunuh diri",
    "kill myself",
    "end my life",
    "tidak ingin hidup lagi",
    "self-harm",
    "menyakiti diri",
    "overdose",
    "mau mati",
    "ingin mati",
)

# ---------------------------------------------------------------------------
# Smalltalk exact-match vocabulary
# ---------------------------------------------------------------------------
# Tier-1 gate: if the entire normalised message is in this set the message is
# treated as social filler and bypasses the full LLM decision call.
SMALLTALK_EXACT: frozenset[str] = frozenset({
    # English greetings / acks
    "hi", "hello", "hey", "yo", "sup",
    "ok", "okay", "okey", "okk", "alright", "sure", "yep", "nope", "noted",
    "thanks", "thank you", "thx", "ty",
    "bye", "bye bye", "see you", "good morning", "good night", "good afternoon",
    "p", "ping",
    # Indonesian greetings / acks
    "halo", "hai",
    "oke", "oke deh", "sip", "siap", "iya", "ya", "yap", "nggak",
    "makasih", "terima kasih", "trims",
    "baik", "baik baik",
    "dadah", "sampai jumpa",
    "selamat pagi", "selamat siang", "selamat sore", "selamat malam",
    "selamat tidur",
    # Filler / acknowledgment
    "hmm", "hm", "oh", "oh oke", "oh okay", "oh baik", "ooh",
})

# ---------------------------------------------------------------------------
# Health-AI-name prefix smalltalk variants (Tier-2, max 22 chars)
# ---------------------------------------------------------------------------
SMALLTALK_HEALTH_AI_PREFIX: frozenset[str] = frozenset({
    "hi health-ai", "halo health-ai", "hai health-ai", "hello health-ai", "hey health-ai",
    "thank you health-ai", "makasih ya", "terima kasih ya",
    "oke health-ai", "ok health-ai", "sip health-ai", "noted health-ai", "bye health-ai",
    "hi health_ai", "halo health_ai", "hai health_ai", "hello health_ai", "hey health_ai",
    "thank you health_ai", "oke health_ai", "ok health_ai", "sip health_ai", "noted health_ai", "bye health_ai",
})

# ---------------------------------------------------------------------------
# Conversation history window
# ---------------------------------------------------------------------------
# Maximum number of conversation *turns* (user + model pairs) to include in
# the context window on each non-crisis direct-response call.  10 turns
# (= 20 messages) caps per-request input token cost while preserving enough
# recency for coherent replies.
MAX_HISTORY_TURNS: int = 10
