from __future__ import annotations

import re
import sys
from copy import deepcopy
from typing import Any

from gbp_common import LOCATION_CACHE_PATH, PROFILE_REGISTRY_PATH, read_json, write_json


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def location_id_from_name(name: str) -> str:
    return name.rsplit("/", 1)[-1] if "/" in name else name


def best_match(profile: dict[str, Any], locations: list[dict[str, Any]]) -> dict[str, Any] | None:
    display_name = normalize(profile.get("displayName", ""))
    profile_id = normalize(profile.get("id", ""))
    best: tuple[int, dict[str, Any]] | None = None

    for item in locations:
        location = item.get("location", {})
        title = normalize(location.get("title", ""))
        score = 0
        if title == display_name:
            score += 100
        if display_name and display_name in title:
            score += 80
        if profile_id and profile_id in title:
            score += 60
        for token in display_name.split():
            if token and token in title:
                score += 5
        if score and (best is None or score > best[0]):
            best = (score, item)

    return best[1] if best else None


def main() -> int:
    if not LOCATION_CACHE_PATH.exists():
        print("No GBP location cache found. Run scripts/gbp_list_locations.py first.", file=sys.stderr)
        return 1

    registry = read_json(PROFILE_REGISTRY_PATH)
    cache = read_json(LOCATION_CACHE_PATH)
    locations = cache.get("locations", [])
    updated = deepcopy(registry)
    matched = 0

    for profile in updated.get("profiles", []):
        match = best_match(profile, locations)
        if not match:
            continue

        account = match.get("account", {})
        location = match.get("location", {})
        profile["gbp"] = {
            "accountName": account.get("name", "pending"),
            "accountDisplayName": account.get("accountName", account.get("type", "pending")),
            "locationName": location.get("name", "pending"),
            "locationId": location_id_from_name(location.get("name", "pending")),
            "placeId": location.get("metadata", {}).get("placeId", "pending"),
            "title": location.get("title", profile.get("displayName"))
        }
        matched += 1

    write_json(PROFILE_REGISTRY_PATH, updated)
    print(f"Updated profile registry: {PROFILE_REGISTRY_PATH}")
    print(f"Matched profiles: {matched}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
