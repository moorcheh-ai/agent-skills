See [AGENTS.md](AGENTS.md) for full setup instructions.

## Ingest Workflow

When ingesting a document into the wiki, check file type and size **before** reading it.

### Pre-check (mandatory — run before every ingest)

Before reading any source file:
1. Check file extension and size
2. If binary format (PDF, DOCX, XLSX) or file exceeds 200K characters:
   - Inform the user: "This document will be ingested via Moorcheh deep ingest."
   - Upload to staging namespace via `upload_file` (Moorcheh handles extraction)
   - Switch to deep ingest workflow automatically
3. If plain text < 200K chars: proceed with standard ingest

```python
import os

BINARY_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".xls", ".doc", ".pptx"}
MAX_DIRECT_READ = 200_000  # characters

def should_deep_ingest(file_path: str) -> bool:
    ext = os.path.splitext(file_path)[1].lower()
    if ext in BINARY_EXTENSIONS:
        return True
    try:
        size = os.path.getsize(file_path)
        if size > MAX_DIRECT_READ:
            return True
    except OSError:
        return True  # can't stat — safer to deep ingest
    return False
```

**For plain text files < 200K characters (MD, TXT, CSV):**
Use standard ingest — read the file directly into context and build wiki pages.

**For large documents (> 200K characters or any PDF/DOCX/XLSX binary format):**
Use the Deep Ingest workflow instead of reading the file directly.
See [references/deep_ingest.md](skills/moorcheh-cookbooks/references/deep_ingest.md) for the full procedure.

The agent should:
1. Check file type and size before reading
2. If binary format (PDF, DOCX, XLSX) or > 200K chars:
   - Upload the file to a Moorcheh staging namespace via `upload_file`
   - Moorcheh handles extraction, chunking, and indexing automatically
   - Query the staging namespace to build wiki pages
3. If plain text < 200K chars: standard ingest (read directly)

## Uploading to Moorcheh

When uploading local files to a Moorcheh namespace, **always prefer `upload_file`** over constructing JSON payloads with `upload_text`. The agent never needs to read or modify the file contents for upload.

```python
# Preferred: upload file directly (agent never reads/modifies the file)
client.documents.upload_file(namespace_name="wiki-<topic>", file_path="wiki/<page>.md")
```

Or via script:
```bash
uv run skills/moorcheh/scripts/upload_file.py --namespace "wiki-<topic>" --file "wiki/<page>.md"
```
