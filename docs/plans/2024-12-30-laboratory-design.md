# Laboratory Plugin Design

**Date**: 2024-12-30
**Version**: 1.0
**Status**: Approved

---

## Overview

### Name & Entry Point
- **Name**: `laboratory` (serena-refactor sub-command)
- **Entry Point**: `/serena-refactor:laboratory "problem description"`

### Core Philosophy
> **"Apply scientific methodology to code implementation"**
> - Problem decomposition → Hypothesis formation → Parallel experimentation → Rigorous verification
> - Record and learn from failures
> - Balance between existing solutions and creative approaches

### Trigger Scenarios
| Mode | Situation | Example |
|------|-----------|---------|
| **Exploration** | Don't know how to implement | "How do I implement OAuth?" |
| **Breakthrough** | Standard approach doesn't work | "Need to bypass API limitations" |
| **Optimization** | Looking for better methods | "Any performance improvements?" |

---

## 7-Stage Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│  1️⃣ Problem Decomposition ──[✋ User Approval]──→ 2️⃣ Existing Approaches │
│        │                                              │             │
│        │                                   [LLM Consult Available]  │
│        ▼                                              ▼             │
│  3️⃣ Creative Approaches ────────────→ 4️⃣ Hypothesis Formation ──[✋]│
│                                               │                     │
│        ┌──────────────────────────────────────┘                     │
│        ▼                                                            │
│  5️⃣ PoC Experiments ──[✋]──→ Parallel Execution (max 5)            │
│        │                                                            │
│   ┌────┴────┬────────┬────────┬────────┐                           │
│   ▼         ▼        ▼        ▼        ▼                           │
│ Hyp.A    Hyp.B    Hyp.C    Hyp.D    Hyp.E                          │
│   │         │        │        │        │                           │
│   └────┬────┴────────┴────────┴────────┘                           │
│        ▼                                                            │
│  6️⃣ Verification ──[LLM Consult on Failure]──→ 7️⃣ Result Report    │
└─────────────────────────────────────────────────────────────────────┘
```

### Stage Details

| Stage | Name | Agent | Output |
|-------|------|-------|--------|
| 1️⃣ | Problem Decomposition | `lab-analyst` | Sub-problems, constraints |
| 2️⃣ | Existing Approaches | `source-fetcher` | GitHub/SO/docs solutions |
| 3️⃣ | Creative Approaches | `creative-generator` | Bypass/combination/contrarian ideas |
| 4️⃣ | Hypothesis Formation | `lab-analyst` | Hypothesis cards (expected results, risks) |
| 5️⃣ | PoC Experiments | `lab-experimenter` × N | PoC code (1 per hypothesis) |
| 6️⃣ | Verification | `lab-verifier` | Test results, reproducibility check |
| 7️⃣ | Result Report | `lab-verifier` | Final report + Serena memory |

### User Approval Points
- 1️⃣ Problem decomposition confirmation
- 4️⃣ Hypothesis review before experimentation
- 5️⃣ Before PoC execution

### Verification Criteria (Stage 6)
- ✅ Test pass/fail
- ✅ Edge case coverage
- ✅ Reproducibility

---

## Information Sources (Priority Order)

1. **GitHub Issues/Discussions** - Real developer problem-solving cases
2. **Stack Overflow** - Verified solutions, community-vetted quality
3. **Official Docs + Context7** - Standard methods, API usage

---

## Creative Approaches Scope

| Type | Description |
|------|-------------|
| **API Bypass/Hacking** | Implement features not officially supported |
| **Technology Combination** | Novel combinations of different libraries/patterns |
| **Constraint-Ignoring Experiments** | Try things assumed impossible |

**Examples from skillmaker patterns**:
- Isolated Daemonized Serena → MCP server isolation strategy
- Claude-only SDK prompt injection → Solve with system prompts, no tools
- Creative CLI usage → Undocumented combinations

---

## Agent Architecture

### Core Agents (3)

| Agent | Role | Key Tools |
|-------|------|-----------|
| **`lab-analyst`** | Problem decomposition, hypothesis design | Serena symbol analysis, code exploration |
| **`lab-experimenter`** | PoC writing, parallel experiment coordination | Serena editing, Task (parallel spawn) |
| **`lab-verifier`** | Test execution, judgment, report writing | Bash (tests), Write (reports) |

### Helper Agents (4)

| Agent | Role | Invocation | Technology |
|-------|------|------------|------------|
| **`source-fetcher`** | External info collection | Stage 2️⃣ | WebSearch, Context7, WebFetch |
| **`creative-generator`** | Creative approach generation | Stage 3️⃣ | Bypass/combination patterns |
| **`llm-consultant`** | External LLM consultation | Stages 2️⃣~3️⃣, 6️⃣ on failure | u-llm-sdk (Gemini, Codex) |
| **`edge-case-hunter`** | Edge case discovery | Stages 4️⃣, 6️⃣ | Boundary condition analysis |

### Parallel Experiment Execution

```
[lab-experimenter] (coordinator)
        │
        ├──→ Task(experimenter-instance-1, Hypothesis A) ──→ Result A
        ├──→ Task(experimenter-instance-2, Hypothesis B) ──→ Result B
        ├──→ Task(experimenter-instance-3, Hypothesis C) ──→ Result C
        ├──→ Task(experimenter-instance-4, Hypothesis D) ──→ Result D
        └──→ Task(experimenter-instance-5, Hypothesis E) ──→ Result E
                      │
                      ▼
              [lab-verifier] Comparative Analysis
```

---

## LLM Consultant Query Protocol

### Context Injection Requirements

External LLMs (Gemini, Codex) cannot access project context, so queries must be **self-contained**.

```markdown
## Query Template

### 1. Project Context
- Language/Framework: {e.g., TypeScript, Next.js 14}
- Related Dependencies: {e.g., prisma, zod, next-auth}
- Architecture Pattern: {e.g., App Router, Server Actions}

### 2. Problem Situation
- Feature being implemented: {detailed description}
- Current constraints: {API limits, performance requirements, etc.}
- Approaches already tried: {what's been attempted}

### 3. Related Code Snippet
```{language}
// Core code excerpt (full, not abbreviated)
```

### 4. Specific Question
- {Clear and specific question}
```

### Example: Failure Analysis Consultation

```markdown
## Project Context
- TypeScript + Express.js
- Redis used for caching
- Expected ~1000 concurrent connections

## Problem Situation
- Rate limiting implementation test failing
- Applied sliding window algorithm but fails on edge cases
- Count error when requests arrive exactly at window boundary

## Related Code
```typescript
async checkRateLimit(userId: string): Promise<boolean> {
  const now = Date.now();
  const windowStart = now - this.windowMs;
  // ... full code, no omissions
}
```

## Questions
1. Are there edge cases missed in window boundary handling?
2. Should this be handled atomically with Redis MULTI/EXEC?
```

---

## Failure Handling

| Handling | Description |
|----------|-------------|
| **Record Failure Reasons** | Document why it failed → Prevent repeating mistakes |
| **Analyze Partial Success** | Under what conditions did it work? → Explore limited applicability |

---

## File Structure

### Plugin Files

```
serena-refactor/
├── .claude-plugin/
│   └── marketplace.json          # Version update (2.7.0)
├── commands/
│   └── laboratory.md             # Entry point command
├── agents/
│   ├── lab-analyst.md            # Problem decomposition + hypothesis
│   ├── lab-experimenter.md       # PoC writing + parallel coordination
│   ├── lab-verifier.md           # Verification + reporting
│   ├── source-fetcher.md         # External info collection
│   ├── creative-generator.md     # Creative approaches
│   ├── llm-consultant.md         # External LLM consultation
│   └── edge-case-hunter.md       # Edge case discovery
├── skills/
│   └── laboratory-patterns/      # Experiment pattern references
│       ├── SKILL.md
│       └── references/
│           ├── creative-approaches.md   # Bypass/combination pattern examples
│           ├── query-templates.md       # LLM consultation templates
│           └── verification-criteria.md # Verification criteria details
└── hooks/
    └── hooks.json                # Workflow hooks added
```

### Experiment Results (in target project)

```
target-project/
├── docs/
│   └── lab-reports/
│       └── YYYY-MM-DD-{topic}.md    # Markdown report
└── .serena/
    └── memories/
        └── lab-{topic}.md           # Serena memory
```

---

## Report Template

```markdown
# 🧪 Experiment Report: {Topic}

**Date**: {YYYY-MM-DD HH:mm}
**Problem**: {Original problem description}

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

### Hypothesis A: {Name}
- **Expected Result**: ...
- **PoC Code**: `experiments/hypothesis-a/`
- **Result**: ✅ Success / ❌ Failure / ⚠️ Partial Success
- **Tests Passed**: 5/5
- **Edge Case Coverage**: 3/3
- **Reproducibility**: Confirmed

### Hypothesis B: {Name}
- **Result**: ❌ Failure
- **Failure Reason**: {Detailed analysis}
- **Partial Success Conditions**: {Under what conditions it worked}

## 4. LLM Consultation Log
| LLM | Question Summary | Key Advice |
|-----|------------------|------------|
| Gemini | Boundary handling | Recommend atomic operations |
| Codex | Race condition | Suggest mutex pattern |

## 5. Final Recommendation
**Selection**: Hypothesis A
**Reason**: Met all verification criteria, simplest implementation

## 6. Lessons Learned
- {Insights applicable to similar future problems}
```

---

## Serena Memory Format

```markdown
# Lab: {Topic}

## Key Findings
- {Concise summary}

## Working Approaches
- {Verified solutions}

## Approaches to Avoid
- {Failed methods and reasons}

## Related Resources
- {Useful GitHub Issues, SO links}
```

---

## Implementation Checklist

- [ ] Create `commands/laboratory.md`
- [ ] Create `agents/lab-analyst.md`
- [ ] Create `agents/lab-experimenter.md`
- [ ] Create `agents/lab-verifier.md`
- [ ] Create `agents/source-fetcher.md`
- [ ] Create `agents/creative-generator.md`
- [ ] Create `agents/llm-consultant.md`
- [ ] Create `agents/edge-case-hunter.md`
- [ ] Create `skills/laboratory-patterns/` structure
- [ ] Update `hooks/hooks.json` with workflow hooks
- [ ] Update `marketplace.json` to version 2.7.0
