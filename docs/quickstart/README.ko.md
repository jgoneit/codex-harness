# Harness Quickstart

이 quickstart는 Codex에서 Harness plugin을 사용할 수 있는 상태를 기준으로 설명합니다.

## 1. Harness를 명시적으로 호출하기

요청을 `$harness`로 시작하거나 작업 내용에 명확히 포함합니다.

```text
Use $harness to plan, implement, and review this change:
Update the public docs for the payment retry behavior.
```

Harness는 `$harness`를 명시적으로 호출하는 방식으로 사용하도록 의도되어 있습니다. 현재 제한: hook trigger는 제출된 prompt 안에 `$harness` token/substring이 있는지만 확인하므로, `$harness`가 포함된 문서 설명도 Harness active context를 받을 수 있습니다.

## 2. Plan 검토하기

Harness는 먼저 local project rules를 확인하고 작업을 `Tiny`, `Small`, `Non-trivial`로 분류합니다.

`Small`과 `Non-trivial` 작업에서는 planner role이 다음 내용을 포함한 Plan을 만듭니다.

- classification
- requirements and current state
- constraints and risks
- acceptance criteria
- verification strategy
- orchestration topology
- implementation scope

Plan은 반드시 다음 문장으로 끝나야 합니다.

```text
Proceed with this Plan? [y/N]
```

정확히 `y`로 답해야 승인됩니다. 다른 모든 응답은 Plan을 승인하지 않은 것으로 처리됩니다.

## 3. Implement를 허용된 범위 안에서 실행하기

정확한 Plan approval 이후 Harness는 accepted scope와 write boundary만 implementer에게 전달합니다. implementer는 다음을 보고합니다.

- identity and domain
- files changed
- implementation summary
- verification performed
- blocked checks
- deviations or risk areas

accepted Plan 밖에서 새 파일, 더 넓은 범위, destructive command, secret access, deployment, production-impact operation이 필요해지면 Harness는 조용히 범위를 넓히지 않고 새 gate를 위해 멈춥니다.

## 4. Review 기다리기

`Small`과 `Non-trivial` 작업에서 Review는 clean-context read-only reviewer가 수행해야 합니다. reviewer는 변경이 accepted Plan과 일치하는지 확인하고, concrete finding 또는 다음 정확한 no-finding 형식을 반환합니다.

```text
No concrete findings. Residual verification risk:
- ...
```

main agent의 자체 점검은 Review로 인정되지 않습니다.

## 5. 필요한 경우에만 Repair 승인하기

Review에서 must-fix issue가 나오면 Harness는 Repair Plan을 작성합니다. Repair 작업에는 다음 정확한 prompt가 필요합니다.

```text
Proceed with this Repair Plan? [y/N]
```

정확히 `y`로 답해야 repair implementation이 승인됩니다. 다른 모든 응답은 repair work를 승인하지 않은 것으로 처리됩니다.

## 6. Completion Report 확인하기

Harness는 마지막에 다음 내용을 포함한 Completion report를 냅니다.

- task classification
- orchestration topology and spawned roles
- implemented changes
- verification performed
- Review status
- findings addressed
- unresolved risks or follow-ups

Review status는 다음 중 하나입니다.

- `clean_context_review_completed`
- `review_not_required_tiny_only`
- `review_blocked_degraded`

## Example Prompt

```text
Use $harness for this change.

Objective: update the CLI usage docs so they explain dry-run mode and failure exit codes.

Constraints:
- Do not change CLI implementation.
- Do not touch release scripts.
- Verify by inspecting the docs and running existing docs lint if available.
```

이렇게 objective, scope boundary, verification expectation을 분명히 적으면 Plan gate 전에 Harness가 작업 범위를 더 정확히 잡을 수 있습니다.
