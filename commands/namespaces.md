---
description: List all namespaces or inspect a specific namespace's details
argument-hint: [name "NamespaceName"]
allowed-tools: Bash(uv:*), AskUserQuestion, Skill
---

# Namespaces

List all namespaces in your Moorcheh account, or inspect details of a specific namespace.

## Usage

```
# List all namespaces
/moorcheh:namespaces

# Get details for a specific namespace
/moorcheh:namespaces name "my-documents"
```

## Workflow

1. Run the list script (it always returns **all** namespaces- there is no per-name HTTP call in this pack):
   ```bash
   uv run ${SKILL_ROOT}/skills/moorcheh/scripts/list_namespaces.py
   ```
2. If no `name` argument was provided:
   - Display every namespace with type, `vector_dimension` (when vector), and `item_count`
3. If `name` **was** provided:
   - Locate that namespace in the script output (or re-run and filter client-side)
   - If missing, say so clearly; if present, echo **type**, **item_count**, and **vector_dimension** when relevant

## Environment

Requires:
- `MOORCHEH_API_KEY`: Moorcheh API key
