# Artifact Storage Policy

Harness process artifacts stay in conversation by default.

## Default Policy

- Do not create repository files only for Harness process artifacts.
- Persist artifacts only when the user or project rules require it.
- If persistence is required, write below:

```text
.codex/harness/runs/<run-id>/
```

- Do not put process artifacts in source directories.
- If persistent artifacts are created, list every path in the Completion report.

## Scope

This policy applies to Plan, Implement, Review, Repair Plan, Completion, Improvement, and subagent handoff artifacts. Source code, test fixtures, and product docs remain normal repository outputs when they are the actual work product.
