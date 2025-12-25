---
description: Serena MCP-based automated refactoring. Executes the full workflow of analysis, planning, execution, and verification.
allowed-tools:
  - Task
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - mcp__plugin_serena_serena__find_symbol
  - mcp__plugin_serena_serena__find_referencing_symbols
  - mcp__plugin_serena_serena__get_symbols_overview
  - mcp__plugin_serena_serena__replace_symbol_body
  - mcp__plugin_serena_serena__replace_content
  - mcp__plugin_serena_serena__insert_after_symbol
  - mcp__plugin_serena_serena__insert_before_symbol
  - mcp__plugin_serena_serena__rename_symbol
  - mcp__plugin_serena_serena__activate_project
  - mcp__plugin_serena_serena__execute_shell_command
  - mcp__plugin_serena_serena__write_memory
---

# Refactor Command

Full refactoring workflow using Serena MCP.

## Usage

```
/serena-refactor:refactor [target]
```

## Workflow Overview

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                     SERENA REFACTORING WORKFLOW                            ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  ┌─────────────────┐                                                      ║
║  │ 0. INITIALIZE   │ ← Activate Serena project + Git backup               ║
║  └────────┬────────┘                                                      ║
║           ▼                                                               ║
║  ┌─────────────────┐                                                      ║
║  │ 1. SOLID ANAL.  │ ← serena-solid-analyzer                              ║
║  └────────┬────────┘                                                      ║
║           ▼                                                               ║
║  ┌─────────────────┐                                                      ║
║  │ 2. PLAN         │ ← refactor-planner                                   ║
║  └────────┬────────┘                                                      ║
║           ▼                                                               ║
║  ╔═════════════════════════════════════════════════════════════════════╗  ║
║  ║  GATE: User Plan Approval                                           ║  ║
║  ╚═══════════════════════════════╤═════════════════════════════════════╝  ║
║                                  ▼                                        ║
║  ┌─────────────────────────────────────────────────────────────────┐     ║
║  │ 3. STEP-BY-STEP EXECUTION                                        │     ║
║  │    ┌────────────────────────────────────────────────────────┐   │     ║
║  │    │ FOR each step:                                          │   │     ║
║  │    │   3.1 Execute serena-refactor-executor                 │   │     ║
║  │    │   3.2 Verify with refactor-auditor                     │   │     ║
║  │    │   3.3 PASS → next step / FAIL → fix                    │   │     ║
║  │    │   [LOOP until all steps complete]                       │   │     ║
║  │    └────────────────────────────────────────────────────────┘   │     ║
║  └────────────────────────────────┬────────────────────────────────┘     ║
║                                   ▼                                       ║
║  ┌─────────────────┐                                                      ║
║  │ 4. FINAL VERIFY │ ← refactor-auditor (full)                            ║
║  └────────┬────────┘                                                      ║
║           ▼                                                               ║
║  ┌─────────────────┐                                                      ║
║  │ 5. REPORT       │                                                      ║
║  └─────────────────┘                                                      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## Step 0: Initialize

### Activate Serena Project
```
mcp__plugin_serena_serena__activate_project:
  project: [target directory]
```

### Create Git Backup
```bash
git stash push -m "pre-refactor-backup-$(date +%Y%m%d-%H%M%S)"
```

---

## Step 1: SOLID Analysis

```
Task:
  agent: serena-solid-analyzer
  prompt: |
    Perform SOLID analysis on [target].

    Using Serena symbol tools:
    1. Analyze all class/function structures
    2. Map reference relationships
    3. Detect SOLID violations
    4. Provide auto-fix paths for each violation
```

Display analysis summary

---

## Step 2: Refactoring Plan

```
Task:
  agent: refactor-planner
  prompt: |
    Create refactoring plan based on SOLID analysis results.

    Requirements:
    1. Define steps by priority
    2. Serena tool execution plan for each step
    3. Impact scope analysis
    4. Specify rollback paths
```

### User Approval

```yaml
AskUserQuestion:
  question: "Reviewed the refactoring plan. Proceed?"
  header: "Plan Approval"
  options:
    - label: "Approve - Proceed"
      description: "Execute refactoring as planned"
    - label: "Needs modification"
      description: "Adjust plan and re-review"
    - label: "Cancel"
      description: "Abort refactoring"
```

---

## Step 3: Step-by-Step Execution

### For each step:

#### 3.1 Execute
```
Task:
  agent: serena-refactor-executor
  prompt: |
    Execute refactoring Step [N].

    Goal: [step goal]
    Target: [symbol path]

    Serena tool execution order:
    1. [tool and parameters]
    2. [tool and parameters]
    ...
```

#### 3.2 Verify
```
Task:
  agent: refactor-auditor
  prompt: |
    Verify Step [N] refactoring results.

    Check items:
    1. Incomplete patterns (TODO, FIXME)
    2. Reference integrity
    3. SOLID improvement
    4. Test passing
```

#### 3.3 Handle Results

**If PASS:**
- Proceed to next step
- Update progress

**If FAIL:**
```yaml
AskUserQuestion:
  question: "Step [N] verification failed. What to do?"
  header: "Verification Failed"
  options:
    - label: "Fix issues and re-verify"
      description: "Fix discovered issues"
    - label: "Skip this step"
      description: "Proceed to next step (not recommended)"
    - label: "Rollback"
      description: "Undo this step's changes"
```

---

## Step 4: Final Verification

```
Task:
  agent: refactor-auditor
  prompt: |
    Perform final verification of all refactoring results.

    Scope: All changed files

    Check items:
    1. Overall SOLID improvement
    2. All tests passing
    3. No new violations
    4. Reference integrity
```

---

## Step 5: Completion Report

```markdown
## Refactoring Completion Report

### Summary
- Total steps: [N]
- Successful steps: [M]
- Changed files: [X]

### SOLID Improvement
| Principle | Before | After | Improvement |
|-----------|--------|-------|-------------|
| SRP | X | Y | +Z% |
| OCP | X | Y | +Z% |
| ... | ... | ... | ... |

### Major Changes
1. [Change 1]
2. [Change 2]
...

### Test Results
✓ All tests passed

### Next Steps
- `git commit` to commit changes
- `git stash drop` to delete backup (optional)
```

---

## Rollback

Rollback available anytime:

```bash
# Full rollback
git stash pop

# Or specific files only
git checkout -- [file]
```

---

## Core Rules

1. **Symbol tools first** - Serena symbol tools are always priority
2. **Step-by-step verification** - Must verify after each step
3. **User consent** - Major decisions require user approval
4. **Rollback ready** - Always maintain restorable state
5. **No incomplete code** - Leaving TODO/FIXME means failure
