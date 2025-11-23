#!/usr/bin/env python3
"""
AVOT-core: full secret + system diagnostic

Checks:
- Environment: GH_PAT, OpenAI / OPENAI_API_KEY presence
- GitHub API: /user with GH_PAT
- OpenAI API: simple models list using OpenAI SDK (if available)
- AVOT registry: loads avot_registry.json and inspects agents
- TCOP: imports core.tcop.heartbeat() and records result

Outputs a single JSON object to stdout.
"""

import importlib.util
import json
import os
import sys
import urllib.request as _req
from typing import Any, Dict


def _env_snapshot(name: str) -> Dict[str, Any]:
    val = os.getenv(name)
    return {
        "name": name,
        "present": bool(val),
        "length": len(val or ""),
        "prefix": val[:4] if val else None,
    }


def check_github() -> Dict[str, Any]:
    token = os.getenv("GH_PAT") or os.getenv("GITHUB_TOKEN")
    if not token:
        return {"ok": False, "reason": "GH_PAT/GITHUB_TOKEN not set in environment"}

    try:
        req = _req.Request(
            "https://api.github.com/user",
            headers={
                "Authorization": f"token {token}",
                "User-Agent": "AVOT-core-diagnostic",
                "Accept": "application/vnd.github+json",
            },
        )
        with _req.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return {
            "ok": True,
            "login": data.get("login"),
            "id": data.get("id"),
        }
    except Exception as exc:  # pragma: no cover - best effort
        return {"ok": False, "error": str(exc)}


def _get_openai_key() -> str:
    # Support multiple naming conventions
    return (
        os.getenv("OPENAI_API_KEY")
        or os.getenv("OpenAI")
        or os.getenv("OPENAI")
        or ""
    )


def check_openai() -> Dict[str, Any]:
    key = _get_openai_key()
    if not key:
        return {
            "ok": False,
            "reason": "No OpenAI key found in OPENAI_API_KEY / OpenAI / OPENAI",
        }

    if importlib.util.find_spec("openai") is None:
        return {"ok": False, "error": "openai package not installed"}

    from openai import OpenAI  # type: ignore

    try:
        client = OpenAI(api_key=key)
        # A light-weight call: list a few models
        models = client.models.list()
        ids = [m.id for m in getattr(models, "data", [])[:3]]
        return {"ok": True, "models_seen": ids}
    except Exception as exc:  # pragma: no cover - best effort
        return {"ok": False, "error": str(exc)}


def check_avot_registry() -> Dict[str, Any]:
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        root = os.path.dirname(here)
        path = os.path.join(root, "avot_registry.json")
        with open(path, "r", encoding="utf-8") as f:
            reg = json.load(f)

        agents = reg.get("agents") if isinstance(reg, dict) else reg
        agents = agents or []
        names = []
        for a in agents:
            if isinstance(a, dict):
                names.append(a.get("name") or a.get("id") or "<unnamed>")
            else:
                names.append(str(a))

        return {
            "ok": True,
            "agent_count": len(agents),
            "agents_preview": sorted(names)[:10],
        }
    except FileNotFoundError:
        return {"ok": False, "error": "avot_registry.json not found at repo root"}
    except Exception as exc:  # pragma: no cover
        return {"ok": False, "error": str(exc)}


def check_tcop_heartbeat() -> Dict[str, Any]:
    try:
        from core.tcop import heartbeat  # type: ignore
    except Exception as exc:  # pragma: no cover
        return {"ok": False, "error": f"import core.tcop.heartbeat failed: {exc}"}

    try:
        hb = heartbeat()
        return {"ok": True, "heartbeat": hb}
    except Exception as exc:  # pragma: no cover
        return {"ok": False, "error": f"heartbeat() raised: {exc}"}


def main() -> None:
    report: Dict[str, Any] = {
        "env": {
            "GH_PAT": _env_snapshot("GH_PAT"),
            "OpenAI": _env_snapshot("OpenAI"),
            "OPENAI_API_KEY": _env_snapshot("OPENAI_API_KEY"),
        },
        "github": check_github(),
        "openai": check_openai(),
        "avot_registry": check_avot_registry(),
        "tcop": check_tcop_heartbeat(),
    }

    ok = all(
        section.get("ok", False)
        for section in [
            report["github"],
            report["openai"],
            report["avot_registry"],
            report["tcop"],
        ]
    )

    report["summary"] = {
        "ok": bool(ok),
        "message": (
            "All core checks passed."
            if ok
            else "One or more checks failed; inspect report sections."
        ),
    }

    json.dump(report, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

