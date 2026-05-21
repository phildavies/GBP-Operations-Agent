---
name: gbp-event-creator
description: Generate GBP Event, Offer, and Update post drafts from Sheets, JSON, or webhook inputs with duplicate prevention and approval gates.
---

# GBP Event Creator

## Workflow

1. Load event, offer, or update input.
2. Normalize dates, CTA, image requirements, and target business.
3. Check recent post history for duplicates.
4. Generate headline, body, CTA text, and optional hashtags.
5. Select an existing image or prepare an image-generation prompt.
6. Save the draft for approval.

## Safety

Publishing is blocked unless the draft is approved and live publishing is enabled.
