# Debug Patterns

## Common Bug Categories

### 1. Null/Undefined Errors

**Symptoms:**
- "Cannot read property X of undefined"
- "TypeError: X is not a function"
- Silent failures with unexpected null values

**Investigation Pattern:**
```yaml
trace:
  - Find where the value is expected to be set
  - Track all code paths that could skip initialization
  - Check async timing issues
  - Verify API response structure matches expectations
```

**Common Fixes:**
- Add null checks / optional chaining
- Provide default values
- Validate at boundaries

---

### 2. Race Conditions

**Symptoms:**
- Inconsistent behavior
- Works locally, fails in production
- Timing-dependent failures

**Investigation Pattern:**
```yaml
trace:
  - Identify all async operations
  - Map shared state access
  - Find missing await/locks
  - Check event ordering assumptions
```

**Common Fixes:**
- Add proper synchronization
- Use atomic operations
- Implement optimistic locking
- Queue concurrent operations

---

### 3. Memory Leaks

**Symptoms:**
- Growing memory usage over time
- Performance degradation
- Out of memory errors

**Investigation Pattern:**
```yaml
trace:
  - Find event listener registrations without cleanup
  - Check for circular references
  - Identify caches without eviction
  - Look for closures capturing large objects
```

**Common Fixes:**
- Remove event listeners on cleanup
- Use WeakMap/WeakRef where appropriate
- Implement cache eviction policies
- Break circular references

---

### 4. State Management Bugs

**Symptoms:**
- UI shows stale data
- Updates not reflecting
- Inconsistent state across components

**Investigation Pattern:**
```yaml
trace:
  - Map all state mutations
  - Check for direct mutations (non-immutable updates)
  - Verify subscription/reactivity setup
  - Find missing state synchronization
```

**Common Fixes:**
- Use immutable update patterns
- Fix subscription logic
- Add state synchronization
- Implement proper change detection

---

### 5. API Integration Issues

**Symptoms:**
- Unexpected response handling
- Missing error states
- Data transformation failures

**Investigation Pattern:**
```yaml
trace:
  - Compare actual vs expected API contract
  - Check error handling for all status codes
  - Verify request/response transformation
  - Look for timeout handling
```

**Common Fixes:**
- Update to match current API contract
- Add comprehensive error handling
- Fix data transformation logic
- Implement retry/timeout logic

---

## Parallel Exploration Strategies

### Strategy 1: Breadth-First Investigation

Launch agents with these focuses:

| Agent | Focus | Starting Point |
|-------|-------|----------------|
| 1 | Execution Path | Entry point where error occurs |
| 2 | Data Flow | Data source to error location |
| 3 | Recent Changes | Git blame on affected files |

---

### Strategy 2: Layer-Based Investigation

For architecture with clear layers:

| Agent | Focus | Layer |
|-------|-------|-------|
| 1 | Presentation | UI components, event handlers |
| 2 | Business Logic | Services, use cases |
| 3 | Data/Infrastructure | Repositories, API clients |

---

### Strategy 3: Symptom-Cause Investigation

| Agent | Focus | Approach |
|-------|-------|----------|
| 1 | Symptom | Where does the error manifest? |
| 2 | Intermediate | What code paths lead there? |
| 3 | Origin | Where does the bad data originate? |

---

## Root Cause Analysis Templates

### 5 Whys Template

```markdown
## Bug: [Brief description]

**Why 1**: [Immediate cause]
→ Because: [Answer]

**Why 2**: [Why that happened]
→ Because: [Answer]

**Why 3**: [Why that happened]
→ Because: [Answer]

**Why 4**: [Why that happened]
→ Because: [Answer]

**Why 5**: [Root cause]
→ Because: [Answer]

**Root Cause**: [Final determination]
**Prevention**: [How to prevent recurrence]
```

### Fault Tree Analysis

```markdown
## Bug: [Brief description]

### Top Event
[The observed failure]

### Intermediate Events
- [Event A] AND/OR [Event B]
  - [Sub-event A1]
  - [Sub-event A2]

### Basic Events (Root Causes)
- [Fundamental cause 1]
- [Fundamental cause 2]

### Most Likely Path
[Top Event] ← [Intermediate] ← [Root Cause]
```

---

## Fix Strategy Templates

### Minimal Fix

```markdown
## Strategy: Minimal Fix

### Goal
Fix the immediate symptom with smallest possible change.

### Change
[Specific code change]

### Pros
- Low risk of regression
- Quick to implement
- Easy to review

### Cons
- May not address root cause
- Technical debt remains
- Could recur in different form

### When to Use
- Production hotfix needed
- Root cause requires larger refactor
- Time pressure
```

### Comprehensive Fix

```markdown
## Strategy: Comprehensive Fix

### Goal
Address root cause and prevent recurrence.

### Changes
1. [Primary fix]
2. [Related improvements]
3. [Preventive measures]

### Pros
- Addresses root cause
- Prevents recurrence
- Improves code quality

### Cons
- Larger change scope
- More testing needed
- Higher regression risk

### When to Use
- Development environment
- Clear root cause identified
- Time available for thorough testing
```

### Defensive Fix

```markdown
## Strategy: Defensive Fix

### Goal
Add guards and validation to fail safely.

### Changes
1. [Input validation]
2. [Error boundaries]
3. [Fallback behaviors]

### Pros
- Handles unknown edge cases
- Fails gracefully
- Better error messages

### Cons
- May hide underlying issues
- Additional code complexity
- Performance overhead possible

### When to Use
- Cause uncertain
- External data involved
- Critical path code
```

---

## Verification Patterns

### Direct Verification

```yaml
steps:
  - Reproduce original bug → Should no longer occur
  - Test with original failing input → Should pass
  - Check error logs → Should be clean
```

### Regression Verification

```yaml
steps:
  - Run existing test suite
  - Test related functionality manually
  - Review code for unintended side effects
  - Check performance metrics
```

### Edge Case Verification

```yaml
steps:
  - Test boundary values
  - Test empty/null inputs
  - Test concurrent access
  - Test error paths
```

---

## Confidence Assessment Guidelines

### High Confidence (80-100%)

- Direct evidence in code
- Reproducible locally
- Clear cause-effect relationship
- Verified with tests

### Medium Confidence (50-79%)

- Indirect evidence
- Partially reproducible
- Plausible explanation
- Some uncertainty remains

### Low Confidence (0-49%)

- Speculation based on patterns
- Cannot reproduce
- Multiple possible causes
- Needs more investigation

---

## Anti-Patterns to Avoid

### 1. Premature Fixing

**Problem:** Fixing symptoms without understanding cause
**Result:** Bug resurfaces in different form
**Prevention:** Complete Phase 1-3 before Phase 5

### 2. Scope Creep

**Problem:** Expanding fix to unrelated improvements
**Result:** Increased risk, delayed delivery
**Prevention:** Separate bug fix from refactoring

### 3. Untested Fixes

**Problem:** Skipping verification phase
**Result:** New bugs introduced
**Prevention:** Always complete Phase 6

### 4. Inadequate Documentation

**Problem:** Not recording root cause and fix
**Result:** Same bug reoccurs, knowledge lost
**Prevention:** Document in commit message and comments

### 5. Over-Engineering

**Problem:** Building elaborate solution for simple bug
**Result:** Unnecessary complexity
**Prevention:** Start with minimal fix, expand if needed
