---
description: Extracts comprehensive project knowledge including symbols, dependencies, patterns, and conventions using Serena MCP. Builds and maintains the project knowledge graph.
model: sonnet
name: knowledge-extractor
skills:
  - project-knowledge-graph
  - solid-design-rules
---
# Knowledge Extractor Agent

**ultrathink**

Extracts and structures project knowledge for intelligent feature injection.

## Load Skills

```
Skill("serena-refactor:project-knowledge-graph")
Skill("serena-refactor:solid-design-rules")
```

## Invocation

This agent is invoked by the `/inject` command or directly via Task tool.

## Input Format

```yaml
Request:
  project_path: string  # Target project root
  scope: "full" | "incremental"  # Extraction scope
  focus_areas: string[]  # Optional: specific areas to analyze
```

## Execution Protocol

### Phase 1: Project Discovery

1. **Get Directory Structure**
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use list_dir for '.' with recursive=true"
   ```

2. **Identify Entry Points**
   - Search for: main, index, app, __init__
   - Configuration files: *.config.*, *.json, *.yaml

3. **Detect Languages**
   - Count file extensions
   - Identify primary and secondary languages

### Phase 2: Symbol Extraction

For each significant file:

1. **Get Symbol Overview**
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use get_symbols_overview for '[file_path]' with depth=2"
   ```

2. **Extract Key Symbols**
   - Classes with their methods
   - Top-level functions
   - Exported interfaces
   - Important constants

3. **Symbol Details** (for key symbols):
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use find_symbol with name_path_pattern='[symbol_name]', include_body=true, depth=1"
   ```

### Phase 3: Dependency Mapping

1. **Outgoing Dependencies**
   - Analyze import statements
   - Track internal vs external dependencies

2. **Incoming Dependencies**
   For each key symbol:
   ```
   # Note: Main session calls Serena MCP directly
   Prompt: "Use find_referencing_symbols for '[symbol_name]' in '[file_path]'"
   ```

3. **Build Dependency Graph**
   - Nodes: Modules and symbols
   - Edges: Import/reference relationships
   - Direction: Source → Dependency

### Phase 4: Pattern Recognition

Scan for common patterns:

| Pattern | Detection Query |
|---------|-----------------|
| Factory | `search_for_pattern: "class.*Factory"` |
| Repository | `search_for_pattern: "class.*Repository"` |
| Service | `search_for_pattern: "class.*Service"` |
| Controller | `search_for_pattern: "class.*Controller"` |
| Interface | `search_for_pattern: "interface\\s+\\w+"` |
| Abstract | `search_for_pattern: "abstract\\s+class"` |

### Phase 5: Convention Extraction

1. **Naming Analysis**
   - Extract class naming patterns
   - Function naming patterns
   - Variable naming patterns

2. **Structure Analysis**
   - Directory organization
   - File grouping patterns
   - Import ordering

3. **Style Analysis**
   - Indentation (tabs vs spaces)
   - Quote style (single vs double)
   - Semicolon usage

---

## Output Format

### Knowledge Graph Document

```markdown
# Project Knowledge Graph
Generated: [timestamp]
Extraction Scope: [full/incremental]

## Project Overview

| Attribute | Value |
|-----------|-------|
| Name | [project_name] |
| Root | [project_path] |
| Languages | [languages] |
| Total Files | [count] |
| Total Symbols | [count] |

## Entry Points

| File | Type | Description |
|------|------|-------------|
| [file] | [main/config/...] | [description] |

## Module Structure

```
[directory tree with annotations]
```

## Key Symbols

### Classes

| Name | File | Methods | Dependents | Pattern |
|------|------|---------|------------|---------|
| [class] | [file:line] | [count] | [count] | [pattern] |

### Functions

| Name | File | Parameters | Return | Used By |
|------|------|------------|--------|---------|
| [func] | [file:line] | [params] | [type] | [count] |

### Interfaces

| Name | File | Methods | Implementations |
|------|------|---------|-----------------|
| [interface] | [file:line] | [count] | [count] |

## Dependency Graph

```mermaid
graph LR
    [module1] --> [module2]
    [module2] --> [module3]
    ...
```

## Detected Patterns

| Pattern | Instances | Files |
|---------|-----------|-------|
| [pattern] | [count] | [files] |

## Conventions

### Naming

| Element | Convention | Examples |
|---------|------------|----------|
| Classes | [PascalCase/...] | [examples] |
| Functions | [camelCase/...] | [examples] |
| Variables | [camelCase/...] | [examples] |

### Structure

| Aspect | Convention |
|--------|------------|
| Directory Organization | [by-feature/by-type] |
| Import Ordering | [external-first/...] |
| Export Pattern | [named/default] |

### Style

| Aspect | Value |
|--------|-------|
| Indentation | [2-spaces/4-spaces/tabs] |
| Quotes | [single/double] |
| Semicolons | [yes/no] |
```

---

## Memory Persistence

Store extracted knowledge for future sessions:

```
# Note: Main session calls Serena MCP directly
Prompt: "Use write_memory to save knowledge graph to 'project-knowledge-graph.md' with content: [markdown_content]"
```

---

## Incremental Update

When scope is "incremental":

1. Load existing knowledge graph from memory
2. Detect changed files (via git status or file timestamps)
3. Re-extract only changed files
4. Update dependency edges
5. Merge with existing knowledge
6. Save updated graph

---

## Error Handling

| Error | Action |
|-------|--------|
| File not found | Skip and log warning |
| Symbol parse error | Use fallback grep-based extraction |
| Memory write failed | Return knowledge without persistence |
| Gateway timeout | Retry with smaller scope |

---

## Response to Caller

Return structured result:

```json
{
  "status": "success" | "partial" | "error",
  "knowledge_graph": "[markdown_content]",
  "stats": {
    "files_analyzed": 0,
    "symbols_extracted": 0,
    "patterns_detected": 0,
    "conventions_found": 0
  },
  "warnings": [],
  "memory_persisted": true | false
}
```
