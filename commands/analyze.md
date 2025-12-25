---
description: Serena MCP-based SOLID analysis. Symbol-level analysis for accurate violation detection and auto-fix paths.
allowed-tools:
  - Task
  - Read
  - Glob
  - Grep
  - mcp__plugin_serena_serena__get_symbols_overview
  - mcp__plugin_serena_serena__list_dir
  - mcp__plugin_serena_serena__activate_project
---

# Analyze Command

Symbol-level SOLID analysis using Serena MCP.

## Usage

```
/serena-refactor:analyze [target]
```

## Workflow

### Step 0: Activate Serena Project

```
mcp__plugin_serena_serena__activate_project:
  project: [current directory]
```

### Step 1: Target Selection

If no target provided:
```yaml
AskUserQuestion:
  question: "What would you like to analyze?"
  header: "Analysis Target"
  options:
    - label: "Current directory"
      description: "Analyze entire project"
    - label: "Specific path"
      description: "Specify directory or file"
```

### Step 2: Run Analysis

```
Task:
  agent: serena-solid-analyzer
  prompt: |
    Perform SOLID analysis on [target].

    Must include:
    1. Symbol-level analysis (get_symbols_overview, find_symbol)
    2. Reference impact analysis (find_referencing_symbols)
    3. Serena tool-based fix paths for each violation
    4. Accurate file:line references
```

### Step 3: Output Results

```markdown
## Analysis Report: [target]

### Quick Summary
| Principle | Status | Violations | Impact Scope |
|-----------|--------|------------|--------------|
| SRP | OK/WARN/FAIL | X | Y files |
| OCP | OK/WARN/FAIL | X | Y files |
| LSP | OK/WARN/FAIL | X | Y files |
| ISP | OK/WARN/FAIL | X | Y files |
| DIP | OK/WARN/FAIL | X | Y files |

### Key Issues (Priority Order)
1. **[CRITICAL]** [file:line] - [issue] → Serena fix: [tool name]
2. ...

### Recommendations
- Run `/serena-refactor:refactor` for auto-fix
- Run `/serena-refactor:plan` for step-by-step planning
```
