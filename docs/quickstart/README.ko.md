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

`Small`과 `Non-trivial` 작업에서 Review는 clean-context read-only reviewer가 수행해야 합니다. reviewer는 변경이 accepted Plan과 일치하는지 확인하고, 필수 Review Matrix를 반환하며, concrete findings를 blocking findings와 non-blocking findings로 분리하거나 다음 정확한 no-finding 형식을 반환합니다.

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
- Approval Ledger
- unresolved risks or follow-ups

Review status는 다음 중 하나입니다.

- `clean_context_review_completed`
- `review_not_required_tiny_only`
- `review_blocked_degraded`

## Configuration & Scope

프로젝트는 `.harness/guard.json`으로 좁은 soft-category 완화와 workflow metadata를 opt-in할 수 있습니다.

지원되는 allow key는 다음과 같습니다.

- `allow_db_local_connections`: `localhost` 또는 `127.0.0.1` 같은 DB host 목록
- `allow_paths`: `tmp/` 또는 `fixtures/` 같은 project path 목록

지원되는 workflow metadata key는 다음과 같습니다.

- `verification_commands`: 프로젝트가 기대하는 verification command 목록
- `review_required`: project policy가 Review를 요구하는지 나타내는 boolean
- `approval_required_paths`: 수정 전 추가 project approval이 필요한 path 목록

Harness guard decision은 Codex approval과 sandboxing 아래의 defense-in-depth signal입니다. allow rule은 현재 `db_client_access` 같은 soft category의 false positive 마찰만 줄이며, secret file read, credential exfiltration, protected broad delete, destructive Git command, destructive SQL, environment dump 같은 hard-deny category는 완화할 수 없습니다. Workflow metadata key는 project expectation을 문서화할 뿐이며 `PreToolUse` hard-deny 또는 soft-relaxation decision을 바꾸지 않습니다. 알 수 없는 key나 잘못된 value가 있으면 guard는 전체 config를 무시하고 stderr warning을 씁니다.

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
