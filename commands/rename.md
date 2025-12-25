---
description: Serena-based safe symbol renaming. Automatically updates all references across the entire codebase.
allowed-tools:
  - Task
  - Read
  - AskUserQuestion
  - mcp__plugin_serena_serena__find_symbol
  - mcp__plugin_serena_serena__find_referencing_symbols
  - mcp__plugin_serena_serena__rename_symbol
  - mcp__plugin_serena_serena__activate_project
---

# Rename Command

Safe symbol renaming using Serena MCP.

## Usage

```
/serena-refactor:rename <symbol> <new-name>
```

## Examples

```
/serena-refactor:rename UserService/getUser fetchUserById
/serena-refactor:rename OldClassName NewClassName
```

## Workflow

### Step 1: Verify Symbol

```
mcp__plugin_serena_serena__find_symbol:
  name_path_pattern: [symbol]
  include_body: False
```

If symbol not found:
```yaml
AskUserQuestion:
  question: "Symbol '[symbol]' not found. Please enter the correct path."
  header: "Symbol Path"
```

### Step 2: Impact Analysis

```
mcp__plugin_serena_serena__find_referencing_symbols:
  name_path: [symbol]
  relative_path: [file]
```

### Step 3: Change Preview

```markdown
## Rename Preview

### Target Symbol
- Name: [symbol]
- File: [file:line]
- Type: [class/method/function/variable]

### Impact Scope
| File | References | Code Snippet |
|------|------------|--------------|
| src/service.ts | 3 | `userService.getUser()` |
| src/controller.ts | 2 | `getUser(id)` |
| ... | ... | ... |

**Total references: N**
```

### Step 4: User Confirmation

```yaml
AskUserQuestion:
  question: "Proceed with [symbol] → [new-name]? (N references to update)"
  header: "Rename"
  options:
    - label: "Proceed"
      description: "Auto-update all references"
    - label: "Cancel"
      description: "Cancel change"
```

### Step 5: Execute Rename

```
mcp__plugin_serena_serena__rename_symbol:
  name_path: [symbol]
  relative_path: [file]
  new_name: [new-name]
```

### Step 6: Verify Results

```markdown
## Rename Complete

✓ [symbol] → [new-name]
✓ [N] references updated

### Changed Files
- src/service.ts
- src/controller.ts
- ...

### Next Steps
- Recommended: Run tests `npm test`
- On issues: Rollback with `git checkout -- .`
```

---

## Core Rules

1. **Trust symbol tools** - Serena rename_symbol auto-updates all references
2. **Preview required** - Verify impact scope before change
3. **User confirmation** - Explicit consent before execution
4. **Recommend tests** - Recommend test run after change
