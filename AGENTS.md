# Moorcheh Agent Skills — Setup Instructions

This document provides setup instructions for AI agents using the Moorcheh skill and plugin.

## Prerequisites

### 1. Moorcheh Account

If the user does not have an account yet, direct them to the console to register and get an API key.

- Sign up at [console.moorcheh.ai](https://console.moorcheh.ai)
- Generate an API key from the dashboard

### 2. Environment Variables

```bash
export MOORCHEH_API_KEY="your-api-key-here"
```

Optional (defaults to `https://api.moorcheh.ai/v1`):
```bash
export MOORCHEH_BASE_URL="https://api.moorcheh.ai/v1"
```

### 3. Python Runtime

- Python 3.10+ required
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### 4. Install Dependencies

```bash
pip install moorcheh-sdk requests
```

Or with uv:
```bash
uv pip install moorcheh-sdk requests
```

## Project Structure

```
.
├── skills/
│   ├── moorcheh/               # Core Moorcheh operations
│   │   ├── SKILL.md            # Skill definition
│   │   ├── references/         # Detailed operation guides
│   │   └── scripts/            # Executable Python scripts
│   └── moorcheh-cookbooks/     # Application blueprints
│       ├── SKILL.md            # Cookbook skill definition
│       └── references/         # Implementation guides
├── commands/                   # Claude Code slash commands
├── .claude-plugin/             # Claude Code plugin config
├── .cursor-plugin/             # Cursor plugin config
├── AGENTS.md                   # This file
├── CLAUDE.md                   # Points to AGENTS.md
├── README.md
└── package.json
```

## Ingest Workflow

When the user asks to ingest a document into the wiki, the agent must check file type and size **before** attempting to read it.

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

| Document size | Format | Method |
|---|---|---|
| < 100K characters | Text (MD, TXT, CSV) | Standard ingest |
| 100K–200K characters | Text | Standard ingest (verify no truncation) |
| > 200K characters | Any | Deep ingest |
| Any size | PDF, DOCX, XLSX | Deep ingest — Moorcheh handles extraction |

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

## Running Scripts

All scripts are in `skills/moorcheh/scripts/` and accept command-line arguments.

Run with uv (recommended):
```bash
uv run skills/moorcheh/scripts/search.py --query "your search query" --namespaces "my-namespace"
```

Or with python directly:
```bash
python skills/moorcheh/scripts/search.py --query "your search query" --namespaces "my-namespace"
```

## Available Scripts

### Namespace Management
- [Create Namespace](skills/moorcheh/scripts/create_namespace.py): Create a new text or vector namespace
- [List Namespaces](skills/moorcheh/scripts/list_namespaces.py): List all namespaces in the account

### Data Operations
- [Upload Text](skills/moorcheh/scripts/upload_text.py): Upload text documents with metadata to a namespace
- [Upload File](skills/moorcheh/scripts/upload_file.py): Upload a file directly (PDF, TXT, MD, CSV, JSON, DOCX) to a namespace
- [Deep Ingest](skills/moorcheh-cookbooks/scripts/deep_ingest.py): Stage large/binary files via a temporary Moorcheh namespace for wiki ingestion
- [Example Data](skills/moorcheh/scripts/example_data.py): Create sample data for demos and testing

### Search & AI
- [Search](skills/moorcheh/scripts/search.py): Perform semantic search across namespaces with ITS scoring
- [Generate Answer](skills/moorcheh/scripts/generate_answer.py): Generate AI-powered answers from namespace data (RAG)

## Dependencies

Scripts require:
- `moorcheh-sdk` — Official Moorcheh Python SDK
- `requests` — HTTP library (fallback for direct API calls)

## Moorcheh Cookbooks

The cookbooks skill provides blueprints for building complete AI applications:

- **Knowledge Base RAG**: Build a document Q&A system
- **Customer Support Bot**: Build a customer support chatbot
- **Semantic Search App**: Build a search application with ITS scoring
- **AI Q&A System**: Build a question-answering system with structured output
- **LLM Wiki**: Self-maintaining personal knowledge base (Karpathy pattern + Moorcheh ITS)
- **Deep Ingest**: Ingest large documents (>200K chars) or binary files (PDF, DOCX, XLSX) via Moorcheh staging namespace — no local extraction needed

### Optional Frontend Guide
- [Frontend Interface](skills/moorcheh-cookbooks/references/frontend_interface.md): Build a Next.js frontend for Moorcheh backends

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new skills, references, or cookbooks.
