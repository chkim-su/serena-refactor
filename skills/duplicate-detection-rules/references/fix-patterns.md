# Duplication Fix Patterns

## Clone Code Consolidation

```
1. Identify common parts
2. Parameterize differences
3. Extract common function/method
4. Replace originals with calls
5. Run tests
```

## Role Duplication Consolidation

```
1. Analyze responsibilities of both classes
2. Determine consolidation target (by reference count)
3. Merge methods
4. Migrate references
5. Remove deletion target
```

## Constantization

```
1. Identify duplicate values
2. Assign meaningful names
3. Add constant definitions
4. Replace usages
5. Code review
```

---

## Variable/Constant Duplication Examples

### Magic Numbers - Prohibited Pattern

```javascript
// Bad
if (retryCount > 3) { ... }
setTimeout(() => {}, 5000);
if (users.length > 100) { ... }
```

### Magic Numbers - Fixed

```javascript
// Good
const MAX_RETRIES = 3;
const TIMEOUT_MS = 5000;
const MAX_USERS = 100;
```

### Duplicate Config Values

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

## Metrics

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
