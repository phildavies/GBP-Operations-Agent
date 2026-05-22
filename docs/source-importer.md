# Source Importer

The source importer turns a business source manifest into a structured knowledge pack for draft GBP workflows.

## Input

Use a source manifest like:

```text
config/businesses/professional-diver-training.sources.example.yaml
```

The manifest maps business material from OneDrive into content and media groups.

## Output

The importer writes:

```text
reports/generated/<business-id>-knowledge-pack.json
reports/generated/<business-id>-knowledge-pack.md
```

These files are intentionally ignored by Git because they may contain business-specific material.

## Run

Use the bundled Python runtime in Codex, or any Python environment with:

- `python-docx`
- `openpyxl`
- `pillow`
- `pypdf`

Example:

```powershell
python scripts/import_business_sources.py config/businesses/professional-diver-training.sources.example.yaml
```

## Supported Sources

- Word documents: `.docx`
- Excel workbooks: `.xlsx`, `.xlsm`
- PDFs: `.pdf`
- Images: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`, `.tif`, `.tiff`
- Text-like files: `.txt`, `.md`, `.html`, `.htm`, `.csv`, `.json`, `.rtf`
- Directories: scanned for file counts, image counts, and sample filenames

## Safety

The importer is read-only against business source folders. It writes only generated reports inside this project.
