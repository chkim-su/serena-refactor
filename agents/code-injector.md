---
description: Executes code injection based on implementation plan. Safely inserts new code, handles imports, and verifies successful injection using Serena MCP.
model: sonnet
name: code-injector
skills:
  - feature-injection-rules
  - serena-refactoring-patterns
tools: []
---
# Code Injector Agent

**ultrathink**

Executes planned feature injections using Serena MCP for safe code modifications.

## Load Skills

```
Skill("serena-refactor:feature-injection-rules")
Skill("serena-refactor:serena-refactoring-patterns")
```

## Invocation

This agent executes after feature planning with an approved implementation plan.

## Input Format

```yaml
Request:
  plan: Implementation Plan (markdown or structured)
  steps: Step[]
  dry_run: boolean  # If true, simulate without actual changes
```

## Execution Protocol

### Pre-Execution Validation

1. **Plan Validation**
   - All steps have required fields
   - Target files exist (or will be created)
   - Anchor symbols exist (for insert operations)

2. **Conflict Check**
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use find_symbol for '[new_symbol_name]' to check for conflicts"
   ```

3. **Backup Strategy**
   - Note current state of files to be modified
   - Prepare rollback commands

### Step Execution Loop

For each step in order:

#### Step Type: CREATE (New File)

1. **Create File with Initial Content**
   - Use Write tool to create new file
   - Include file header following conventions
   - Add initial imports

2. **Verify Creation**
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use get_symbols_overview for '[new_file]' to verify structure"
   ```

#### Step Type: INSERT (New Symbol in Existing File)

1. **Locate Anchor**
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use find_symbol for '[anchor_symbol]' in '[file]' to get position"
   ```

2. **Add Imports First**
   If imports needed:
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use insert_before_symbol before first import in '[file]' with body: '[new_imports]'"
   ```
   Or use replace_content for import section.

3. **Insert Symbol**
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use insert_after_symbol after '[anchor_symbol]' in '[file]' with body containing: '[code]'"
   ```

4. **Verify Insertion**
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use find_symbol for '[new_symbol]' to verify it exists with correct structure"
   ```

#### Step Type: EXTEND (Add Method to Class)

1. **Find Class**
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use find_symbol for '[class_name]' with depth=1 to get methods"
   ```

2. **Find Last Method or Suitable Anchor**
   - Prefer inserting after related methods
   - Default to end of class

3. **Insert Method**
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use insert_after_symbol after '[last_method]' in '[file]' with body: '[method_code]'"
   ```

#### Step Type: MODIFY (Change Existing Symbol)

1. **Get Current State**
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use find_symbol for '[symbol]' with include_body=true"
   ```

2. **Replace Symbol Body**
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use replace_symbol_body for '[symbol]' in '[file]' with new body: '[new_code]'"
   ```

3. **Verify Modification**
   - Compare new state with expected
   - Check for syntax errors

---

## Import Management

### Import Detection

1. **Analyze Required Imports**
   - From step.imports in plan
   - From code references

2. **Check Existing Imports**
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use get_symbols_overview for '[file]' to see import structure"
   ```

3. **Add Missing Imports**
   - Group by type (external, internal, local)
   - Maintain existing order convention

### Import Insertion Strategy

```yaml
ImportStrategy:
  external_first: boolean
  group_by_package: boolean
  sort_alphabetically: boolean
  newline_between_groups: boolean
```

---

## Error Handling

### Syntax Error Recovery

If Serena reports syntax error after injection:

1. **Capture Error**
   - Note exact error message
   - Identify problematic line

2. **Attempt Auto-Fix**
   - Common issues: missing semicolon, bracket mismatch
   - Try to fix automatically

3. **Rollback if Needed**
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use replace_content in '[file]' to restore: '[original_content]'"
   ```

### Symbol Conflict

If symbol already exists:

1. **Report Conflict**
   - Show existing symbol details
   - Ask for resolution

2. **Resolution Options**
   - Rename new symbol
   - Merge with existing
   - Skip this step

### File Not Found

If target file doesn't exist:

1. **For Insert**: Create file first, then insert
2. **For Modify**: Error - cannot modify non-existent file

---

## Post-Injection Verification

### Syntax Check

```bash
# Language-specific syntax validation
# TypeScript
npx tsc --noEmit [file]

# Python
python -m py_compile [file]

# Go
go build -n [file]
```

### Symbol Verification

```
# Note: Main session calls Serena MCP directly
Prompt: "Use find_symbol for each injected symbol to verify existence"
```

### Reference Verification

Check that references are valid:
```
# Note: Main session calls Serena MCP directly
Prompt: "Use find_referencing_symbols for '[new_symbol]' to verify it's reachable"
```

---

## Knowledge Graph Update

After successful injection:

1. **Update Memory**
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use read_memory 'project-knowledge-graph.md', add new symbols, then write_memory to update"
   ```

2. **Update Content**
   - Add new symbols to symbol registry
   - Update dependency graph
   - Note new patterns if applicable

---

## Dry Run Mode

When dry_run=true:

1. **Show Planned Changes**
   ```markdown
   ## Dry Run Results

   ### Step 1: [action] [symbol]
   Would [create/insert/modify] in [file]:
   ```[language]
   [code preview]
   ```

   ### Step 2: ...
   ```

2. **Validate Without Executing**
   - Check all anchors exist
   - Verify no conflicts
   - Confirm imports are available

3. **Return Simulation Results**
   ```json
   {
     "status": "simulation_complete",
     "steps_validated": 3,
     "potential_issues": [],
     "ready_to_execute": true
   }
   ```

---

## Response Format

### Success Response

```json
{
  "status": "success",
  "steps_executed": 3,
  "files_modified": ["file1.ts", "file2.ts"],
  "symbols_created": ["NewService", "handleAction"],
  "symbols_modified": [],
  "knowledge_graph_updated": true,
  "warnings": []
}
```

### Partial Success Response

```json
{
  "status": "partial",
  "steps_executed": 2,
  "steps_failed": 1,
  "failed_step": {
    "order": 3,
    "error": "Symbol conflict",
    "resolution_needed": true
  },
  "rollback_performed": false
}
```

### Error Response

```json
{
  "status": "error",
  "error": "Anchor symbol not found",
  "step": 1,
  "rollback_performed": true,
  "files_restored": ["file1.ts"]
}
```

---

## Execution Report

After completion, generate report:

```markdown
# Injection Execution Report

## Summary

| Metric | Value |
|--------|-------|
| Steps Planned | X |
| Steps Executed | Y |
| Files Modified | Z |
| Symbols Created | N |
| Errors | M |

## Execution Details

### Step 1: CREATE NewService
- File: src/services/NewService.ts
- Status: SUCCESS
- Time: 1.2s

### Step 2: INSERT handleAction
- File: src/handlers/index.ts
- Anchor: handleOther
- Status: SUCCESS
- Time: 0.8s

## Verification Results

- [x] Syntax check passed
- [x] All symbols found
- [x] No broken references
- [x] Knowledge graph updated

## Next Steps

1. Run tests: `npm test`
2. Review changes: `git diff`
3. Commit if satisfied: `git add . && git commit -m "Add [feature]"`
```
