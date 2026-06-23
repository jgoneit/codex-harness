# Docs Change Demo

This is an illustrative scenario, not an actual execution transcript. Sample user responses, statuses, review evidence, and verification notes below are illustrative only.

This example shows a Tiny-to-Small documentation change with only the simple Harness Plan gate approved. The full Harness loop is Harness Plan -> Execute approval -> Implement -> Clean-context Review -> Repair Plan -> Repair approval -> Repair Implement -> Completion Report; in this illustrative path, Clean-context Review returns `PASS`, so repair phases are recorded as `not_applicable`.

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

- Classification: Small, from a Tiny-shaped docs edit classified as Small because explicit Harness review expectations apply.
- Reason: The requested change is a narrow public README wording update, but the workflow asks Harness to separate planning, implementation, and clean-context review.
- Required gates: Plan approval, Implement, Clean-context Review, Completion Report. Repair Plan and Repair Implement are only entered if Review returns `REPAIR_REQUIRED`.

## Harness Plan Shape

Illustrative Harness Plan excerpt:

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

Illustrative Findings Table:

| Severity | Finding | Evidence | Required Action |
| --- | --- | --- | --- |
| not_applicable | No findings requiring action. | Illustrative evidence: changed file list contains only `README.md`, wording is clearer, and command meaning is unchanged. | No action required. |

Illustrative Verdict:

```text
PASS
```

## Repair Plan If Needed

No Repair Plan is needed in this illustrative path.

If a future Review returned `REPAIR_REQUIRED`, Harness would write a Repair Plan before any repair implementation and use this exact prompt:

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
| Repair plan approval | not_applicable | not_applicable | not_applicable | not_applicable | Review returned `PASS`; no repair was required. |
| Verification exception approval | not_applicable | not_applicable | not_applicable | not_applicable | Verification matched the accepted docs-only plan. |
