# LLM Query Templates

Templates for consulting external LLMs (Gemini, Codex) via u-llm-sdk.

## Critical Rule

**External LLMs cannot access the current project.**

Every query MUST be self-contained with:
- Complete project context
- Full code snippets (no abbreviations)
- All relevant constraints
- Specific, answerable questions

---

## Template 1: Approach Collection

Use during Phases 2-3 when gathering implementation ideas.

```markdown
## Project Context
- **Language/Framework**: [e.g., TypeScript 5.3, Next.js 14.1]
- **Runtime**: [e.g., Node.js 20, Edge Runtime, Browser]
- **Key Dependencies**:
  - [dep1@version] - [purpose]
  - [dep2@version] - [purpose]
  - [dep3@version] - [purpose]
- **Architecture**: [e.g., App Router with Server Actions, Microservices]
- **Scale**: [e.g., 10k concurrent users, 1M daily requests]

## Problem Description
[Detailed problem description with specific requirements]

[Include any relevant background information]

## Constraints
### Hard Constraints (Cannot Violate)
1. [Constraint 1]
2. [Constraint 2]

### Soft Constraints (Preferred)
1. [Preference 1]
2. [Preference 2]

## What We've Already Considered
1. **[Approach 1]**
   - Pros: [pros]
   - Cons: [cons]
   - Why it might not work: [reason]

2. **[Approach 2]**
   - Pros: [pros]
   - Cons: [cons]
   - Why it might not work: [reason]

## Specific Questions
1. What approaches would you recommend for [specific aspect]?
2. Are there any patterns or libraries we might have missed?
3. What edge cases should we consider?
4. Are there any risks we haven't identified?
```

---

## Template 2: Failure Analysis

Use during Phase 6 when an experiment fails verification.

```markdown
## Project Context
- **Language/Framework**: [e.g., TypeScript 5.3, Express.js 4.18]
- **Runtime**: [e.g., Node.js 20.10.0]
- **Key Dependencies**:
  - [dep1@version]
  - [dep2@version]
- **Environment**: [e.g., Ubuntu 22.04, Docker, AWS Lambda]

## What We Tried

### Hypothesis
**Name**: [Hypothesis name]
**Approach**: [Description of the approach]
**Goal**: [What we were trying to achieve]

### Implementation
```[language]
// FULL implementation code - no abbreviations
// Include all relevant files

[Complete code that was tested]
```

### Expected Behavior
[What should have happened]

### Actual Behavior
[What actually happened]

## Failure Details

### Test Output
```
[Complete test output including all assertions]
```

### Error Message
```
[Exact error message if any]
```

### Stack Trace
```
[Full stack trace if available]
```

### Logs
```
[Relevant log entries]
```

## Environment Details
- Node version: [exact version]
- npm/yarn version: [version]
- OS: [name and version]
- Relevant env vars: [list any that might matter]

## Debugging We've Done
- [x] [Check 1] - Result: [OK/Issue found]
- [x] [Check 2] - Result: [OK/Issue found]
- [ ] [Check 3] - Not yet verified

## Specific Questions
1. Why might this approach have failed?
2. Is there a fix, or should we try a different approach?
3. What edge cases might we have missed?
4. Are there any subtle bugs in the implementation?
```

---

## Template 3: Architecture Decision

Use when choosing between multiple valid approaches.

```markdown
## Project Context
- **Language/Framework**: [details]
- **Current Architecture**: [description]
- **Team Size**: [number]
- **Timeline**: [constraints]

## Decision Context
[What decision needs to be made and why]

## Options Under Consideration

### Option A: [Name]
**Description**: [How it works]
**Pros**:
- [Pro 1]
- [Pro 2]
**Cons**:
- [Con 1]
- [Con 2]
**Effort**: [Low/Medium/High]

### Option B: [Name]
**Description**: [How it works]
**Pros**:
- [Pro 1]
- [Pro 2]
**Cons**:
- [Con 1]
- [Con 2]
**Effort**: [Low/Medium/High]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Questions
1. Which option would you recommend and why?
2. Are there options we haven't considered?
3. What are the long-term implications of each?
```

---

## Template 4: Edge Case Exploration

Use when looking for edge cases to test.

```markdown
## Implementation Overview
```[language]
// Core implementation to analyze for edge cases
[Complete relevant code]
```

## Function Signature
- **Input**: [types and expected ranges]
- **Output**: [types and expected values]
- **Side Effects**: [any side effects]

## Known Edge Cases Already Handled
- [x] [Edge case 1]
- [x] [Edge case 2]

## Questions
1. What edge cases might we have missed?
2. What boundary conditions should we test?
3. What failure modes should we handle?
4. Are there any concurrency issues to consider?
```

---

## Template 5: Performance Optimization

Use when seeking performance improvements.

```markdown
## Current Implementation
```[language]
// Performance-critical code
[Complete code with any metrics annotations]
```

## Performance Metrics
- Current: [e.g., 500ms average response time]
- Target: [e.g., 100ms average response time]
- Bottleneck: [identified bottleneck if known]

## Constraints
- Memory limit: [limit]
- CPU limit: [limit]
- Cannot change: [fixed requirements]

## Environment
- [Runtime details]
- [Infrastructure details]

## Questions
1. What optimizations would you suggest?
2. Are there algorithmic improvements possible?
3. What caching strategies might help?
4. Are there any quick wins we might be missing?
```

---

## Usage Examples

### Gemini Query (Broad Knowledge)

```bash
gemini "
## Project Context
- Language: TypeScript 5.3
- Framework: Next.js 14.1 (App Router)
- Database: PostgreSQL with Prisma

## Problem
Need to implement real-time collaborative editing like Google Docs.

## Constraints
1. Must work with existing PostgreSQL database
2. Must support 50+ concurrent editors
3. Must handle offline mode

## Questions
1. What patterns work best for this (OT vs CRDT)?
2. What libraries should we evaluate?
3. What are the main architectural considerations?
"
```

### Codex Query (Code Analysis)

```bash
codex "
## Code
\`\`\`typescript
async function processQueue(items: Item[]): Promise<Result[]> {
  const results: Result[] = [];
  for (const item of items) {
    const result = await processItem(item);
    results.push(result);
  }
  return results;
}
\`\`\`

## Issue
Processing 1000 items takes 60 seconds (60ms each).
Need to reduce to under 10 seconds.

## Constraints
- processItem makes network call
- Order doesn't matter
- Memory: 512MB limit

## Question
How can I parallelize this safely?
"
```

---

## Response Handling

### What to Extract

From each LLM response, extract:

1. **Key Points**: Main insights
2. **Suggested Approaches**: Specific recommendations
3. **Code Suggestions**: Any code provided
4. **Warnings**: Caveats or risks mentioned
5. **Follow-up Questions**: What to ask next

### Synthesis

When consulting multiple LLMs:

```markdown
## Consensus
[Points where both agree]

## Divergence
| Topic | Gemini | Codex |
|-------|--------|-------|
| [X] | [view] | [view] |

## Recommendation
[Combined best approach based on both]
```
