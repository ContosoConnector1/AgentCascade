# Sprint 1 — launch-readiness readout

**Sprint:** 2026-06-01 → 2026-06-12 · **Readout:** Fri 2026-06-12
**Goal:** Detector + drafting pipeline end-to-end on staging; connectors to staging; reviews filed.

The honest version: the **pipeline is real**, the **connectors are the risk**. We hit the pipeline and review goals; we did not hit connector parity, and the benchmark moved. September private preview is still the target, with connectors + benchmark as the two things we are watching.

## Where we are

| Area | Status | Detail |
|---|---|---|
| Orchestrator + renewal-nudge pipeline | 🟢 Green | Demoed end-to-end on staging. Orchestrator prompt (#6) and renewal-nudge sub-agent (#9) done. |
| Per-account memory | 🟢 Green | Schema v1 done (#11); write-path in progress (#12). |
| Architecture | 🟢 Green | Locked; review signed off (#8), diagram captured (#13). Threat model follows the lock (#20). |
| **Salesforce connector** | 🟡 Yellow | Read adapters done; staging deploy blocked on OAuth refresh (#2 / AC-114). Known workaround; expected green Sprint 2. |
| **Zendesk connector** | 🔴 Red | Webhook drops under load (#1 / AC-113). Needs polling-fallback redesign. Parity commit at risk. |
| Eval framework + benchmark | 🟡 Yellow | Framework + query set in progress (#14, #15). 500-account benchmark (#17) re-baselined to **early July**. |
| Compliance | 🟢 On track | RAI package filed (#23) and Privacy ticket opened (#24) inside the early-June target; sign-offs in progress (#18, #19). |

## The connector call (R/Y/G)

This is the one the Plan committed to before architecture lock, and it came back split:

- **Salesforce → YELLOW.** Real adapters, real blocker, known fix. I'm comfortable calling this green by Sprint 2.
- **Zendesk → RED.** The webhook drops are a design issue, not a bug we patch in a day — it needs the polling fallback. This is the item that can move the September date if it slips again.

We committed to "Salesforce + Zendesk parity" at Phase 1. As of this readout we have **neither connector green**. That's the gap between the launch narrative and the build, and I'd rather name it now than at launch-minus-two-weeks.

## Benchmark

The 500-account benchmark moved to **early July**. We're holding **κ ≥ 0.7** over raw speed — I'd rather ship a number we can defend than a faster one we can't. No quantitative claim goes in the public post until the benchmark lands (launch + 2).

## What's on the line for September

1. **Zendesk to green** — polling-fallback redesign (#1 → #4).
2. **Salesforce to green** — proactive token refresh (#2 → #3).
3. **Benchmark v1 at κ ≥ 0.7** (#17).

Everything else (pipeline, memory, architecture, compliance) is tracking. Connectors and the benchmark are the watch list.
