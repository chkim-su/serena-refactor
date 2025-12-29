---
description: Execute real user behavior simulation tests. UI interactions (clicks, inputs, drag-drop), API sequences, and scenario-based E2E testing using Playwright MCP.
skills:
  - user-simulation-test
allowed-tools:
  - Task
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - TodoWrite
  - mcp__plugin_playwright_playwright__browser_navigate
  - mcp__plugin_playwright_playwright__browser_snapshot
  - mcp__plugin_playwright_playwright__browser_click
  - mcp__plugin_playwright_playwright__browser_type
  - mcp__plugin_playwright_playwright__browser_fill_form
  - mcp__plugin_playwright_playwright__browser_wait_for
  - mcp__plugin_playwright_playwright__browser_take_screenshot
  - mcp__plugin_playwright_playwright__browser_console_messages
  - mcp__plugin_playwright_playwright__browser_network_requests
  - mcp__plugin_playwright_playwright__browser_drag
  - mcp__plugin_playwright_playwright__browser_hover
  - mcp__plugin_playwright_playwright__browser_select_option
  - mcp__plugin_playwright_playwright__browser_file_upload
  - mcp__plugin_playwright_playwright__browser_press_key
  - mcp__plugin_playwright_playwright__browser_close
---

# E2E Test Command

Execute real user behavior simulation tests using Playwright MCP tools.

## Load Skills

```
Skill("serena-refactor:user-simulation-test")
```

## Usage

```
/serena-refactor:e2e-test [options]
```

### Options

- `--type=ui|api|integration|scenario` - Test type (default: auto-detect)
- `--url=<url>` - Target URL (default: auto-detect from project)
- `--scenario=<name>` - Run specific scenario only
- `--env=local|staging|production` - Environment (default: local)
- `--screenshots` - Capture screenshots on failure
- `--verbose` - Detailed output
- `--dry-run` - Show test plan without execution

---

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    /e2e-test Workflow                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐                                             │
│  │   Start     │                                             │
│  └──────┬──────┘                                             │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────────────┐                                     │
│  │ Environment Check   │                                     │
│  │ - Playwright MCP?   │                                     │
│  │ - Dev server?       │                                     │
│  │ - Project type?     │                                     │
│  └──────┬──────────────┘                                     │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────────────────────────────────────────┐         │
│  │              Test Type Selection                 │         │
│  │     (UI / API / Integration / Scenario)         │         │
│  └──────────────────────┬──────────────────────────┘         │
│                         │                                    │
│                         ▼                                    │
│  ┌─────────────────────────────────────────────────┐         │
│  │           Scenario Generation/Load               │         │
│  │       (Auto-generate or load from file)         │         │
│  └──────────────────────┬──────────────────────────┘         │
│                         │                                    │
│                         ▼                                    │
│  ┌─────────────────────────────────────────────────┐         │
│  │                User Review                       │         │
│  │           (Approve test plan)                   │         │
│  └──────────────────────┬──────────────────────────┘         │
│                         │                                    │
│                         ▼                                    │
│  ┌─────────────────────────────────────────────────┐         │
│  │              e2e-test-runner agent              │         │
│  │             (Execute tests)                     │         │
│  └──────────────────────┬──────────────────────────┘         │
│                         │                                    │
│                         ▼                                    │
│  ┌─────────────────────────────────────────────────┐         │
│  │              Results & Report                    │         │
│  └──────────────────────┬──────────────────────────┘         │
│                         │                                    │
│                         ▼                                    │
│  ┌─────────────┐                                             │
│  │   Complete  │                                             │
│  └─────────────┘                                             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Step 1: Environment Check

### Check Playwright MCP Availability

Look for these tools in available MCP tools:
- `mcp__plugin_playwright_playwright__browser_navigate`
- `mcp__plugin_playwright_playwright__browser_snapshot`
- `mcp__plugin_playwright_playwright__browser_click`

If not available:

```markdown
## Playwright MCP 필요

E2E 테스트를 실행하려면 Playwright MCP 서버가 필요합니다.

### 설치 방법

1. `~/.claude/mcp_servers.json`에 추가:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-playwright"]
    }
  }
}
```

2. Claude Code 재시작
```

### Check Dev Server

```bash
# Try common development ports
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000
curl -s -o /dev/null -w "%{http_code}" http://localhost:5173  # Vite
curl -s -o /dev/null -w "%{http_code}" http://localhost:4200  # Angular
```

If no server running:

```yaml
AskUserQuestion:
  question: "개발 서버가 실행 중이지 않습니다. 어떻게 할까요?"
  header: "서버 상태"
  options:
    - label: "서버 시작 명령어 제공"
      description: "npm run dev, python manage.py runserver 등"
    - label: "외부 URL 사용"
      description: "staging 또는 production URL 입력"
    - label: "테스트 취소"
      description: "서버 시작 후 다시 시도"
```

---

## Step 2: Test Type Selection

If not specified in command:

```yaml
AskUserQuestion:
  question: "어떤 유형의 테스트를 실행하시겠습니까?"
  header: "테스트 유형"
  options:
    - label: "UI E2E 테스트 (Recommended)"
      description: "Playwright로 브라우저 상호작용 테스트"
    - label: "API 시퀀스 테스트"
      description: "HTTP 요청 시퀀스로 API 플로우 테스트"
    - label: "통합 테스트"
      description: "UI + API 조합 테스트"
    - label: "시나리오 기반"
      description: "미리 정의된 시나리오 파일 실행"
  multiSelect: false
```

---

## Step 3: Scenario Generation

### Auto-Generate Scenarios

1. **Discover Project Routes**
   ```
   Grep: "path=|Route|router\." in src/**/*.{js,jsx,ts,tsx,py}
   ```

2. **Identify Key User Flows**
   - Look for authentication (login, logout, register)
   - Look for CRUD operations
   - Look for forms and submissions

3. **Generate Test Plan**
   ```markdown
   ## 자동 생성된 테스트 계획

   ### 발견된 플로우

   | 플로우 | 페이지/엔드포인트 | 예상 단계 |
   |--------|-------------------|-----------|
   | 로그인 | /login | 3 |
   | 회원가입 | /register | 5 |
   | 대시보드 | /dashboard | 2 |

   ### 제안 시나리오

   1. **인증 플로우**
      - 로그인 → 대시보드 확인 → 로그아웃

   2. **주요 기능 플로우**
      - [프로젝트별 기능 기반 생성]
   ```

### Load Existing Scenarios

If scenario file exists (e.g., `e2e/scenarios.yaml`, `tests/e2e/*.spec.ts`):

```
Read: e2e/scenarios.yaml
# or
Read: tests/e2e/login.spec.ts
```

---

## Step 4: User Review

Present test plan:

```markdown
## 테스트 계획

### 환경
- **URL**: http://localhost:3000
- **Environment**: local
- **Test Type**: UI E2E

### 실행할 시나리오

| # | 시나리오 | 단계 수 | 예상 시간 |
|---|----------|---------|-----------|
| 1 | 로그인 플로우 | 4 | ~10s |
| 2 | 메인 기능 테스트 | 8 | ~30s |
| 3 | 에러 핸들링 | 3 | ~10s |

### 예상 리소스 사용
- 브라우저 세션: 1개
- 스크린샷: 실패 시만
- 예상 소요 시간: ~1분
```

```yaml
AskUserQuestion:
  question: "이 테스트 계획을 실행할까요?"
  header: "실행 승인"
  options:
    - label: "실행"
      description: "테스트 시작"
    - label: "시나리오 수정"
      description: "특정 시나리오만 선택하거나 수정"
    - label: "취소"
      description: "테스트 취소"
```

---

## Step 5: Execute Tests

```
Task:
  agent: e2e-test-runner
  prompt: |
    Execute E2E tests with the following configuration:

    ## Test Configuration
    - Type: ${test_type}
    - URL: ${target_url}
    - Environment: ${environment}
    - Options:
      - screenshots: ${screenshots}
      - verbose: ${verbose}
      - fail_fast: ${fail_fast}

    ## Scenarios
    ${scenarios_yaml}

    Execute all scenarios and report results.
```

---

## Step 6: Results & Report

### Success Report

```markdown
## E2E 테스트 완료!

### 결과 요약

| 항목 | 결과 |
|------|------|
| 총 시나리오 | 5 |
| 성공 | 5 |
| 실패 | 0 |
| 소요 시간 | 45.2초 |

### 시나리오별 결과

- [x] 로그인 플로우 (8.1s)
- [x] 회원가입 플로우 (12.3s)
- [x] 대시보드 네비게이션 (5.2s)
- [x] 프로필 수정 (10.1s)
- [x] 로그아웃 (2.5s)

### 다음 단계

모든 테스트가 통과했습니다! 이제:
- `git add . && git commit -m "feat: ..."` 로 커밋
- 또는 추가 기능 개발 진행
```

### Failure Report

```markdown
## E2E 테스트 완료 (일부 실패)

### 결과 요약

| 항목 | 결과 |
|------|------|
| 총 시나리오 | 5 |
| 성공 | 3 |
| 실패 | 2 |
| 소요 시간 | 62.5초 |

### 실패한 테스트

#### 회원가입 플로우
- **실패 단계**: 3/5 (이메일 입력)
- **에러**: `Element [data-testid='email-input'] not found`
- **스크린샷**: register_step3_fail.png

**가능한 원인**:
- data-testid가 변경됨
- 페이지 로딩 지연

**제안 수정**:
```typescript
// 기존 selector 확인
await page.getByTestId('email-input')
// 또는 대안 사용
await page.getByPlaceholder('이메일')
```

---

#### 결제 플로우
- **실패 단계**: 6/8 (결제 버튼 클릭)
- **에러**: `Button disabled due to validation error`
- **콘솔 에러**: `Invalid card number format`

**가능한 원인**:
- 테스트 카드 번호 형식 오류
- 유효성 검사 로직 변경

### 다음 단계

1. 실패한 테스트 원인 분석
2. 코드 또는 테스트 시나리오 수정
3. `/serena-refactor:e2e-test --scenario=register` 로 재실행
```

---

## Error Handling

### Playwright Not Available

```markdown
## Playwright MCP를 찾을 수 없습니다

E2E 테스트에는 Playwright MCP 서버가 필요합니다.

### 설정 방법

1. MCP 서버 설정 파일 열기:
   ```bash
   code ~/.claude/mcp_servers.json
   ```

2. Playwright 추가:
   ```json
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["@anthropic-ai/mcp-playwright"]
       }
     }
   }
   ```

3. Claude Code 재시작

### API 테스트 대안

브라우저 테스트 없이 API 테스트만 실행하려면:
```
/serena-refactor:e2e-test --type=api
```
```

### Server Not Running

```markdown
## 개발 서버가 실행 중이지 않습니다

테스트 대상 서버를 찾을 수 없습니다.

### 서버 시작 방법

프로젝트 유형에 따라:

```bash
# Node.js/React/Vue
npm run dev

# Python/FastAPI
uvicorn main:app --reload

# Django
python manage.py runserver

# Next.js
npm run dev
```

### 외부 URL 사용

이미 배포된 환경을 테스트하려면:
```
/serena-refactor:e2e-test --url=https://staging.example.com
```
```

### Browser Installation Required

```markdown
## 브라우저 설치 필요

Playwright 브라우저가 설치되지 않았습니다.

### 자동 설치 시도

```
mcp__plugin_playwright_playwright__browser_install
```

### 수동 설치

```bash
npx playwright install chromium
```
```

---

## Examples

### Example 1: Quick Smoke Test

```
/serena-refactor:e2e-test
```

Auto-detects project, generates basic scenarios, runs tests.

### Example 2: Specific URL

```
/serena-refactor:e2e-test --url=http://localhost:3000
```

### Example 3: API Only

```
/serena-refactor:e2e-test --type=api --url=http://localhost:8000
```

### Example 4: With Screenshots

```
/serena-refactor:e2e-test --screenshots --verbose
```

### Example 5: Staging Environment

```
/serena-refactor:e2e-test --env=staging --url=https://staging.example.com
```

### Example 6: Dry Run

```
/serena-refactor:e2e-test --dry-run
```

Shows what would be tested without actually running.
