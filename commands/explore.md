---
description: Explore data in a Moorcheh namespace — preview documents, test searches, and check namespace stats
argument-hint: namespace [NamespaceName] [limit number]
allowed-tools: Bash(uv:*), AskUserQuestion, Skill
---

# Explore Data

Explore the contents of a Moorcheh namespace. Preview documents, run test searches, and understand what data is available.

## Usage

```
/moorcheh:explore namespace "my-documents"
/moorcheh:explore namespace "my-documents" limit 5
```

## Workflow

1. If namespace is not provided:
   - List all namespaces:
     ```bash
     uv run ${SKILL_ROOT}/skills/moorcheh/scripts/list_namespaces.py
     ```
   - Use AskUserQuestion to select a namespace
2. Run a broad search to preview content:
   ```bash
   uv run ${SKILL_ROOT}/skills/moorcheh/scripts/search.py --query "*" --namespaces "NAMESPACE" --top-k 5
   ```
3. Display:
   - Namespace type and size
   - Sample documents with metadata
   - Available metadata fields for filtering
4. Suggest next steps:
   - `/moorcheh:search` to search this namespace
   - `/moorcheh:answer` to ask questions
   - `/moorcheh:upload` to add more data

## Environment

Requires:
- `MOORCHEH_API_KEY`: Moorcheh API key
