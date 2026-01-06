# Serena Refactor Plugin

Serena MCP 기반 심볼릭 리팩토링 플러그인입니다.

## 특징

- **데이터 드리븐 아키텍처**: 에이전트는 MCP 도구를 호출하지 않고 미리 수집된 데이터만 분석
- **심볼 수준 분석**: Serena daemon의 AST 기반 정확한 코드 구조 분석
- **안전한 리팩토링**: 참조 무결성 보장, 모든 변경사항 자동 추적
- **SOLID 원칙 적용**: 설계 원칙 위반 자동 탐지 및 수정 제안
- **Hook 기반 워크플로우**: 품질 게이트로 안전한 단계별 진행 보장
- **지능형 기능 주입**: 프로젝트 지식 그래프 기반 컨벤션 준수 코드 생성

## 버전

**v2.4.0** - 데이터 드리븐 아키텍처, 직접 MCP 통합

## 아키텍처

### 데이터 드리븐 에이전트 패턴

```
Main Session
  ├─ MCP 도구로 코드 데이터 수집 (find_symbol, get_symbols_overview 등)
  └─ 수집된 데이터를 에이전트에게 전달
       ↓
  Specialized Agents (도구 없음, 분석 전담)
    ├─ serena-solid-analyzer: SOLID 위반 분석
    ├─ refactor-planner: 리팩토링 계획 수립
    ├─ duplicate-detector: 중복 코드 탐지
    └─ feature-planner: 기능 구현 계획
```

**장점**:
- 에이전트 컨텍스트가 깨끗함 (도구 스키마 없음)
- 분석 로직에만 집중 (재현 가능, 테스트 용이)
- 동일 입력 → 동일 결과 보장

### Serena MCP 통합

Serena daemon과 직접 통합:
- ✅ 멀티 프로젝트 동시 관리 (`activate_project`)
- ✅ AST 캐시로 빠른 응답
- ✅ SSE 프로토콜로 장기 실행 (포트 8765)
- ✅ 프로젝트별 메모리 상태 유지

## 명령어

| 명령어 | 설명 | 워크플로우 단계 |
|--------|------|----------------|
| `/serena-refactor:analyze` | SOLID 분석 실행 | 1단계: 분석 |
| `/serena-refactor:plan` | 리팩토링 계획 수립 | 2단계: 계획 |
| `/serena-refactor:refactor` | 전체 리팩토링 워크플로우 | 3단계: 실행 |
| `/serena-refactor:audit` | 코드 품질 감사 | 4단계: 검증 |
| `/serena-refactor:rename` | 안전한 심볼 이름 변경 | 단독 작업 |
| `/serena-refactor:extract` | 메서드/클래스 추출 | 단독 작업 |
| `/serena-refactor:detect-duplicates` | 중복 코드 탐지 | 분석 단계 |
| `/serena-refactor:inject` | 지능형 기능 주입 | 기능 추가 워크플로우 |

## 워크플로우

### 리팩토링 워크플로우

```
/serena-refactor:analyze    → .refactor-analysis-done
         ↓
/serena-refactor:plan       → .refactor-plan-approved
         ↓ (Hook: 선행 조건 검증)
/serena-refactor:refactor   → .refactor-execution-done
         ↓ (필수)
/serena-refactor:audit      → .refactor-audit-passed (PASS 시)
         ↓
     git commit
```

### 기능 주입 워크플로우

```
knowledge-extractor         → .inject-knowledge-extracted
         ↓
feature-planner             → .inject-plan-approved
         ↓ (Hook: 계획 승인 확인)
code-injector               → .inject-execution-done
         ↓
  검증 및 git commit
```

## Hook 시스템

### Quality Gates

**차단형 Hook** (선행 조건 미충족 시 실행 거부):
- `serena-refactor-executor`: 분석 + 계획 완료 확인
- `code-injector`: 기능 계획 승인 확인

**경고형 Hook** (정보 제공):
- `refactor-planner`: 분석 완료 권장
- `feature-planner`: 지식 추출 완료 권장

### 상태 파일

| 파일 | 생성 시점 | 의미 |
|------|----------|------|
| `.refactor-analysis-done` | analyze/detect-duplicates 완료 | 분석 완료 |
| `.refactor-plan-approved` | plan 완료 | 계획 승인 (자동) |
| `.refactor-execution-done` | refactor 완료 | 실행 완료 |
| `.refactor-audit-passed` | audit PASS | 품질 검증 통과 |
| `.inject-knowledge-extracted` | knowledge-extractor 완료 | 지식 추출 완료 |
| `.inject-plan-approved` | feature-planner 완료 | 기능 계획 승인 |
| `.inject-execution-done` | code-injector 완료 | 코드 주입 완료 |

## 에이전트

### 분석 에이전트
- `serena-solid-analyzer`: SOLID 원칙 위반 분석 (데이터 전용)
- `duplicate-detector`: 코드 클론 탐지 (데이터 전용)

### 계획 에이전트
- `refactor-planner`: 리팩토링 계획 수립 (데이터 전용)
- `feature-planner`: 기능 구현 계획 (데이터 전용)

### 실행 에이전트
- `serena-refactor-executor`: 리팩토링 실행 (계획 기반)
- `code-injector`: 코드 주입 (계획 기반)

### 검증 에이전트
- `refactor-auditor`: 품질 검증 (실행 결과 분석)
- `knowledge-extractor`: 프로젝트 지식 그래프 생성

### 디버깅 에이전트 (v2.6.0+)
- `debug-explorer`: 버그 탐색 및 실행 경로 추적
- `debug-strategist`: 수정 전략 설계 (최소/포괄/방어적)
- `debug-verifier`: 수정 결과 검증 (직접/회귀/엣지케이스)

### E2E 테스트 에이전트 (v2.6.0+)
- `e2e-test-runner`: Playwright 기반 사용자 시뮬레이션 테스트

### 실험실 에이전트 (v2.7.0+)
- **lab-analyst**: 문제 분해 및 가설 설계
- **lab-experimenter**: 병렬 PoC 실험 조율
- **lab-verifier**: 실험 결과 검증 및 보고
- **source-fetcher**: 외부 솔루션 수집 (GitHub, Stack Overflow)
- **creative-generator**: 창의적/비정통 접근법 생성
- **llm-consultant**: 멀티 모델 접근법 수집 (Gemini, Codex)
- **edge-case-hunter**: 엣지 케이스 체계적 발견

## 스킬

| 스킬 | 용도 |
|------|------|
| `solid-design-rules` | SOLID 원칙 및 TDD 규칙 |
| `serena-refactoring-patterns` | Serena 도구 기반 리팩토링 패턴 |
| `duplicate-detection-rules` | 코드 클론 탐지 및 수정 패턴 |
| `project-knowledge-graph` | 프로젝트별 누적 지식 |
| `feature-injection-rules` | 코드 주입 템플릿 및 가이드 |

## Serena MCP 도구

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

### 프로젝트 관리
- `activate_project`: 프로젝트 전환
- `list_memories`: 메모리 목록
- `read_memory` / `write_memory`: 프로젝트 지식 저장

## 설치

### 자동 설치 (권장)

플러그인 설치 시 SessionStart hook이 Serena MCP 자동 설정:
```bash
# 플러그인 설치
claude plugin add local refactor

# Claude Code 재시작 → Serena MCP 자동 등록
```

### 수동 설치

```bash
# Serena MCP 등록
claude mcp add --transport stdio --scope user serena -- \
  uvx --from git+https://github.com/oraios/serena serena start-mcp-server

# 플러그인 설치
cd ~/.claude/plugins/local/
git clone <this-repo> serena-refactor
```

## 요구사항

- **Serena MCP 서버**: 자동 설정 또는 수동 등록
- **uv/uvx**: Serena 실행 필요 (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **지원 언어**: Python, TypeScript, Java, Go 등 (Serena 지원 언어)

## 사용 예시

### SOLID 분석 및 리팩토링

```bash
# 1. 분석
/serena-refactor:analyze src/

# 2. 계획
/serena-refactor:plan

# 3. 실행
/serena-refactor:refactor

# 4. 검증
/serena-refactor:audit
```

### 심볼 이름 변경

```bash
/serena-refactor:rename src/service.ts UserService/getUser fetchUserById
```

### 지능형 기능 추가

```bash
/serena-refactor:inject 사용자 알림을 처리하는 NotificationService 추가
```

## 변경 이력

### v2.4.0 (2025-12-29)
- ✅ 레거시 Gateway 코드 제거 (`serena_gateway.py`)
- ✅ 데이터 드리븐 아키텍처로 완전 전환
- ✅ 문서 업데이트 (README, marketplace.json)
- ✅ 직접 MCP 통합 최적화

### v2.3.0 (2025-12-28)
- Gateway Agent 제거, 직접 MCP 호출로 전환
- 에이전트 아키텍처 리팩토링 (데이터 드리븐 패턴)
- Hook 시스템 강화

### v2.2.x (2025-12-26)
- SDK 기반 Gateway 구현 (컨텍스트 격리)
- MCP isolation 실험

## 라이선스

MIT

## 기여

Issues 및 Pull Requests 환영합니다!

## 저자

chanhokim
