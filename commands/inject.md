---
description: Intelligent feature injection with project knowledge. Extracts project structure, plans implementation following conventions, and safely injects new code.
allowed-tools:
  - Task
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# Inject Command

Intelligent feature injection based on project knowledge extraction.

## Load Skills

```
Skill("serena-refactor:project-knowledge-graph")
Skill("serena-refactor:feature-injection-rules")
```

## Usage

```
/serena-refactor:inject [feature description]
```

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    /inject Workflow                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐                                             │
│  │   Start     │                                             │
│  └──────┬──────┘                                             │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────────────┐    ┌─────────────────────┐          │
│  │ Check for existing  │───▶│ knowledge-extractor │          │
│  │ knowledge graph     │ No │      agent          │          │
│  └──────┬──────────────┘    └──────────┬──────────┘          │
│         │ Yes                          │                     │
│         ▼                              ▼                     │
│  ┌─────────────────────────────────────────────────┐         │
│  │           Project Knowledge Available            │         │
│  └──────────────────────┬──────────────────────────┘         │
│                         │                                    │
│                         ▼                                    │
│  ┌─────────────────────────────────────────────────┐         │
│  │              feature-planner agent              │         │
│  │         (Design implementation plan)            │         │
│  └──────────────────────┬──────────────────────────┘         │
│                         │                                    │
│                         ▼                                    │
│  ┌─────────────────────────────────────────────────┐         │
│  │                 User Review                      │         │
│  │            (Approve/Modify Plan)                │         │
│  └──────────────────────┬──────────────────────────┘         │
│                         │                                    │
│                         ▼                                    │
│  ┌─────────────────────────────────────────────────┐         │
│  │              code-injector agent                │         │
│  │            (Execute injection)                  │         │
│  └──────────────────────┬──────────────────────────┘         │
│                         │                                    │
│                         ▼                                    │
│  ┌─────────────────────────────────────────────────┐         │
│  │              Update Knowledge Graph              │         │
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

## Step 1: Check/Extract Project Knowledge

### Check for Existing Knowledge

```
Task: serena-gateway
Prompt: "Use read_memory 'project-knowledge-graph.md'"
```

### If No Knowledge Exists

```yaml
AskUserQuestion:
  question: "프로젝트 지식 그래프가 없습니다. 추출할까요?"
  header: "지식 추출"
  options:
    - label: "전체 추출 (Recommended)"
      description: "프로젝트 전체를 분석하여 지식 그래프 생성"
    - label: "특정 디렉토리만"
      description: "분석할 디렉토리 지정"
    - label: "건너뛰기"
      description: "지식 그래프 없이 진행 (비권장)"
```

### Run Knowledge Extraction

```
Task:
  agent: knowledge-extractor
  prompt: |
    Extract project knowledge for feature injection.

    Project path: [current directory]
    Scope: [full/specific path based on user choice]

    Return comprehensive knowledge graph including:
    - Project structure
    - Key symbols and their relationships
    - Detected patterns
    - Coding conventions
```

---

## Step 2: Get Feature Description

If not provided in command:

```yaml
AskUserQuestion:
  question: "어떤 기능을 추가하시겠습니까?"
  header: "기능 설명"
  options:
    - label: "새 서비스/클래스"
      description: "새로운 비즈니스 로직 컴포넌트"
    - label: "기존 클래스 확장"
      description: "기존 클래스에 메서드/기능 추가"
    - label: "새 엔드포인트/핸들러"
      description: "새로운 API 엔드포인트 또는 이벤트 핸들러"
    - label: "유틸리티/헬퍼"
      description: "재사용 가능한 유틸리티 함수"
```

Then ask for details:

```yaml
AskUserQuestion:
  question: "기능에 대해 자세히 설명해주세요 (목적, 입출력, 동작 등)"
  header: "상세 설명"
```

---

## Step 3: Plan Feature Implementation

```
Task:
  agent: feature-planner
  prompt: |
    Plan feature implementation based on project knowledge.

    ## Project Knowledge
    [knowledge_graph from step 1]

    ## Feature Request
    [user's feature description from step 2]

    ## Requirements
    1. Follow existing project conventions
    2. Maintain SOLID principles
    3. Plan safe injection points
    4. Include all necessary imports
    5. Consider impact on existing code

    Return detailed implementation plan with:
    - Step-by-step instructions
    - Exact code to inject
    - File locations and anchors
    - Import requirements
    - Rollback plan
```

---

## Step 4: User Review and Approval

Present the plan to user:

```markdown
## 구현 계획

### 요약
[Brief summary of what will be created/modified]

### 단계별 계획

| 단계 | 작업 | 대상 | 설명 |
|------|------|------|------|
| 1 | [create/insert/modify] | [file:symbol] | [description] |
| 2 | ... | ... | ... |

### 코드 미리보기

[Code preview for each step]

### 영향 분석

- 영향받는 파일: [count]
- 생성할 심볼: [count]
- 수정할 심볼: [count]
- Breaking changes: [yes/no]
```

```yaml
AskUserQuestion:
  question: "이 계획대로 진행할까요?"
  header: "승인"
  options:
    - label: "승인 및 실행"
      description: "계획대로 코드 삽입 진행"
    - label: "Dry Run 먼저"
      description: "실제 변경 없이 시뮬레이션"
    - label: "계획 수정 필요"
      description: "요구사항 변경 또는 추가 설명"
    - label: "취소"
      description: "작업 취소"
```

---

## Step 5: Execute Injection

### If Dry Run Selected

```
Task:
  agent: code-injector
  prompt: |
    Perform dry run of injection plan.

    ## Plan
    [implementation plan from step 3]

    ## Mode
    dry_run: true

    Validate all steps without making changes.
    Report any potential issues.
```

### If Approved

```
Task:
  agent: code-injector
  prompt: |
    Execute injection plan.

    ## Plan
    [implementation plan from step 3]

    ## Mode
    dry_run: false

    Execute all steps in order.
    Verify each step before proceeding.
    Report results and any issues.
```

---

## Step 6: Post-Injection Actions

### Verify Results

1. **Syntax Check**
   Run appropriate linter/compiler for the language

2. **Symbol Verification**
   Confirm all new symbols are accessible

3. **Reference Check**
   Ensure no broken references

### Update Knowledge Graph

```
Task: serena-gateway
Prompt: |
  Update project knowledge graph with new additions:
  - New symbols: [list]
  - New dependencies: [list]
  - Updated patterns: [list]

  Read existing 'project-knowledge-graph.md', merge updates, and write back.
```

### Suggest Next Steps

```markdown
## 완료!

### 추가된 항목
- [list of created/modified items]

### 다음 단계 제안

1. **테스트 작성**
   ```bash
   # 새 기능에 대한 테스트 추가
   [test command suggestion]
   ```

2. **변경사항 검토**
   ```bash
   git diff
   ```

3. **커밋** (만족스러운 경우)
   ```bash
   git add . && git commit -m "feat: [feature description]"
   ```

4. **추가 기능**
   `/serena-refactor:inject` 로 더 많은 기능 추가
```

---

## Error Handling

### Knowledge Extraction Failed

```markdown
지식 추출 중 오류가 발생했습니다.

**가능한 원인:**
- Serena 프로젝트가 활성화되지 않음
- 지원되지 않는 언어/프레임워크
- 파일 접근 권한 문제

**해결 방법:**
1. `/serena-refactor:analyze` 로 프로젝트 상태 확인
2. Serena 설정 확인
```

### Planning Failed

```markdown
구현 계획 생성 중 오류가 발생했습니다.

**가능한 원인:**
- 기능 설명이 모호함
- 일치하는 패턴을 찾을 수 없음
- 프로젝트 구조와 맞지 않는 요청

**해결 방법:**
1. 더 구체적인 기능 설명 제공
2. 예시 코드나 참조할 기존 코드 지정
```

### Injection Failed

```markdown
코드 삽입 중 오류가 발생했습니다.

**오류 상세:**
[error details]

**롤백 상태:**
[rollback status]

**복구 방법:**
1. `git status` 로 변경된 파일 확인
2. `git checkout [file]` 로 원복
3. 계획 수정 후 재시도
```

---

## Examples

### Example 1: Add New Service

```
/serena-refactor:inject 사용자 알림을 처리하는 NotificationService 추가
```

Expected flow:
1. Extract knowledge (if needed)
2. Analyze existing service patterns
3. Plan NotificationService following conventions
4. Insert in appropriate location
5. Update exports and registrations

### Example 2: Extend Existing Class

```
/serena-refactor:inject UserRepository에 findByEmail 메서드 추가
```

Expected flow:
1. Load existing knowledge
2. Find UserRepository symbol
3. Analyze existing methods for style
4. Plan new method following patterns
5. Insert after existing methods

### Example 3: Add New Endpoint

```
/serena-refactor:inject POST /api/orders 엔드포인트 추가, 주문 생성 처리
```

Expected flow:
1. Load knowledge
2. Identify controller/handler patterns
3. Plan new handler with validation, service call, response
4. Insert following existing endpoint patterns
5. Update route registrations
