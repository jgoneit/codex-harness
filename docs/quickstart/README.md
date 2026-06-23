# Harness Quickstart

This quickstart shows how to use Harness once the plugin is available in Codex.

First-time users should package, install, and load the plugin for their Codex CLI environment before following this guide. See the top-level [README](../../README.md) for the supported packaging prerequisites, `make package`, and the `dist/harness.zip` artifact.

For the full workflow contract, including canonical artifact sections, approval gates, blocked/degraded behavior, and status values, see [docs/contracts/harness-contract.md](../contracts/harness-contract.md).

## 1. Invoke Harness Explicitly

Start a request with `$harness` or include it clearly in the task:

```text
Use $harness to plan, implement, and review this change:
Update the public docs for the payment retry behavior.
```

Harness is intended for explicit `$harness` invocation. Current limitation: the hook trigger checks for the `$harness` token/substring anywhere in the submitted prompt, so documentation mentions containing `$harness` can also receive active Harness context.

## 2. Review the Plan

Harness first inspects local project rules and classifies the task as `Tiny`, `Small`, or `Non-trivial`.

For `Small` and `Non-trivial` tasks, Harness uses a planner role to produce a Plan with:

- task classification and risk level
- reasoning for classification
- in-scope and out-of-scope boundaries
- files or areas to inspect
- proposed change plan
- verification plan
- risks and assumptions

The Plan Approval Gate must include:

```text
Proceed with this Plan? [y/N]
```

Reply with exactly `y` to approve. Any other response leaves the Plan unapproved.

## 3. Let Implement Run Inside Scope

After exact Plan approval, Harness gives the implementer only the accepted scope and write boundary. The Implementation Summary reports:

- accepted Plan reference
- changed files
- summary of changes
- scope compliance
- verification performed
- deviations from Plan
- blockers or residual risks

If the work needs new files, broader scope, destructive commands, secret access, deployment, or production-impact operations outside the accepted Plan, Harness stops for a new gate instead of silently expanding scope.

## 4. Wait for Review

For `Small` and `Non-trivial` work, Review must be performed by a clean-context read-only reviewer. The reviewer compares the diff against the accepted Plan, does not rely on implementer intent, must not modify files, flags undocumented scope expansion, and returns a Findings Table with this shape:

```text
| Severity | Finding | Evidence | Required Action |
```

The Review verdict is one of `PASS`, `PASS_WITH_NOTES`, `REPAIR_REQUIRED`, or `BLOCKED`.

Main-agent self-review does not count as Review.

## 5. Approve Repairs Only When Needed

If Review finds must-fix issues, Harness writes a Repair Plan. The Repair Approval Gate must include this exact prompt:

```text
Proceed with this Repair Plan? [y/N]
```

Reply with exactly `y` to approve repair implementation. Any other response leaves repair work unapproved.

## 6. Read the Completion Report

Harness finishes with a Completion report covering:

- status
- Review status
- whether a Repair Plan was required
- changed files
- verification
- Review result
- Approval Ledger
- unresolved risks or follow-ups

Completion status is one of:

- `completed`
- `completed_with_residual_risk`
- `blocked`
- `degraded`
- `cancelled`

The Review status is one of:

- `clean_context_review_completed`
- `review_not_required_tiny_only`
- `review_blocked_degraded`

## Configuration & Scope

Projects can opt in to narrow soft-category relaxations and workflow metadata with `.harness/guard.json`.

Supported allow keys are:

- `allow_db_local_connections`: list of DB hosts such as `localhost` or `127.0.0.1`
- `allow_paths`: list of project paths such as `tmp/` or `fixtures/`

Supported workflow metadata keys are:

- `verification_commands`: list of commands the project expects for verification
- `review_required`: boolean marker that Review is required by project policy
- `approval_required_paths`: list of paths that require extra project approval before modification

Harness guard decisions are a defense-in-depth signal below Codex approval and sandboxing. Allow rules only reduce false-positive friction for soft categories, currently `db_client_access`, and cannot relax hard-deny categories such as secret file reads, credential exfiltration, protected broad deletes, destructive Git commands, destructive SQL, or environment dumps. Workflow metadata keys document project expectations; they do not change `PreToolUse` hard-deny or soft-relaxation decisions. Unknown keys or invalid values cause the guard to ignore the entire config and write a stderr warning.

## Example Prompt

```text
Use $harness for this change.

Objective: update the CLI usage docs so they explain dry-run mode and failure exit codes.

Constraints:
- Do not change CLI implementation.
- Do not touch release scripts.
- Verify by inspecting the docs and running existing docs lint if available.
```

This gives Harness a clear objective, scope boundary, and verification expectation before the Plan gate.
