# Logging and Reporting

## Action Log

Append machine-readable action events to `logs/actions.jsonl`.

Suggested event fields:

- `eventId`
- `timestamp`
- `businessId`
- `locationId`
- `workflow`
- `mode`
- `status`
- `inputSource`
- `draftId`
- `approvalId`
- `publishedResourceId`
- `summary`

## Human Reports

Generated reports should be written to `reports/generated`.

Recommended report types:

- GBP audit report
- optimization recommendations
- review theme report
- competitor comparison
- post draft batch
- approval queue export
