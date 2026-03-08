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

1. If no `name` argument provided:
   - Run list namespaces script:
     ```bash
     uv run ${SKILL_ROOT}/skills/moorcheh/scripts/list_namespaces.py
     ```
   - Display all namespaces with their types and sizes
2. If `name` argument is provided:
   - Show namespace details (type, document/vector count, configuration)

## Environment

Requires:
- `MOORCHEH_API_KEY`: Moorcheh API key
