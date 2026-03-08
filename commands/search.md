---
description: Perform semantic search across Moorcheh namespaces with ITS scoring and filtering
argument-hint: query [search text] namespaces [Namespace1,Namespace2] top_k [number] threshold [0.0-1.0]
allowed-tools: Bash(uv:*), AskUserQuestion, Skill
---

# Semantic Search

Perform semantic search across one or more Moorcheh namespaces using ITS (Information-Theoretic Scoring).

## Usage

```
/moorcheh:search query "your search text" namespaces "Namespace1,Namespace2"
```

## Workflow

When necessary, use AskUserQuestion to make entering arguments easier.

1. Parse the query and namespaces arguments
2. If namespaces are missing:
   - Run `/moorcheh:namespaces` to list available namespaces
   - Use AskUserQuestion to prompt user to select
3. Run the search script:
   ```bash
   uv run ${SKILL_ROOT}/skills/moorcheh/scripts/search.py --query "USER_QUERY" --namespaces "NS1,NS2" --top-k 10
   ```
4. Display results with ITS scores and relevance labels

## Examples

```
/moorcheh:search query "machine learning" namespaces "my-documents"
/moorcheh:search query "product features #category:tech" namespaces "articles" top_k 5
/moorcheh:search query "best practices" namespaces "docs,guides" threshold 0.5
```

## Environment

Requires:
- `MOORCHEH_API_KEY`: Moorcheh API key
