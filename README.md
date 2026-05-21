# GBP Operations Agent

Reusable modular AI-assisted operations system for managing and optimizing multiple Google Business Profile listings from one framework.

The project is designed around skill-based workflows, per-business configuration, approval gates, and human-readable reporting. Initial behavior defaults to:

```text
generate -> review -> approve -> publish
```

Live publishing and destructive updates should remain disabled until authentication, permissions, audit logging, and approval controls are fully implemented.

## Core Modules

- `GBP Optimizer`: audits listing content, SEO signals, media coverage, reviews, posts, Q&A, categories, services, and conversion opportunities.
- `GBP Event Creator`: generates Event, Offer, and Update post drafts from Sheets, JSON, or webhook inputs.
- `GBP Review Reply Generator`: drafts review responses using business-specific tone, prohibited wording, and SEO guidance.
- `GBP Competitor Tracker`: compares a selected listing against local competitors and creates content gap reports.

## Architecture Principles

- Multi-business by default.
- Skills are reusable and business-agnostic.
- Business rules live in configuration, not workflow code.
- Every live action goes through an approval gate.
- Logging captures intent, generated output, approver, publish status, and rollback notes.
- Integrations are adapters that can be replaced without rewriting workflows.

## Quick Start

1. Copy `.env.example` to `.env` when credentials are ready.
2. Copy `config/businesses/example.business.yaml` for each real business.
3. Keep `livePublishing.enabled` set to `false` until approvals and API permissions are verified.
4. Add real Google Business Profile, Sheets, and webhook integration code under `src/integrations`.
5. Run workflows in draft mode first and review output in `reports/`.

## Suggested Businesses

Starter config templates are included for:

- Professional Diver Training
- Site Skills Knowhow
- Parawan's Thai Home Cooking Classes
- The Gold Bar Koh Tao

## Repository Layout

```text
config/                 Global and per-business settings
docs/                   Architecture, approvals, APIs, logging, roadmap
reports/                Generated human-readable reports
skills/                 Reusable workflow instructions
src/                    Future automation framework source
workflows/              Workflow specifications and runbooks
```

## Safety Model

The system starts in semi-automated mode. It may analyze listings, generate recommendations, draft posts, draft review replies, and prepare competitor summaries. It must not publish posts, update listings, or reply to reviews without explicit approval.
