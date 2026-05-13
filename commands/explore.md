---
description: Explore data in a Moorcheh namespace- preview documents, test searches, and check namespace stats
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
2. From `list_namespaces` output, note **`type`** for the chosen namespace:
   - **Text**- list up to **100** indexed chunks (best preview):
     ```bash
     uv run ${SKILL_ROOT}/skills/moorcheh/scripts/fetch_text_data.py --namespace "NAMESPACE"
     ```
     Add `--json` for the raw API body if needed.
   - **Text (optional second pass)**- semantic sample (broad natural-language query, not a `*` literal):
     ```bash
     uv run ${SKILL_ROOT}/skills/moorcheh/scripts/search.py --query "overview introduction summary" --namespaces "NAMESPACE" --top-k 5
     ```
   - **Vector**- this pack has no CLI to dump vectors; show **item_count** / **vector_dimension** from the list output and suggest semantic [Search](../skills/moorcheh/references/search.md) with a query vector from their embedding pipeline.
3. Display:
   - Namespace type and size
   - Sample chunks or search hits with metadata (if **`limit`** was passed, show at most that many items)
   - Available metadata fields for filtering (from samples)
4. Suggest next steps:
   - `/moorcheh:search` to search this namespace
   - `/moorcheh:answer` to ask questions
   - `/moorcheh:upload` to add more data

## Environment

Requires:
- `MOORCHEH_API_KEY`: Moorcheh API key
