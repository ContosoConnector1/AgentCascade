"""500-account labeled benchmark (WIP — AC-27).

The headline quality measure for private preview. Construction:
  - 500 accounts sampled across segment + renewal-stage strata.
  - Each labeled by two reviewers; inter-rater agreement tracked.
  - Cascade drafts scored against labels; report Cohen's kappa.

Re-baselined to early July at the Sprint 1 readiness call. We hold the bar
at kappa >= 0.7 over raw speed — a defensible number beats a fast one. No
quantitative claim ships publicly until this lands (launch + 2).
"""
from __future__ import annotations

from dataclasses import dataclass, field

KAPPA_FLOOR = 0.70


@dataclass
class BenchmarkSpec:
    n_accounts: int = 500
    reviewers_per_item: int = 2
    strata: list[str] = field(
        default_factory=lambda: ["segment", "renewal_stage"]
    )


def passes(kappa: float) -> bool:
    """Benchmark clears the bar only at or above the kappa floor."""
    return kappa >= KAPPA_FLOOR
