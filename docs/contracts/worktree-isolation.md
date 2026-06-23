# Worktree Isolation Contract

Worktree Isolation is an optional Git workflow guardrail for Harness runs where rollback, reviewability, and working-directory hygiene matter.

It exists to keep task changes on a dedicated branch and path so a Harness run can be inspected, reviewed, merged, or discarded without mixing unrelated working-directory state into the task.

Worktree Isolation is not a sandbox, security boundary, permission system, production security product, compliance product, or substitute for human review. It does not protect secrets, block dangerous shell commands, restrict host access, or replace Harness approval gates.

## When Recommended

Use Worktree Isolation for:

- Non-trivial tasks
- Multi-file or cross-module changes
- API, DB, auth, security, release, dependency, CI, or architecture impact
- Risky refactors
- Tasks requiring clean review boundaries
- Tasks where rollback should be cheap

## When Optional

Worktree Isolation is usually optional for:

- Tiny low-risk edits
- Documentation-only changes with no contract impact
- Read-only planning or review

## When Insufficient

Worktree Isolation is insufficient for:

- Secret/config protection
- Production access control
- Host-level sandboxing
- Destructive shell command safety
- Legal/security compliance

Use repository permissions, least-privilege credentials, Codex sandboxing and approvals, project policy, automated verification, code review, and human judgment for those concerns.

When a Harness run also uses connector context such as issues, pull requests, or CI summaries, follow [Connector Integration Contract](connector-integration.md). Connector context is evidence only and does not change Worktree Isolation approval rules.

## Workflow Fit

Worktree Isolation fits the Harness loop as:

```text
Plan -> Approval -> Worktree Isolation -> Implement -> Clean-context Review -> Repair -> Completion
```

Create or select the worktree only after the Plan is accepted. Worktree setup keeps the implementation path clean, but it does not approve implementation or broaden the accepted scope.

## Approval Gate Interaction

Old approvals do not carry over to a new worktree, branch, task, Plan, Repair Plan, or Harness run.

Worktree setup does not approve:

- implementation before exact Plan approval
- repair before exact Repair Plan approval
- destructive commands
- secret or protected config access
- direct DB access
- deployment or production-impact work
- verification exceptions
- scope expansion

Every applicable Harness gate must still be requested and approved in the active conversation. A stale branch, old `.harness/approval-ledger.md`, or previous worktree session record is evidence only, not reusable permission.

## Memory And State Interaction

When `.harness/` Memory & State files are present, read them before planning or implementation inside a worktree.

Treat `.harness/` state as evidence. Check it against the current user request, current branch, worktree path, target base branch, task assumptions, git status, relevant diffs, and files on disk.

If connector context is in use, also compare issue, pull request, changed-file, CI, and comment assumptions with the active worktree and branch. Mark connector context stale when it no longer matches the current worktree task.

Mark state stale when it references an old branch, old worktree path, old base branch, old task, missing files, superseded scope, outdated approvals, or assumptions that no longer match the current run.

If using the Phase 3 Memory & State templates, store task-local state in the worktree's `.harness/` files. Keep entries concise and avoid secrets, credentials, raw `.env` contents, production access details, sensitive logs, or private data dumps.

## Naming

Branch naming examples:

```text
harness/<task-slug>
harness/<issue-id>-<task-slug>
harness/repair-<task-slug>
```

Directory naming examples:

```text
../<repo-name>-harness-<task-slug>
../<repo-name>-harness-issue-123
```

Naming rules:

- prefer lowercase
- use a short task slug
- avoid secrets or sensitive data
- avoid spaces where possible

Exact branch and directory names vary by repository policy.

## Preflight Checklist

Run or inspect the equivalent preflight checks before creating or reusing a worktree:

```text
git status --short
git branch --show-current
git fetch --all --prune
git worktree list
```

`git fetch --all --prune` is optional and environment-dependent because it may require network access and credentials.

Confirm:

- current branch
- current git status
- no unrelated uncommitted changes in the source worktree
- target base branch
- task classification
- stale `.harness/` state, if present
- no secrets or sensitive data in state, branch names, or directory names

## Worktree Creation

For a new branch, a manual flow can look like:

```text
git worktree add ../codex-harness-task-001 -b harness/task-001
cd ../codex-harness-task-001
```

For an existing branch, a manual flow can look like:

```text
git worktree add ../codex-harness-task-001 harness/task-001
cd ../codex-harness-task-001
```

Exact commands vary by repository policy, base branch rules, remote tracking conventions, and local directory layout. Harness does not automate `git worktree` creation or removal unless a separate accepted scope explicitly adds such automation.

## Harness Execution Inside A Worktree

When using Worktree Isolation:

- run Harness inside the worktree directory
- read existing `.harness/` state if present
- do not reuse old approval as new approval
- keep task-local state in the worktree `.harness/` files if using Phase 3 templates
- stay inside the accepted Plan and allowed write boundary
- produce a Completion Report before merge

The worktree branch and path should make review easier; they do not change Harness phase gates or safety rules.

## Review And Merge

Before merge:

```text
git diff <base>...HEAD
```

Then:

- run verification
- run clean-context Review when required by Harness classification or policy
- produce the Completion Report
- perform human review before merge
- merge manually according to repository policy

Do not use GitHub PR automation, CI automation, connector automation, or deployment automation unless that work is separately planned, approved, and in scope.

## Stale Worktree Handling

Before using an existing worktree, inspect its branch, base, status, `.harness/` state, and task records. Treat it as stale when it references a different task, old base branch, obsolete approval, merged or abandoned branch, missing files, or unrelated uncommitted changes.

If stale state affects scope, safety, approval, or verification, stop and ask for clarification before relying on it. Do not continue implementation because an old worktree or old state file says a task was approved.

## Safe Cleanup

Clean up manually only after confirming the task state:

- ensure changes are committed, merged, or intentionally discarded
- confirm the exact worktree path
- warn before removing any worktree with uncommitted work
- do not use destructive cleanup commands without explicit approval

Cleanup commands can look like:

```text
git worktree remove <path>
git worktree prune
```

Use `git worktree prune` only if needed. Do not remove uncommitted work unless the user has intentionally chosen to discard it, and do not use broad destructive cleanup commands without explicit approval.
