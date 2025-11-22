"""
Archivist Indexer
Scans repo directories for scrolls (.md), code files, and TIPs
and maintains the lightweight JSON index.
"""
import os, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "archivist" / "knowledge_index.json"

def scan_files():
    index = {
        "scrolls": [],
        "repo_files": [],
        "decision_logs": [],
        "tips": []
    }

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        rel_path = path.relative_to(ROOT)
        rel_str = str(rel_path)

        if path.suffix == ".md" and "docs" in rel_path.parts:
            index["scrolls"].append({
                "title": path.stem,
                "path": rel_str,
                "tags": ["scroll"],
                "summary": "Unparsed"
            })

        elif path.suffix in [".py", ".json", ".yml", ".yaml"]:
            index["repo_files"].append({
                "path": rel_str,
                "language": path.suffix.lstrip("."),
                "summary": "Unparsed"
            })

        elif "TIP" in rel_str:
            index["tips"].append({
                "id": path.stem,
                "path": rel_str,
                "summary": "Unparsed"
            })

    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)

    return index

if __name__ == "__main__":
    result = scan_files()
    print("Archivist index updated.")
    print(json.dumps(result, indent=2))
