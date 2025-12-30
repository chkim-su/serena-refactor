# Verification Criteria Reference

Standards and protocols for rigorously verifying laboratory experiments.

## Core Verification Criteria

| Criterion | Description | Required |
|-----------|-------------|----------|
| **Test Pass** | All tests pass | Yes |
| **Edge Case Coverage** | Boundary conditions handled | Yes |
| **Reproducibility** | Same results on repeat | Yes |
| **Performance** | Meets performance requirements | If specified |
| **Security** | No obvious vulnerabilities | If relevant |

---

## Criterion 1: Test Pass

### Requirements

- All unit tests pass
- All integration tests pass (if applicable)
- No flaky tests
- Tests run in reasonable time

### Verification Protocol

```bash
# Run test suite
npm test

# Check for failures
# All tests must pass (0 failures)

# Check for skipped tests
# Skipped tests should have documented reason
```

### Pass Threshold

| Scenario | Threshold |
|----------|-----------|
| Normal | 100% pass |
| With documented skips | 100% of non-skipped |
| Flaky tests | Must be fixed or documented |

### Output Format

```markdown
### Test Results
| Suite | Passed | Failed | Skipped | Time |
|-------|--------|--------|---------|------|
| Unit | X | 0 | Y | Zms |
| Integration | X | 0 | Y | Zms |

**Overall**: PASS / FAIL
```

---

## Criterion 2: Edge Case Coverage

### Edge Case Categories

| Category | Examples |
|----------|----------|
| **Input Boundaries** | Empty, null, max, min, special chars |
| **State Boundaries** | Uninitialized, transitional, terminal |
| **Timing** | Concurrent, timeout, race conditions |
| **Resources** | Exhausted, unavailable, slow |
| **Data** | Malformed, encoding issues, special values |

### Minimum Coverage Requirements

| Priority | Coverage Required |
|----------|-------------------|
| Critical | 100% |
| High | 90%+ |
| Medium | 80%+ |
| Low | Best effort |

### Edge Case Checklist

```markdown
### Input Edge Cases
- [ ] Empty input
- [ ] Null/undefined input
- [ ] Single element
- [ ] Maximum size
- [ ] Special characters (unicode, control chars)
- [ ] Type mismatches

### State Edge Cases
- [ ] Uninitialized state
- [ ] During initialization
- [ ] After cleanup/disposal
- [ ] Error state

### Timing Edge Cases
- [ ] Concurrent access
- [ ] Timeout conditions
- [ ] Order-dependent operations

### Resource Edge Cases
- [ ] Resource unavailable
- [ ] Rate limited
- [ ] Connection timeout
```

### Output Format

```markdown
### Edge Case Coverage
| Category | Cases | Covered | Coverage |
|----------|-------|---------|----------|
| Input | 10 | 9 | 90% |
| State | 5 | 5 | 100% |
| Timing | 3 | 2 | 67% |

**Critical Edge Cases**: 100% covered
**Overall**: PASS / PARTIAL / FAIL
```

---

## Criterion 3: Reproducibility

### Requirements

- Same input produces same output
- No dependency on external state
- No race conditions
- No timing-dependent behavior

### Verification Protocol

```markdown
### Reproducibility Test

1. **Initial Run**
   - Reset all state
   - Run test suite
   - Record results (hash output if applicable)
   - Record timing

2. **Repeat Run**
   - Do NOT reset state
   - Run test suite again
   - Compare results to Run 1
   - Check for state leakage

3. **Order Independence**
   - Shuffle test order
   - Run again
   - Verify same results

4. **Environment Independence**
   - Run on different machine/container
   - Verify same results
```

### Pass Threshold

| Test | Requirement |
|------|-------------|
| Same results across runs | 100% match |
| Same results with different order | 100% match |
| Same results on different env | Functional match |

### Output Format

```markdown
### Reproducibility Check
| Run | Result Hash | Time | Match |
|-----|-------------|------|-------|
| 1 | abc123 | 100ms | - |
| 2 | abc123 | 102ms | Yes |
| 3 (shuffled) | abc123 | 98ms | Yes |

**Reproducibility**: CONFIRMED / ISSUES FOUND
```

---

## Criterion 4: Performance (When Required)

### When to Verify

- User specified performance requirements
- Performance-sensitive component
- Scalability is important

### Metrics to Check

| Metric | Description |
|--------|-------------|
| Response Time | Time to complete operation |
| Throughput | Operations per second |
| Memory Usage | Peak and average memory |
| CPU Usage | Peak and average CPU |
| Scalability | Performance under load |

### Verification Protocol

```markdown
### Performance Test

1. **Baseline**
   - Measure current performance
   - Record all metrics

2. **Load Test**
   - Gradually increase load
   - Monitor for degradation
   - Find breaking point

3. **Stress Test**
   - Push beyond expected load
   - Check for graceful degradation
```

### Output Format

```markdown
### Performance Results
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Response Time | <100ms | 85ms | PASS |
| Throughput | >1000/s | 1200/s | PASS |
| Memory | <256MB | 180MB | PASS |

**Performance**: MEETS REQUIREMENTS / NEEDS IMPROVEMENT
```

---

## Criterion 5: Security (When Relevant)

### When to Verify

- Handles user input
- Deals with authentication/authorization
- Processes sensitive data
- Network communication

### Security Checklist

```markdown
### Security Verification

#### Input Validation
- [ ] All user input sanitized
- [ ] No SQL injection possible
- [ ] No XSS possible
- [ ] No command injection possible

#### Authentication
- [ ] Tokens properly validated
- [ ] No hardcoded credentials
- [ ] Proper session management

#### Data Protection
- [ ] Sensitive data encrypted
- [ ] No secrets in logs
- [ ] Proper access controls

#### Dependencies
- [ ] No known vulnerabilities
- [ ] Up-to-date packages
```

### Output Format

```markdown
### Security Check
| Category | Items | Passed | Issues |
|----------|-------|--------|--------|
| Input | 5 | 5 | 0 |
| Auth | 3 | 3 | 0 |
| Data | 4 | 3 | 1 |

**Issues Found**:
- [Issue description and severity]

**Security**: PASS / ISSUES FOUND
```

---

## Verification Verdicts

### Final Verdict Scale

| Verdict | Meaning | Criteria |
|---------|---------|----------|
| **PASS** | Fully verified | All required criteria met |
| **CONDITIONAL** | Passes with caveats | Minor issues documented |
| **PARTIAL** | Partially working | Some criteria not met |
| **FAIL** | Does not work | Critical criteria failed |

### Verdict Decision Tree

```
All tests pass?
├── No → FAIL
└── Yes
    └── Edge cases covered?
        ├── No → PARTIAL or FAIL
        └── Yes
            └── Reproducible?
                ├── No → PARTIAL
                └── Yes
                    └── Performance OK (if required)?
                        ├── No → CONDITIONAL
                        └── Yes → PASS
```

---

## Confidence Scoring

Rate overall confidence 0-100:

| Score | Meaning |
|-------|---------|
| 90-100 | Very high confidence, production-ready |
| 80-89 | High confidence, minor improvements possible |
| 70-79 | Moderate confidence, some uncertainty |
| 60-69 | Low confidence, needs more verification |
| <60 | Insufficient verification, do not proceed |

### Confidence Calculation

```
Confidence = (
  Test Pass Weight * Test Score +
  Edge Case Weight * Edge Case Score +
  Reproducibility Weight * Reproducibility Score +
  [Optional] Performance Weight * Performance Score
) / Total Weight

Default Weights:
- Test Pass: 40%
- Edge Cases: 30%
- Reproducibility: 30%
```

---

## Failure Documentation

When verification fails, document:

```markdown
## Verification Failure Report

### Hypothesis
[Name and description]

### What Failed
| Criterion | Expected | Actual | Impact |
|-----------|----------|--------|--------|
| [criterion] | [expected] | [actual] | [severity] |

### Root Cause Analysis
[Why did it fail?]

### Partial Success
[What worked under what conditions?]

### Lessons Learned
[What to avoid in future]

### Recommended Next Steps
1. [Option 1]
2. [Option 2]
```
