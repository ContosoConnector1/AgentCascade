"""Signal router.

Maps customer signals to the sub-agent that should handle them. Kept
deliberately small — routing policy lives here, drafting lives in the
sub-agents. Mirrors the routing section of the orchestrator system prompt.
"""
from __future__ import annotations

from agent_cascade.config import FeatureFlags
from agent_cascade.connectors.base import CustomerSignal

RENEWAL_KINDS = {"renewal_date", "renewal_risk"}
ARR_KINDS = {"arr_change"}


def route(signal: CustomerSignal, flags: FeatureFlags) -> str | None:
    """Return the sub-agent name for a signal, or None if not actionable."""
    if signal.kind in RENEWAL_KINDS and flags.renewal_nudge:
        return "renewal_nudge"
    if signal.kind in ARR_KINDS and flags.arr_hygiene:
        return "arr_hygiene"
    return None
