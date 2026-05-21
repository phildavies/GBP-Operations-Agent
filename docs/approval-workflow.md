# Approval Workflow

The initial system uses a strict approval-first model.

## States

- `draft`: generated recommendation, post, reply, or report.
- `needs_review`: ready for human review.
- `approved`: approved by an authorized reviewer.
- `rejected`: blocked from publishing or updating.
- `published`: live action completed successfully.
- `failed`: attempted action failed and needs review.

## Required Approvals

Approval is required before:

- publishing GBP posts
- updating descriptions, categories, services, hours, attributes, or Q&A
- replying to reviews
- uploading or selecting generated media for publication

## Minimum Approval Record

Each approval should capture:

- business id
- GBP location id
- workflow name
- generated draft
- proposed live action
- reviewer
- timestamp
- approval decision
- notes
