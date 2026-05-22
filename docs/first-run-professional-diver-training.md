# First Run: Professional Diver Training

This is the recommended first-run path for using the GBP Operations Agent with Professional Diver Training.

The current project is a framework scaffold. It is ready for configuration, source organization, and draft-first workflows, but it does not yet connect directly to the live Google Business Profile API. Until that integration is added, use it as a structured assistant workflow:

```text
business source material -> GBP audit inputs -> draft report -> human review -> approved changes
```

## 1. Confirm Business Config

Start with:

```text
config/businesses/professional-diver-training.yaml
```

Fill in the real `gbpLocationId` after the connected Google account can list available GBP locations.

Keep:

```yaml
autoPostingEnabled: false
```

## 2. Attach Existing OneDrive Source Material

Use the source manifest:

```text
config/businesses/professional-diver-training.sources.example.yaml
```

Suggested OneDrive source folder:

```text
C:\Users\zugon\OneDrive\Professional Diver Training
```

Useful current source groups:

- `Course Descriptions Chat.docx`
- `Homepage Content & Structure.docx`
- `Main pages.xlsx`
- `Info PDF's`
- `Images`
- `Images from FB`
- `Local Post Images`
- `Header section images`
- `Logos`

## 3. Gather GBP Inputs

For the first manual/semi-automated run, export or copy:

- current business description
- primary and secondary categories
- services
- opening hours
- attributes
- recent reviews
- current Q&A
- recent posts
- current GBP photos
- competitor names or Maps links

## 4. Run Draft Workflows

Recommended order:

1. `gbp-optimizer`: identify listing gaps and SEO/conversion opportunities.
2. `gbp-review-reply-generator`: analyze reviews and create reply drafts.
3. `gbp-event-creator`: create post drafts from course dates, events, offers, or updates.
4. `gbp-competitor-tracker`: compare against local dive training competitors.

## 5. Review Before Publishing

Nothing should be published directly from the first run. The expected output is:

- audit report
- image/content gap list
- suggested services/categories
- suggested FAQs
- suggested GBP posts
- review reply drafts
- approval checklist

Only after review should approved changes be copied into GBP or later published through an API integration.

## 6. Next Integration Step

The next useful build step is a local importer that reads the source manifest, extracts text from `.docx`, `.xlsx`, and PDFs, indexes image folders, and produces a structured business knowledge summary for the GBP Optimizer.
