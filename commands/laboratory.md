---
description: Scientific experimentation workflow for exploring implementation approaches through hypothesis-driven parallel experiments, creative problem-solving, and rigorous verification.
skills:
  - laboratory-patterns
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
  - WebSearch
  - WebFetch
  - AskUserQuestion
  - TodoWrite
  - mcp__plugin_context7_context7__resolve-library-id
  - mcp__plugin_context7_context7__query-docs
---

# Laboratory Command

Scientific experimentation workflow for exploring implementation approaches.

## Load Skills

```
Skill("serena-refactor:laboratory-patterns")
```

## Usage

```
/serena-refactor:laboratory [problem description]
```

---

## Philosophy

> **"Apply scientific methodology to code implementation"**
> - Problem decomposition -> Hypothesis formation -> Parallel experimentation -> Rigorous verification
> - Record and learn from failures
> - Balance between existing solutions and creative approaches

---

## Trigger Scenarios

| Mode | Situation | Example |
|------|-----------|---------|
| **Exploration** | Don't know how to implement | "How do I implement OAuth?" |
| **Breakthrough** | Standard approach doesn't work | "Need to bypass API limitations" |
| **Optimization** | Looking for better methods | "Any performance improvements?" |

---

## 7-Stage Workflow

```
+---------------------------------------------------------------------+
|  1. Problem Decomposition --[User Approval]--> 2. Existing Approaches |
|        |                                              |               |
|        |                                   [LLM Consult Available]    |
|        v                                              v               |
|  3. Creative Approaches ---------------> 4. Hypothesis Formation --[Approval]|
|                                               |                       |
|        +--------------------------------------+                       |
|        v                                                              |
|  5. PoC Experiments --[Approval]--> Parallel Execution (max 5)        |
|        |                                                              |
|   +----+----+--------+--------+--------+                              |
|   v         v        v        v        v                              |
| Hyp.A    Hyp.B    Hyp.C    Hyp.D    Hyp.E                             |
|   |         |        |        |        |                              |
|   +----+----+--------+--------+--------+                              |
|        v                                                              |
|  6. Verification --[LLM Consult on Failure]--> 7. Result Report       |
+---------------------------------------------------------------------+
```

---

## Phase 1: Problem Decomposition

### Goal

Break down the problem into smaller, testable units.

### Steps

1. Understand the full problem context
2. Identify core requirements and constraints
3. Decompose into sub-problems
4. Define success criteria for each

### User Approval Required

```yaml
AskUserQuestion:
  questions:
    - question: "문제를 이렇게 분해했습니다. 맞나요?"
      header: "분해 확인"
      options:
        - label: "맞음, 계속 진행"
          description: "분해가 올바름"
        - label: "수정 필요"
          description: "일부 조정 필요"
        - label: "다시 분석"
          description: "완전히 다시 분석"
      multiSelect: false
```

### Output Template

```markdown
## Problem Decomposition

### Original Problem
[User's problem description]

### Core Constraints
- [Constraint 1]
- [Constraint 2]

### Sub-Problems
1. **[Sub-problem 1]**
   - Scope: [description]
   - Success Criteria: [criteria]

2. **[Sub-problem 2]**
   - Scope: [description]
   - Success Criteria: [criteria]

### Dependencies
- [Sub-problem 1] must be solved before [Sub-problem 2]
```

---

## Phase 2: Existing Approaches Collection

### Goal

Gather verified solutions from external sources.

### Information Sources (Priority Order)

1. **GitHub Issues/Discussions** - Real developer problem-solving cases
2. **Stack Overflow** - Community-vetted solutions
3. **Official Docs + Context7** - Standard methods, API usage

### Launch Helper Agent

```yaml
Task:
  subagent_type: "serena-refactor:source-fetcher"
  prompt: |
    Problem: [description]
    Constraints: [list]

    Search for existing solutions from:
    1. GitHub Issues (search for similar problems)
    2. Stack Overflow (search for verified answers)
    3. Official documentation via Context7

    Return structured findings with source links.
```

### LLM Consultant Available

If existing sources are insufficient, consult external LLMs:

```yaml
Task:
  subagent_type: "serena-refactor:llm-consultant"
  prompt: |
    ## Project Context
    - Language/Framework: [e.g., TypeScript, Next.js 14]
    - Dependencies: [e.g., prisma, zod]
    - Architecture: [e.g., App Router]

    ## Problem
    [Detailed problem description]

    ## Constraints
    [List all constraints]

    ## Question
    What approaches would you recommend for solving this problem?
```

---

## Phase 3: Creative Approaches Generation

### Goal

Generate novel approaches beyond documented solutions.

### Creative Approach Types

| Type | Description |
|------|-------------|
| **API Bypass** | Implement features not officially supported |
| **Technology Combination** | Novel combinations of libraries/patterns |
| **Constraint-Ignoring** | Try things assumed impossible |

### Launch Helper Agent

```yaml
Task:
  subagent_type: "serena-refactor:creative-generator"
  prompt: |
    Problem: [description]
    Existing Approaches: [from Phase 2]
    Constraints: [list]

    Generate creative approaches:
    1. API bypass/workarounds
    2. Unexpected technology combinations
    3. Constraint-ignoring experiments

    Consider patterns from skillmaker (isolated daemons, prompt injection, CLI tricks).
```

---

## Phase 4: Hypothesis Formation

### Goal

Structure approaches into testable hypotheses.

### Launch Core Agent

```yaml
Task:
  subagent_type: "serena-refactor:lab-analyst"
  prompt: |
    Existing Approaches: [from Phase 2]
    Creative Approaches: [from Phase 3]
    Constraints: [list]

    Form up to 5 testable hypotheses:
    - Expected outcome
    - Risks and limitations
    - Required resources
    - Success criteria
```

### User Approval Required

```yaml
AskUserQuestion:
  questions:
    - question: "이 가설들로 실험을 진행할까요?"
      header: "가설 승인"
      options:
        - label: "승인 - 모두 실험"
          description: "제시된 모든 가설 테스트"
        - label: "일부만 선택"
          description: "특정 가설만 테스트"
        - label: "가설 수정"
          description: "가설 조정 후 재검토"
        - label: "접근법 재수집"
          description: "Phase 2-3로 돌아가기"
      multiSelect: false
```

### Hypothesis Card Template

```markdown
### Hypothesis [A-E]: [Name]

**Approach**: [description]
**Source**: Existing / Creative / LLM Suggestion

**Expected Outcome**
[What should happen if this works]

**Risks**
- [Risk 1]
- [Risk 2]

**Limitations**
- [Limitation 1]

**Resources Required**
- [Library/tool 1]
- [API/service 1]

**Success Criteria**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

---

## Phase 5: PoC Experiments

### Goal

Implement and run parallel proof-of-concept experiments.

### User Approval Required

```yaml
AskUserQuestion:
  questions:
    - question: "PoC 코드 작성을 시작할까요?"
      header: "실험 승인"
      options:
        - label: "승인 - 실험 시작"
          description: "선택된 가설들의 PoC 구현"
        - label: "Dry run 먼저"
          description: "코드 구조만 미리보기"
        - label: "가설 재검토"
          description: "Phase 4로 돌아가기"
        - label: "취소"
          description: "실험 세션 종료"
      multiSelect: false
```

### Launch Parallel Experiments

```yaml
# Launch up to 5 parallel experimenter agents
Agent 1 - Hypothesis A:
  Task:
    subagent_type: "serena-refactor:lab-experimenter"
    run_in_background: true
    prompt: |
      Hypothesis: A - [name]
      Approach: [description]
      Success Criteria: [list]

      Implement PoC and run initial tests.
      Return: code location, test results, issues found.

Agent 2 - Hypothesis B:
  Task:
    subagent_type: "serena-refactor:lab-experimenter"
    run_in_background: true
    prompt: |
      Hypothesis: B - [name]
      ...

# Continue for all selected hypotheses (max 5)
```

### Collect Results

```yaml
# Wait for all experiments to complete
TaskOutput:
  task_id: [experimenter-A-id]
  block: true

TaskOutput:
  task_id: [experimenter-B-id]
  block: true

# ... for all experiments
```

---

## Phase 6: Verification

### Goal

Rigorously verify experimental results.

### Verification Criteria

- **Test Pass/Fail**: All tests must pass
- **Edge Case Coverage**: Handle boundary conditions
- **Reproducibility**: Same results on repeat

### Launch Verification Agents

```yaml
Task:
  subagent_type: "serena-refactor:lab-verifier"
  prompt: |
    Hypothesis: [name]
    PoC Location: [path]
    Expected: [criteria]

    Verify:
    1. Run all tests
    2. Check edge cases
    3. Confirm reproducibility

    Return: PASS/FAIL with confidence score.
```

### Edge Case Analysis

```yaml
Task:
  subagent_type: "serena-refactor:edge-case-hunter"
  prompt: |
    Implementation: [description]
    Code Location: [path]

    Identify edge cases:
    1. Boundary conditions
    2. Error scenarios
    3. Concurrent access
    4. Resource limits
```

### On Verification Failure

If verification fails, consult external LLMs:

```yaml
Task:
  subagent_type: "serena-refactor:llm-consultant"
  prompt: |
    ## Context
    [Full project context]

    ## What We Tried
    [Hypothesis and implementation]

    ## Failure Details
    [Test results, error messages]

    ## Questions
    1. Why might this have failed?
    2. What alternatives exist?
```

---

## Phase 7: Result Report

### Goal

Document findings and recommendations.

### Generate Reports

1. **Markdown Report**: `docs/lab-reports/YYYY-MM-DD-{topic}.md`
2. **Serena Memory**: `.serena/memories/lab-{topic}.md`

### Report Template

```markdown
# Experiment Report: [Topic]

**Date**: [YYYY-MM-DD HH:mm]
**Problem**: [Original problem description]

## 1. Problem Decomposition
- Sub-problem 1: ...
- Sub-problem 2: ...

## 2. Explored Approaches

### Existing Solutions
| Source | Approach | Summary |
|--------|----------|---------|
| GitHub Issue #123 | ... | ... |
| Stack Overflow | ... | ... |

### Creative Attempts
| Approach | Idea | Risk |
|----------|------|------|
| API Bypass | ... | ... |

## 3. Tested Hypotheses

### Hypothesis A: [Name]
- **Result**: [Success/Failure/Partial]
- **Tests Passed**: X/Y
- **Edge Cases**: X/Y
- **Reproducibility**: [Confirmed/Issues]

### Hypothesis B: [Name]
- **Result**: [Failure]
- **Failure Reason**: [Analysis]
- **Partial Success Conditions**: [When it worked]

## 4. LLM Consultation Log
| LLM | Question | Key Advice |
|-----|----------|------------|
| Gemini | ... | ... |
| Codex | ... | ... |

## 5. Final Recommendation
**Selection**: Hypothesis [X]
**Reason**: [Justification]

## 6. Lessons Learned
- [Insight for future problems]
```

### Serena Memory Template

```markdown
# Lab: [Topic]

## Key Findings
- [Summary]

## Working Approaches
- [Verified solutions]

## Approaches to Avoid
- [Failed methods and reasons]

## Related Resources
- [Useful links]
```

---

## Workflow State Management

State files track progress:

| File | Phase | Purpose |
|------|-------|---------|
| `.lab-problem-defined` | 1 | Problem decomposed |
| `.lab-approaches-collected` | 2-3 | Approaches gathered |
| `.lab-hypotheses-approved` | 4 | Hypotheses confirmed |
| `.lab-experiments-running` | 5 | Experiments in progress |
| `.lab-experiments-done` | 5 | Experiments complete |
| `.lab-verified` | 6 | Verification done |
| `.lab-report-generated` | 7 | Report created |

---

## Examples

### Example 1: Implementation Exploration

```
/serena-refactor:laboratory "How should I implement rate limiting for my API?"
```

### Example 2: Breakthrough Mode

```
/serena-refactor:laboratory "The official SDK doesn't support batch operations, need alternative"
```

### Example 3: Optimization Research

```
/serena-refactor:laboratory "Current image processing takes 10 seconds, need faster approach"
```

---

## Error Handling

### No Viable Approaches Found

If Phase 2-3 finds nothing:
- Expand search scope
- Try different keywords
- Consult LLMs with broader context
- Report limitation to user

### All Hypotheses Fail

If all experiments fail:
- Document failure reasons
- Analyze partial successes
- Suggest alternative problem framing
- Save learnings for future

### Resource Constraints

If experiments exceed resources:
- Prioritize by expected success
- Run sequentially instead of parallel
- Suggest scope reduction
