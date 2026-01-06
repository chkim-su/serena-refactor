---
description: Systematic debugging workflow with parallel agent exploration, root cause analysis, fix strategy design, and verification. Adapted from feature-dev methodology.
skills:
  - debugging-workflow
  - solid-design-rules
  - serena-refactoring-patterns
allowed-tools:
  - Task
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - TodoWrite
---

# Debug Command

Systematic 6-phase debugging workflow with parallel agent exploration.

## Load Skills

```
Skill("serena-refactor:debugging-workflow")
```

## Usage

```
/serena-refactor:debug [bug description or error message]
```

---

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    /debug Workflow                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Phase 1: DISCOVERY                                          │
│  ┌─────────────────────────────────────────────────┐         │
│  │ Gather bug symptoms, reproduction steps,        │         │
│  │ error messages, and context                     │         │
│  └──────────────────────┬──────────────────────────┘         │
│                         │                                    │
│  Phase 2: EXPLORATION (Parallel Agents)                      │
│  ┌─────────────────────────────────────────────────┐         │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐       │         │
│  │  │ Explorer │  │ Explorer │  │ Explorer │       │         │
│  │  │ (Path)   │  │ (Data)   │  │ (Deps)   │       │         │
│  │  └──────────┘  └──────────┘  └──────────┘       │         │
│  └──────────────────────┬──────────────────────────┘         │
│                         │                                    │
│  Phase 3: ROOT CAUSE ANALYSIS                                │
│  ┌─────────────────────────────────────────────────┐         │
│  │ Synthesize exploration findings,                │         │
│  │ identify true root cause                        │         │
│  └──────────────────────┬──────────────────────────┘         │
│                         │                                    │
│  Phase 4: FIX STRATEGY (Parallel Agents)                     │
│  ┌─────────────────────────────────────────────────┐         │
│  │  ┌───────────┐  ┌─────────────┐  ┌───────────┐  │         │
│  │  │ Minimal   │  │Comprehensive│  │ Defensive │  │         │
│  │  │ Strategy  │  │  Strategy   │  │ Strategy  │  │         │
│  │  └───────────┘  └─────────────┘  └───────────┘  │         │
│  └──────────────────────┬──────────────────────────┘         │
│                         │                                    │
│                    USER APPROVAL                             │
│                         │                                    │
│  Phase 5: IMPLEMENTATION                                     │
│  ┌─────────────────────────────────────────────────┐         │
│  │ Apply chosen fix strategy                       │         │
│  └──────────────────────┬──────────────────────────┘         │
│                         │                                    │
│  Phase 6: VERIFICATION (Parallel Agents)                     │
│  ┌─────────────────────────────────────────────────┐         │
│  │  ┌──────────┐  ┌───────────┐  ┌───────────┐     │         │
│  │  │ Direct   │  │Regression │  │ Edge Case │     │         │
│  │  │ Verify   │  │  Check    │  │  Check    │     │         │
│  │  └──────────┘  └───────────┘  └───────────┘     │         │
│  └──────────────────────┬──────────────────────────┘         │
│                         │                                    │
│                    COMPLETE                                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Bug Discovery

### Goal

Gather complete information about the bug before investigation.

### Questions to Answer

```yaml
AskUserQuestion:
  questions:
    - question: "버그의 증상을 자세히 설명해주세요"
      header: "증상"
      options:
        - label: "에러 발생"
          description: "에러 메시지, 예외, 크래시"
        - label: "잘못된 동작"
          description: "기능이 예상과 다르게 동작"
        - label: "성능 문제"
          description: "느림, 메모리 증가, 응답 없음"
        - label: "데이터 문제"
          description: "잘못된 데이터, 손실, 불일치"

    - question: "버그를 재현할 수 있나요?"
      header: "재현"
      options:
        - label: "항상 재현"
          description: "동일 조건에서 100% 재현"
        - label: "가끔 재현"
          description: "특정 조건에서만 재현"
        - label: "드물게 재현"
          description: "재현이 어려움"
        - label: "재현 불가"
          description: "한 번 발생 후 재현 안됨"
```

### Collect Information

```markdown
## Bug Report

### Symptom
[What is happening]

### Expected Behavior
[What should happen]

### Reproduction Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Error Output
```
[Error message, stack trace, logs]
```

### Context
- Environment: [dev/staging/prod]
- Version: [app version]
- First occurred: [date/time]
- Frequency: [always/sometimes/rare]

### Recent Changes
[Any relevant recent changes]
```

---

## Phase 2: Codebase Exploration

### Goal

Trace execution paths and understand affected code areas.

### Launch Parallel Agents

Launch 2-3 **debug-explorer** agents with different focuses:

```yaml
Agent 1 - Execution Path:
  Task:
    agent: "debug-explorer"
    prompt: |
      Focus: execution_path
      Bug: [description]
      Error location: [file:line if known]

      Trace the complete execution path from entry point to error.
      Identify all functions called, conditions evaluated, and branches taken.

Agent 2 - Data Flow:
  Task:
    agent: "debug-explorer"
    prompt: |
      Focus: data_flow
      Bug: [description]
      Error location: [file:line if known]

      Track data from its source to the error point.
      Identify all transformations, mutations, and handoffs.

Agent 3 - Dependencies:
  Task:
    agent: "debug-explorer"
    prompt: |
      Focus: dependencies
      Bug: [description]
      Error location: [file:line if known]

      Map all related components, shared state, and integrations.
      Identify potential interaction issues.
```

### Serena MCP Integration

Use Serena MCP tools for symbol-level investigation:

```
# Find the symbol at error location
mcp__serena-daemon__find_symbol:
  name_path_pattern: "[function_name]"
  relative_path: "[file_path]"
  include_body: true

# Find all callers
mcp__serena-daemon__find_referencing_symbols:
  name_path: "[symbol_name]"
  relative_path: "[file_path]"

# Search for error patterns
mcp__serena-daemon__search_for_pattern:
  substring_pattern: "[error_text]"
```

---

## Phase 3: Root Cause Analysis

### Goal

Synthesize exploration findings to identify true root cause.

### Analysis Template

```markdown
## Root Cause Analysis

### Exploration Summary
[Key findings from Phase 2 agents]

### Immediate Cause
[What directly triggers the error]

### Underlying Cause
[Why this condition exists]

### Contributing Factors
- [Factor 1]
- [Factor 2]

### Root Cause Statement
**The bug occurs because [root cause] which leads to [immediate cause] resulting in [symptom].**

### Confidence: [X]%
[Justification for confidence level]
```

### User Confirmation

```yaml
AskUserQuestion:
  question: "분석된 근본 원인이 맞는 것 같나요?"
  header: "확인"
  options:
    - label: "맞음, 계속 진행"
      description: "근본 원인 분석에 동의"
    - label: "부분적으로 맞음"
      description: "추가 조사 필요"
    - label: "틀림, 재조사 필요"
      description: "다른 방향으로 조사"
```

---

## Phase 4: Fix Strategy Design

### Goal

Design multiple fix approaches with risk assessment.

### Launch Parallel Agents

Launch 2-3 **debug-strategist** agents with different approaches:

```yaml
Agent 1 - Minimal:
  Task:
    agent: "debug-strategist"
    prompt: |
      Approach: minimal
      Root Cause: [from Phase 3]
      Findings: [from Phase 2]

      Design the smallest possible fix that addresses the immediate problem.
      Minimize risk and touched files.

Agent 2 - Comprehensive:
  Task:
    agent: "debug-strategist"
    prompt: |
      Approach: comprehensive
      Root Cause: [from Phase 3]
      Findings: [from Phase 2]

      Design a thorough fix that addresses the root cause and prevents recurrence.
      Include related improvements if appropriate.

Agent 3 - Defensive:
  Task:
    agent: "debug-strategist"
    prompt: |
      Approach: defensive
      Root Cause: [from Phase 3]
      Findings: [from Phase 2]

      Design defensive measures: input validation, error boundaries, fallbacks.
      Focus on graceful failure and robust error handling.
```

### Present Options

```markdown
## Fix Strategy Options

### Option 1: Minimal Fix
- **Changes:** [count] files, [count] lines
- **Risk:** Low
- **Pros:** Quick, safe, minimal impact
- **Cons:** May not prevent recurrence

### Option 2: Comprehensive Fix
- **Changes:** [count] files, [count] lines
- **Risk:** Medium
- **Pros:** Addresses root cause, improves quality
- **Cons:** More testing needed

### Option 3: Defensive Fix
- **Changes:** [count] files, [count] lines
- **Risk:** Low-Medium
- **Pros:** Handles unknown edge cases
- **Cons:** May hide underlying issues
```

### User Selection

```yaml
AskUserQuestion:
  question: "어떤 수정 전략을 선택하시겠습니까?"
  header: "전략 선택"
  options:
    - label: "Minimal Fix (Recommended for hotfix)"
      description: "가장 작은 변경으로 증상 해결"
    - label: "Comprehensive Fix"
      description: "근본 원인 해결, 재발 방지"
    - label: "Defensive Fix"
      description: "방어 로직 추가, 안전한 실패"
    - label: "Combine approaches"
      description: "여러 전략 조합"
```

---

## Phase 5: Implementation

### Pre-Implementation Gate

**Explicit user approval required before making changes.**

```yaml
AskUserQuestion:
  question: "선택한 전략으로 수정을 진행할까요?"
  header: "구현 승인"
  options:
    - label: "승인 - 수정 진행"
      description: "선택한 전략대로 코드 수정"
    - label: "Dry run 먼저"
      description: "변경 내용 미리보기만"
    - label: "전략 재검토"
      description: "Phase 4로 돌아가기"
    - label: "취소"
      description: "디버깅 세션 종료"
```

### Implementation

Apply the chosen fix:

1. Make code changes as specified
2. Add defensive checks if applicable
3. Update comments/documentation
4. Stage changes for review

```markdown
## Implementation Log

### Changes Made
| File | Lines | Description |
|------|-------|-------------|
| `file1.ts` | 45-50 | [change description] |

### Code Diff
[Show git diff or before/after]
```

---

## Phase 6: Verification

### Goal

Confirm the fix works and doesn't introduce new issues.

### Launch Parallel Agents

Launch 2-3 **debug-verifier** agents with different focuses:

```yaml
Agent 1 - Direct:
  Task:
    agent: "debug-verifier"
    prompt: |
      Focus: direct
      Original bug: [description]
      Fix applied: [description]
      Changed files: [list]

      Verify the original bug no longer occurs.
      Test the exact reproduction steps.

Agent 2 - Regression:
  Task:
    agent: "debug-verifier"
    prompt: |
      Focus: regression
      Original bug: [description]
      Fix applied: [description]
      Changed files: [list]

      Check for any new issues introduced by the fix.
      Review code for unintended side effects.

Agent 3 - Edge Cases:
  Task:
    agent: "debug-verifier"
    prompt: |
      Focus: edge_cases
      Original bug: [description]
      Fix applied: [description]
      Changed files: [list]

      Test boundary conditions and edge cases.
      Verify robust handling of unusual inputs.
```

### Verification Summary

```markdown
## Verification Results

### Direct Verification
- Original bug: [Fixed/Not Fixed]
- Confidence: [X]%

### Regression Check
- New issues found: [None/List]
- Confidence: [X]%

### Edge Case Check
- Edge cases handled: [Yes/Partial/No]
- Confidence: [X]%

### Final Verdict: [PASS/FAIL/CONDITIONAL]
```

### Post-Verification Decision

```yaml
AskUserQuestion:
  question: "검증 결과를 검토한 후 어떻게 할까요?"
  header: "다음 단계"
  options:
    - label: "커밋 및 완료"
      description: "수정 사항 커밋"
    - label: "추가 수정 필요"
      description: "발견된 이슈 수정"
    - label: "롤백"
      description: "변경 사항 되돌리기"
```

---

## Workflow State Management

State files track progress:

| File | Phase | Purpose |
|------|-------|---------|
| `.debug-discovery-done` | 1 | Bug info collected |
| `.debug-exploration-done` | 2 | Exploration complete |
| `.debug-rootcause-done` | 3 | Root cause identified |
| `.debug-strategy-approved` | 4 | Strategy selected |
| `.debug-fix-applied` | 5 | Fix implemented |
| `.debug-verified` | 6 | Verification passed |

---

## Examples

### Example 1: Simple Error

```
/serena-refactor:debug "TypeError: Cannot read property 'name' of undefined in UserService"
```

### Example 2: Performance Issue

```
/serena-refactor:debug "API response takes 10+ seconds for large datasets"
```

### Example 3: Intermittent Bug

```
/serena-refactor:debug "Login sometimes fails with 'session expired' even for new sessions"
```

---

## Error Handling

### Exploration Timeout

If exploration takes too long:
- Summarize partial findings
- Ask user to narrow scope
- Continue with available information

### No Root Cause Found

If root cause unclear:
- Present best hypotheses
- Suggest additional investigation
- Offer defensive fix option

### Fix Fails Verification

If fix doesn't work:
- Document what was tried
- Return to Phase 4
- Consider alternative approach
