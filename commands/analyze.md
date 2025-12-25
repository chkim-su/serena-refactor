---
description: Serena MCP 기반 SOLID 분석. 심볼 수준 분석으로 정확한 위반 탐지와 자동 수정 경로를 제시합니다.
allowed-tools:
  - Task
  - Read
  - Glob
  - Grep
  - mcp__plugin_serena_serena__get_symbols_overview
  - mcp__plugin_serena_serena__list_dir
  - mcp__plugin_serena_serena__activate_project
---

# Analyze Command

Serena MCP를 활용한 심볼 수준 SOLID 분석.

## 사용법

```
/serena-refactor:analyze [target]
```

## 워크플로우

### Step 0: Serena 프로젝트 활성화

```
mcp__plugin_serena_serena__activate_project:
  project: [현재 디렉토리]
```

### Step 1: 대상 선택

대상이 제공되지 않은 경우:
```yaml
AskUserQuestion:
  question: "무엇을 분석할까요?"
  header: "분석 대상"
  options:
    - label: "현재 디렉토리"
      description: "전체 프로젝트 분석"
    - label: "특정 경로"
      description: "디렉토리 또는 파일 지정"
```

### Step 2: 분석 실행

```
Task:
  agent: serena-solid-analyzer
  prompt: |
    [target] 대상으로 SOLID 분석을 수행하세요.

    다음을 포함해야 합니다:
    1. 심볼 수준 분석 (get_symbols_overview, find_symbol)
    2. 참조 영향도 분석 (find_referencing_symbols)
    3. 각 위반에 대한 Serena 도구 기반 수정 경로
    4. 정확한 file:line 레퍼런스
```

### Step 3: 결과 출력

```markdown
## 분석 리포트: [target]

### 빠른 요약
| 원칙 | 상태 | 위반 수 | 영향 범위 |
|------|------|---------|-----------|
| SRP | OK/WARN/FAIL | X | Y files |
| OCP | OK/WARN/FAIL | X | Y files |
| LSP | OK/WARN/FAIL | X | Y files |
| ISP | OK/WARN/FAIL | X | Y files |
| DIP | OK/WARN/FAIL | X | Y files |

### 주요 이슈 (우선순위순)
1. **[CRITICAL]** [file:line] - [이슈] → Serena 수정: [도구명]
2. ...

### 권장 사항
- `/serena-refactor:refactor`를 사용하여 자동 수정 실행
- `/serena-refactor:plan`으로 단계별 계획 수립
```
