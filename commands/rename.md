---
description: Serena 기반 안전한 심볼 이름 변경. 코드베이스 전체에서 모든 참조를 자동으로 업데이트합니다.
allowed-tools:
  - Task
  - Read
  - AskUserQuestion
  - mcp__plugin_serena_serena__find_symbol
  - mcp__plugin_serena_serena__find_referencing_symbols
  - mcp__plugin_serena_serena__rename_symbol
  - mcp__plugin_serena_serena__activate_project
---

# Rename Command

Serena MCP를 활용한 안전한 심볼 이름 변경.

## 사용법

```
/serena-refactor:rename <symbol> <new-name>
```

## 예시

```
/serena-refactor:rename UserService/getUser fetchUserById
/serena-refactor:rename OldClassName NewClassName
```

## 워크플로우

### Step 1: 심볼 확인

```
mcp__plugin_serena_serena__find_symbol:
  name_path_pattern: [symbol]
  include_body: False
```

심볼을 찾지 못한 경우:
```yaml
AskUserQuestion:
  question: "심볼 '[symbol]'을 찾을 수 없습니다. 정확한 경로를 입력해주세요."
  header: "심볼 경로"
```

### Step 2: 영향 범위 분석

```
mcp__plugin_serena_serena__find_referencing_symbols:
  name_path: [symbol]
  relative_path: [파일]
```

### Step 3: 변경 미리보기

```markdown
## 이름 변경 미리보기

### 대상 심볼
- 이름: [symbol]
- 파일: [file:line]
- 타입: [class/method/function/variable]

### 영향 범위
| 파일 | 참조 수 | 코드 스니펫 |
|------|---------|-------------|
| src/service.ts | 3 | `userService.getUser()` |
| src/controller.ts | 2 | `getUser(id)` |
| ... | ... | ... |

**총 참조: N개**
```

### Step 4: 사용자 확인

```yaml
AskUserQuestion:
  question: "[symbol] → [new-name] 변경을 진행할까요? (N개 참조 업데이트)"
  header: "이름 변경"
  options:
    - label: "진행"
      description: "모든 참조 자동 업데이트"
    - label: "취소"
      description: "변경 취소"
```

### Step 5: 이름 변경 실행

```
mcp__plugin_serena_serena__rename_symbol:
  name_path: [symbol]
  relative_path: [파일]
  new_name: [new-name]
```

### Step 6: 결과 확인

```markdown
## 이름 변경 완료

✓ [symbol] → [new-name]
✓ [N]개 참조 업데이트 완료

### 변경된 파일
- src/service.ts
- src/controller.ts
- ...

### 다음 단계
- 테스트 실행 권장: `npm test`
- 문제 발생 시 롤백: `git checkout -- .`
```

---

## 핵심 규칙

1. **심볼 도구 신뢰** - Serena rename_symbol은 모든 참조 자동 업데이트
2. **미리보기 필수** - 변경 전 영향 범위 확인
3. **사용자 확인** - 실행 전 명시적 동의
4. **테스트 권장** - 변경 후 테스트 실행 권장
