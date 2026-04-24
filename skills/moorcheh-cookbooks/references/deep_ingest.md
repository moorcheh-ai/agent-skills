# Deep Ingest — Large Document Workflow

Ingest documents that exceed the LLM prompt window (~200K characters) or are in binary formats (PDF, DOCX, XLSX). Moorcheh handles all file extraction, chunking, and indexing — the agent never reads the raw file locally.

## The Problem

Standard ingest reads the file directly into the agent's context. Documents exceeding the prompt window get **silently truncated** — the agent processes only the first portion with no error or warning. Binary formats (PDF, DOCX) can't be read locally at all without extra dependencies.

## When to Use

| Document size | Format | Method |
|---|---|---|
| < 100K characters | Text (MD, TXT, CSV) | Standard ingest (read file directly) |
| 100K–200K characters | Text | Standard ingest (verify no truncation) |
| > 200K characters | Any | **Deep ingest** |
| Any size | PDF, DOCX, XLSX | **Deep ingest** — always safer, Moorcheh handles extraction |

**Rule of thumb:** If the file is binary or you're unsure about size, use deep ingest.

## Workflow

```
raw/big-report.pdf
    │
    ▼
┌─────────────────────────────┐
│ 1. Upload to staging        │  upload_file → Moorcheh extracts, chunks, indexes
│    namespace via upload_file │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ 2. Wait ~15 seconds         │  Moorcheh processes the file
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ 3. Discover structure       │  query="table of contents chapters sections"
│    via search (top_k=20)    │  → agent learns what the document contains
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ 4. Query chapter-by-chapter │  one search per section (top_k=15)
│    to retrieve full content │  → agent gets the full document in pieces
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ 5. Build wiki pages locally │  same as standard ingest from here
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ 6. Batch upload wiki pages  │  upload_file each .md to wiki namespace
│    to wiki namespace        │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ 7. Delete staging namespace │  cleanup
└─────────────────────────────┘
```

**No local extraction needed.** No pymupdf, no text parsing, no TOC extraction scripts. Moorcheh handles all of that. The agent's only job is to upload the file and then query it.

## Step-by-Step

### Step 1 — Create staging namespace and upload file

```python
from moorcheh_sdk import MoorchehClient
import os, time

client = MoorchehClient(api_key=os.environ["MOORCHEH_API_KEY"])

STAGING = "staging-big-report"

# Create a temporary staging namespace
client.namespaces.create(namespace_name=STAGING, type="text")

# Upload the file — Moorcheh extracts, chunks, and indexes it
client.documents.upload_file(
    namespace_name=STAGING,
    file_path="raw/big-report.pdf"
)
```

Or use the helper script:

```bash
uv run skills/moorcheh/scripts/deep_ingest.py \
  --file "raw/big-report.pdf" \
  --staging-namespace "staging-big-report"
```

### Step 2 — Wait for indexing

```python
print("[WAIT] Waiting for Moorcheh to process the file...")
time.sleep(15)
```

### Step 3 — Discover document structure

```python
results = client.similarity_search.query(
    namespaces=[STAGING],
    query="table of contents chapters sections overview structure",
    top_k=20
)
for r in results.get("results", []):
    print(f"[{r['score']:.3f}] {r['text'][:150]}...")
```

The agent reads these results to understand what sections/chapters the document contains.

### Step 4 — Query chapter-by-chapter

For each section discovered in step 3, the agent queries for full content:

```python
sections = ["introduction", "methodology", "results", "discussion", "conclusion"]

section_content = {}
for section in sections:
    results = client.similarity_search.query(
        namespaces=[STAGING],
        query=section,
        top_k=15
    )
    section_content[section] = results.get("results", [])
```

### Step 5 — Build wiki pages

The agent now has the full document content in `section_content`. From here, the workflow is identical to standard ingest — create wiki pages, update index, glossary, overview, etc.

### Step 6 — Upload wiki pages to wiki namespace

Use the standard sync workflow (delete-then-upload) to push all new wiki pages to the wiki namespace.

### Step 7 — Delete staging namespace

```python
client.namespaces.delete(namespace_name=STAGING)
print(f"[OK] Staging namespace '{STAGING}' deleted")
```

## Staging Namespace Convention

| Purpose | Namespace name |
|---|---|
| Single file ingest | `staging-<filename-slug>` |
| Batch ingest | `staging-batch-<date>` |

Always delete staging namespaces after the wiki pages are built. They are temporary.

## Script

```bash
# Create staging namespace and upload file (steps 1-2)
uv run skills/moorcheh/scripts/deep_ingest.py \
  --file "raw/big-report.pdf" \
  --staging-namespace "staging-big-report"

# The agent handles steps 3-6 via search queries and wiki page creation

# Cleanup (step 7)
uv run skills/moorcheh/scripts/deep_ingest.py \
  --cleanup "staging-big-report"
```

## Important Notes

- Moorcheh supports PDF, DOCX, XLSX, TXT, CSV, JSON, MD for file upload
- Indexing takes ~15 seconds for most files; very large files may take longer
- The staging namespace is temporary — always clean it up after wiki pages are built
- The agent never reads the raw file locally — all content comes from Moorcheh search results
- This workflow avoids all local dependencies (no pymupdf, no docx parser, etc.)
