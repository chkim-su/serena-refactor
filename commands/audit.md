---
description: 빠른 코드 품질 감사. 리팩토링 전후 품질을 검증합니다.
allowed-tools:
  - Task
  - Read
  - Glob
  - Grep
  - mcp__plugin_serena_serena__find_symbol
  - mcp__plugin_serena_serena__search_for_pattern
  - mcp__plugin_serena_serena__execute_shell_command
  - mcp__plugin_serena_serena__activate_project
---

# Audit Command

리팩토링 품질 감사.

## 사용법

```
/serena-refactor:audit [target]
```

## 워크플로우

### Step 1: 대상 확인

대상이 제공되지 않은 경우:
- Git으로 변경된 파일 자동 감지
- `git diff --name-only HEAD~1`

### Step 2: 감사 실행

```
Task:
  agent: refactor-auditor
  prompt: |
    [target] 대상으로 코드 품질 감사를 수행하세요.

    체크 항목:
    1. 불완전 패턴 (TODO, FIXME)
    2. 참조 무결성
    3. 빈 구현체
    4. SOLID 위반
    5. 테스트 통과
```

### Step 3: 결과 출력

```markdown
## 감사 결과

### 빠른 상태
| 항목 | 상태 |
|------|------|
| 불완전 패턴 | ✓/✗ |
| 참조 무결성 | ✓/✗ |
| 테스트 | ✓/✗ |

### VERDICT: PASS/FAIL

### FAIL 시 조치 사항
1. [수정 필요 항목]
...
```
