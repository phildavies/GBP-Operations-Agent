from __future__ import annotations

import http.server
import secrets
import sys
import threading
import urllib.parse
import webbrowser
from datetime import datetime, timedelta, timezone

from gbp_common import BUSINESS_SCOPE, GbpError, TOKEN_PATH, post_form, require_google_oauth_config, write_json


class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    server: "OAuthCallbackServer"

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        self.server.authorization_code = params.get("code", [None])[0]
        self.server.authorization_state = params.get("state", [None])[0]
        self.server.authorization_error = params.get("error", [None])[0]

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"<html><body><h1>GBP Operations Agent connected</h1>"
            b"<p>You can close this browser tab and return to Codex.</p></body></html>"
        )

    def log_message(self, format: str, *args: object) -> None:
        return


class OAuthCallbackServer(http.server.HTTPServer):
    authorization_code: str | None = None
    authorization_state: str | None = None
    authorization_error: str | None = None


def main() -> int:
    env = require_google_oauth_config()
    redirect_uri = env["GOOGLE_REDIRECT_URI"]
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    host = parsed_redirect.hostname or "localhost"
    port = parsed_redirect.port or 3000

    state = secrets.token_urlsafe(24)
    auth_params = {
        "client_id": env["GOOGLE_CLIENT_ID"],
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": BUSINESS_SCOPE,
        "access_type": "offline",
        "prompt": "consent",
        "state": state
    }
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(auth_params)

    server = OAuthCallbackServer((host, port), OAuthCallbackHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    print("Opening Google OAuth consent screen...")
    print(f"If the browser does not open, visit:\n{auth_url}\n")
    webbrowser.open(auth_url)

    while server.authorization_code is None and server.authorization_error is None:
        thread.join(timeout=0.2)

    server.shutdown()

    if server.authorization_error:
        raise GbpError(f"OAuth authorization failed: {server.authorization_error}")
    if server.authorization_state != state:
        raise GbpError("OAuth state mismatch. Please run the flow again.")
    if not server.authorization_code:
        raise GbpError("No OAuth authorization code was received.")

    token_response = post_form(
        "https://oauth2.googleapis.com/token",
        {
            "client_id": env["GOOGLE_CLIENT_ID"],
            "client_secret": env["GOOGLE_CLIENT_SECRET"],
            "code": server.authorization_code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }
    )
    token_response["scope"] = BUSINESS_SCOPE
    token_response["created_at"] = datetime.now(timezone.utc).isoformat()
    token_response["expires_at"] = (
        datetime.now(timezone.utc) + timedelta(seconds=int(token_response.get("expires_in", 3600)))
    ).isoformat()
    write_json(TOKEN_PATH, token_response)

    print(f"Connected. Token saved locally at {TOKEN_PATH}")
    print("This token file is ignored by Git.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
