---
description: Code duplication detection rules. Patterns and thresholds for identifying clone code, role duplication, and variable duplication. Guide for removing duplicates through refactoring.
name: duplicate-detection-rules
allowed-tools: ["Read", "Grep", "Glob", "Task"]
---
# Duplicate Detection Rules

## Core Principle

**Duplication is the enemy of change.**
When you change one, you must change all copies. Miss one, and you have a bug.

---

## Detection Categories

### 1. Clone Code

| Type | Definition | Similarity | Severity |
|------|------------|------------|----------|
| Type-1 | Exact clone (whitespace ignored) | 100% | CRITICAL |
| Type-2 | Same structure, different names/literals | >90% | HIGH |
| Type-3 | Similar with some modifications | >70% | MEDIUM |

> **Details**: `Read("references/clone-patterns.md")`

### 2. Role Duplication

**Detection Signals:**

| Signal | Description | Probability |
|--------|-------------|-------------|
| Similar names | `*Manager`, `*Handler`, `*Service` | High |
| Same interface | Implements same interface | Very High |
| Similar methods | 3+ same method names | High |

**Synonym Groups to Watch:**
- Retrieve: `get`, `fetch`, `retrieve`, `find`, `load`
- Create: `create`, `make`, `build`, `generate`, `new`
- Validate: `validate`, `check`, `verify`, `ensure`

### 3. Variable/Constant Duplication

| Type | Detection Criteria |
|------|--------------------|
| Magic numbers | Same value used 2+ times |
| Duplicate strings | Same string (5+ chars) used 3+ times |
| Config values | Same config in multiple places |

---

## Detection Thresholds

| Type | Threshold | Report |
|------|-----------|--------|
| Type-1 Clone | 5 lines | Always |
| Type-2 Clone | 90% similar | Always |
| Type-3 Clone | 70% similar | 10+ lines |
| Role duplication | 3 same methods | Always |
| Magic numbers | 2+ usages | Always |

---

## Exceptions (Allowed Duplication)

| Situation | Reason |
|-----------|--------|
| Test code | Maintain test independence |
| Generated code | Auto-generation tool responsibility |
| External interface | Contract compliance required |
| Performance code | Intentional inlining |

**Not Considered Duplication:**
- Code 2 lines or less
- Idiomatic patterns (e.g., `if (err) return;`)
- Language boilerplate

---

## Fix Strategies

> **Detailed patterns**: `Read("references/fix-patterns.md")`

| Duplication Type | Strategy |
|------------------|----------|
| Clone code | Extract common function |
| Role duplication | Consolidate classes |
| Constants | Centralize config |
