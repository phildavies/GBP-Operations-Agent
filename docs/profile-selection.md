# Profile Selection

The GBP Operations Agent is designed to work across multiple Google Business Profile listings.

The current reusable selection layer uses a local registry:

```text
config/profile-registry.example.json
```

Each profile points to:

- the business config
- the optional source manifest
- the future GBP account and location identifiers
- publishing safety settings

## List Profiles

```powershell
python scripts/select_profile.py --list
```

## Select a Profile

```powershell
python scripts/select_profile.py --profile professional-diver-training
```

This writes the selected profile to:

```text
.gbp-agent/selected-profile.json
```

That file is ignored by Git because it is local runtime state.

## Import Sources for Selected Profile

```powershell
python scripts/import_selected_profile.py
```

For Professional Diver Training, this reads:

```text
config/businesses/professional-diver-training.sources.example.yaml
```

and writes:

```text
reports/generated/professional-diver-training-knowledge-pack.json
reports/generated/professional-diver-training-knowledge-pack.md
```

## Future GBP Account Sync

The live Google Business Profile integration should populate this registry from the connected Google account.

The official Google Business Profile Business Information API exposes `accounts.locations.list` for listing accessible locations under an account. Once OAuth is configured, the sync flow should be:

```text
authenticate Google account
  -> list accessible GBP accounts
  -> list locations per account
  -> match locations to local business configs
  -> update profile registry
  -> select profile for workflow
```

Live publishing should remain disabled unless a profile is selected, the action is approved, and the global publishing gate is enabled.
