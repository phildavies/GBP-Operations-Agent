from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SELECTED_PROFILE_PATH = PROJECT_ROOT / ".gbp-agent" / "selected-profile.json"
IMPORTER = PROJECT_ROOT / "scripts" / "import_business_sources.py"


def main() -> int:
    if not SELECTED_PROFILE_PATH.exists():
        print("No profile selected. Run scripts/select_profile.py first.", file=sys.stderr)
        return 1

    selected = json.loads(SELECTED_PROFILE_PATH.read_text(encoding="utf-8"))
    manifest = selected.get("sourceManifest")
    if not manifest:
        print(f"Selected profile has no source manifest: {selected['displayName']}", file=sys.stderr)
        return 1

    return subprocess.call([sys.executable, str(IMPORTER), manifest], cwd=str(PROJECT_ROOT))


if __name__ == "__main__":
    raise SystemExit(main())
