"""Generate scroll files for AVOT agents based on configured templates."""

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List


def load_registry(registry_path: Path) -> List[Dict[str, str]]:
    """Return AVOT entries from a registry JSON file."""
    if not registry_path.exists():
        raise FileNotFoundError(f"Registry file not found: {registry_path}")

    with registry_path.open() as f:
        registry = json.load(f)

    avots: List[Dict[str, str]] = registry.get("avots", [])
    if not isinstance(avots, list):
        raise ValueError("Registry JSON must include an 'avots' list.")
    return avots


def render_scroll(template: str, avot: Dict[str, str]) -> str:
    """Insert AVOT attributes into a template string."""
    return (
        template.replace("{{AVOT_NAME}}", avot.get("name", ""))
        .replace("{{SCROLL_TOPIC}}", avot.get("scroll_topic", ""))
    )


def generate_scrolls(
    avots: Iterable[Dict[str, str]], template_dir: Path, output_dir: Path
) -> None:
    """Write rendered scrolls for each AVOT using matching templates."""
    output_dir.mkdir(exist_ok=True)

    for avot in avots:
        name = avot.get("name")
        topic = avot.get("scroll_topic")
        if not name or not topic:
            print("Skipping entry missing 'name' or 'scroll_topic':", avot)
            continue

        template_path = template_dir / f"{topic}.txt"
        if not template_path.exists():
            print(f"Template not found for {topic}; skipping {name}.")
            continue

        template = template_path.read_text()
        scroll_content = render_scroll(template, avot)

        output_path = output_dir / f"{name}_{topic}_scroll.txt"
        output_path.write_text(scroll_content)
        print(f"Generated scroll for {name} at {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render scrolls for AVOT registry entries using templates."
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("avot_registry.json"),
        help="Path to the AVOT registry JSON file.",
    )
    parser.add_argument(
        "--templates",
        type=Path,
        default=Path("scroll_templates"),
        help="Directory containing scroll templates.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("generated_scrolls"),
        help="Directory to write generated scrolls to.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    avots = load_registry(args.registry)
    generate_scrolls(avots, args.templates, args.output)


if __name__ == "__main__":
    main()