---
description: Serena-based code extraction. Safely performs method, interface, and class extraction at the symbol level.
skills:
  - serena-refactoring-patterns
  - solid-design-rules
allowed-tools:
  - Task
  - Read
  - AskUserQuestion
  - mcp__serena__find_symbol
  - mcp__serena__find_referencing_symbols
  - mcp__serena__replace_symbol_body
  - mcp__serena__replace_content
  - mcp__serena__insert_after_symbol
  - mcp__serena__insert_before_symbol
  - mcp__serena__activate_project
---

# Extract Command

Code extraction refactoring using Serena MCP.

## Usage

```
/serena-refactor:extract <type> <source> [options]
```

### Extraction Types

| Type | Description | Example |
|------|-------------|---------|
| `method` | Extract method | `/extract method UserService/processUser` |
| `interface` | Extract interface | `/extract interface UserService` |
| `class` | Split class | `/extract class UserService` |

---

## Method Extraction

### Workflow

#### 1. Analyze Target Method

```
mcp__serena__find_symbol:
  name_path_pattern: [source]
  include_body: True
```

#### 2. Identify Extraction Target

```yaml
AskUserQuestion:
  question: "Select code block to extract"
  header: "Extraction Target"
  options:
    - label: "Auto-detect"
      description: "Auto-identify repeated/complex logic"
    - label: "Specify manually"
      description: "Specify line range"
```

#### 3. Create New Method

```
mcp__serena__insert_after_symbol:
  name_path: [source]
  relative_path: [file]
  body: |
    def extracted_method(params):
        # Extracted logic
```

#### 4. Modify Original

```
mcp__serena__replace_content:
  relative_path: [file]
  needle: "extracted code pattern"
  repl: "self.extracted_method(args)"
  mode: "regex"
```

---

## Interface Extraction

### Workflow

#### 1. Analyze Class

```
mcp__serena__find_symbol:
  name_path_pattern: [source]
  depth: 1
  include_body: False
```

#### 2. Identify Public Methods

Only public methods included in interface

#### 3. Create Interface

```
mcp__serena__insert_before_symbol:
  name_path: [source]
  relative_path: [file]
  body: |
    interface IClassName {
        method1(param: Type): ReturnType;
        method2(): void;
    }
```

#### 4. Modify Class

```
mcp__serena__replace_symbol_body:
  name_path: [source]
  relative_path: [file]
  body: |
    class ClassName implements IClassName {
        // Existing implementation
    }
```

---

## Class Split

### Workflow

#### 1. Responsibility Analysis

```
mcp__serena__find_symbol:
  name_path_pattern: [source]
  depth: 1
  include_body: False
```

Group methods by responsibility

#### 2. Split Plan

```yaml
AskUserQuestion:
  question: "Select class split approach"
  header: "Split Strategy"
  options:
    - label: "Auto-grouping"
      description: "Auto-split based on method names/dependencies"
    - label: "Specify manually"
      description: "Specify method groups to split"
```

#### 3. Create New Class

```
mcp__serena__insert_after_symbol:
  name_path: [source]
  relative_path: [file]
  body: |
    class ExtractedClass {
        // Separated methods
    }
```

#### 4. Delegate from Original Class

```
mcp__serena__replace_symbol_body:
  # Replace moved methods with delegation calls
```

---

## Output Format

```markdown
## Extraction Complete: [type]

### Created Symbol
- Name: [new_symbol]
- File: [file:line]
- Type: [method/interface/class]

### Modified Symbol
- Original: [source]
- Changes: [description]

### Reference Updates
| File | Change |
|------|--------|
| ... | ... |

### Next Steps
- Run tests: `npm test`
- For further refactoring: `/serena-refactor:refactor`
```

---

## Core Rules

1. **Symbol-level operations** - Use Serena symbol tools instead of text replacement
2. **Auto-update references** - Automatically fix all call sites after extraction
3. **Atomic changes** - Complete extraction in one operation
4. **Rollback ready** - Always restorable via Git
