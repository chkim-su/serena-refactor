#!/bin/bash
# Serena MCP Auto-Configuration Script
# This script is called by SessionStart hook to ensure Serena MCP is configured

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  🔧 Serena Refactor Plugin - MCP Configuration Check"
echo "════════════════════════════════════════════════════════════"
echo ""

# Check if uvx is available
if ! command -v uvx &> /dev/null; then
  echo "  ⚠️  uvx not installed - Serena MCP requires uv"
  echo ""
  echo "  Install uv first:"
  echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
  echo ""
  echo "════════════════════════════════════════════════════════════"
  exit 0
fi

# Check if Serena MCP is already registered using claude mcp list
if claude mcp list 2>/dev/null | grep -q "^serena:"; then
  echo "  ✓ Serena MCP already configured"
  echo "════════════════════════════════════════════════════════════"
  exit 0
fi

# Register Serena MCP server using claude mcp add
echo "  ⚙️  Registering Serena MCP server..."

if claude mcp add --transport stdio --scope user serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --project-from-cwd 2>&1; then
  echo ""
  echo "  ✅ Serena MCP registered!"
  echo ""
  echo "  ⚠️  RESTART REQUIRED"
  echo "  → Restart Claude Code for changes to take effect"
  echo "  → Run: claude (or restart your IDE)"
  echo ""
else
  echo "  ❌ Failed to register Serena MCP"
  echo "  → Try manual registration:"
  echo "  claude mcp add --transport stdio --scope user serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --project-from-cwd"
fi

echo "════════════════════════════════════════════════════════════"
