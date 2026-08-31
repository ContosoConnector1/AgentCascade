"""Three-tier eval framework (WIP — AC-21).

The launch gate. Three tiers, each a hard blocker:
  1. routing      — did the orchestrator pick the right sub-agent?
  2. grounding    — is every claim in the draft backed by a cited signal?
  3. end_to_end   — human/label judgement of draft quality (kappa).

Thresholds below are PLACEHOLDERS. The real floors come from the labeled
500-account benchmark (AC-27); we do not name a threshold we can't defend.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TierResult:
    tier: str
    passed: bool
    score: float
    detail: str


# Placeholder gates — finalized against the benchmark before launch.
GATES = {
    "routing": 0.95,       # routing accuracy
    "grounding": 1.00,     # zero tolerance for uncited claims
    "end_to_end": 0.70,    # Cohen's kappa vs. labels (kappa >= 0.7)
}


def gate(results: list[TierResult]) -> bool:
    """Launch gate: every tier must clear its floor."""
    return all(r.passed for r in results)
