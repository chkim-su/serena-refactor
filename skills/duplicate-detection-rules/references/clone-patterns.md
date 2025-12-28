# Clone Code Patterns - Detailed Examples

## Type-1: Exact Clone

**Definition:** Exactly identical code excluding whitespace/comments

**Detection Criteria:**
- 5+ consecutive identical lines
- 100% token sequence match

**Severity:** CRITICAL

**Fix Strategy:**
- Extract to common function
- Separate into utility module

---

## Type-2: Parameterized Clone

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

---

## Type-3: Similar Structure Clone

**Definition:** Similar code with some lines added/deleted/modified

**Detection Criteria:**
- Structural similarity > 70%
- Same core logic pattern

**Severity:** MEDIUM

**Fix Strategy:**
- Convert to strategy pattern
- Apply template method pattern
