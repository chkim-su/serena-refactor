# Feature Injection Templates

## Injection Type Templates

### Type 1: New Symbol (Class/Function/Method)

**When to use**: Adding new functionality that doesn't modify existing code

**Process**:
1. Identify appropriate module based on pattern matching
2. Check naming conventions from knowledge graph
3. Verify no naming conflicts with `find_symbol`
4. Use `insert_after_symbol` or `insert_before_symbol`

**Template**:
```yaml
Injection:
  type: new_symbol
  target_file: string
  anchor_symbol: string  # Insert after/before this
  position: "after" | "before"
  content: string
  imports_needed: string[]
```

### Type 2: Extension (Add Method to Existing Class)

**When to use**: Enhancing existing class capabilities

**Process**:
1. Find class with `find_symbol`
2. Analyze existing methods for style consistency
3. Check for method name conflicts
4. Use `insert_after_symbol` targeting last method

**Template**:
```yaml
Injection:
  type: extension
  target_class: string
  method_name: string
  method_body: string
  visibility: "public" | "private" | "protected"
```

### Type 3: Implementation (New Interface Implementation)

**When to use**: Adding new implementation of existing interface

**Process**:
1. Find interface with `find_symbol`
2. List existing implementations for pattern reference
3. Create new class following implementation pattern
4. Register in appropriate factory/container if exists

**Template**:
```yaml
Injection:
  type: implementation
  interface: string
  class_name: string
  file_path: string
  method_implementations:
    - name: string
      body: string
```

### Type 4: Modification (Change Existing Code)

**When to use**: Enhancing or fixing existing functionality

**Process**:
1. Get current symbol body with `find_symbol`
2. Analyze all references with `find_referencing_symbols`
3. Plan backward-compatible change if possible
4. Use `replace_symbol_body`

**Template**:
```yaml
Injection:
  type: modification
  target_symbol: string
  new_body: string
  breaking_change: boolean
  affected_dependents: string[]
```
