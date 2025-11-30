#!/usr/bin/env python3
"""
CMS.UNIFIED-SYNC handler

Orchestrates a "unified sync" operation:

1. Reads the high-level task / type / targets (CLI args).
2. Calls the OpenAI bridge with a structured prompt to act as the
   AVOT lattice (Tyme → Quill → Fabricator → Guardian → Archivist).
3. Expects a JSON plan describing file edits per repository.
4. Applies file changes for AVOT-core locally.
5. Writes per-repo change sets into ./artifacts/<repo_name>/ for
   downstream GitHub Actions to sync into other repositories.
6. Saves the full plan as ./artifacts/unified_sync_plan.json

The actual pushing to other repos is handled by .github/workflows/unified-sync.yml
"""

import argparse
import importlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

# Ensure repo root on path if needed
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

ARTIFACTS_DIR = REPO_ROOT / "artifacts"
ARTIFACTS_DIR.mkdir(exist_ok=True)


def load_run_chat():
    spec = importlib.util.find_spec("core.openai_bridge")
    if spec is None:
        raise RuntimeError("core.openai_bridge.run_chat not available; ensure imports are correct.")

    module = importlib.import_module("core.openai_bridge")
    run_chat = getattr(module, "run_chat", None)
    if run_chat is None:
        raise RuntimeError("core.openai_bridge.run_chat not available; ensure imports are correct.")

    return run_chat


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run CMS.UNIFIED-SYNC orchestration")
    parser.add_argument("--task", required=True, help="High-level description of what to generate")
    parser.add_argument("--type", dest="type_", default=None,
                        help="Content type: scroll | diagram | schema | manifest | ui | code")
    parser.add_argument("--targets", default=None,
                        help="Optional comma-separated repo names to override UMX routing")
    parser.add_argument("--mode", default="create",
                        help="create | update | sync-only")
    return parser.parse_args()


def build_system_prompt() -> str:
    return """You are TYME orchestrating the AVOT lattice (Quill, Fabricator,
Guardian, Archivist, Convergence) for a CMS.UNIFIED-SYNC operation.

Your job:

1. Understand the user's high-level task and content type.
2. Have Quill draft content, Fabricator convert it into concrete file edits,
   Guardian check coherence/ethics, and Archivist assign scroll metadata.
3. Produce a STRICT JSON OBJECT (no prose) describing file changes per repository.

JSON format:

{
  "summary": "short summary of what was generated",
  "repos": [
    {
      "name": "AVOT-core",
      "changes": [
        {
          "path": "relative/path/from/repo/root.ext",
          "mode": "write",  // or "append"
          "content": "full file content after change"
        }
      ]
    },
    {
      "name": "Hall-of-Tyme",
      "changes": [
        {
          "path": "relative/path/in/hall/of/tyme.ext",
          "mode": "write",
          "content": "..."
        }
      ]
    }
  ]
}

Rules:

- Always include an entry for AVOT-core when new scrolls/schemas are created.
- Only include other repos (Hall-of-Tyme, etc.) if relevant.
- Do NOT suggest running shell commands or modifying GitHub workflows directly.
- Do NOT include markdown fences. Return ONLY valid JSON.
"""


def build_user_prompt(task: str, type_: str | None, targets: List[str] | None, mode: str) -> str:
    return json.dumps(
        {
            "task": task,
            "type": type_ or "unspecified",
            "targets_override": targets or [],
            "mode": mode,
        },
        indent=2,
    )


def call_model(task: str, type_: str | None, targets: List[str] | None, mode: str) -> Dict[str, Any]:
    run_chat = load_run_chat()

    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(task, type_, targets, mode)

    raw = run_chat(system_prompt, user_prompt)
    try:
        plan = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Model returned non-JSON response: {exc}\nRaw:\n{raw}") from exc

    if "repos" not in plan or not isinstance(plan["repos"], list):
        raise RuntimeError(f"Plan missing 'repos' list. Plan: {plan}")

    return plan


def apply_changes_for_avot_core(repos: List[Dict[str, Any]]) -> None:
    for repo in repos:
        if repo.get("name") != "AVOT-core":
            continue
        for change in repo.get("changes", []):
            rel_path = change.get("path")
            mode = change.get("mode", "write")
            content = change.get("content", "")

            if not rel_path:
                continue

            dest = REPO_ROOT / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)

            if mode == "append" and dest.exists():
                existing = dest.read_text(encoding="utf-8")
                dest.write_text(existing + content, encoding="utf-8")
            else:
                dest.write_text(content, encoding="utf-8")


def write_artifacts_for_other_repos(repos: List[Dict[str, Any]]) -> None:
    """
    For any repo other than AVOT-core, write their planned file changes
    into ./artifacts/<repo_name>/ so that the GitHub Actions workflow can
    check out those repos and copy the files into place.
    """
    for repo in repos:
        name = repo.get("name")
        if not name or name == "AVOT-core":
            continue

        repo_dir = ARTIFACTS_DIR / name
        repo_dir.mkdir(parents=True, exist_ok=True)

        for change in repo.get("changes", []):
            rel_path = change.get("path")
            mode = change.get("mode", "write")
            content = change.get("content", "")

            if not rel_path:
                continue

            dest = repo_dir / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)

            if mode == "append" and dest.exists():
                existing = dest.read_text(encoding="utf-8")
                dest.write_text(existing + content, encoding="utf-8")
            else:
                dest.write_text(content, encoding="utf-8")


def main() -> None:
    args = parse_args()
    targets = [t.strip() for t in args.targets.split(",")] if args.targets else None

    plan = call_model(args.task, args.type_, targets, args.mode)

    # Save full plan for debugging / downstream steps
    plan_path = ARTIFACTS_DIR / "unified_sync_plan.json"
    plan_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")

    repos = plan.get("repos", [])
    apply_changes_for_avot_core(repos)
    write_artifacts_for_other_repos(repos)

    summary = plan.get("summary") or "CMS.UNIFIED-SYNC completed."
    print(summary)
    print(f"Plan saved to: {plan_path}")
    print(f"Artifacts dir: {ARTIFACTS_DIR}")


if __name__ == "__main__":
    main()
