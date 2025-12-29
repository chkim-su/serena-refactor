# Changelog

All notable changes to the Serena Refactor Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.4.0] - 2025-12-29

### Removed
- **Legacy Gateway code**: Removed `scripts/serena_gateway.py` and related infrastructure
- **Gateway documentation**: Deprecated `docs/mcp-isolation-solution.md`
- **Python cache**: Cleaned up `scripts/__pycache__`

### Changed
- **marketplace.json**: Updated descriptions to reflect direct daemon integration architecture
  - Removed "context-isolated Serena Gateway" references
  - Added "data-driven agent architecture" description
- **README.md**: Complete rewrite with v2.4.0 architecture
  - Added data-driven agent pattern explanation
  - Added Serena daemon integration details
  - Added comprehensive workflow documentation
  - Added hook system documentation
  - Added changelog section

### Improved
- **Documentation accuracy**: All documentation now accurately reflects the current architecture
- **Code clarity**: Removed confusing legacy code that was no longer in use

## [2.3.0] - 2025-12-28

### Changed
- **Architecture**: Transitioned from SDK-based Gateway to direct MCP integration
  - Agents no longer call MCP tools directly
  - Main session collects data via MCP, then passes to agents
  - Agents focus purely on analysis logic (data-driven pattern)

### Added
- **Hook system enhancements**: Expanded workflow enforcement hooks
  - PreToolUse hooks for all major agents
  - PostToolUse hooks for state management
  - Stop hook for session cleanup warnings

### Removed
- **Gateway Agent**: Removed intermediate gateway agent
- **Isolated sessions**: No longer using separate Claude SDK sessions

### Improved
- **Performance**: Direct daemon integration for faster response times
- **Simplicity**: Cleaner architecture without gateway complexity
- **Debugging**: Easier to debug with direct tool calls

## [2.2.x] - 2025-12-26

### Added
- **SDK-based Gateway**: Implemented `serena_gateway.py` for context isolation
  - Used `claude-only-sdk` to spawn isolated sessions
  - Serena MCP only loaded in gateway sessions
  - Main session saved ~22k tokens of context

### Added
- **MCP isolation documentation**: Created `docs/mcp-isolation-solution.md`
  - Documented context overhead problem
  - Explained SDK-based isolation solution
  - Provided verification steps

### Experimental
- Context isolation via separate SDK sessions
- Trade-off: Complexity vs. context efficiency

## Architecture Evolution

### v2.4.0 (Current)
```
Main Session → Serena MCP daemon (direct)
              ↓
           Data → Agents (analysis only)
```

**Trade-offs**:
- ✅ Simple, fast, easy to debug
- ⚠️ Serena tools always loaded (~22k tokens)

### v2.2.x (Deprecated)
```
Main Session → Gateway Agent → SDK Session → Serena MCP
```

**Trade-offs**:
- ✅ Context isolation (saved 22k tokens)
- ❌ Complex, slow, hard to debug

## Design Decisions

### Why Remove Gateway? (v2.3.0 → v2.4.0)

**Performance over Context**:
- Gateway added significant latency (separate session startup)
- Debugging was difficult (multiple session layers)
- Code complexity hindered maintenance

**Data-Driven Pattern**:
- Agents don't need tools if they only analyze data
- Main session MCP calls are fast (daemon caching)
- Context "overhead" acceptable for single-project workflows

**Future Considerations**:
- If Claude Code adds native on-demand MCP loading, reconsider
- For multi-project workflows, daemon's `activate_project` handles switching
- Context efficiency can be improved at Claude Code level, not plugin level

## Contributors

- chanhokim - Initial implementation and architecture evolution

## License

MIT
