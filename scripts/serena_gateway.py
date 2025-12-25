#!/usr/bin/env python3
"""
Serena Gateway - SDK-based MCP Isolation Wrapper

This script runs Serena operations in an isolated Claude session,
keeping the main session's context window clean.
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from claude_only_sdk import ClaudeAdvanced, ClaudeAdvancedConfig
from llm_types import ModelTier, AutoApproval


async def run_serena_task(prompt: str, project_path: str = ".") -> dict:
    """
    Run a Serena task in an isolated Claude session.

    Args:
        prompt: The task prompt for Serena
        project_path: The project path for Serena to analyze

    Returns:
        dict with status, result, and metadata
    """
    # Path to Serena-only MCP config
    mcp_config_path = str(PROJECT_ROOT / "config" / "serena.mcp.json")

    # Verify MCP config exists
    if not os.path.exists(mcp_config_path):
        return {
            "status": "error",
            "error": f"MCP config not found: {mcp_config_path}"
        }

    config = ClaudeAdvancedConfig(
        tier=ModelTier.HIGH,  # Use Sonnet for efficiency
        auto_approval=AutoApproval.FULL,  # Auto-approve for automation
        timeout=300.0,  # 5 minutes timeout
        cwd=project_path,
        mcp_config=mcp_config_path,  # Serena-only MCP!
    )

    # Wrap prompt with Serena context
    full_prompt = f"""You have access to Serena MCP tools for semantic code analysis.

Project path: {project_path}

Task:
{prompt}

Use Serena tools to complete this task. Return results in JSON format:
{{
    "status": "success" | "error",
    "result": "...",
    "affected_files": [...],
    "affected_symbols": [...]
}}
"""

    try:
        async with ClaudeAdvanced(config) as client:
            result = await client.run(full_prompt)

            return {
                "status": "success",
                "result": result.text,
                "files_modified": [str(f) for f in (result.files_modified or [])],
                "session_id": result.session_id,
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Serena Gateway - Isolated MCP Wrapper")
    parser.add_argument("--prompt", "-p", required=True, help="Task prompt for Serena")
    parser.add_argument("--project", "-d", default=".", help="Project directory path")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Run async task
    result = asyncio.run(run_serena_task(args.prompt, args.project))

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result["status"] == "success":
            print(result["result"])
        else:
            print(f"Error: {result.get('error', 'Unknown error')}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
