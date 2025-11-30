#!/usr/bin/env python
"""Command-line interface for AVOT-core."""

import argparse
import sys
from pathlib import Path

# Ensure local package is importable when running from repo root
REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON_PATH = REPO_ROOT / "python"
if str(PYTHON_PATH) not in sys.path:
    sys.path.insert(0, str(PYTHON_PATH))

from avot_core import registry, runtime  # noqa: E402


def cmd_list(args: argparse.Namespace) -> None:
    agents = registry.list_agents()
    for agent in agents:
        print(f"- {agent.id}: {agent.role} ({agent.status})")


def cmd_show(args: argparse.Namespace) -> None:
    agent = registry.get_agent(args.agent_id)
    if agent is None:
        print(f"Agent '{args.agent_id}' not found.")
        sys.exit(1)

    print(f"id: {agent.id}")
    print(f"name: {agent.name}")
    print(f"role: {agent.role}")
    print(f"status: {agent.status}")
    print(f"repo: {agent.repo}")
    print(f"capabilities: {', '.join(agent.capabilities)}")
    print(f"entrypoint: {agent.entrypoint.module}.{agent.entrypoint.function}")
    print(f"tags: {', '.join(agent.tags)}")
    if agent.extra:
        print(f"extra: {agent.extra}")


def cmd_run(args: argparse.Namespace) -> None:
    runtime.run_agent(args.agent_id, intent=args.intent)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AVOT-core registry helper")
    subparsers = parser.add_subparsers(required=True)

    list_parser = subparsers.add_parser("list", help="List all AVOTs")
    list_parser.set_defaults(func=cmd_list)

    show_parser = subparsers.add_parser("show", help="Show one AVOT manifest")
    show_parser.add_argument("agent_id", help="Agent id to display")
    show_parser.set_defaults(func=cmd_show)

    run_parser = subparsers.add_parser("run", help="Simulate running an AVOT")
    run_parser.add_argument("agent_id", help="Agent id to simulate")
    run_parser.add_argument("--intent", default="",
                           help="Optional description of the requested task")
    run_parser.set_defaults(func=cmd_run)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":  # pragma: no cover
    main()
