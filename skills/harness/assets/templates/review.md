# Review

## Artifact Metadata

- Harness run id:
- Artifact id:
- Phase: Review
- Artifact status: draft / accepted / revised / completed / blocked_degraded
- Created at:
- Updated at:
- Source request:
- Task classification: Tiny / Small / Non-trivial
- Related artifacts:

## Review Status

- Status: clean_context_review_completed / review_not_required_tiny_only / review_blocked_degraded
- Guard: Small/Non-trivial can only use `clean_context_review_completed` or `review_blocked_degraded`.
- Review required? Yes/No:
- Review entered? Yes/No:
- Review trigger: Tiny risk / Small required gate / Non-trivial required gate / project rule / user instruction

## Review Authorization

- Authorization model: policy preauthorization / explicit approval required
- Authorization result: preauthorized / granted / denied / blocked
- Approved scope:
- Non-goals:

## Reviewer Subagent

- Reviewer subagent used? Yes/No:
- Reviewer subagent identity:
- Clean-context? Yes/No:
- Read-only? Yes/No:
- Intended/actual reasoning effort:
- Fallback decision:

## Review Result

Choose exactly one.

### A. Completed Review

Use only when Status is `clean_context_review_completed`.

- Reviewer subagent identity:
- Clean-context: Yes/No
- Read-only: Yes/No

#### Review Matrix

Use columns exactly as shown. Verdict values are only `pass`, `fail`, `unknown`, or `not_applicable`. `unknown` is not a pass and must be treated as residual risk. Do not leave any cells blank; use `not_applicable` where applicable.

| Criterion | Verdict | Evidence | Residual Risk |
| --- | --- | --- | --- |
| Scope compliance | pass / fail / unknown / not_applicable | evidence | residual risk or not_applicable |
| Acceptance criteria satisfaction | pass / fail / unknown / not_applicable | evidence | residual risk or not_applicable |
| Test coverage / verification fidelity | pass / fail / unknown / not_applicable | evidence | residual risk or not_applicable |
| Security / secret handling | pass / fail / unknown / not_applicable | evidence | residual risk or not_applicable |
| Data / DB risk | pass / fail / unknown / not_applicable | evidence | residual risk or not_applicable |
| Bypass surface | pass / fail / unknown / not_applicable | evidence | residual risk or not_applicable |
| API or contract drift | pass / fail / unknown / not_applicable | evidence | residual risk or not_applicable |
| Maintainability / normalization consistency | pass / fail / unknown / not_applicable | evidence | residual risk or not_applicable |

#### Blocking Findings

Findings that must be fixed before completion. If none, write `not_applicable`.

#### Finding N

- Severity:
- Evidence:
- Why it matters:
- Suggested action:
- Must fix now?:

#### Non-blocking Findings

Findings that may be deferred, with rationale. If none, write `not_applicable`.

#### Finding N

- Severity:
- Evidence:
- Why it matters:
- Suggested action:
- Must fix now?:

If there are no concrete findings in either findings section, write exactly:

```text
No concrete findings. Residual verification risk:
- ...
```

### B. Blocked / Degraded Review

Use only when Status is `review_blocked_degraded`.

- Fallback condition: subagent tooling unavailable / user denied authorization / authorization cannot be requested / project or security rules prohibit delegation
- Reason clean-context reviewer subagent review was not completed:
- Authorization result or blocker:
- Evidence inspected:
- Criteria applied:
- Risk observations:
- Required statement: `Review blocked/degraded; no clean-context reviewer findings are available.`
- Degraded independence statement:

## Orchestrator Decision

- Accepted findings:
- Rejected findings with rationale:
- Deferred follow-ups:
- Repair Plan required? Yes/No:
