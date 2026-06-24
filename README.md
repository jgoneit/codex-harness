# Codex Harness

**Language:** [한국어](README.ko.md) | English

![CI](https://github.com/jgoneit/harness/actions/workflows/ci.yml/badge.svg)

Codex Harness is an early-stage gated workflow plugin for Codex CLI. It helps keep higher-risk agent work deliberate by separating planning, approval, scoped implementation, clean-context review, repair, and completion reporting instead of jumping straight into edits.

```text
Plan -> Execute approval -> Implement -> Review -> Repair Plan -> Repair approval -> Repair Implement -> Completion
```

Use it when a request is risky enough that planning, scoped implementation, and clean-context review should be separated: multi-file edits, workflow or policy updates, behavior changes, security-sensitive work, API or contract changes, and anything that benefits from explicit approval gates.

Harness is not a sandbox, security boundary, or replacement for least-privilege permissions, code review, tests, or human judgment. This project is being shared early so people can experiment with the workflow and provide feedback. The authoritative workflow contract is [docs/contracts/harness-contract.md](docs/contracts/harness-contract.md).

## 👥 Who Is This For?

Harness is for:

- Developers using Codex on multi-file or higher-risk changes where scope control, explicit approval, and independent review matter more than speed
- People experimenting with agent workflow patterns such as planning gates, role separation, and clean-context review
- Teams exploring approval-gated AI coding workflows before deciding whether the pattern fits their process

It is usually not worth using for tiny, low-risk work such as spelling fixes, one-line local cleanups, throwaway experiments, exploratory questions, or tasks where normal Codex execution is already enough.

## 🧭 At a Glance

| Area | What Harness adds |
| --- | --- |
| 🚦 Gates | Implementation and repair only run after exact approval prompts. |
| 🧩 Roles | Planner, implementer, and clean-context read-only reviewer are separated for `Small` and `Non-trivial` work. |
| 🛡️ Scope control | Implementers stay inside the accepted Plan and allowed write boundary. |
| 🔎 Review | Main-agent self-review does not count; Review must come from a clean-context read-only reviewer and use the canonical findings table. |
| 📋 Completion | Final output records the Approval Ledger, verification, Review status, unresolved risks, and follow-ups. |
| 🧰 Hooks | Minimal validators check Harness artifact shape and block obvious dangerous command patterns. |

## ⚙️ Quickstart / Install From Source

Packaging uses tools already assumed by this repository:

- `make`
- `sh`
- `git`
- `zip`
- `unzip`

From a local checkout, build the plugin archive with:

```text
make package
```

This creates `dist/harness.zip`, a loadable Codex plugin bundle that includes `.codex-plugin/plugin.json` and the Harness plugin files.

Install or load that bundle through the Codex CLI plugin or marketplace mechanism supported by your environment, then invoke Harness with a command-like `$harness` prompt. This repository does not currently document one confirmed install command.

The repository marketplace entry `.agents/plugins/marketplace.json` is planned for a later release and is not present in this checkout.

## ⚡ 2-Minute Quickstart

1. Start a prompt line with a command-like `$harness` invocation and give a concrete objective. Optional leading whitespace is allowed, and `use $harness` works when `use` is lowercase.

   ```text
   use $harness for this change.

   Objective: update the CLI usage docs so they explain dry-run mode and failure exit codes.

   Constraints:
   - Do not change CLI implementation.
   - Do not touch release scripts.
   - Verify by inspecting the docs and running existing docs lint if available.
   ```

2. Read the generated Plan. Harness classifies the work as `Tiny`, `Small`, or `Non-trivial`, then states the scope, risks, assumptions, proposed change plan, and verification path.

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

## 📣 Current Status

Harness is an early-stage workflow harness intended for experimentation and feedback. Review it before team or production use, especially the workflow prompts, hook behavior, packaging output, and how it fits your repository rules.

Harness does not replace sandboxing, least-privilege access, normal code review, project-specific security controls, automated verification, or human judgment.

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
- Documentation that merely mentions Harness; do not start a prompt line with a command-like `$harness` invocation unless you actually want the gated workflow

## 🧱 Task Sizes

`Tiny` is for narrow typo, formatting, comment, or short wording cleanup where one simple check is enough. Review is optional unless project rules, user instructions, or discovered risk require it.

`Small` is for local, low-risk work with a clear verification path. It requires a planner, implementer, and clean-context read-only reviewer.

`Non-trivial` is for meaningful coordination or risk: behavior, API, data, security, dependency, deployment, workflow, policy, contract, multi-file, or cross-module changes. It requires planner, implementer, and reviewer roles, and may use more than one implementer domain.

When a task fits multiple categories, Harness chooses the higher-risk category.

For concrete examples, see [docs/classification-examples.md](docs/classification-examples.md).

## 👥 Roles

- **Orchestrator:** manages gates, subagent handoffs, scope control, integration, and the final Completion report.
- **Planner:** drafts the accepted Plan with classification, risk level, in-scope and out-of-scope boundaries, proposed changes, verification strategy, and assumptions.
- **Implementer:** changes only the accepted files and areas, runs targeted verification, reports changed files, deviations, blocked checks, and risk areas, then stops on scope drift.
- **Reviewer:** runs clean-context read-only Review against the accepted Plan and diff, returns the canonical findings table, and gives a `PASS`, `PASS_WITH_NOTES`, `REPAIR_REQUIRED`, or `BLOCKED` verdict.

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
- If a required subagent cannot complete, Harness records the affected role or gate as blocked or degraded. If Review cannot run through the reviewer subagent, the Review status is `review_blocked_degraded`.

## 🛡️ Hooks and Guardrails

Harness includes hook configuration for `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `SubagentStop`, and `Stop`.

The canonical bundled hook config is `hooks/hooks.json`; root `hooks.json` is a compatibility copy and must stay in sync.

The active validators are intentionally minimal:

- `UserPromptSubmit` adds Harness context only when a non-quoted, non-code prompt line starts with a command-like `$harness` invocation: optional leading whitespace, optional lowercase `use `, then exact `$harness` followed by whitespace or end of line. It does not activate for prose-middle mentions, inline backtick mentions, fenced code blocks, blockquotes, uppercase variants, or non-exact tokens such as `$harness-extra`.
- `SubagentStop` checks planner, implementer, and reviewer output shape.
- `Stop` checks Plan, Repair Plan, and Completion report structure.
- `PreToolUse` blocks obvious dangerous shell-like commands, including credential reads, environment dumps, recursive secret searches, broad destructive deletes, destructive Git operations, destructive SQL, and production-impact commands.

These hooks support Harness gates. They do not replace sandboxing, permissions, project security controls, or human judgment.

## 📦 Release Packaging

Create a release zip with:

```text
make package
```

This writes `dist/harness.zip` from Git-tracked and non-ignored files. The archive is the loadable Codex plugin bundle and includes `.codex-plugin/plugin.json`. It verifies the archive does not contain `.git/`, `__MACOSX/`, `__pycache__/`, `*.pyc`, `.DS_Store`, or `dist/` paths; ignored local files are not packaged.

For public releases, attach `dist/harness.zip` as the GitHub release artifact. The repository marketplace entry `.agents/plugins/marketplace.json` is planned for a later release and is not present now.

For the first manual `v0.1.0` release:

- Ensure the working tree is clean.
- Run `make test`.
- Run `make package`.
- Verify `dist/harness.zip`.
- Create the `v0.1.0` tag.
- Create the GitHub Release.
- Upload `dist/harness.zip`.
- Mark the release as pre-release if appropriate.

## ⚠️ Current Limitation

The Harness guard is a denylist-based advisory heuristic, not a security boundary. It blocks known dangerous patterns that its validators recognize, and unrecognized inputs fail open by design. This means fail-open behavior is a structural limit of the guard, not a bug.

The test suite's [`KNOWN_FALSE_NEGATIVE_GAPS`](tests/test_harness_guard_pre_tool_use.py#L160) cases intentionally document examples of this limit. They cover patterns that policy should treat as unsafe but a denylist can miss because they require runtime decoding, variable resolution, embedded interpreter analysis, or coverage of an unbounded set of command forms.

Harness still does not replace sandboxing, least-privilege permissions, project-specific security controls, automated verification, code review, or human judgment.

Prompt activation is narrower than ordinary mentions: Harness context is added only for command-like `$harness` invocations at the start of a non-code, non-quoted prompt line, with optional leading whitespace and optional lowercase `use `; prose-middle mentions, inline code, fenced code blocks, blockquotes, uppercase variants, and non-exact tokens do not activate it.

The planned transition beyond this advisory denylist model is documented in [ADR 0001: P3 Enforcement Model](docs/adr/0001-p3-enforcement-model.md).

## 🧠 Reasoning Effort

Harness reasoning effort is part of the workflow contract.

- Harness minimum reasoning effort is `high`.
- Planner, Orchestrator, and Improvement use `high` or above.
- Implementer and Reviewer use `xhigh` when available.
- `medium`, `low`, and `minimal` are not valid for Harness workflow roles.
- If `xhigh` is unsupported, Harness falls back to `high`.
- Harness prefers switching to an `xhigh`-capable Codex model before accepting fallback.
- If neither `xhigh` nor a safe fallback path is available, Harness records the run as blocked or degraded, records `review_blocked_degraded` for Review, or asks for user approval before continuing.

## 📚 More Docs

- Full quickstart: [docs/quickstart/README.md](docs/quickstart/README.md)
- Workflow contract: [docs/contracts/harness-contract.md](docs/contracts/harness-contract.md)
- P3 enforcement model ADR: [docs/adr/0001-p3-enforcement-model.md](docs/adr/0001-p3-enforcement-model.md)
- Connector integration contract: [docs/contracts/connector-integration.md](docs/contracts/connector-integration.md)
- Worktree Isolation contract: [docs/contracts/worktree-isolation.md](docs/contracts/worktree-isolation.md)
- Sub-agent handoff contract: [docs/contracts/subagent-handoff.md](docs/contracts/subagent-handoff.md)
- Demo scenario: [docs/examples/docs-change.md](docs/examples/docs-change.md)
- Demo scenario: [docs/examples/api-change.md](docs/examples/api-change.md)
- Demo scenario: [docs/examples/security-sensitive-change.md](docs/examples/security-sensitive-change.md)
- Demo scenario: [docs/examples/failed-review-repair-loop.md](docs/examples/failed-review-repair-loop.md)
- Korean README: [README.ko.md](README.ko.md)
