---
description: Code duplication detection rules. Patterns and thresholds for identifying clone code, role duplication, and variable duplication. Guide for removing duplicates through refactoring.
name: duplicate-detection-rules
---
# Duplicate Detection Rules

## Core Principle

**Duplication is the enemy of change.**
When you change one, you must change all copies. Miss one, and you have a bug.

---

## 1. Clone Code

### 1.1 Type-1: Exact Clone

**Definition:** Exactly identical code excluding whitespace/comments

**Detection Criteria:**
- 5+ consecutive identical lines
- 100% token sequence match

**Severity:** CRITICAL

**Fix Strategy:**
- Extract to common function
- Separate into utility module

### 1.2 Type-2: Parameterized Clone

**Definition:** Same structure with only different variable names/literals

```javascript
// Clone A
const result = users.filter(u => u.age > 18);
return result.map(u => u.name);

// Clone B
const data = items.filter(i => i.price > 100);
return data.map(i => i.title);
```

**Detection Criteria:**
- Structural similarity > 90%
- Identical token type sequence

**Severity:** HIGH

**Fix Strategy:**
- Extract parameterized function
- Use generics/templates

### 1.3 Type-3: Similar Structure Clone

**Definition:** Similar code with some lines added/deleted/modified

**Detection Criteria:**
- Structural similarity > 70%
- Same core logic pattern

**Severity:** MEDIUM

**Fix Strategy:**
- Convert to strategy pattern
- Apply template method pattern

---

## 2. Role Duplication

### 2.1 Same Responsibility Classes

**Detection Signals:**

| Signal | Description | Duplication Probability |
|--------|-------------|-------------------------|
| Similar names | `*Manager`, `*Handler`, `*Service` | High |
| Same interface | Implements same interface | Very High |
| Similar method set | 3+ same method names | High |
| Same dependencies | Depends on same classes | Medium |

**Severity:** HIGH

**Fix Strategy:**
- Consolidate into one
- Redefine roles and separate

### 2.2 Synonym Usage

**Synonym pairs to watch:**

| Group | Synonyms |
|-------|----------|
| Retrieve | `get`, `fetch`, `retrieve`, `find`, `load` |
| Create | `create`, `make`, `build`, `generate`, `new` |
| Validate | `validate`, `check`, `verify`, `ensure` |
| Process | `process`, `handle`, `execute`, `run`, `do` |
| Transform | `convert`, `transform`, `parse`, `map`, `to` |

**Rules:**
- Use only one synonym per project
- Convention documentation required

---

## 3. Variable/Constant Duplication

### 3.1 Magic Numbers

**Prohibited Pattern:**
```javascript
// Bad
if (retryCount > 3) { ... }
setTimeout(() => {}, 5000);
if (users.length > 100) { ... }
```

**Fix:**
```javascript
// Good
const MAX_RETRIES = 3;
const TIMEOUT_MS = 5000;
const MAX_USERS = 100;
```

### 3.2 Duplicate Strings

**Detection Criteria:**
- Same string used 3+ times
- String length 5+ characters

**Exceptions:**
- Empty string `""`
- Single character `" "`, `","` etc.
- Logging messages (but error codes should be constants)

### 3.3 Duplicate Config Values

**Detection Pattern:**
```javascript
// Duplicate config
const timeout1 = 30000;
const timeout2 = 30000;
const requestTimeout = 30000;
```

**Fix:**
```javascript
// Single config
const CONFIG = {
  TIMEOUT_MS: 30000
};
```

---

## 4. Duplication Thresholds

### Detection Thresholds

| Type | Threshold | Reporting Condition |
|------|-----------|---------------------|
| Type-1 Clone | 5 lines | Always report |
| Type-2 Clone | 90% similarity | Always report |
| Type-3 Clone | 70% similarity | 10+ lines only |
| Role duplication | 3 same methods | Always report |
| Magic numbers | 2+ usages | Always report |
| Duplicate strings | 3+ usages | Always report |

### Severity Criteria

| Severity | Definition | Action Deadline |
|----------|------------|-----------------|
| CRITICAL | Immediate fix required | Current task |
| HIGH | Quick fix recommended | This sprint |
| MEDIUM | Planning required | Next sprint |
| LOW | Awareness only | When time permits |

---

## 5. Exceptions

### Allowed Duplication

| Situation | Reason |
|-----------|--------|
| Test code | Maintain test independence |
| Generated code | Auto-generation tool responsibility |
| External interface implementation | Contract compliance required |
| Performance optimization code | Intentional inlining |

### Not Considered Duplication

- Code 2 lines or less
- Idiomatic patterns (e.g., `if (err) return;`)
- Language boilerplate

---

## 6. Fix Patterns

### Clone Code Consolidation

```
1. Identify common parts
2. Parameterize differences
3. Extract common function/method
4. Replace originals with calls
5. Run tests
```

### Role Duplication Consolidation

```
1. Analyze responsibilities of both classes
2. Determine consolidation target (by reference count)
3. Merge methods
4. Migrate references
5. Remove deletion target
```

### Constantization

```
1. Identify duplicate values
2. Assign meaningful names
3. Add constant definitions
4. Replace usages
5. Code review
```

---

## 7. Metrics

### Code Duplication Rate

```
Duplication Rate = (Duplicate Lines / Total Lines) × 100%

Target: < 5%
Warning: 5% ~ 10%
Danger: > 10%
```

### DRY Score

```
DRY Score = 100 - Duplication Rate

Excellent: > 95
Good: 90 ~ 95
Needs Improvement: < 90
```
