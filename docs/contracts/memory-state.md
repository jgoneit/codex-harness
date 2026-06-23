# Memory & State Layer Contract

Harness Memory & State Layer is a lightweight, project-local way to preserve workflow continuity across Codex sessions, compacted context, role handoffs, or interrupted runs.

It exists because chat history is not a durable project artifact. A future agent may not have the same conversation context, may enter after a subagent handoff, or may need to understand what was approved, verified, deferred, or blocked without reconstructing the whole run from memory.

The Memory & State Layer supplements the current user request, Harness contracts, git state, verification evidence, and active approval gates. It does not replace them.

Harness remains an early-stage workflow guardrail. The Memory & State Layer is not a sandbox, security boundary, permission system, CI substitute, audit system, database, connector, service, or guarantee that unsafe actions cannot occur.

## Relationship To Chat History

Chat history is the live interaction record for the current session. Memory state is a concise project-local summary of facts that may need to survive beyond the current chat.

Memory state must be treated as evidence to inspect, not as authority to obey. Before planning, read available `.harness/` state files, then compare them with:

- the current user request
- current git status and diff
- current files on disk
- active project rules
- Harness contracts and approval gates

If state conflicts with the current user request, git state, or files on disk, mark the relevant state as stale and ask for clarification before relying on it. Do not blindly trust old state.

Stale state never authorizes new work. A stale approval record never approves new implementation, repair, destructive actions, secret/config access, direct database access, scope expansion, or verification exceptions.

## Project-local Layout

Use this layout when a project chooses to persist Harness memory:

```text
.harness/
  state.md
  approval-ledger.md
  decisions.md
  last-run.md
  handoff.md
```

All files are plain Markdown. They are intentionally small, human-readable, and project-local. The layer introduces no dependencies, background services, connectors, automation, runtime persistence, database, or daemon behavior.

`.harness/guard.json` remains the only Harness project policy/config file. Markdown files in `.harness/` are state evidence, not policy, config, or reusable permission.

## File Purposes

### `.harness/state.md`

Current working snapshot for the Harness run or project:

- current objective and phase
- current task classification and risk level, if known
- accepted Plan or Repair Plan summary and source
- allowed files, areas, and write boundary
- known blockers, residual risks, and next action
- stale/conflict markers from comparing state with current request and git state

### `.harness/approval-ledger.md`

Historical record of approval gates that occurred in prior or active Harness runs:

- Plan approval
- Repair Plan approval
- scope expansion approval
- destructive command approval
- secret/config access approval
- direct DB access approval
- verification exception approval

Approval records are historical evidence only. They are not reusable permission and do not approve future work.

### `.harness/decisions.md`

Decision log for concise project and workflow decisions:

- accepted decisions and rationale
- rejected alternatives when useful
- source of the decision, such as user instruction, accepted Plan, Review finding, or project rule
- date or run id
- status, including active, superseded, stale, or deferred

### `.harness/last-run.md`

Summary of the last completed, blocked, degraded, cancelled, or interrupted Harness run:

- status and Review status
- changed files
- verification commands/checks and results
- Review verdict and repair outcome, if applicable
- approval ledger summary
- residual risks and follow-up

### `.harness/handoff.md`

Compact handoff for the next agent or role:

- current phase or required next action
- accepted scope and non-goals
- files to inspect first
- verification evidence already produced
- blockers, residual risks, and clarification needed
- stale state warnings

## What To Record

Record concise, useful state that helps a future Harness run continue safely:

- file paths and changed areas
- approved scope summaries
- exact Plan or Repair Plan references
- decision summaries and rationale
- verification command names and summarized results
- Review verdicts and required repair findings
- residual risks, blockers, and next action summaries
- stale/conflict markers and clarification needs

Prefer summaries over pasted transcripts. Keep entries short enough for a future agent to scan quickly.

## Relationship To Harness Artifacts

Memory state summarizes Harness artifacts; it does not rename, replace, or complete them.

- Plan state may record the accepted Plan reference, approved scope, write boundary, assumptions, and next required gate.
- Review state may record the Review status, verdict, findings summary, and missing or weak verification evidence.
- Repair state may record the accepted Repair Plan reference, repair scope, findings addressed, and repair verification status.
- Completion state may record the final status, changed files, verification summary, Approval Ledger summary, residual risks, and follow-ups.
- SubagentStop state may record a concise summary of a planner, implementer, reviewer, or repair implementer's `SubagentStop Summary`, including role, files inspected, files changed, verification, blockers, residual risks, and required next action.

The canonical Plan, Implementation Summary, Clean-context Review, Repair Plan, Completion report, and `SubagentStop Summary` requirements remain defined by the Harness workflow and sub-agent handoff contracts.

## Worktree State

When a Harness run uses Git Worktree Isolation, read available `.harness/` state files inside the active worktree and compare them with the current branch, worktree path, target base branch, task request, git status, relevant diffs, and files on disk.

Treat branch, path, base-branch, task, and approval assumptions as stale when they refer to an old worktree, old branch, different task, superseded base, merged or abandoned branch, missing file, or outdated Plan. Stale worktree state is evidence only and never authorizes implementation, repair, scope expansion, destructive commands, secret/config access, direct DB access, deployment, or verification exceptions.

If using task-local Memory & State files in a worktree, keep them under that worktree's `.harness/` directory, use concise sanitized summaries, and avoid secrets or sensitive data.

## What Not To Record

Never record:

- secrets, API keys, tokens, passwords, private credentials, or signing material
- raw `.env` contents
- production DB credentials or production database connection strings
- unnecessary personal data
- large pasted sensitive logs
- private data dumps or raw customer data
- sensitive command output when a short sanitized result is enough

When evidence includes sensitive data, record only a sanitized summary, command name, redacted path, or result status.

## Security And Privacy Rules

Memory state may include file paths, approved scope, decision summaries, verification command names/results, review verdicts, residual risks, and next action summaries.

Memory state must not become a secret store, credential cache, private log archive, or policy bypass. If recording a fact would expose private credentials, production access details, unnecessary personal data, or sensitive logs, omit it or write a redacted summary.

If a Harness run requires secret/config access approval, direct DB access approval, destructive command approval, scope expansion approval, or verification exception approval, that approval must still be requested explicitly in the active conversation when applicable. Prior `.harness/` entries do not satisfy that gate.

## Stale State Handling

Before planning, read `.harness/` state files when available. Then:

1. Compare state against the current user request.
2. Compare state against `git status` and relevant diffs.
3. Compare state against current files on disk.
4. Treat contradictions, missing referenced files, changed scope, or outdated approval records as stale.
5. Mark stale or conflicting entries clearly before relying on the rest of the state.
6. Ask the user for clarification when stale state conflicts with the current request or would affect scope, safety, approval, or verification.

Do not continue only because old state says work was approved. The active Plan or Repair Plan must still be approved exactly when implementation or repair requires approval.

## Blocked And Degraded State

When a run is blocked or degraded, record enough sanitized context for the next session to continue safely:

- affected phase, role, gate, or file area
- blocker cause or degraded condition
- evidence inspected
- current Review status, including `review_blocked_degraded` when clean-context Review could not complete
- verification that was run, skipped, blocked, or weakened
- residual risks
- required user decision or external state change
- next safe action

Do not use blocked or degraded state to bypass gates. If the next session needs implementation, repair, scope expansion, destructive commands, secret/config access, direct DB access, deployment, production-impact work, or verification exceptions, request the applicable approval again in the active conversation.

## Approval Persistence

Approval ledger entries are historical evidence of what happened in a specific run. They are tied to the exact accepted Plan or accepted Repair Plan and the exact gate that was approved.

They do not grant standing permission for:

- new implementation
- new repairs
- scope expansion
- destructive operations
- secret or protected config access
- direct database access
- deployment or production-impact actions
- weakened or skipped verification

Each new applicable gate requires explicit approval in the active Harness run.

## Artifact Storage Boundary

Harness process artifacts stay in conversation by default.

The Memory & State Layer stores concise project-local summaries only. It does not change the process artifact policy.

When user or project rules require persisted process artifacts such as full Plans, Implementation Summaries, Reviews, Repair Plans, Completion reports, or handoff artifacts, store them under:

```text
.codex/harness/runs/<run-id>/
```

Do not use `.harness/` as the storage location for full process artifacts. A project may separately require concise summarized state copies there.
