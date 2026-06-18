# Architecture

> Stub. The end-state architecture diagram (AC-20) and the threat model (AC-34)
> land via PR during Sprint 1.

## Components

- **Orchestrator** — receives customer signals and routes to a sub-agent.
- **Sub-agents** — renewal-nudge (live), ARR-hygiene (in progress).
- **Connectors** — Salesforce + Zendesk read adapters (Phase 1 scope).
- **Memory** — per-account, schema v1.
- **Eval** — three-tier suite gating launch.

## Phase 1 boundaries

- Connectors are **read-only**.
- Two connectors only: **Salesforce + Zendesk**.
- Memory is **per-account** (not cross-account).
