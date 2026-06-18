# Hook Policy

Bundled hooks are minimal non-destructive validators. They support discovery, lifecycle visibility, and text-shape checks for Harness artifacts.

## Current Status

- `SessionStart` remains visibility-only.
- `UserPromptSubmit`, `SubagentStop`, and `Stop` run minimal non-destructive validators.
- `PreToolUse` v1 blocks obvious dangerous commands before tool execution.
- Validators and guardrails are deterministic and pattern-based.
- Hooks do not replace Harness gates, sandboxing, code review, permissions, or project security controls.
- The canonical bundled hook config is `hooks/hooks.json`. Root `hooks.json` is a compatibility copy and must not drift from the canonical event set.

## Principles

- Hooks must be deterministic, minimal, and auditable.
- Hooks must be easy to disable.
- Hook failures may be recorded as evidence but do not make skill use impossible by themselves.
- Do not duplicate hook definitions across the same layer.

## Active Validator Scope

- `UserPromptSubmit`: inject Harness context when the submitted prompt contains `$harness`.
- `SubagentStop`: validate planner, implementer, and reviewer output structure.
- `Stop`: validate Plan, Repair Plan, and Completion report structure.
- `PreToolUse`: block obvious dangerous shell-like commands, including secret-file reads, environment dumps, broad destructive deletion, destructive Git operations, destructive SQL, production-impact commands, and credential exfiltration.

## Out of Scope

These hooks are not a complete security boundary. They do not perform live runtime validation, infer production environment state, or replace existing project security controls.

## Limitations

Hooks cannot convert orchestration failure into success. If required subagents are unavailable, record `blocked_degraded`. If clean-context reviewer Review is unavailable, record `review_blocked_degraded`.

## Future Work

- Allowlist policy.
- Configurable deny and warn modes.
- Project-specific patterns.
- Database and production environment detection.
- Live runtime validation.
