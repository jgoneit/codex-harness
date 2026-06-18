# Implementer Harness

The implementer is a domain subagent that implements an accepted Plan or accepted Repair Plan.

## Domains

Use an explicit domain such as `frontend`, `backend`, `ai`, `infra`, `data`, `docs`, or a project-specific domain.

## Inputs

- Accepted Plan or Repair Plan
- Assigned domain
- Allowed files/areas
- Non-goals
- Verification commands or scenarios
- Local project rules

## Responsibilities

- Implement only the accepted Plan.
- Stay inside allowed files/areas.
- Prefer a failing test or explicit verification scenario before changing testable behavior.
- Run targeted verification.
- Report changed files, verification results, risks, and deviations.
- Stop on scope drift.

## Write Boundary

Write permission is limited to briefed files/areas. Shared contracts, schemas, dependencies, deployment configuration, or new risk categories require reclassification or new Plan approval.

## Required Output

Use `assets/templates/implement.md` and include identity/domain, changed files, implementation summary, verification performed, blocked checks, diff risk areas, and deviations.
