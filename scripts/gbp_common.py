from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"
STATE_DIR = PROJECT_ROOT / ".gbp-agent"
TOKEN_PATH = STATE_DIR / "google-token.json"
LOCATION_CACHE_PATH = STATE_DIR / "gbp-locations.json"
PROFILE_REGISTRY_PATH = PROJECT_ROOT / "config" / "profile-registry.example.json"

BUSINESS_SCOPE = "https://www.googleapis.com/auth/business.manage"


class GbpError(RuntimeError):
    pass


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    if ENV_PATH.exists():
        for raw in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"')

    for key, value in os.environ.items():
        if key.startswith("GOOGLE_") or key.startswith("GBP_"):
            values.setdefault(key, value)
    return values


def require_google_oauth_config() -> dict[str, str]:
    env = load_env()
    required = ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REDIRECT_URI"]
    missing = [key for key in required if not env.get(key)]
    if missing:
        raise GbpError(
            "Missing Google OAuth settings in .env: "
            + ", ".join(missing)
            + ". Copy .env.example to .env and add credentials from Google Cloud."
        )
    return env


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def token_is_expired(token: dict[str, Any]) -> bool:
    expires_at = token.get("expires_at")
    if not expires_at:
        return True
    expiry = datetime.fromisoformat(expires_at)
    return datetime.now(timezone.utc) >= expiry - timedelta(minutes=2)


def post_form(url: str, data: dict[str, str]) -> dict[str, Any]:
    body = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise GbpError(f"Google token request failed: {exc.code} {detail}") from exc


def refresh_access_token(token: dict[str, Any], env: dict[str, str]) -> dict[str, Any]:
    refresh_token = token.get("refresh_token")
    if not refresh_token:
        raise GbpError("Token is expired and no refresh token is available. Run gbp_oauth.py again.")

    response = post_form(
        "https://oauth2.googleapis.com/token",
        {
            "client_id": env["GOOGLE_CLIENT_ID"],
            "client_secret": env["GOOGLE_CLIENT_SECRET"],
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
    )

    token.update(response)
    token["refresh_token"] = refresh_token
    token["expires_at"] = (
        datetime.now(timezone.utc) + timedelta(seconds=int(response.get("expires_in", 3600)))
    ).isoformat()
    write_json(TOKEN_PATH, token)
    return token


def get_access_token() -> str:
    env = require_google_oauth_config()
    if not TOKEN_PATH.exists():
        raise GbpError("No Google token found. Run scripts/gbp_oauth.py first.")

    token = read_json(TOKEN_PATH)
    if token_is_expired(token):
        token = refresh_access_token(token, env)

    access_token = token.get("access_token")
    if not access_token:
        raise GbpError("Token file does not contain an access token. Run scripts/gbp_oauth.py again.")
    return str(access_token)


def google_get(url: str, access_token: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise GbpError(f"Google API request failed: {exc.code} {detail}") from exc
