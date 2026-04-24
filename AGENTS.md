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
