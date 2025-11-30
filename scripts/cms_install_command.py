#!/usr/bin/env python3
"""
CMS.INSTALL-COMMAND

Installs or updates a CMS command into AVOT-core:
- Writes the JSON definition into commands/
- Optionally writes a handler script into scripts/
- Updates commands/registry.json so the CMS command becomes active
"""

import argparse
import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COMMANDS_DIR = REPO_ROOT / "commands"
SCRIPTS_DIR = REPO_ROOT / "scripts"
REGISTRY_PATH = COMMANDS_DIR / "registry.json"


def load_registry():
    if not REGISTRY_PATH.exists():
        return {"commands": []}
    try:
        return json.loads(REGISTRY_PATH.read_text())
    except Exception:
        return {"commands": []}


def save_registry(registry):
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2))


def update_registry(registry, cmd_id, file_path, handler_path):
    # Remove old entries
    registry["commands"] = [
        c for c in registry["commands"] if c.get("id") != cmd_id
    ]

    entry = {
        "id": cmd_id,
        "file": file_path.name,
        "title": cmd_id,
        "category": "user-installed",
        "enabled": True,
    }
    if handler_path:
        entry["handler"] = str(handler_path)

    registry["commands"].append(entry)
    return registry


def install_command(cmd_id, json_content, handler_content=None, overwrite=False):
    # Write JSON definition
    cmd_path = COMMANDS_DIR / f"{cmd_id}.json"

    if cmd_path.exists() and not overwrite:
        raise ValueError(f"Command {cmd_id} already exists. Use --overwrite to replace.")

    cmd_path.write_text(json_content, encoding="utf-8")

    # Write handler if provided
    handler_path = None
    if handler_content:
        handler_path = SCRIPTS_DIR / f"{cmd_id}.py"
        handler_path.write_text(handler_content, encoding="utf-8")

    # Update registry
    registry = load_registry()
    registry = update_registry(registry, cmd_id, cmd_path, handler_path)
    save_registry(registry)

    return {
        "status": "installed",
        "command_file": str(cmd_path),
        "handler_file": str(handler_path) if handler_path else None,
        "registry_updated": True
    }


def main():
    parser = argparse.ArgumentParser(description="Install or update a CMS command.")
    parser.add_argument("--id", required=True)
    parser.add_argument("--json", required=True)
    parser.add_argument("--handler", required=False)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    result = install_command(
        cmd_id=args.id,
        json_content=args.json,
        handler_content=args.handler,
        overwrite=args.overwrite
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
