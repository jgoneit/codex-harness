# Orchestrator Harness

The main agent is the orchestrator for `Small` and larger tasks. It manages phase gates and subagent handoff rather than directly implementing.

## Sequence

1. Inspect local project rules.
2. Classify the task.
3. Define required topology for `Small` and larger tasks.
4. Brief the planner subagent.
5. Review planner output and finalize the Plan artifact.
6. Ask exactly `Proceed with this Plan? [y/N]`
7. Only lowercase `y` approves execution of the accepted Plan. Ambiguous natural language means no decision; ask again for explicit `y` or `n`. Non-approval (`n`, empty response, uppercase variants such as `N`, expanded variants, and any other non-`y` response that is not ambiguous) stops by default; do not implement, revise, or replan unless the user explicitly asks to revise/replan. `[y/N]` means No is the default.
8. If the user replies with non-approval, stop the Harness run unless the same response explicitly requests revision or replanning.
9. If the user replies exactly `y`, brief the domain implementer.
10. Integrate implementer output, diff, and verification.
11. Brief the clean-context read-only reviewer.
12. If findings exist, write a Repair Plan.
13. Ask exactly `Proceed with this Repair Plan? [y/N]`
14. Only lowercase `y` approves execution of the accepted Repair Plan. Ambiguous natural language means no decision; ask again for explicit `y` or `n`. Non-approval (`n`, empty response, uppercase variants such as `N`, expanded variants, and any other non-`y` response that is not ambiguous) stops by default; do not repair, revise, or replan unless the user explicitly asks to revise/replan. `[y/N]` means No is the default.
15. If the user replies with non-approval, stop the Repair loop unless the same response explicitly requests revision or replanning. Implement only exactly approved repairs and repeat the bounded loop as needed.
16. Produce the Completion report.

## Orchestration Record

Plan or Completion must record required subagents, spawned subagents, role/domain assignments, authorization or policy preauthorization, `blocked_degraded` roles, handoff summary, approval prompts and responses, integration conflicts, and conflict resolution.

## Conflict Handling

Resolve subagent output conflicts with evidence. If evidence cannot resolve the conflict, stop and escalate.

## Scope Control

Do not accept opportunistic refactors. If implementer work requires scope outside the accepted Plan, return to Plan or defer it.

## Final Responsibility

The orchestrator owns final verification, diff inspection, and final response even when subagents perform work.
