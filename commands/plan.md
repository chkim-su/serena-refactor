---
description: Refactoring plan creation only. Generates step-by-step plans based on analysis results for user review.
allowed-tools:
  - Task
  - Read
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__plugin_serena_serena__find_symbol
  - mcp__plugin_serena_serena__find_referencing_symbols
  - mcp__plugin_serena_serena__get_symbols_overview
  - mcp__plugin_serena_serena__list_dir
  - mcp__plugin_serena_serena__activate_project
---

# Plan Command

Refactoring plan creation command.

## Usage

```
/serena-refactor:plan [target]
```

## Workflow

### Step 1: Activate Serena Project

```
mcp__plugin_serena_serena__activate_project:
  project: [target directory]
```

### Step 2: Analysis (Brief)

```
Task:
  agent: serena-solid-analyzer
  prompt: |
    Perform SOLID analysis on [target].
    Collect only key information needed for planning.
```

### Step 3: Create Plan

```
Task:
  agent: refactor-planner
  prompt: |
    Create detailed refactoring plan based on analysis results.

    Include:
    1. Dependency graph
    2. Steps defined by priority
    3. Serena tool execution plan for each step
    4. Impact scope and risks
    5. Rollback paths
```

### Step 4: Output and Save Plan

```markdown
## Refactoring Plan: [target]

[Detailed plan content]

---

Plan saved to file: .refactor-plan.md

To execute: `/serena-refactor:refactor --plan .refactor-plan.md`
```
