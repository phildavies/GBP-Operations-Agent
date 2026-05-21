# Architecture

## Layers

1. `Skills`: reusable instructions for each capability.
2. `Workflows`: orchestrated steps that combine skills, config, integrations, approval, and logging.
3. `Business Config`: per-business tone, CTAs, keywords, media style, review style, and posting policy.
4. `Integrations`: adapters for Google Business Profile, Google Sheets, webhooks, image generation, and future automation.
5. `Approval`: review queue for generated drafts and pending live actions.
6. `Logging and Reports`: durable action history and human-readable outputs.

## Control Flow

```text
select business
  -> load business config
  -> select GBP listing
  -> run workflow in draft mode
  -> generate report or draft action
  -> request approval
  -> publish only if approved and live publishing is enabled
  -> log result
```

## Modularity Rules

- A skill should not know about one specific business.
- Business-specific wording belongs in `config/businesses`.
- Publishing code must be separated from generation code.
- Read-only analysis should work without publishing permissions.
- Every workflow returns a structured draft plus a human-readable summary.
