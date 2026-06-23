# Codex Harness

**언어:** 한국어 | [English](README.md)

Codex Harness는 Codex에서 사용하는 gated workflow plugin입니다. 바로 실행하기보다 **Harness Plan -> Implement -> Clean-context Review -> Repair -> Completion Report** 흐름으로 조심스럽게 진행해야 하는 작업을 위해 만들었습니다.

```text
Harness Plan -> Execute approval -> Implement -> Clean-context Review -> Repair Plan -> Repair approval -> Repair Implement -> Completion Report
```

여러 파일을 고치는 작업, workflow나 policy 변경, 동작 변경, security 관련 작업, API나 contract 변경처럼 계획, 제한된 구현, 독립 Review를 분리하는 편이 안전한 요청에 사용합니다.

## 🧭 한눈에 보기

| 영역 | Harness가 추가하는 것 |
| --- | --- |
| 🚦 Gate | Implement와 Repair는 정확한 approval prompt 이후에만 실행됩니다. |
| 🧩 역할 분리 | `Small`, `Non-trivial` 작업에서 planner, implementer, Clean-context Review reviewer를 분리합니다. |
| 🛡️ 범위 제어 | implementer는 accepted Plan과 허용된 write boundary 안에서만 작업합니다. |
| 🔎 Review | main agent의 자체 점검은 Clean-context Review로 인정하지 않고, clean-context read-only reviewer가 확인합니다. |
| 📋 Completion | Approval Ledger, verification, Review status, unresolved risks, follow-ups를 Completion Report에 남깁니다. |
| 🧰 Hooks | Harness artifact 형식과 명백히 위험한 command pattern을 최소한으로 검사합니다. |

## ⚡ 2분 Quickstart

1. 요청을 `$harness`로 시작하고 objective를 구체적으로 적습니다.

   ```text
   Use $harness for this change.

   Objective: update the CLI usage docs so they explain dry-run mode and failure exit codes.

   Constraints:
   - Do not change CLI implementation.
   - Do not touch release scripts.
   - Verify by inspecting the docs and running existing docs lint if available.
   ```

2. 생성된 Harness Plan을 검토합니다. Harness는 작업을 `Tiny`, `Small`, `Non-trivial`로 분류하고 scope, risks, acceptance criteria, verification path를 제시합니다.

3. Plan이 적절할 때만 구현을 승인합니다. approval prompt는 반드시 다음과 같아야 합니다.

   ```text
   Proceed with this Plan? [y/N]
   ```

   오직 소문자 `y`만 실행 승인입니다. 다른 응답은 Plan을 승인하지 않은 것으로 처리됩니다.

4. `Small`과 `Non-trivial` 작업에서는 구현 후 Clean-context Review를 기다립니다.

5. Review에서 반드시 고쳐야 할 이슈가 나오면 다음 Repair gate로만 수정을 승인합니다.

   ```text
   Proceed with this Repair Plan? [y/N]
   ```

전체 절차형 안내는 [docs/quickstart/README.ko.md](docs/quickstart/README.ko.md)를 참고하세요.

## ✅ Harness를 쓰기 좋은 경우

- public behavior, API, contract, schema, user-facing workflow 변경
- scope drift가 비용을 만들 수 있는 multi-file edit
- security, permission, deployment, data 관련 risk가 있는 작업
- policy, process, agent, workflow 변경
- 최종 답변 전에 독립 Review가 필요한 작업

## 🚫 Harness가 굳이 필요 없는 경우

- 일반 Codex 실행으로 충분한 아주 작은 한 줄 수정
- 구현이 아니라 설명만 필요한 탐색성 질문
- approval gate 없이 빠르게 반복해야 하는 작업
- Harness를 설명하는 문서 작업 중 실제 gated workflow를 원하지 않는 경우

## 🧱 작업 크기

`Tiny`는 typo 수정, formatting-only 변경, comment-only 변경, 의미가 바뀌지 않는 짧은 문구 정리처럼 범위가 좁고 간단한 확인 하나로 충분한 작업입니다. 다만 project rule, user instruction, 또는 발견된 risk가 Review를 요구하면 Review 규칙을 따릅니다.

`Small`은 명확한 verification path가 있는 local, low-risk 작업입니다. planner, implementer, Clean-context Review reviewer가 필요합니다.

`Non-trivial`은 의미 있는 조율이나 risk가 있는 작업입니다. behavior, API, data, security, dependency, deployment, workflow, policy, contract, multi-file, cross-module 변경이 여기에 들어갑니다. planner, implementer, reviewer가 필요하며, 필요하면 implementer domain을 둘 이상 둘 수 있습니다.

여러 분류에 동시에 해당하면 Harness는 더 높은 risk 분류를 선택합니다.

구체적인 예시는 [docs/classification-examples.md](docs/classification-examples.md)를 참고하세요.

## 👥 역할

- **Orchestrator:** gate, subagent handoff, scope control, integration, 최종 Completion Report를 관리합니다.
- **Planner:** classification, current state, constraints, risks, acceptance criteria, verification strategy, implementation scope가 포함된 accepted Plan을 준비합니다.
- **Implementer:** accepted file과 area 안에서만 변경하고, targeted verification을 실행하며, changed files, deviations, blocked checks, risk areas를 보고합니다. scope drift가 생기면 멈춥니다.
- **Reviewer:** accepted Plan 기준으로 Clean-context Review를 수행하고, `Severity`, `Finding`, `Evidence`, `Required Action` columns가 있는 Findings Table과 `PASS`, `PASS_WITH_NOTES`, `REPAIR_REQUIRED`, `BLOCKED` 중 하나의 Verdict를 반환합니다.

## 🧩 Subagent 활용 정책

`Tiny` 작업은 main agent가 처리할 수 있습니다. `Small`과 `Non-trivial` 작업은 tooling이 허용하는 경우 실제 planner, implementer, reviewer subagent가 필요합니다.

- `Small`: planner 1명, domain implementer 1명, reviewer 1명.
- `Non-trivial`: planner 1명, domain implementer 1명 이상, reviewer 1명.
- 크거나 risk가 높은 작업은 사용자가 더 많이 승인하지 않는 한 기본 최대 4개 subagent를 사용합니다.
- 명시적인 `$harness` 호출은 필요한 planner, implementer, reviewer subagent 생성만 policy preauthorization으로 허용합니다. destructive command, secret access, deployment, production-impact work, external network call, privileged access, accepted Plan 밖의 broad rewrite를 승인하지 않습니다.
- 모든 subagent는 objective, role/domain, scope, 허용된 file 또는 area, constraints, prohibited actions, required evidence, output format, stop conditions가 포함된 bounded brief를 받습니다.
- 기본 subagent 권한은 read-only입니다. write permission은 implementer만 받을 수 있고 accepted scope 안으로 제한됩니다.
- subagent output은 evidence입니다. 최종 integration, conflict resolution, verification, Completion 책임은 orchestrator에게 남습니다.
- Clean-context Review는 clean-context read-only reviewer subagent가 완료해야만 완료로 인정됩니다. main-agent inspection은 Review가 아닙니다.
- 필요한 subagent가 완료되지 못하면 Harness는 해당 role 또는 gate를 blocked/degraded run state로 기록합니다. reviewer subagent로 Review를 실행할 수 없으면 Review status enum은 `review_blocked_degraded`입니다.

## 🛡️ Hooks와 Guardrails

Harness에는 `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `SubagentStop`, `Stop`용 hook configuration이 포함되어 있습니다.

현재 validator는 의도적으로 최소 범위만 다룹니다.

- `UserPromptSubmit`은 prompt에 `$harness`가 있을 때 Harness context를 추가합니다.
- `SubagentStop`은 planner, implementer, reviewer output shape를 확인합니다.
- `Stop`은 Harness Plan, Repair Plan, Completion Report structure를 확인합니다.
- `PreToolUse`는 credential read, environment dump, recursive secret search, broad destructive delete, destructive Git operation, destructive SQL, production-impact command처럼 명백히 위험한 shell-like command를 차단합니다.

이 hooks는 Harness gate를 보조합니다. sandboxing, permission, project security control, 사람의 판단을 대체하지 않습니다.

## ⚠️ 현재 제한

prompt hook은 제출된 prompt 안에 `$harness` token 또는 substring이 있는지만 확인합니다. 그래서 literal token이 포함된 문서 작업도 Harness active context를 받을 수 있습니다.

## 🧠 Reasoning Effort

Harness reasoning effort는 workflow contract의 일부입니다.

- Harness 최소 reasoning effort는 `high`입니다.
- Planner, Orchestrator, Improvement는 `high` 이상을 사용합니다.
- Implementer와 Reviewer는 가능할 때 `xhigh`를 사용합니다.
- Harness workflow role에는 `medium`, `low`, `minimal`을 사용하지 않습니다.
- `xhigh`를 지원하지 않으면 Harness는 `high`로 fallback합니다.
- Harness는 fallback을 받아들이기 전에 `xhigh`를 지원하는 Codex model로 전환하는 것을 우선합니다.
- `xhigh`도 안전한 fallback path도 사용할 수 없으면 Harness는 blocked/degraded run state를 기록하고, Review의 경우 `review_blocked_degraded`를 기록하거나 계속하기 전에 사용자 승인을 요청합니다.

## 📚 더 보기

- 전체 quickstart: [docs/quickstart/README.ko.md](docs/quickstart/README.ko.md)
- English README: [README.md](README.md)
