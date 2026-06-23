# Failed Review Repair Loop Demo

This is an illustrative scenario, not an actual execution transcript. Sample user responses, statuses, review evidence, and verification notes below are illustrative only.

This example shows a Clean-context Review failure that does not get fixed immediately. Harness first writes a Repair Plan, asks for repair approval, and only then performs Repair Implement. The full Harness loop is Harness Plan -> Execute approval -> Implement -> Clean-context Review -> Repair Plan -> Repair approval -> Repair Implement -> Completion Report.

## User Request

```text
Use $harness for this change.

Objective: update the CLI docs so retry behavior and retry exit codes are documented.

Constraints:
- Documentation only.
- Do not change CLI implementation, tests, hooks, packaging, or release scripts.
- Verify by inspecting the edited Markdown.
```

## Task Classification

- Classification: Small
- Reason: The task is local documentation work with clear acceptance criteria, but it affects public CLI behavior documentation and requires Clean-context Review under Harness.
- Required gates: Planner Harness Plan, exact Plan approval, implementer, Clean-context Review, Repair Plan for findings requiring action, exact Repair approval, Repair Implement, follow-up Clean-context Review, and Completion Report.

## Harness Plan Shape

Illustrative Harness Plan excerpt:

- Scope: update only the CLI usage docs for retry behavior and retry exit code descriptions.
- Non-goals: no runtime behavior changes, no tests, no hooks, no packaging, no release scripts.
- Acceptance criteria: retry count behavior is described, retry exhaustion exit code is documented, and wording does not imply a new flag or changed default.
- Verification strategy: inspect the Markdown diff for accuracy and scope.

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

- Changed files: `docs/cli/retries.md`
- Summary: added retry behavior wording and an exit code note.
- Verification: illustrative Markdown diff inspection is reported as sample evidence, not as a real local command result.
- Deviations: none reported by the implementer in this illustrative scenario.

## Review Result

Illustrative Findings Table before repair:

| Severity | Finding | Evidence | Required Action |
| --- | --- | --- | --- |
| High | Retry exhaustion exit code documentation is missing. | Illustrative evidence: `docs/cli/retries.md` describes retry attempts but omits the retry exhaustion exit code required by the accepted Plan. | Add the retry exhaustion exit code note without changing runtime behavior or widening scope. |

Illustrative Verdict:

```text
REPAIR_REQUIRED
```

## Repair Plan

Harness does not immediately fix the finding after Review. It first writes a Repair Plan.

Illustrative Repair Plan excerpt:

- Accepted finding: retry exhaustion exit code documentation is missing.
- Fix now: add the missing exit code note in `docs/cli/retries.md`.
- Scope guard: documentation only; no CLI implementation, tests, hooks, packaging, or release scripts.
- Verification: inspect the edited Markdown and confirm the missing acceptance criterion is now represented.

```text
Proceed with this Repair Plan? [y/N]
```

Only lowercase `y` approves repair implementation.

## Repair Approval Gate

Illustrative user response:

```text
y
```

Result: Repair Plan approved. Any response other than lowercase `y` would leave repair implementation unapproved.

## Repair Implementation Summary

Illustrative repair implementer report shape:

- Changed files: `docs/cli/retries.md`
- Summary: added the retry exhaustion exit code note requested by the accepted Repair Plan.
- Verification: illustrative Markdown diff inspection confirms the missing acceptance criterion is now covered.
- Deviations: none in this illustrative scenario.

## Follow-Up Review Result

Illustrative Findings Table after repair:

| Severity | Finding | Evidence | Required Action |
| --- | --- | --- | --- |
| not_applicable | No findings requiring action. | Illustrative evidence: retry count behavior and retry exhaustion exit code are both documented, and original plus repair changes remain limited to `docs/cli/retries.md`. | No action required. |

Illustrative Verdict:

```text
PASS
```

## Completion Report Shape

Illustrative Completion excerpt:

- Task classification: Small
- Review status: `clean_context_review_completed`
- Completion status: `completed`
- Findings addressed: retry exhaustion exit code note added after approved Repair Plan.

Illustrative partial Approval Ledger:

| Gate | Required? | Requested? | User response | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| Plan approval | required | requested | `y` (illustrative) | approved | Exact prompt was `Proceed with this Plan? [y/N]`; only lowercase `y` approved. |
| Scope expansion approval | not_applicable | not_applicable | not_applicable | not_applicable | Repair stayed inside the accepted docs-only scope. |
| Destructive command approval | not_applicable | not_applicable | not_applicable | not_applicable | No destructive command requested. |
| Secret/config access approval | not_applicable | not_applicable | not_applicable | not_applicable | No secret or protected config access requested. |
| Direct DB access approval | not_applicable | not_applicable | not_applicable | not_applicable | No direct database access requested. |
| Repair plan approval | required | requested | `y` (illustrative) | approved | Exact prompt was `Proceed with this Repair Plan? [y/N]`; only lowercase `y` approved repair implementation. |
| Verification exception approval | not_applicable | not_applicable | not_applicable | not_applicable | Verification matched the accepted Plan and Repair Plan. |
