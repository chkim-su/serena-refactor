---
description: Serena 기반 코드 추출. 메서드, 인터페이스, 클래스 추출을 심볼 수준에서 안전하게 수행합니다.
allowed-tools:
  - Task
  - Read
  - AskUserQuestion
  - mcp__plugin_serena_serena__find_symbol
  - mcp__plugin_serena_serena__find_referencing_symbols
  - mcp__plugin_serena_serena__replace_symbol_body
  - mcp__plugin_serena_serena__replace_content
  - mcp__plugin_serena_serena__insert_after_symbol
  - mcp__plugin_serena_serena__insert_before_symbol
  - mcp__plugin_serena_serena__activate_project
---

# Extract Command

Serena MCP를 활용한 코드 추출 리팩토링.

## 사용법

```
/serena-refactor:extract <type> <source> [options]
```

### 추출 유형

| 유형 | 설명 | 예시 |
|------|------|------|
| `method` | 메서드 추출 | `/extract method UserService/processUser` |
| `interface` | 인터페이스 추출 | `/extract interface UserService` |
| `class` | 클래스 분리 | `/extract class UserService` |

---

## Method 추출

### 워크플로우

#### 1. 대상 메서드 분석

```
mcp__plugin_serena_serena__find_symbol:
  name_path_pattern: [source]
  include_body: True
```

#### 2. 추출 대상 식별

```yaml
AskUserQuestion:
  question: "추출할 코드 블록을 선택하세요"
  header: "추출 대상"
  options:
    - label: "자동 감지"
      description: "반복/복잡 로직 자동 식별"
    - label: "직접 지정"
      description: "라인 범위 지정"
```

#### 3. 새 메서드 생성

```
mcp__plugin_serena_serena__insert_after_symbol:
  name_path: [source]
  relative_path: [파일]
  body: |
    def extracted_method(params):
        # 추출된 로직
```

#### 4. 원본 수정

```
mcp__plugin_serena_serena__replace_content:
  relative_path: [파일]
  needle: "추출된 코드 패턴"
  repl: "self.extracted_method(args)"
  mode: "regex"
```

---

## Interface 추출

### 워크플로우

#### 1. 클래스 분석

```
mcp__plugin_serena_serena__find_symbol:
  name_path_pattern: [source]
  depth: 1
  include_body: False
```

#### 2. 공개 메서드 식별

Public 메서드만 인터페이스에 포함

#### 3. 인터페이스 생성

```
mcp__plugin_serena_serena__insert_before_symbol:
  name_path: [source]
  relative_path: [파일]
  body: |
    interface IClassName {
        method1(param: Type): ReturnType;
        method2(): void;
    }
```

#### 4. 클래스 수정

```
mcp__plugin_serena_serena__replace_symbol_body:
  name_path: [source]
  relative_path: [파일]
  body: |
    class ClassName implements IClassName {
        // 기존 구현
    }
```

---

## Class 분리

### 워크플로우

#### 1. 책임 분석

```
mcp__plugin_serena_serena__find_symbol:
  name_path_pattern: [source]
  depth: 1
  include_body: False
```

메서드를 책임별로 그룹화

#### 2. 분리 계획

```yaml
AskUserQuestion:
  question: "클래스 분리 방식을 선택하세요"
  header: "분리 전략"
  options:
    - label: "자동 그룹화"
      description: "메서드 이름/의존성 기반 자동 분리"
    - label: "직접 지정"
      description: "분리할 메서드 그룹 지정"
```

#### 3. 새 클래스 생성

```
mcp__plugin_serena_serena__insert_after_symbol:
  name_path: [source]
  relative_path: [파일]
  body: |
    class ExtractedClass {
        // 분리된 메서드들
    }
```

#### 4. 원본 클래스에서 위임

```
mcp__plugin_serena_serena__replace_symbol_body:
  # 이동된 메서드를 위임 호출로 교체
```

---

## 출력 형식

```markdown
## 추출 완료: [type]

### 생성된 심볼
- 이름: [new_symbol]
- 파일: [file:line]
- 타입: [method/interface/class]

### 수정된 심볼
- 원본: [source]
- 변경 사항: [설명]

### 참조 업데이트
| 파일 | 변경 내용 |
|------|-----------|
| ... | ... |

### 다음 단계
- 테스트 실행: `npm test`
- 추가 리팩토링 필요 시: `/serena-refactor:refactor`
```

---

## 핵심 규칙

1. **심볼 수준 조작** - 텍스트 치환 대신 Serena 심볼 도구
2. **참조 자동 업데이트** - 추출 후 모든 호출처 자동 수정
3. **원자적 변경** - 추출 작업은 한 번에 완료
4. **롤백 가능** - Git으로 언제든 원복
