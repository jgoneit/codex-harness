---
name: harness
description: Use only on explicit $harness invocation. Runs the Harness workflow loop with classification, Plan approval, role-separated Implement, clean-context Review, Repair Plan approval, and Completion gates. Trigger when the user explicitly invokes $harness for controlled implementation or review workflows; do not use for ordinary requests, documentation mentions, or implicit inference.
---

# Harness

`$harness` is a Codex execution router for the Harness workflow loop. Default explanation language is Korean; fixed workflow terms stay in English.

```text
Plan -> Execute approval -> Implement -> Review -> Repair Plan -> Repair approval -> Repair Implement -> Completion
```

## Activation

- Use this skill only when the user explicitly invokes `$harness`.
- Do not activate from ordinary requests, implicit inference, or documentation mentions.
- Do not require Codex Plan Mode; run the Harness gates inside the conversation.
- Do not assume stack, language, framework, database, test runner, or deployment platform.
- Before planning, inspect local project rules such as `AGENTS.md`, `README.md`, contributing docs, manifests, and `.harness/guard.json` when present.

## Instruction Precedence

Apply instructions and conventions in this order:

1. Explicit user instructions
2. Harness workflow safety rules, including hard-deny rules and approval gates
3. Project policy from `.harness/guard.json` policy keys
4. Local repo docs such as `README.md`, `AGENTS.md`, and contributing docs
5. Inferred conventions

Planning reads `.harness/guard.json` policy keys at the start. `.harness/guard.json` is the only Harness project policy/config file; do not infer `harness.md`, `.harnessrc.yaml`, or other project policy file conventions. Project policy cannot weaken Harness workflow safety rules. Destructive operations and secret or protected-config work need explicit approval regardless of project policy.

For concrete task sizing examples, see [classification examples](../../docs/classification-examples.md).
For the authoritative workflow artifact contract, see [Harness workflow contract](../../docs/contracts/harness-contract.md).

## Required Reference Loading

Read the relevant references before acting:

- Always follow `../../docs/contracts/harness-contract.md` for canonical artifact sections, approval gates, Review rules, and Completion statuses.
- Always read `references/classification-policy.md`, `references/phase-contracts.md`, `references/orchestrator-harness.md`, `references/subagent-policy.md`, `references/model-policy.md`, and `references/completion-policy.md`.
- For planning, read `references/planner-harness.md` and use `assets/templates/plan.md`.
- For implementation, read `references/implementer-harness.md` and use `assets/templates/implement.md`.
- For review, read `references/reviewer-harness.md`, `assets/templates/review.md`, and `assets/templates/reviewer-brief.md`.
- For repair, use `assets/templates/repair-plan.md`.
- For completion, use `assets/templates/completion-report.md`.
- If the task is `Non-trivial`, review is blocked/degraded, repair occurred, two or more Plan revisions occurred, or Harness policy/templates/orchestration rules changed, read `references/improvement-policy.md` and use `assets/templates/improvement.md`.

## Non-Negotiable Rules

- Classification must happen before phase gates.
- `Tiny` may be handled directly by the orchestrator.
- `Small` and `Non-trivial` require planner, implementer, and clean-context read-only reviewer subagents.
- For `Small` and `Non-trivial`, the main agent is the orchestrator.
- Harness minimum reasoning effort is `high`; Implement and Review require `xhigh` when available. Do not use medium, low, or minimal for `$harness`.
- Do not implement before Plan approval.
- The Plan approval prompt must be exactly:

```text
Proceed with this Plan? [y/N]
```

- Only lowercase `y` approves execution of the accepted Plan. Ambiguous natural language means no decision; ask again for explicit `y` or `n`. Non-approval (`n`, empty response, uppercase variants such as `N`, expanded variants, and any other non-`y` response that is not ambiguous) stops by default; do not implement, revise, or replan unless the user explicitly asks to revise/replan. `[y/N]` means No is the default.
- Do not repair before Repair Plan approval.
- The Repair Plan approval prompt must be exactly:

```text
Proceed with this Repair Plan? [y/N]
```

- Only lowercase `y` approves execution of the accepted Repair Plan. Ambiguous natural language means no decision; ask again for explicit `y` or `n`. Non-approval (`n`, empty response, uppercase variants such as `N`, expanded variants, and any other non-`y` response that is not ambiguous) stops by default; do not repair, revise, or replan unless the user explicitly asks to revise/replan. `[y/N]` means No is the default.
- Only a clean-context read-only reviewer subagent can complete Review.
- Main-agent self-review is not Review.
- Required gate failure must be recorded as blocked or degraded.
- Dangerous operations require separate approval.
- A Completion report is required.

## Loop

1. Inspect local project rules, `.harness/guard.json` policy keys, and the user request.
2. Classify the task as `Tiny`, `Small`, or `Non-trivial`.
3. For `Small` or larger tasks, define subagent topology.
4. Produce a Plan artifact and ask for Plan approval.
5. If the user replies exactly `y`, implement only the accepted Plan; otherwise stop unless the user explicitly asks to revise/replan.
6. For `Small` or larger tasks, run clean-context read-only reviewer Review.
7. If Review has findings requiring repair, produce a Repair Plan and ask for repair approval.
8. If the user replies exactly `y`, implement only the accepted Repair Plan and repeat the bounded Review/Repair loop if required; otherwise stop unless the user explicitly asks to revise/replan.
9. Produce the Completion report with status, verification, risks, and follow-ups.

## Hooks

Minimal non-destructive validators run for `UserPromptSubmit`, `SubagentStop`, and `Stop`; `PreToolUse` blocks obvious dangerous commands; `SessionStart` remains visibility-only. Hooks do not replace Harness gates or project security controls.
