# Live GBP Connection

This project supports a draft-safe live connection path for Google Business Profile.

The first live step is read-only:

```text
Google OAuth -> list GBP accounts -> list GBP locations -> sync local profile registry
```

Publishing remains disabled.

## Google Cloud Setup

Create or use a Google Cloud project, then:

1. Configure the OAuth consent screen.
2. Create OAuth client credentials for a desktop/local app flow.
3. Add this redirect URI:

```text
http://localhost:3000/oauth/callback
```

4. Enable the relevant Google Business Profile APIs:

- My Business Account Management API
- My Business Business Information API

The scripts use the OAuth scope:

```text
https://www.googleapis.com/auth/business.manage
```

Google's official docs say `accounts.list` lists accounts accessible to the authenticated user, and requires the `business.manage` scope. The Business Information API `accounts.locations.list` lists locations under an account and requires a `readMask`.

Official references:

- https://developers.google.com/my-business/reference/accountmanagement/rest/v1/accounts/list
- https://developers.google.com/my-business/reference/businessinformation/rest/v1/accounts.locations/list
- https://developers.google.com/my-business/content/implement-oauth

## Local Credentials

Copy:

```text
.env.example
```

to:

```text
.env
```

Then fill:

```text
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:3000/oauth/callback
```

Do not commit `.env`.

## Connect OAuth

Run:

```powershell
python scripts/gbp_oauth.py
```

The browser opens for Google approval. After approval, a token is saved locally:

```text
.gbp-agent/google-token.json
```

This folder is ignored by Git.

## List Live GBP Locations

Run:

```powershell
python scripts/gbp_list_locations.py
```

This writes:

```text
.gbp-agent/gbp-locations.json
```

and prints the accessible live profiles.

## Sync Profiles

Run:

```powershell
python scripts/gbp_sync_profiles.py
```

This updates:

```text
config/profile-registry.example.json
```

with matched GBP account and location identifiers.

## Safety

These scripts only authenticate, list accounts, list locations, and sync local registry metadata. They do not publish posts, update profile fields, reply to reviews, upload images, or modify live GBP content.
