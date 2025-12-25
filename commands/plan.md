---
description: 리팩토링 계획만 수립. 분석 결과를 바탕으로 단계별 계획을 생성하고 사용자 검토를 받습니다.
allowed-tools:
  - Task
  - Read
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__plugin_serena_serena__find_symbol
  - mcp__plugin_serena_serena__find_referencing_symbols
  - mcp__plugin_serena_serena__get_symbols_overview
  - mcp__plugin_serena_serena__list_dir
  - mcp__plugin_serena_serena__activate_project
---

# Plan Command

리팩토링 계획 수립 전용 명령어.

## 사용법

```
/serena-refactor:plan [target]
```

## 워크플로우

### Step 1: Serena 프로젝트 활성화

```
mcp__plugin_serena_serena__activate_project:
  project: [대상 디렉토리]
```

### Step 2: 분석 (간략)

```
Task:
  agent: serena-solid-analyzer
  prompt: |
    [target] 대상으로 SOLID 분석을 수행하세요.
    계획 수립에 필요한 핵심 정보만 수집합니다.
```

### Step 3: 계획 수립

```
Task:
  agent: refactor-planner
  prompt: |
    분석 결과를 바탕으로 상세 리팩토링 계획을 수립하세요.

    포함 사항:
    1. 의존성 그래프
    2. 우선순위별 단계 정의
    3. 각 단계의 Serena 도구 실행 계획
    4. 영향 범위 및 리스크
    5. 롤백 경로
```

### Step 4: 계획 출력 및 저장

```markdown
## 리팩토링 계획: [target]

[상세 계획 내용]

---

계획을 파일로 저장했습니다: .refactor-plan.md

실행하려면: `/serena-refactor:refactor --plan .refactor-plan.md`
```
