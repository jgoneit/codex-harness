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
| 📋 Completion | Final output records verification, Review status, unresolved risks, and follow-ups. |
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
- **Reviewer:** runs clean-context read-only Review against the accepted Plan and looks for bugs, missing tests, contract drift, security issues, performance risk, scope creep, and rule violations.

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

Harness requires high reasoning effort or above. Implement and Review require `xhigh` when available. If `xhigh` is unavailable, Harness records the fallback or degraded state according to policy.

## 📚 More Docs

- Full quickstart: [docs/quickstart/README.md](docs/quickstart/README.md)
- Korean README: [README.ko.md](README.ko.md)
