---
description: Serena MCP-based SOLID analysis. Symbol-level analysis for accurate violation detection and auto-fix paths.
skills:
  - solid-design-rules
  - serena-refactoring-patterns
allowed-tools:
  - AskUserQuestion
  - TodoWrite
---

# Analyze Command

Symbol-level SOLID analysis using Serena MCP.

## Usage

```
/serena-refactor:analyze [target]
```

## Important: MCP Tool Access

**MCP tools are only accessible in the main session.** This command executes MCP calls directly, then delegates analysis logic to the agent.

---

## Workflow

### Step 0: MCP Server Discovery (MANDATORY)

**Before any analysis, discover the Serena MCP server name:**

The Serena MCP server may be registered under different names (e.g., `serena`, `serena-daemon`).

1. **Check available MCP servers** by looking at the system prompt or using available MCP tools
2. **Identify the Serena server** - look for names containing "serena"
3. **Use the discovered name** for all subsequent MCP calls

Common server names:
- `serena-daemon` (most common)
- `serena`
- `plugin:serena:serena`

**If Serena MCP is NOT available:**
- Inform the user: "Serena MCP server not found. Please ensure it's configured in ~/.claude/mcp_servers.json"
- DO NOT fall back to generic tools (Bash/Search/Read) - this defeats the purpose
- Guide user to run the setup or restart Claude Code

### Step 1: Target Selection

If no target provided:
```yaml
AskUserQuestion:
  question: "What would you like to analyze?"
  header: "Analysis Target"
  options:
    - label: "Current directory"
      description: "Analyze entire project"
    - label: "Specific path"
      description: "Specify directory or file"
```

### Step 2: Gather Data (Main Session MCP Calls)

**Execute these MCP calls directly in the main session.**

> Note: Replace `{SERENA_SERVER}` with the actual server name discovered in Step 0 (e.g., `serena-daemon`)

1. **List directory structure:**
```
mcp__{SERENA_SERVER}__list_dir:
  relative_path: [target or "."]
  recursive: false
```

2. **For each source file, get symbols:**
```
mcp__{SERENA_SERVER}__get_symbols_overview:
  relative_path: [file path]
  depth: 1
```

3. **Search for SOLID violation patterns:**
```
mcp__{SERENA_SERVER}__search_for_pattern:
  substring_pattern: "switch\\s*\\(|if\\s*\\(.*instanceof"
  restrict_search_to_code_files: true
```

4. **For suspicious symbols, get body:**
```
mcp__{SERENA_SERVER}__find_symbol:
  name_path_pattern: [symbol name]
  relative_path: [file path]
  include_body: true
```

5. **Analyze references for impact scope:**
```
mcp__{SERENA_SERVER}__find_referencing_symbols:
  name_path: [symbol name]
  relative_path: [file path]
```

### Step 3: Delegate Analysis

Pass gathered data to analysis agent:

```yaml
Task:
  agent: "serena-solid-analyzer"
  prompt: |
    Analyze the following code data for SOLID principle violations.

    ## Project Structure
    [paste list_dir results]

    ## Symbols Overview
    [paste get_symbols_overview results for each file]

    ## Pattern Search Results
    [paste search_for_pattern results]

    ## Symbol Bodies (for suspicious items)
    [paste find_symbol results with bodies]

    ## Reference Analysis
    [paste find_referencing_symbols results]

    Provide a comprehensive SOLID analysis report with:
    1. Violation summary table
    2. Detailed violations with file:line references
    3. Impact scope for each violation
    4. Prioritized fix recommendations
```

### Step 4: Output Results

```markdown
## Analysis Report: [target]

### Quick Summary
| Principle | Status | Violations | Impact Scope |
|-----------|--------|------------|--------------|
| SRP | OK/WARN/FAIL | X | Y files |
| OCP | OK/WARN/FAIL | X | Y files |
| LSP | OK/WARN/FAIL | X | Y files |
| ISP | OK/WARN/FAIL | X | Y files |
| DIP | OK/WARN/FAIL | X | Y files |

### Key Issues (Priority Order)
1. **[CRITICAL]** [file:line] - [issue] → Serena fix: [tool name]
2. ...

### Recommendations
- Run `/serena-refactor:refactor` for auto-fix
- Run `/serena-refactor:plan` for step-by-step planning
```

---

## Architecture Note

```
┌─────────────────────────────────────────────────────────┐
│                    Main Session                         │
│  ┌─────────────┐     ┌─────────────────────────────┐   │
│  │ Step 0:     │────▶│ Discover Serena MCP server  │   │
│  │ Discovery   │     │ (serena-daemon, serena, etc)│   │
│  └─────────────┘     └──────────────┬──────────────┘   │
│                                      │                  │
│  ┌─────────────┐     ┌──────────────▼──────────────┐   │
│  │ MCP Tools   │────▶│ mcp__{SERENA}__* calls      │   │
│  │ (accessible)│     │ (gather code data)          │   │
│  └─────────────┘     └──────────────┬──────────────┘   │
│                                      │                  │
│                                      ▼                  │
│                      ┌──────────────────────────────┐   │
│                      │ Task: serena-solid-analyzer  │   │
│                      │ (receives data, not tools)   │   │
│                      │ - Analyzes symbols           │   │
│                      │ - Detects SOLID violations   │   │
│                      │ - Provides recommendations   │   │
│                      └──────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## CRITICAL: Do NOT Fall Back to Generic Tools

If Serena MCP is unavailable or fails:
- DO NOT use Bash, Search, Read, Grep, or Glob as alternatives
- These generic tools cannot provide symbol-level analysis
- Inform user and guide them to configure Serena MCP properly

The serena-mcp-guard hook will warn if generic tools are used without MCP.
