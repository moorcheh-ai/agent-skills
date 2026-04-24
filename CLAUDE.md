See [AGENTS.md](AGENTS.md) for full setup instructions.

## Ingest Workflow

When ingesting a document into the wiki, check file type and size **before** reading it.

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
