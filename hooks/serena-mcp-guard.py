#!/usr/bin/env python3
"""
Serena MCP Usage Enforcement Hook

Detects when generic tools (Bash/Search/Read) are used during /serena-refactor:*
commands WITHOUT prior successful MCP usage, and enforces progressive warnings.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict

STATE_DIR = Path("/tmp/serena-mcp-state")
STATE_DIR.mkdir(exist_ok=True)

# Violation thresholds
FIRST_VIOLATION_WARN = 1   # First generic tool without MCP
ESCALATED_WARN = 2         # Second generic tool without MCP
BLOCK_THRESHOLD = 4        # Fourth+ generic tool without MCP

# Allowed patterns that don't count as violations
ALLOWED_PATTERNS = [
    "listmcpresources",     # MCP connection check
    "listmcpservers",       # Server availability check
    "test",                 # Testing commands
    "echo",                 # Informational output
    "git",                  # Git operations
    "which",                # Environment checks
]


def read_input() -> Dict:
    """Read and parse stdin JSON."""
    try:
        data = sys.stdin.read()
        return json.loads(data) if data.strip() else {}
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        return {}


def get_state_file(session_id: str) -> Path:
    """Get state file path for session."""
    return STATE_DIR / f"{session_id}.json"


def load_state(session_id: str) -> Dict:
    """Load session state."""
    state_file = get_state_file(session_id)
    if not state_file.exists():
        return {
            "session_id": session_id,
            "command": None,
            "mcp_tools_used": [],
            "generic_tools_used": [],
            "violation_count": 0,
            "mcp_available": True,
            "last_warning_at": None,
            "created_at": datetime.now().isoformat()
        }

    try:
        return json.loads(state_file.read_text())
    except json.JSONDecodeError:
        return load_state(session_id)  # Reset on corruption


def save_state(state: Dict) -> None:
    """Save session state."""
    session_id = state["session_id"]
    state_file = get_state_file(session_id)
    state_file.write_text(json.dumps(state, indent=2))


def is_serena_refactor_context(cwd: str) -> bool:
    """Check if we're in a context where serena-refactor enforcement applies."""
    cwd_path = Path(cwd)

    # Check for PLUGIN.md with serena-refactor
    plugin_md = cwd_path / "PLUGIN.md"
    if plugin_md.exists():
        try:
            content = plugin_md.read_text()
            if "serena-refactor" in content.lower():
                return True
        except:
            pass

    # Check for serena-refactor specific directories
    if (cwd_path / "agents").exists() and (cwd_path / "commands").exists():
        return True

    return False


def is_allowed_command(tool_input: Dict) -> bool:
    """Check if command is in allowed patterns."""
    command = str(tool_input.get("command", "")).lower()
    pattern = str(tool_input.get("pattern", "")).lower()

    for allowed in ALLOWED_PATTERNS:
        if allowed in command or allowed in pattern:
            return True

    return False


def format_warning_message(state: Dict, tool_name: str) -> str:
    """Format warning message based on violation count."""
    violation_count = state["violation_count"]
    mcp_tools = state["mcp_tools_used"]

    if violation_count == FIRST_VIOLATION_WARN:
        return f"""
  Serena MCP Tools Reminder

  You're using generic tool '{tool_name}' during a serena-refactor context.
  Consider using specialized Serena MCP tools instead:

  * mcp__serena-daemon__find_symbol - Find code definitions
  * mcp__serena-daemon__search_for_pattern - Search codebase
  * mcp__serena-daemon__get_symbols_overview - Code analysis

  This is an informational warning.
"""

    elif violation_count == ESCALATED_WARN:
        return f"""
  Serena MCP Tools - Escalated Warning

  You've used generic tools {violation_count} times without using Serena MCP.
  MCP tools used so far: {len(mcp_tools)}

  Generic tools are less effective than specialized analysis tools.

  To proceed effectively:
  1. Use 'mcp__serena-daemon__*' tools for code analysis
  2. Or acknowledge you understand the limitation
"""

    else:  # BLOCK_THRESHOLD reached
        return f"""
  Serena MCP Tools - Usage Pattern Violation

  You've used generic tools {violation_count} times with minimal MCP usage.
  This defeats the purpose of the serena-refactor plugin.

  Current MCP tools used: {mcp_tools or 'NONE'}
  Generic tools used: {state['generic_tools_used']}

  Please use mcp__serena-daemon__* tools for analysis.
"""


def check_recent_warning(state: Dict) -> bool:
    """Check if we warned recently (within 60 seconds)."""
    if not state.get("last_warning_at"):
        return False

    try:
        last_warning = datetime.fromisoformat(state["last_warning_at"])
        return datetime.now() - last_warning < timedelta(seconds=60)
    except:
        return False


def main():
    """Main enforcement logic."""
    input_data = read_input()

    session_id = input_data.get("session_id", "unknown")
    cwd = input_data.get("cwd", "")
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Check if we're in a serena-refactor context
    if not is_serena_refactor_context(cwd):
        sys.exit(0)

    # Load state
    state = load_state(session_id)

    # Check allowed patterns
    if is_allowed_command(tool_input):
        sys.exit(0)

    # Track generic tool usage
    if tool_name and tool_name not in state["generic_tools_used"]:
        state["generic_tools_used"].append(tool_name)

    # Calculate violations (generic tools without MCP usage)
    mcp_count = len(state["mcp_tools_used"])

    if mcp_count == 0:
        state["violation_count"] += 1

    # Determine action based on violation count
    violation_count = state["violation_count"]

    if violation_count >= FIRST_VIOLATION_WARN:
        # Show warning (don't block, just inform)
        if not check_recent_warning(state):
            message = format_warning_message(state, tool_name)
            print(message, file=sys.stderr)
            state["last_warning_at"] = datetime.now().isoformat()

    # Save state and allow
    save_state(state)
    sys.exit(0)


if __name__ == "__main__":
    main()
