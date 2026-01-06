---
description: Quick code quality audit. Verifies code quality before and after refactoring.
skills:
  - solid-design-rules
  - serena-refactoring-patterns
allowed-tools:
  - Task
  - Read
  - Glob
  - Grep
  - mcp__serena__find_symbol
  - mcp__serena__search_for_pattern
  - mcp__serena__execute_shell_command
  - mcp__serena__activate_project
---

# Audit Command

Refactoring quality audit.

## Usage

```
/serena-refactor:audit [target]
```

## Workflow

### Step 1: Identify Target

If no target provided:
- Auto-detect changed files via Git
- `git diff --name-only HEAD~1`

### Step 2: Run Audit

```
Task:
  agent: "refactor-auditor"
  prompt: |
    Perform code quality audit on [target].

    Check items:
    1. Incomplete patterns (TODO, FIXME)
    2. Reference integrity
    3. Empty implementations
    4. SOLID violations
    5. Test passing
```

### Step 3: Output Results

```markdown
## Audit Results

### Quick Status
| Item | Status |
|------|--------|
| Incomplete patterns | ✓/✗ |
| Reference integrity | ✓/✗ |
| Tests | ✓/✗ |

### VERDICT: PASS/FAIL

### On FAIL - Required Actions
1. [Item to fix]
...
```
