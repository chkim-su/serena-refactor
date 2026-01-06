---
description: Duplicate code and role detection. Identifies clone code, similar functions, and duplicate constants, suggesting consolidation approaches.
skills:
  - duplicate-detection-rules
allowed-tools:
  - Task
  - Read
  - Glob
  - Grep
  - mcp__serena__activate_project
---

# Detect Duplicates Command

Detects duplicated code and roles in the codebase.

## Usage

```
/serena-refactor:detect-duplicates [target]
```

## Workflow

### Step 0: Activate Serena Project

```
mcp__serena__activate_project:
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

### Step 2: Run Duplicate Detection

```
Task:
  agent: "duplicate-detector"
  prompt: |
    Perform duplicate detection on [target].

    Detection targets:
    1. Clone code (Type 1-3)
       - Exact identical code
       - Code differing only in variable names
       - Structurally similar code
    2. Role duplication
       - Classes/functions with similar responsibilities
       - Synonym usage (get/fetch/retrieve etc.)
    3. Variable/constant duplication
       - Magic numbers
       - Duplicate strings
       - Duplicate config values

    Perform symbol analysis through Serena Gateway.
```

### Step 3: Output Results

```markdown
## Duplicate Detection Report: [target]

### Quick Summary
| Type | Found | Severity |
|------|-------|----------|
| Clone code | X | CRITICAL/HIGH |
| Role duplication | Y | HIGH |
| Constant duplication | Z | MEDIUM/LOW |

### Key Findings (Priority Order)
1. **[CRITICAL]** [file:line] - [description]
2. **[HIGH]** [file:line] - [description]
...

### Recommendations
- Run `/serena-refactor:refactor` for consolidation
- Run `/serena-refactor:extract` for common function extraction
```

---

## Detection Criteria

### Clone Code Thresholds

| Type | Similarity | Min Lines |
|------|------------|-----------|
| Type-1 (Identical) | 100% | 5 lines |
| Type-2 (Parameterized) | > 90% | 5 lines |
| Type-3 (Similar) | > 70% | 10 lines |

### Role Duplication Signals

- Same prefix/suffix (e.g., `*Manager`, `*Handler`)
- 3+ identical method names
- Same dependency injection

### Constant Duplication Criteria

- Magic numbers: 2+ usages
- Strings: 3+ usages (5+ characters)

---

## Core Rules

1. **Analyze through Serena Gateway** - Symbol-level accuracy
2. **Respect thresholds** - Don't report below 70% similarity
3. **Include impact** - Specify reference count, consolidation complexity
4. **Concrete fix paths** - Provide Serena tool names and sequence
