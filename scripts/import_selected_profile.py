from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SELECTED_PROFILE_PATH = PROJECT_ROOT / ".gbp-agent" / "selected-profile.json"
IMPORTER = PROJECT_ROOT / "scripts" / "import_business_sources.py"


def read_config_text(path: str) -> str:
    config_path = PROJECT_ROOT / path
    if not config_path.exists():
        return ""
    return config_path.read_text(encoding="utf-8")


def collect_exclusions(config_text: str) -> list[str]:
    exclusions: list[str] = []
    for line in config_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("prohibitedWording:") and "[" in stripped and "]" in stripped:
            raw_values = stripped.split("[", 1)[1].rsplit("]", 1)[0]
            exclusions.extend(value.strip().strip("'\"") for value in raw_values.split(","))
        elif "old PayPal" in stripped or "paypal.me" in stripped:
            exclusions.extend(["PayPal", "paypal.me", "djlkohtao"])
    return sorted({value for value in exclusions if value})


def main() -> int:
    if not SELECTED_PROFILE_PATH.exists():
        print("No profile selected. Run scripts/select_profile.py first.", file=sys.stderr)
        return 1

    selected = json.loads(SELECTED_PROFILE_PATH.read_text(encoding="utf-8"))
    manifest = selected.get("sourceManifest")
    if not manifest:
        print(f"Selected profile has no source manifest: {selected['displayName']}", file=sys.stderr)
        return 1

    config_text = read_config_text(selected.get("businessConfig", ""))
    exclusions = collect_exclusions(config_text)
    command = [sys.executable, str(IMPORTER), manifest]
    for exclusion in exclusions:
        command.extend(["--exclude", exclusion])

    return subprocess.call(command, cwd=str(PROJECT_ROOT))


if __name__ == "__main__":
    raise SystemExit(main())
