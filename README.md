# Serena Refactor Plugin

Serena MCP 기반 심볼릭 리팩토링 플러그인입니다.

## 특징

- **심볼 수준 분석**: AST 기반 정확한 코드 구조 분석
- **안전한 리팩토링**: Serena 심볼 도구로 참조 무결성 보장
- **SOLID 원칙 적용**: 설계 원칙 위반 탐지 및 자동 수정
- **단계별 워크플로우**: 분석 → 계획 → 실행 → 검증

## 명령어

| 명령어 | 설명 |
|--------|------|
| `/serena-refactor:analyze` | SOLID 분석 실행 |
| `/serena-refactor:plan` | 리팩토링 계획 수립 |
| `/serena-refactor:refactor` | 전체 리팩토링 워크플로우 |
| `/serena-refactor:rename` | 안전한 심볼 이름 변경 |
| `/serena-refactor:extract` | 메서드/인터페이스/클래스 추출 |
| `/serena-refactor:audit` | 코드 품질 감사 |

## 에이전트

| 에이전트 | 역할 |
|----------|------|
| `serena-solid-analyzer` | SOLID 원칙 위반 분석 |
| `refactor-planner` | 리팩토링 계획 수립 |
| `serena-refactor-executor` | 리팩토링 실행 |
| `refactor-auditor` | 품질 검증 |

## Serena MCP 통합

이 플러그인은 Serena MCP의 심볼릭 도구들을 핵심으로 활용합니다:

### 분석 도구
- `find_symbol`: 심볼 검색 및 본문 읽기
- `find_referencing_symbols`: 참조 추적
- `get_symbols_overview`: 파일 구조 분석
- `search_for_pattern`: 패턴 검색

### 편집 도구
- `replace_symbol_body`: 심볼 본문 교체
- `rename_symbol`: 안전한 이름 변경 (모든 참조 자동 업데이트)
- `insert_before/after_symbol`: 심볼 삽입
- `replace_content`: 정규식 기반 콘텐츠 교체

## 설치

```bash
# 플러그인 디렉토리로 복사
cp -r . ~/.claude/plugins/local/serena-refactor/
```

## 요구사항

- Serena MCP 서버가 설정되어 있어야 합니다
- 프로젝트가 Serena에서 지원하는 언어여야 합니다 (Python, TypeScript, Java 등)

## 사용 예시

### SOLID 분석
```
/serena-refactor:analyze src/
```

### 심볼 이름 변경
```
/serena-refactor:rename UserService/getUser fetchUserById
```

### 전체 리팩토링
```
/serena-refactor:refactor src/services/
```

## 워크플로우

```
1. /serena-refactor:analyze    → SOLID 위반 탐지
2. /serena-refactor:plan       → 단계별 계획 수립
3. /serena-refactor:refactor   → 계획 실행
4. /serena-refactor:audit      → 품질 검증
```

## 스킬

- `solid-design-rules`: SOLID 원칙 및 TDD 규칙
- `serena-refactoring-patterns`: Serena 도구 기반 리팩토링 패턴
