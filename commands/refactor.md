---
description: Serena MCP 기반 자동 리팩토링. 분석 → 계획 → 실행 → 검증의 전체 워크플로우를 수행합니다.
allowed-tools:
  - Task
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - mcp__plugin_serena_serena__find_symbol
  - mcp__plugin_serena_serena__find_referencing_symbols
  - mcp__plugin_serena_serena__get_symbols_overview
  - mcp__plugin_serena_serena__replace_symbol_body
  - mcp__plugin_serena_serena__replace_content
  - mcp__plugin_serena_serena__insert_after_symbol
  - mcp__plugin_serena_serena__insert_before_symbol
  - mcp__plugin_serena_serena__rename_symbol
  - mcp__plugin_serena_serena__activate_project
  - mcp__plugin_serena_serena__execute_shell_command
  - mcp__plugin_serena_serena__write_memory
---

# Refactor Command

Serena MCP를 활용한 전체 리팩토링 워크플로우.

## 사용법

```
/serena-refactor:refactor [target]
```

## 워크플로우 개요

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                     SERENA REFACTORING WORKFLOW                            ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  ┌─────────────────┐                                                      ║
║  │ 0. INITIALIZE   │ ← Serena 프로젝트 활성화 + Git 백업                   ║
║  └────────┬────────┘                                                      ║
║           ▼                                                               ║
║  ┌─────────────────┐                                                      ║
║  │ 1. SOLID 분석   │ ← serena-solid-analyzer                              ║
║  └────────┬────────┘                                                      ║
║           ▼                                                               ║
║  ┌─────────────────┐                                                      ║
║  │ 2. 계획 수립    │ ← refactor-planner                                   ║
║  └────────┬────────┘                                                      ║
║           ▼                                                               ║
║  ╔═════════════════════════════════════════════════════════════════════╗  ║
║  ║  GATE: 사용자 계획 승인                                              ║  ║
║  ╚═══════════════════════════════╤═════════════════════════════════════╝  ║
║                                  ▼                                        ║
║  ┌─────────────────────────────────────────────────────────────────┐     ║
║  │ 3. 단계별 실행                                                    │     ║
║  │    ┌────────────────────────────────────────────────────────┐   │     ║
║  │    │ FOR each step:                                          │   │     ║
║  │    │   3.1 serena-refactor-executor 실행                     │   │     ║
║  │    │   3.2 refactor-auditor 검증                             │   │     ║
║  │    │   3.3 PASS → 다음 단계 / FAIL → 수정                    │   │     ║
║  │    │   [LOOP until all steps complete]                       │   │     ║
║  │    └────────────────────────────────────────────────────────┘   │     ║
║  └────────────────────────────────┬────────────────────────────────┘     ║
║                                   ▼                                       ║
║  ┌─────────────────┐                                                      ║
║  │ 4. 최종 검증    │ ← refactor-auditor (전체)                            ║
║  └────────┬────────┘                                                      ║
║           ▼                                                               ║
║  ┌─────────────────┐                                                      ║
║  │ 5. 완료 리포트  │                                                      ║
║  └─────────────────┘                                                      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## Step 0: 초기화

### Serena 프로젝트 활성화
```
mcp__plugin_serena_serena__activate_project:
  project: [대상 디렉토리]
```

### Git 백업 생성
```bash
git stash push -m "pre-refactor-backup-$(date +%Y%m%d-%H%M%S)"
```

---

## Step 1: SOLID 분석

```
Task:
  agent: serena-solid-analyzer
  prompt: |
    [target] 대상으로 SOLID 분석을 수행하세요.

    Serena 심볼 도구를 활용하여:
    1. 모든 클래스/함수의 구조 분석
    2. 참조 관계 매핑
    3. SOLID 위반 탐지
    4. 각 위반에 대한 자동 수정 경로 제시
```

분석 결과 요약 표시

---

## Step 2: 리팩토링 계획

```
Task:
  agent: refactor-planner
  prompt: |
    SOLID 분석 결과를 바탕으로 리팩토링 계획을 수립하세요.

    요구사항:
    1. 우선순위별 단계 정의
    2. 각 단계의 Serena 도구 실행 계획
    3. 영향 범위 분석
    4. 롤백 경로 명시
```

### 사용자 승인

```yaml
AskUserQuestion:
  question: "리팩토링 계획을 검토했습니다. 진행할까요?"
  header: "계획 승인"
  options:
    - label: "승인 - 진행"
      description: "계획대로 리팩토링 실행"
    - label: "수정 필요"
      description: "계획 조정 후 재검토"
    - label: "취소"
      description: "리팩토링 중단"
```

---

## Step 3: 단계별 실행

### 각 단계에 대해:

#### 3.1 실행
```
Task:
  agent: serena-refactor-executor
  prompt: |
    리팩토링 Step [N]을 실행하세요.

    목표: [단계 목표]
    대상: [심볼 경로]

    Serena 도구 실행 순서:
    1. [도구 및 파라미터]
    2. [도구 및 파라미터]
    ...
```

#### 3.2 검증
```
Task:
  agent: refactor-auditor
  prompt: |
    Step [N] 리팩토링 결과를 검증하세요.

    체크 항목:
    1. 불완전 패턴 (TODO, FIXME)
    2. 참조 무결성
    3. SOLID 개선도
    4. 테스트 통과
```

#### 3.3 결과 처리

**PASS인 경우:**
- 다음 단계 진행
- 진행 상황 업데이트

**FAIL인 경우:**
```yaml
AskUserQuestion:
  question: "Step [N] 검증 실패. 어떻게 할까요?"
  header: "검증 실패"
  options:
    - label: "문제 수정 후 재검증"
      description: "발견된 문제 수정"
    - label: "이 단계 건너뛰기"
      description: "다음 단계로 진행 (권장하지 않음)"
    - label: "롤백"
      description: "이 단계 변경 취소"
```

---

## Step 4: 최종 검증

```
Task:
  agent: refactor-auditor
  prompt: |
    전체 리팩토링 결과를 최종 검증하세요.

    검증 범위: 모든 변경 파일

    체크 항목:
    1. 전체 SOLID 개선도
    2. 모든 테스트 통과
    3. 새로운 위반 없음
    4. 참조 무결성
```

---

## Step 5: 완료 리포트

```markdown
## 리팩토링 완료 리포트

### 요약
- 총 단계: [N]
- 성공 단계: [M]
- 변경 파일: [X]

### SOLID 개선도
| 원칙 | Before | After | 개선율 |
|------|--------|-------|--------|
| SRP | X | Y | +Z% |
| OCP | X | Y | +Z% |
| ... | ... | ... | ... |

### 주요 변경 사항
1. [변경 1]
2. [변경 2]
...

### 테스트 결과
✓ 모든 테스트 통과

### 다음 단계
- `git commit`으로 변경 사항 커밋
- `git stash drop`으로 백업 삭제 (선택)
```

---

## 롤백

언제든지 롤백 가능:

```bash
# 전체 롤백
git stash pop

# 또는 특정 파일만
git checkout -- [file]
```

---

## 핵심 규칙

1. **심볼 도구 우선** - Serena 심볼 도구가 항상 1순위
2. **단계별 검증** - 각 단계 완료 후 반드시 검증
3. **사용자 동의** - 주요 결정은 사용자 승인 필요
4. **롤백 가능** - 언제든 원복 가능한 상태 유지
5. **불완전 금지** - TODO/FIXME 남기면 실패
