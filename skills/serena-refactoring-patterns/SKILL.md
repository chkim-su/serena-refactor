---
description: Serena MCP 도구를 활용한 심볼릭 리팩토링 패턴. 안전한 코드 수정, 참조 추적, 자동화된 리팩토링 워크플로우의 핵심 패턴들.
name: serena-refactoring-patterns
---
# Serena Symbolic Refactoring Patterns

## 핵심 원칙

**심볼 수준에서 코드를 이해하고 수정하라.**
텍스트 치환이 아닌 AST 기반 편집으로 안전성을 보장한다.

---

## 1. 심볼 탐색 패턴

### 1.1 계층적 심볼 탐색

```
1. get_symbols_overview로 파일 구조 파악 (depth=0)
2. 관심 클래스 발견 시 depth=1로 메서드 목록 확인
3. 특정 메서드 본문 필요 시 find_symbol + include_body=True
```

### 1.2 이름 패턴 검색

| 패턴 | 의미 | 예시 |
|------|------|------|
| `ClassName` | 해당 이름의 모든 클래스 | `UserService` |
| `ClassName/method` | 특정 클래스의 메서드 | `UserService/create` |
| `/ClassName/method` | 정확한 경로 매칭 | `/UserService/create` |
| `get*` (substring_matching=True) | 접두사 매칭 | `getValue`, `getData` |

### 1.3 참조 추적

```
find_referencing_symbols 사용:
- 리팩토링 영향 범위 파악
- 의존성 그래프 구축
- 순환 참조 탐지
```

---

## 2. 안전한 수정 패턴

### 2.1 심볼 교체 (Replace Symbol Body)

**사용 시점:**
- 함수/메서드 전체 재작성
- 클래스 정의 변경
- 시그니처 포함 수정

**주의사항:**
- body는 docstring/주석 미포함
- 시그니처부터 포함해야 함
- 들여쓰기 정확히 맞춰야 함

### 2.2 콘텐츠 교체 (Replace Content)

**사용 시점:**
- 심볼 내부 일부 라인만 수정
- 정규식 기반 일괄 치환
- 여러 위치 동시 수정

**패턴:**
```
mode: "regex"
needle: "old_pattern.*?end_marker"
repl: "new_content"
allow_multiple_occurrences: True/False
```

### 2.3 삽입 패턴

| 도구 | 용도 |
|------|------|
| `insert_before_symbol` | import 추가, 데코레이터 추가 |
| `insert_after_symbol` | 새 메서드/클래스 추가 |

---

## 3. 리팩토링 워크플로우

### 3.1 Extract Method

```
1. find_symbol로 대상 메서드 본문 읽기
2. 추출할 코드 블록 식별
3. 새 메서드 시그니처 설계
4. insert_after_symbol로 새 메서드 추가
5. replace_content로 원본에서 호출로 교체
6. find_referencing_symbols로 영향 확인
```

### 3.2 Rename Symbol

```
1. find_referencing_symbols로 모든 사용처 파악
2. rename_symbol로 코드베이스 전체 이름 변경
3. 결과 검증 (자동으로 모든 참조 업데이트)
```

### 3.3 Extract Interface

```
1. find_symbol + depth=1로 클래스 메서드 목록
2. 공통 메서드 식별
3. 새 인터페이스 정의 작성
4. insert_before_symbol로 인터페이스 추가
5. replace_symbol_body로 클래스가 인터페이스 구현하도록 수정
```

### 3.4 Move Method

```
1. find_symbol로 원본 메서드 읽기 (include_body=True)
2. 대상 클래스에 insert_after_symbol로 메서드 추가
3. find_referencing_symbols로 모든 호출처 파악
4. replace_content로 호출처 업데이트
5. 원본 메서드 삭제 (replace_symbol_body with empty or remove)
```

---

## 4. SOLID 위반 자동 수정

### 4.1 SRP 위반 → 클래스 분리

```
탐지: 클래스에 메서드 10개 초과
수정:
1. get_symbols_overview로 메서드 그룹화
2. 책임별 새 클래스 생성
3. 메서드 이동 패턴 적용
4. 원본 클래스에서 새 클래스 위임
```

### 4.2 DIP 위반 → 인터페이스 추출

```
탐지: 비즈니스 로직에 직접 인프라 의존
수정:
1. find_referencing_symbols로 의존 관계 파악
2. 인터페이스 추출 패턴 적용
3. 생성자 주입으로 변경
```

### 4.3 OCP 위반 → 전략 패턴

```
탐지: 타입 기반 switch/if 체인
수정:
1. search_for_pattern으로 switch 문 탐지
2. 각 case를 전략 클래스로 추출
3. 팩토리/레지스트리 패턴 적용
```

---

## 5. 검증 패턴

### 5.1 수정 전 체크리스트

- [ ] find_symbol로 대상 심볼 존재 확인
- [ ] find_referencing_symbols로 영향 범위 파악
- [ ] 테스트 파일 존재 확인

### 5.2 수정 후 검증

- [ ] 심볼 도구는 오류 없으면 신뢰 가능
- [ ] find_referencing_symbols로 참조 무결성 확인
- [ ] execute_shell_command로 테스트 실행

---

## 6. 메모리 활용

### 프로젝트 컨텍스트 저장

```
write_memory:
- 아키텍처 결정 기록
- 리팩토링 히스토리
- 코딩 컨벤션
```

### 세션 간 연속성

```
read_memory:
- 이전 리팩토링 진행 상황
- 알려진 기술 부채
- 우선순위 높은 수정 대상
```
