# Docs Change Demo

This is an illustrative scenario, not an actual execution transcript. Sample user responses, statuses, review evidence, and verification notes below are illustrative only.

This example shows a Tiny-to-Small documentation change with only the simple Plan gate approved. The full Harness loop is Plan -> Execute approval -> Implement -> Review -> Repair Plan -> Repair approval -> Repair Implement -> Completion; in this illustrative path, Review finds no must-fix issue, so repair phases are recorded as `not_applicable`.

## User Request

```text
Use $harness for this change.

Objective: clarify the README sentence that explains dry-run mode.

Constraints:
- Documentation only.
- Do not change CLI behavior, tests, hooks, packaging, or release scripts.
- Verify by inspecting the edited Markdown.
```

## Task Classification

- Classification: Small, from a Tiny-shaped docs edit escalated by explicit Harness review expectations.
- Reason: The requested change is a narrow public README wording update, but the workflow asks Harness to separate planning, implementation, and clean-context review.
- Required gates: Plan approval, Implement, Review, Completion. Repair Plan and Repair Implement are only entered if Review finds a must-fix issue.

## Plan Shape

Illustrative Plan excerpt:

- Scope: edit only the specific README sentence about dry-run mode.
- Non-goals: no CLI code, tests, hooks, packaging, release scripts, or behavior changes.
- Acceptance criteria: wording is clearer, existing command meaning is unchanged, and the diff is documentation only.
- Verification strategy: inspect the edited Markdown and diff.

```text
Proceed with this Plan? [y/N]
```

Only lowercase `y` approves execution of the accepted Plan.

## Approval Gate

Illustrative user response:

```text
y
```

Result: Plan approved. Any response other than lowercase `y` would leave implementation unapproved.

## Implementation Summary

Illustrative implementer report shape:

- Changed files: `README.md`
- Summary: clarified the dry-run sentence without changing command names or behavior claims.
- Verification: inspected the Markdown diff and confirmed no non-doc files were changed.
- Deviations: none in this illustrative scenario.

## Review Result

Illustrative partial Review Matrix:

| Criterion | Verdict | Evidence | Residual Risk |
| --- | --- | --- | --- |
| Scope compliance | pass | Illustrative evidence: changed file list contains only `README.md`. | not_applicable |
| Acceptance criteria satisfaction | pass | Illustrative evidence: wording is clearer and command meaning is unchanged. | not_applicable |
| Test coverage / verification fidelity | pass | Illustrative evidence: raw Markdown and diff inspection match the docs-only acceptance criteria. | not_applicable |
| Security / secret handling | not_applicable | Illustrative evidence: no security behavior, credentials, or protected config involved. | not_applicable |
| Data / DB risk | not_applicable | Illustrative evidence: no database, migration, or stored data path involved. | not_applicable |
| Bypass surface | not_applicable | Illustrative evidence: no hook, guard, approval, or runtime bypass behavior changed. | not_applicable |
| API or contract drift | not_applicable | Illustrative evidence: no public API, schema, or CLI flag contract changed. | not_applicable |
| Maintainability / normalization consistency | pass | Illustrative evidence: README style remains consistent with nearby prose. | not_applicable |

Illustrative reviewer finding summary:

```text
No concrete findings. Residual verification risk:
- Rendered Markdown was not checked in a browser preview in this illustrative path.
```

## Repair Plan If Needed

No Repair Plan is needed in this illustrative path.

If a future Review found a must-fix issue, Harness would write a Repair Plan before any repair implementation and use this exact prompt:

```text
Proceed with this Repair Plan? [y/N]
```

Only lowercase `y` would approve repair implementation.

## Completion Report Shape

Illustrative Completion excerpt:

- Task classification: Small
- Review status: `clean_context_review_completed`
- Completion status: `completed`
- Findings addressed: `not_applicable`

Illustrative partial Approval Ledger:

| Gate | Required? | Requested? | User response | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| Plan approval | required | requested | `y` (illustrative) | approved | Exact prompt was `Proceed with this Plan? [y/N]`; only lowercase `y` approved. |
| Scope expansion approval | not_applicable | not_applicable | not_applicable | not_applicable | No scope expansion requested. |
| Destructive command approval | not_applicable | not_applicable | not_applicable | not_applicable | No destructive command requested. |
| Secret/config access approval | not_applicable | not_applicable | not_applicable | not_applicable | No secret or protected config access requested. |
| Direct DB access approval | not_applicable | not_applicable | not_applicable | not_applicable | No direct database access requested. |
| Repair plan approval | not_applicable | not_applicable | not_applicable | not_applicable | Review produced no must-fix findings. |
| Verification exception approval | not_applicable | not_applicable | not_applicable | not_applicable | Verification matched the accepted docs-only plan. |
