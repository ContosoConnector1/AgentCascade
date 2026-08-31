"""Seed eval query set (WIP — AC-23).

Ground-truth scenarios the three-tier framework scores against. Each case
pairs an input signal context with the expected routing + a grounding
expectation. Expanded toward the 500-account benchmark (AC-27).
"""
from __future__ import annotations

EVAL_CASES = [
    {
        "id": "renewal-30d",
        "signals": [{"kind": "renewal_date", "days_to_renewal": 30}],
        "expect_route": "renewal_nudge",
        "expect_grounded": True,
    },
    {
        "id": "arr-mismatch",
        "signals": [{"kind": "arr_change", "delta": -12000}],
        "expect_route": "arr_hygiene",   # only when flag on
        "expect_grounded": True,
    },
    {
        "id": "no-signal",
        "signals": [],
        "expect_route": None,
        "expect_grounded": True,
    },
]
