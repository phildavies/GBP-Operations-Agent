# API Requirements

## Google Business Profile

Required capabilities:

- list accounts and locations connected to the authenticated Google account
- read listing details, categories, services, hours, attributes, posts, media, Q&A, and reviews
- create posts only after approval
- reply to reviews only after approval
- upload or attach images only after approval

Recommended initial scope:

- read-first implementation
- write endpoints behind approval and `livePublishing.enabled`

## Google Sheets

Used for:

- event, offer, and update post inputs
- campaign schedules
- content calendars
- business-specific keyword lists

## Webhooks

Used for:

- external content payloads
- event creation requests
- approval callbacks
- future automation triggers

## AI Generation

Used for:

- optimization summaries
- review replies
- post copy
- FAQs
- image prompts
- competitor summaries
