---
description: Rules and patterns for safely injecting new features into existing codebases. Ensures consistency with project conventions and SOLID principles.
name: feature-injection-rules
allowed-tools: ["Read", "Grep", "Glob", "Edit", "Write", "Task"]
---
# Feature Injection Rules

## Core Principle

**Inject features that blend seamlessly with existing code while maintaining architectural integrity.**

---

## Pre-Injection Checklist

| Check | Serena Tool | Required |
|-------|-------------|----------|
| Project knowledge loaded | `read_memory` | Yes |
| Target location identified | `find_symbol` | Yes |
| Conventions extracted | Knowledge graph | Yes |
| Impact scope analyzed | `find_referencing_symbols` | Yes |
| SOLID compliance verified | SOLID rules | Yes |

---

## Injection Types Summary

| Type | Use Case | Key Tool |
|------|----------|----------|
| New Symbol | Add new class/function | `insert_after_symbol` |
| Extension | Add method to class | `insert_after_symbol` |
| Implementation | New interface impl | `insert_before_symbol` |
| Modification | Change existing | `replace_symbol_body` |

> **Detailed templates**: `Read("references/injection-templates.md")`

---

## Convention Matching Rules

### Naming Conventions

| Element | Common Patterns |
|---------|-----------------|
| Class | PascalCase, suffix (Service, Controller) |
| Method | camelCase, verb prefix (get, set, is) |
| Variable | camelCase or snake_case |
| Constant | UPPER_SNAKE_CASE |
| Interface | I-prefix or -able/-er suffix |

### Structure Conventions

1. **Import Ordering**: External → Internal → Local
2. **Method Ordering**: Constructor → Public → Private → Static
3. **File Organization**: Match existing patterns

---

## SOLID Compliance for Injection

| Principle | Injection Rule |
|-----------|----------------|
| SRP | One clear purpose per symbol |
| OCP | Prefer new implementations over modifications |
| LSP | Honor interface contracts |
| ISP | Don't bloat existing interfaces |
| DIP | Inject dependencies, depend on abstractions |

---

## Post-Injection Verification

1. **Syntax Check**: Run linter/type checker
2. **Import Resolution**: Verify all imports valid
3. **Reference Check**: No broken references
4. **SOLID Check**: Validate against SOLID rules
5. **Test Suggestion**: Propose test cases

> **Code templates**: `Read("references/code-templates.md")`
