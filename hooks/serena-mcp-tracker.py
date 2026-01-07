#!/usr/bin/env python3
"""
Track Serena MCP tool usage to update enforcement state.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

STATE_DIR = Path("/tmp/serena-mcp-state")
STATE_DIR.mkdir(exist_ok=True)


def read_input():
    """Read and parse stdin JSON."""
    try:
        data = sys.stdin.read()
        return json.loads(data) if data.strip() else {}
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        return {}


def get_state_file(session_id):
    """Get state file path for session."""
    return STATE_DIR / f"{session_id}.json"


def load_state(session_id):
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
        return load_state(session_id)


def save_state(state):
    """Save session state."""
    session_id = state["session_id"]
    state_file = get_state_file(session_id)
    state_file.write_text(json.dumps(state, indent=2))


def main():
    """Track MCP tool usage."""
    input_data = read_input()

    session_id = input_data.get("session_id", "unknown")
    tool_name = input_data.get("tool_name", "")

    if not tool_name:
        sys.exit(0)

    # Only track serena-daemon MCP tools
    if "serena" not in tool_name.lower():
        sys.exit(0)

    # Load state
    state = load_state(session_id)

    # Track MCP tool usage
    if tool_name not in state["mcp_tools_used"]:
        state["mcp_tools_used"].append(tool_name)
        print(f"  MCP tool tracked: {tool_name}", file=sys.stderr)

    # Reset violation count if MCP is being used
    if state["violation_count"] > 0:
        print(f"  Resetting violation count (was: {state['violation_count']})", file=sys.stderr)
        state["violation_count"] = 0

    save_state(state)
    sys.exit(0)


if __name__ == "__main__":
    main()
