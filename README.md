# Agent Cascade

A customer-success agent that runs natively on **Microsoft 365 Copilot**. Cascade proactively watches the customer and communication graphs and drafts the next best CSM action — renewal nudges, ARR-hygiene fixes, and follow-ups — grounded in connected systems of record.

> **Phase 1 — Private Preview.** This repo tracks the Phase 1 build. See the launch plan and scope in Confluence (space `Cascade`); engineering execution is tracked in Jira project `AC`.

## Status — Sprint 1 (2026-06-01 → 2026-06-12)

End-of-sprint snapshot. The detector + drafting pipeline (orchestrator + renewal-nudge sub-agent) runs end-to-end on staging; architecture is locked; RAI and Privacy submissions are filed. The connector parity commitment is the watch item:

| Area | Status | Notes |
|---|---|---|
| Orchestrator + renewal-nudge pipeline | 🟢 Green | Demoed end-to-end on staging |
| Memory (per-account) | 🟢 Green | Schema v1 landed; write-path in progress |
| **Salesforce connector** | 🟡 Yellow | Read adapters done; staging deploy blocked on OAuth refresh (#AC-114) |
| **Zendesk connector** | 🔴 Red | Webhook deliveries drop under load (#AC-113); needs polling-fallback redesign |
| Eval framework + 500-account benchmark | 🟡 Yellow | Framework in progress; benchmark re-baselined to early July |

The 500-account benchmark target slipped, holding κ ≥ 0.7 over raw speed. September private-preview target still stands, with **connectors + benchmark** as the open risks.

## Architecture

```
M365 Copilot ──▶ Orchestrator ──┬──▶ Renewal-nudge sub-agent
                                └──▶ ARR-hygiene sub-agent
                                         │
                  Per-account Memory ◀───┤
                                         ▼
                 Connectors:  Salesforce  ·  Zendesk
```

See [`docs/architecture.md`](docs/architecture.md) for the end-state diagram and threat model.

## Repository layout

```
src/agent_cascade/
  orchestrator/   Main orchestrator prompt + routing
  subagents/      Renewal-nudge, ARR-hygiene sub-agents
  connectors/     Salesforce + Zendesk read adapters
  memory/         Per-account memory schema + write path
  eval/           Eval framework, query set, benchmark
docs/             Architecture, threat model, sprint status
tests/
```

## Contributing

Branch per work item, open a PR linked to its `AC-` issue, and keep PRs scoped to one capability or connector. Connector work ships behind a feature flag (per connector + capability slice).
