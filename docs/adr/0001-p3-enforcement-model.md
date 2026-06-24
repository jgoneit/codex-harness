# ADR 0001: P3 Enforcement Model

## Context

The current Harness guard is a denylist-based advisory heuristic, as defined by the [Harness Workflow Contract](../contracts/harness-contract.md). It blocks known dangerous patterns that its validators recognize, and unrecognized input is allowed to pass. This is fail-open by design: a denylist can identify known command shapes, but it cannot prove that an arbitrary command is safe.

The same contract freezes the denylist parser and detector set. Newly identified bypasses must be documented as known structural false negatives, not closed by adding more denylist cases, regular expressions, parser branches, or detector logic. The contract names the intended closure path as a P3 enforcement model transition.

The test suite records this limit in [`KNOWN_FALSE_NEGATIVE_GAPS`](../../tests/test_harness_guard_pre_tool_use.py). Those cases are policy-unsafe examples that the current advisory detector model intentionally treats as known structural gaps:

- `xxd .env` demonstrates secret reads through an unbounded set of file-reading utilities. A denylist can block `cat .env`, but it cannot enumerate every existing and future program that can read bytes from a file.
- `awk '{print}' .env` demonstrates command forms whose behavior depends on runtime interpretation by another tool. Denylist matching sees a shell command, but the meaningful read operation is expressed inside `awk` semantics.
- `X=rm; $X -rf /` demonstrates shell variable indirection. The destructive operation is only visible after shell variable resolution, so string-level matching cannot reliably decide the command's effect before execution.
- `echo cm0gLXJmIC8= | base64 -d | bash` demonstrates encoded payload execution. The dangerous command is produced by runtime decode and then executed by another process.
- `python3 -c "print(open('.env').read())"` demonstrates embedded interpreter reads. The shell command invokes Python, and the sensitive file access is expressed inside interpreter code rather than as a top-level shell file operand.

Together, these examples show that denylist expansion cannot structurally close the gap. Runtime decode, variable resolution, embedded interpreter behavior, and the unbounded form of shell commands move the security-relevant operation outside the recognizer's finite pattern set.

## Decision

Harness will close these bypass classes through a P3 enforcement model transition to default-deny allowlist enforcement.

In the P3 model, actions are denied unless the active run policy explicitly allows the tool, capability, resource, and path shape required for the action. The policy model should be expressed in terms of allowed capabilities rather than blocked strings. Examples of policy dimensions include:

- which tools may run in a given Harness phase
- which commands or command families are permitted for that phase
- which filesystem paths may be read, written, created, moved, or deleted
- which network, connector, database, production, or external resources are permitted
- which operations require separate explicit approval even when otherwise in scope

This model requires capability and path scoping. A tool is not generally safe or unsafe in isolation; it is safe only relative to the current task, phase, approved scope, and resource boundary. For example, a documentation task may allow reads from `docs/`, writes to one ADR file, and read-only inspection of specific tests as evidence, while denying secret paths, broad deletion, direct database clients, and unrelated repository writes by default.

P3 should integrate with [Worktree Isolation](../contracts/worktree-isolation.md) as a reviewability and confinement aid. A Harness run may bind allowed write paths to the active worktree and approved task scope, making it easier to detect writes outside the expected task boundary. This does not make Worktree Isolation a sandbox. The Worktree Isolation Contract remains authoritative that worktrees are not a security boundary, permission system, host sandbox, or substitute for human review.

P3 also needs run-level policy identity. Enforcement decisions should be associated with a `run_id` and phase identifier so that policy can be bound to the active Plan, Implementation, Review, Repair, or Completion phase. These identifiers are design requirements for later implementation work; this ADR does not implement them. The identifiers should prevent stale approvals, old worktree state, or prior runs from being treated as reusable permission.

## Alternatives considered

### Continue expanding the denylist

Rejected. This would keep the current whack-a-mole model and directly conflict with the Frozen Detector Set decision in the Harness Workflow Contract. The known false-negative cases show why expansion does not converge: each new detector still leaves other runtime decodes, variable indirections, embedded interpreters, file-reading utilities, shell forms, and future tools outside the recognized pattern set.

### Full sandbox or container isolation

Considered as a stronger containment model, but not selected as the Harness P3 enforcement model by itself. A sandbox or container can reduce host exposure and may be useful as a separate defense-in-depth layer, but it introduces portability, platform, filesystem, credential, network, performance, debugging, and developer-experience trade-offs. It also does not replace Harness workflow semantics: Plans, phase gates, scoped approvals, [clean-context handoff and review rules](../contracts/subagent-handoff.md), CI, and human review still need to exist outside the sandbox boundary.

### Keep the current advisory model

Rejected as insufficient for the documented bypass classes. The advisory denylist remains useful for known-risk warnings and compatibility during migration, but it cannot be the final closure mechanism for structural false negatives that require runtime understanding or broad semantic interpretation.

## Consequences / Trade-offs

Default-deny allowlists increase operational cost. Projects and Harness phases will need explicit policy configuration, and narrowly scoped policies may create false positives when legitimate work uses a new tool, path, or command form. The migration must make these denials explainable so users can revise scope, request explicit approval, or update project policy without weakening the model back into a denylist.

The existing advisory denylist can coexist during migration. It may continue to provide early warnings for known dangerous patterns, compatibility with current workflows, and audit evidence for commands that are blocked under the legacy model. It should not grow new detectors for newly discovered bypass classes, and it should not be treated as sufficient enforcement once P3 policy is available.

Some behavior will remain advisory even after P3. Harness still cannot prove intent, replace code review, validate production safety by itself, or decide whether a human-approved task is wise. P3 can enforce declared tool, capability, path, resource, run, and phase boundaries; it cannot make unrestricted credentials safe, validate all generated code behavior, or remove the need for project-specific security controls.

## Scope boundary

P3 enforcement is a future design direction, not an implementation completed by this ADR. This record defines the architecture decision and the transition target.

P3 does not replace least-privilege repository and service permissions, explicit Harness approval gates, human review, automated tests, CI, project policy, or security judgment. It narrows what a Harness run may attempt by default, but it remains one control in a broader workflow.
