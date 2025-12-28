---
description: Symbolic refactoring patterns using Serena MCP tools. Core patterns for safe code modification, reference tracking, and automated refactoring workflows.
name: serena-refactoring-patterns
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Task"]
---
# Serena Symbolic Refactoring Patterns

## Core Principle

**Understand and modify code at the symbol level.**
Ensure safety through AST-based editing, not text replacement.

---

## 1. Symbol Navigation Patterns

### 1.1 Hierarchical Symbol Navigation

```
1. get_symbols_overview to understand file structure (depth=0)
2. When class of interest found, use depth=1 to check method list
3. When specific method body needed, use find_symbol + include_body=True
```

### 1.2 Name Pattern Search

| Pattern | Meaning | Example |
|---------|---------|---------|
| `ClassName` | All classes with that name | `UserService` |
| `ClassName/method` | Method of specific class | `UserService/create` |
| `/ClassName/method` | Exact path matching | `/UserService/create` |
| `get*` (substring_matching=True) | Prefix matching | `getValue`, `getData` |

### 1.3 Reference Tracking

```
Using find_referencing_symbols:
- Assess refactoring impact scope
- Build dependency graph
- Detect circular references
```

---

## 2. Safe Modification Patterns

### 2.1 Replace Symbol Body

**When to Use:**
- Rewriting entire function/method
- Changing class definition
- Modification including signature

**Cautions:**
- body excludes docstring/comments
- Must include signature
- Indentation must be exact

### 2.2 Replace Content

**When to Use:**
- Modifying only some lines within a symbol
- Regex-based bulk replacement
- Simultaneous modification of multiple locations

**Pattern:**
```
mode: "regex"
needle: "old_pattern.*?end_marker"
repl: "new_content"
allow_multiple_occurrences: True/False
```

### 2.3 Insertion Patterns

| Tool | Use Case |
|------|----------|
| `insert_before_symbol` | Adding imports, adding decorators |
| `insert_after_symbol` | Adding new methods/classes |

---

## 3. Refactoring Workflows

### 3.1 Extract Method

```
1. Read target method body with find_symbol
2. Identify code block to extract
3. Design new method signature
4. Add new method with insert_after_symbol
5. Replace original with call using replace_content
6. Verify impact with find_referencing_symbols
```

### 3.2 Rename Symbol

```
1. Identify all usages with find_referencing_symbols
2. Rename across entire codebase with rename_symbol
3. Verify results (all references updated automatically)
```

### 3.3 Extract Interface

```
1. Get class method list with find_symbol + depth=1
2. Identify common methods
3. Write new interface definition
4. Add interface with insert_before_symbol
5. Modify class to implement interface with replace_symbol_body
```

### 3.4 Move Method

```
1. Read original method with find_symbol (include_body=True)
2. Add method to target class with insert_after_symbol
3. Identify all call sites with find_referencing_symbols
4. Update call sites with replace_content
5. Delete original method (replace_symbol_body with empty or remove)
```

---

## 4. SOLID Violation Auto-fix

### 4.1 SRP Violation → Class Split

```
Detection: Class has more than 10 methods
Fix:
1. Group methods with get_symbols_overview
2. Create new classes by responsibility
3. Apply move method pattern
4. Delegate from original class to new classes
```

### 4.2 DIP Violation → Extract Interface

```
Detection: Business logic directly depends on infrastructure
Fix:
1. Map dependencies with find_referencing_symbols
2. Apply extract interface pattern
3. Change to constructor injection
```

### 4.3 OCP Violation → Strategy Pattern

```
Detection: Type-based switch/if chains
Fix:
1. Detect switch statements with search_for_pattern
2. Extract each case to strategy class
3. Apply factory/registry pattern
```

---

## 5. Verification Patterns

### 5.1 Pre-modification Checklist

- [ ] Verify target symbol exists with find_symbol
- [ ] Assess impact scope with find_referencing_symbols
- [ ] Verify test file exists

### 5.2 Post-modification Verification

- [ ] Symbol tools are reliable if no errors
- [ ] Verify reference integrity with find_referencing_symbols
- [ ] Run tests with execute_shell_command

---

## 6. Memory Utilization

### Saving Project Context

```
write_memory:
- Architecture decision records
- Refactoring history
- Coding conventions
```

### Cross-session Continuity

```
read_memory:
- Previous refactoring progress
- Known technical debt
- High-priority fix targets
```
