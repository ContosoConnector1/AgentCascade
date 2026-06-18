# Contributing

Phase 1 is built in short sprints tracked in Jira project `AC`. Conventions:

- **Branch per work item.** Name branches after the work, e.g. `feat/salesforce-connector`, `fix/zendesk-webhook-drops`.
- **Link every PR to its `AC-` issue** in the description (`Closes AC-15`).
- **Scope PRs to one capability or connector.** Connector work ships behind a feature flag (per connector + capability slice).
- **Reviews:** connector + memory changes need an eng-manager review; eval + prompt changes need a DS review.

## Ownership

| Area | Owner |
|---|---|
| Orchestrator + sub-agent prompts, eval | Marcus (DS) |
| Connectors, memory, architecture | Ana (Eng), Felix (SWE) |
| Frontier sign-up + UI | Felix (SWE), Leo (UX) |
| Launch coordination | Priya (PM) |
