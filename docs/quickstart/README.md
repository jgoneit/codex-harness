# Harness Quickstart

This quickstart shows how to use Harness once the plugin is available in Codex.

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

- classification
- requirements and current state
- constraints and risks
- acceptance criteria
- verification strategy
- orchestration topology
- implementation scope

The Plan must end with:

```text
Proceed with this Plan? [y/N]
```

Reply with exactly `y` to approve. Any other response leaves the Plan unapproved.

## 3. Let Implement Run Inside Scope

After exact Plan approval, Harness gives the implementer only the accepted scope and write boundary. The implementer reports:

- identity and domain
- files changed
- implementation summary
- verification performed
- blocked checks
- deviations or risk areas

If the work needs new files, broader scope, destructive commands, secret access, deployment, or production-impact operations outside the accepted Plan, Harness stops for a new gate instead of silently expanding scope.

## 4. Wait for Review

For `Small` and `Non-trivial` work, Review must be performed by a clean-context read-only reviewer. The reviewer checks the change against the accepted Plan and reports either concrete findings or this exact no-finding form:

```text
No concrete findings. Residual verification risk:
- ...
```

Main-agent self-review does not count as Review.

## 5. Approve Repairs Only When Needed

If Review finds must-fix issues, Harness writes a Repair Plan. Repair work requires this exact prompt:

```text
Proceed with this Repair Plan? [y/N]
```

Reply with exactly `y` to approve repair implementation. Any other response leaves repair work unapproved.

## 6. Read the Completion Report

Harness finishes with a Completion report covering:

- task classification
- orchestration topology and spawned roles
- implemented changes
- verification performed
- Review status
- findings addressed
- unresolved risks or follow-ups

The Review status is one of:

- `clean_context_review_completed`
- `review_not_required_tiny_only`
- `review_blocked_degraded`

## Configuration & Scope

Projects can opt in to narrow soft-category relaxations with `.harness/guard.json`. Supported keys are `allow_db_local_connections`, a list of DB hosts such as `localhost` or `127.0.0.1`, and `allow_paths`, a list of project paths such as `tmp/` or `fixtures/`. Harness guard decisions are a defense-in-depth signal below Codex approval and sandboxing: allow rules only reduce false-positive friction for soft categories, currently `db_client_access`, and cannot relax hard-deny categories such as secret file reads, credential exfiltration, protected broad deletes, destructive Git commands, destructive SQL, or environment dumps.

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
