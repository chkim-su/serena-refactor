---
description: Project knowledge extraction and graph structure rules. Defines how to analyze, document, and maintain project architecture knowledge using Serena MCP.
name: project-knowledge-graph
allowed-tools: ["Read", "Grep", "Glob", "Task"]
---
# Project Knowledge Graph

## Purpose

Define rules and patterns for extracting, structuring, and maintaining comprehensive project knowledge using Serena MCP's symbol-level analysis capabilities.

---

## Knowledge Graph Structure

### Core Entities

| Entity Type | Description | Serena Tool |
|-------------|-------------|-------------|
| `Module` | File or directory that groups related code | `list_dir`, `get_symbols_overview` |
| `Symbol` | Class, function, method, variable | `find_symbol` |
| `Dependency` | Import or reference relationship | `find_referencing_symbols` |
| `Pattern` | Repeated design pattern or convention | Pattern analysis |
| `Convention` | Naming, structure, or style rules | Convention extraction |

### Graph Schema

```yaml
KnowledgeGraph:
  project:
    name: string
    root_path: string
    language: string[]

  modules:
    - path: string
      type: "file" | "directory"
      symbols: Symbol[]
      dependencies: Dependency[]

  symbols:
    - name: string
      type: "class" | "function" | "method" | "variable" | "interface"
      file: string
      line: number
      visibility: "public" | "private" | "protected"
      dependencies: string[]
      dependents: string[]

  patterns:
    - name: string
      type: "structural" | "behavioral" | "creational"
      instances: SymbolRef[]

  conventions:
    - category: "naming" | "structure" | "import" | "export"
      rule: string
      examples: string[]
```

---

## Extraction Rules

### Phase 1: Structure Discovery

1. **Directory Scan**
   ```
   Serena: list_dir with recursive=true
   Output: File tree with types
   ```

2. **Entry Points Identification**
   - Look for: `main`, `index`, `app`, `__init__`
   - Configuration files: `*.config.*`, `*.json`, `*.yaml`

### Phase 2: Symbol Extraction

1. **Per-File Symbol Overview**
   ```
   Serena: get_symbols_overview for each file
   Extract: Classes, functions, methods, variables
   ```

2. **Symbol Details**
   ```
   Serena: find_symbol with include_body=true
   Extract: Full definition, parameters, return types
   ```

### Phase 3: Dependency Mapping

1. **Outgoing Dependencies**
   - Import statements analysis
   - Reference tracking within symbols

2. **Incoming Dependencies (Dependents)**
   ```
   Serena: find_referencing_symbols for key symbols
   Map: Which symbols depend on this one
   ```

### Phase 4: Pattern Recognition

| Pattern | Detection Method |
|---------|-----------------|
| Factory | Classes ending with `Factory`, methods named `create*` |
| Repository | Classes ending with `Repository`, implementing CRUD |
| Service | Classes ending with `Service`, with business logic |
| Controller | Classes ending with `Controller`, handling requests |
| Strategy | Interface + multiple implementations |
| Observer | `subscribe`, `notify`, `emit` patterns |

### Phase 5: Convention Extraction

1. **Naming Conventions**
   - Class naming: PascalCase, camelCase
   - Function naming: verb prefixes (get, set, is, has)
   - File naming: kebab-case, snake_case

2. **Structure Conventions**
   - Directory organization patterns
   - Import grouping rules
   - Export patterns

---

## Memory Storage

### Using Serena Memory for Persistence

Store extracted knowledge in Serena memories for future sessions:

```
Serena: write_memory
Key: "project-knowledge-graph.md"
Content: Serialized knowledge graph
```

### Memory Structure

```markdown
# Project Knowledge Graph
Generated: [timestamp]

## Project Overview
- Name: [project_name]
- Languages: [languages]
- Entry Points: [entry_points]

## Module Map
[Hierarchical module structure]

## Key Symbols
[Top-level classes and functions with roles]

## Dependency Graph
[Mermaid diagram or text representation]

## Detected Patterns
[Pattern instances with locations]

## Conventions
[Extracted naming and structure rules]
```

---

## Query Interface

### Common Queries

| Query | Implementation |
|-------|---------------|
| "Find all services" | `search_for_pattern: "class.*Service"` |
| "Show dependencies of X" | `find_referencing_symbols + find_symbol` |
| "List all entry points" | Search for main/index patterns |
| "Get module structure" | `list_dir + get_symbols_overview` |

### Query Response Format

```yaml
QueryResult:
  query: string
  matches:
    - symbol: string
      file: string
      line: number
      relevance: number
      context: string
```

---

## Update Strategy

### Incremental Updates

When files change, update only affected portions:

1. Detect changed files (git diff or file watcher)
2. Re-extract symbols for changed files
3. Update dependency edges
4. Revalidate patterns

### Full Refresh Triggers

- Major refactoring
- New module addition
- Framework upgrade
- User request

---

## Integration with Feature Injection

The knowledge graph enables intelligent feature injection by providing:

1. **Insertion Points**: Know where to add new code based on patterns
2. **Style Matching**: Follow existing conventions automatically
3. **Dependency Awareness**: Understand import requirements
4. **Impact Analysis**: Predict what will be affected by changes
