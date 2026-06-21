# Codex Harness

**Language:** [한국어](README.ko.md) | English

Codex Harness is a gated workflow plugin for Codex. It is for work where you want a deliberate **Plan -> Implement -> Review -> Repair -> Completion** loop instead of immediate execution.

```text
Plan -> Execute approval -> Implement -> Review -> Repair Plan -> Repair approval -> Repair Implement -> Completion
```

Use it when a request is risky enough that planning, scoped implementation, and clean-context review should be separated: multi-file edits, workflow or policy updates, behavior changes, security-sensitive work, API or contract changes, and anything that benefits from explicit approval gates.

## 🧭 At a Glance

| Area | What Harness adds |
| --- | --- |
| 🚦 Gates | Implementation and repair only run after exact approval prompts. |
| 🧩 Roles | Planner, implementer, and clean-context read-only reviewer are separated for `Small` and `Non-trivial` work. |
| 🛡️ Scope control | Implementers stay inside the accepted Plan and allowed write boundary. |
| 🔎 Review | Main-agent self-review does not count; Review must come from a clean-context read-only reviewer. |
| 📋 Completion | Final output records the Approval Ledger, verification, Review status, unresolved risks, and follow-ups. |
| 🧰 Hooks | Minimal validators check Harness artifact shape and block obvious dangerous command patterns. |

## ⚡ 2-Minute Quickstart

1. Start the request with `$harness` and give a concrete objective.

   ```text
   Use $harness for this change.

   Objective: update the CLI usage docs so they explain dry-run mode and failure exit codes.

   Constraints:
   - Do not change CLI implementation.
   - Do not touch release scripts.
   - Verify by inspecting the docs and running existing docs lint if available.
   ```

2. Read the generated Plan. Harness classifies the work as `Tiny`, `Small`, or `Non-trivial`, then states the scope, risks, acceptance criteria, and verification path.

3. Approve implementation only when the Plan is acceptable. The approval prompt must be exactly:

   ```text
   Proceed with this Plan? [y/N]
   ```

   Only lowercase `y` approves execution. Anything else leaves the Plan unapproved.

4. For `Small` and `Non-trivial` work, wait for clean-context Review after implementation.

5. If Review finds must-fix issues, approve repair only through the exact Repair gate:

   ```text
   Proceed with this Repair Plan? [y/N]
   ```

For the full step-by-step guide, see [docs/quickstart/README.md](docs/quickstart/README.md).

## ✅ When to Use Harness

- Public behavior changes, API changes, contracts, schemas, or user-facing workflows
- Multi-file edits where scope drift would be costly
- Security-sensitive, permission-sensitive, deployment-sensitive, or data-sensitive work
- Policy, process, agent, or workflow changes
- Tasks where independent Review should happen before the final answer

## 🚫 When Not to Use Harness

- Tiny one-line fixes where normal Codex execution is enough
- Exploratory questions where no implementation is requested
- Work where you need fast iteration without approval gates
- Documentation that merely mentions Harness, unless you actually want the gated workflow

## 🧱 Task Sizes

`Tiny` is for narrow typo, formatting, comment, or short wording cleanup where one simple check is enough. Review is optional unless project rules, user instructions, or discovered risk require it.

`Small` is for local, low-risk work with a clear verification path. It requires a planner, implementer, and clean-context read-only reviewer.

`Non-trivial` is for meaningful coordination or risk: behavior, API, data, security, dependency, deployment, workflow, policy, contract, multi-file, or cross-module changes. It requires planner, implementer, and reviewer roles, and may use more than one implementer domain.

When a task fits multiple categories, Harness chooses the higher-risk category.

## 👥 Roles

- **Orchestrator:** manages gates, subagent handoffs, scope control, integration, and the final Completion report.
- **Planner:** drafts the accepted Plan with classification, current state, constraints, risks, acceptance criteria, verification strategy, and implementation scope.
- **Implementer:** changes only the accepted files and areas, runs targeted verification, reports changed files, deviations, blocked checks, and risk areas, then stops on scope drift.
- **Reviewer:** runs clean-context read-only Review against the accepted Plan and returns the required Review Matrix plus separated blocking and non-blocking findings.

## 🧩 Subagent Policy

`Tiny` work may be handled by the main agent. `Small` and `Non-trivial` work require actual planner, implementer, and reviewer subagents when tooling allows it.

- `Small`: one planner, one domain implementer, and one reviewer.
- `Non-trivial`: one planner, one or more domain implementers, and one reviewer.
- Large or high-risk work defaults to a maximum of four subagents unless the user approves more.
- Explicit `$harness` invocation preauthorizes only the required planner, implementer, and reviewer subagents. It does not approve destructive commands, secret access, deployment, production-impact work, external network calls, privileged access, or broad rewrites outside the accepted Plan.
- Every subagent receives a bounded brief with objective, role/domain, scope, allowed files or areas, constraints, prohibited actions, required evidence, output format, and stop conditions.
- Default subagent permission is read-only. Only implementers may receive write permission, and only inside the accepted scope.
- Subagent output is evidence; the orchestrator remains responsible for final integration, conflict resolution, verification, and Completion.
- Review is complete only when a clean-context read-only reviewer subagent completes it. Main-agent inspection is not Review.
- If a required subagent cannot complete, Harness records the affected role or gate as `blocked_degraded`. If Review cannot run through the reviewer subagent, the Review status is `review_blocked_degraded`.

## 🛡️ Hooks and Guardrails

Harness includes hook configuration for `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `SubagentStop`, and `Stop`.

The active validators are intentionally minimal:

- `UserPromptSubmit` adds Harness context when `$harness` appears in the prompt.
- `SubagentStop` checks planner, implementer, and reviewer output shape.
- `Stop` checks Plan, Repair Plan, and Completion report structure.
- `PreToolUse` blocks obvious dangerous shell-like commands, including credential reads, environment dumps, recursive secret searches, broad destructive deletes, destructive Git operations, destructive SQL, and production-impact commands.

These hooks support Harness gates. They do not replace sandboxing, permissions, project security controls, or human judgment.

## ⚠️ Current Limitation

The prompt hook currently checks for the `$harness` token or substring anywhere in the submitted prompt. That means documentation work that includes the literal token can also receive active Harness context.

## 🧠 Reasoning Effort

Harness reasoning effort is part of the workflow contract.

- Harness minimum reasoning effort is `high`.
- Planner, Orchestrator, and Improvement use `high` or above.
- Implementer and Reviewer use `xhigh` when available.
- `medium`, `low`, and `minimal` are not valid for Harness workflow roles.
- If `xhigh` is unsupported, Harness falls back to `high`.
- Harness prefers switching to an `xhigh`-capable Codex model before accepting fallback.
- If neither `xhigh` nor a safe fallback path is available, Harness records `blocked_degraded`, records `review_blocked_degraded` for Review, or asks for user approval before continuing.

## 📚 More Docs

- Full quickstart: [docs/quickstart/README.md](docs/quickstart/README.md)
- Korean README: [README.ko.md](README.ko.md)
