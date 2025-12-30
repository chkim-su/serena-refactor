# Laboratory Patterns Skill

Scientific experimentation patterns for exploring implementation approaches.

## Overview

This skill provides patterns and templates for the `/serena-refactor:laboratory` command, which applies scientific methodology to code implementation:

- **Problem Decomposition**: Breaking complex problems into testable units
- **Approach Collection**: Gathering solutions from multiple sources
- **Creative Generation**: Novel approaches beyond documentation
- **Hypothesis Formation**: Structuring testable experiments
- **Parallel Experimentation**: Running multiple PoCs concurrently
- **Rigorous Verification**: Testing with edge cases and reproducibility
- **Learning from Failure**: Recording what doesn't work and why

## Core Philosophy

> "Apply scientific methodology to code implementation"

1. **Decompose** - Break problems into smaller, testable units
2. **Hypothesize** - Form clear, testable hypotheses
3. **Experiment** - Run controlled experiments (PoCs)
4. **Verify** - Test rigorously with edge cases
5. **Learn** - Record successes AND failures

## References

| Reference | Purpose |
|-----------|---------|
| [creative-approaches.md](references/creative-approaches.md) | Patterns for unconventional solutions |
| [query-templates.md](references/query-templates.md) | Templates for LLM consultation |
| [verification-criteria.md](references/verification-criteria.md) | Standards for experiment verification |

## 7-Stage Workflow

```
1. Problem Decomposition  [User Approval]
      ↓
2. Existing Approaches Collection
      ↓
3. Creative Approaches Generation
      ↓
4. Hypothesis Formation  [User Approval]
      ↓
5. PoC Experiments (Parallel, max 5)  [User Approval]
      ↓
6. Verification
      ↓
7. Result Report
```

## Agent Roles

| Agent | Role | Phases |
|-------|------|--------|
| `lab-analyst` | Problem analysis, hypothesis design | 1, 4 |
| `lab-experimenter` | PoC implementation, parallel coordination | 5 |
| `lab-verifier` | Testing, verification, reporting | 6, 7 |
| `source-fetcher` | External info collection | 2 |
| `creative-generator` | Novel approach generation | 3 |
| `llm-consultant` | External LLM consultation | 2-3, 6 |
| `edge-case-hunter` | Edge case discovery | 4, 6 |

## Information Sources (Priority)

1. **GitHub Issues/Discussions** - Real developer solutions
2. **Stack Overflow** - Community-vetted approaches
3. **Official Docs (Context7)** - Standard methods

## Verification Criteria

| Criterion | Required |
|-----------|----------|
| Test Pass | Yes |
| Edge Case Coverage | Yes |
| Reproducibility | Yes |
| Performance | If specified |

## State Files

| File | Phase | Purpose |
|------|-------|---------|
| `.lab-problem-defined` | 1 | Problem decomposed |
| `.lab-approaches-collected` | 2-3 | Approaches gathered |
| `.lab-hypotheses-approved` | 4 | Hypotheses confirmed |
| `.lab-experiments-running` | 5 | In progress |
| `.lab-experiments-done` | 5 | Complete |
| `.lab-verified` | 6 | Verified |
| `.lab-report-generated` | 7 | Report created |

## Output Locations

- **Reports**: `docs/lab-reports/YYYY-MM-DD-{topic}.md`
- **Memory**: `.serena/memories/lab-{topic}.md`
- **Experiments**: `experiments/hypothesis-{id}/`
