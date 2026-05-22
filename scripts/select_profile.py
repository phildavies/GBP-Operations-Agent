from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = PROJECT_ROOT / "config" / "profile-registry.example.json"
STATE_DIR = PROJECT_ROOT / ".gbp-agent"
SELECTED_PROFILE_PATH = STATE_DIR / "selected-profile.json"


def load_registry(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Profile registry not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def profiles_by_id(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {profile["id"]: profile for profile in registry.get("profiles", [])}


def print_profiles(registry: dict[str, Any]) -> None:
    default_profile_id = registry.get("defaultProfileId")
    selected_profile = load_selected_profile(required=False)
    selected_profile_id = selected_profile.get("id") if selected_profile else None

    print("Available GBP profiles")
    print("======================")
    for profile in registry.get("profiles", []):
        markers = []
        if profile["id"] == default_profile_id:
            markers.append("default")
        if profile["id"] == selected_profile_id:
            markers.append("selected")
        marker_text = f" ({', '.join(markers)})" if markers else ""
        location_id = profile.get("gbp", {}).get("locationId", "pending")
        print(f"- {profile['id']}: {profile['displayName']}{marker_text}")
        print(f"  locationId: {location_id}")
        print(f"  config: {profile.get('businessConfig')}")
        print(f"  sources: {profile.get('sourceManifest') or 'none'}")


def load_selected_profile(required: bool = True) -> dict[str, Any] | None:
    if not SELECTED_PROFILE_PATH.exists():
        if required:
            raise FileNotFoundError("No profile selected yet.")
        return None
    return json.loads(SELECTED_PROFILE_PATH.read_text(encoding="utf-8"))


def select_profile(registry: dict[str, Any], profile_id: str | None) -> dict[str, Any]:
    profiles = profiles_by_id(registry)
    if profile_id is None:
        profile_id = registry.get("defaultProfileId")

    if profile_id not in profiles:
        available = ", ".join(sorted(profiles))
        raise ValueError(f"Unknown profile '{profile_id}'. Available profiles: {available}")

    profile = profiles[profile_id]
    state = {
        **profile,
        "selectedAt": datetime.now(timezone.utc).isoformat(),
        "registryPath": str(DEFAULT_REGISTRY)
    }
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    SELECTED_PROFILE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description="Select a reusable GBP business profile.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY), help="Path to profile registry JSON.")
    parser.add_argument("--profile", help="Profile id to select.")
    parser.add_argument("--list", action="store_true", help="List available profiles.")
    parser.add_argument("--current", action="store_true", help="Show the current selected profile.")
    args = parser.parse_args()

    registry_path = (PROJECT_ROOT / args.registry).resolve() if not Path(args.registry).is_absolute() else Path(args.registry)
    registry = load_registry(registry_path)

    if args.list:
        print_profiles(registry)
        return 0

    if args.current:
        current = load_selected_profile(required=False)
        if current is None:
            print("No profile selected yet.")
        else:
            print(json.dumps(current, indent=2))
        return 0

    selected = select_profile(registry, args.profile)
    print(f"Selected profile: {selected['displayName']} ({selected['id']})")
    print(f"Business config: {selected.get('businessConfig')}")
    print(f"Source manifest: {selected.get('sourceManifest') or 'none'}")
    print(f"GBP location id: {selected.get('gbp', {}).get('locationId', 'pending')}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
