from __future__ import annotations

import sys
import urllib.parse
from typing import Any

from gbp_common import GbpError, LOCATION_CACHE_PATH, get_access_token, google_get, write_json


ACCOUNT_LIST_URL = "https://mybusinessaccountmanagement.googleapis.com/v1/accounts"
LOCATIONS_URL = "https://mybusinessbusinessinformation.googleapis.com/v1/{account}/locations"
READ_MASK = ",".join([
    "name",
    "title",
    "storeCode",
    "phoneNumbers",
    "categories",
    "websiteUri",
    "regularHours",
    "metadata",
    "profile",
    "serviceArea",
    "openInfo"
])


def list_accounts(access_token: str) -> list[dict[str, Any]]:
    accounts: list[dict[str, Any]] = []
    page_token = ""
    while True:
        url = ACCOUNT_LIST_URL
        if page_token:
            url += "?" + urllib.parse.urlencode({"pageToken": page_token})
        response = google_get(url, access_token)
        accounts.extend(response.get("accounts", []))
        page_token = response.get("nextPageToken", "")
        if not page_token:
            return accounts


def list_locations_for_parent(access_token: str, account_name: str) -> list[dict[str, Any]]:
    locations: list[dict[str, Any]] = []
    page_token = ""
    while True:
        params = {"readMask": READ_MASK, "pageSize": "100"}
        if page_token:
            params["pageToken"] = page_token
        url = LOCATIONS_URL.format(account=account_name) + "?" + urllib.parse.urlencode(params)
        response = google_get(url, access_token)
        locations.extend(response.get("locations", []))
        page_token = response.get("nextPageToken", "")
        if not page_token:
            return locations


def main() -> int:
    access_token = get_access_token()
    accounts = list_accounts(access_token)
    all_locations = []

    for account in accounts:
        account_name = account.get("name")
        if not account_name:
            continue
        try:
            locations = list_locations_for_parent(access_token, account_name)
        except GbpError as exc:
            print(f"Could not list locations for {account_name}: {exc}", file=sys.stderr)
            locations = []

        for location in locations:
            all_locations.append({"account": account, "location": location})

    cache = {"accounts": accounts, "locations": all_locations}
    write_json(LOCATION_CACHE_PATH, cache)

    print(f"Accounts found: {len(accounts)}")
    print(f"Locations found: {len(all_locations)}")
    for index, item in enumerate(all_locations, start=1):
        account = item["account"]
        location = item["location"]
        title = location.get("title", "(untitled)")
        name = location.get("name", "")
        place_id = location.get("metadata", {}).get("placeId", "pending")
        print(f"{index}. {title}")
        print(f"   account: {account.get('name')} ({account.get('accountName', account.get('type', 'unknown'))})")
        print(f"   location: {name}")
        print(f"   placeId: {place_id}")

    print(f"Saved cache: {LOCATION_CACHE_PATH}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
