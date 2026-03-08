---
description: Generate AI-powered answers from your data using RAG (Retrieval-Augmented Generation)
argument-hint: query [question] namespace [NamespaceName]
allowed-tools: Bash(uv:*), AskUserQuestion, Skill
---

# Generate AI Answer

Use Moorcheh's RAG engine to answer questions from your data with AI-generated responses.

## Usage

```
/moorcheh:answer query "your question" namespace "NamespaceName"
```

## Workflow

When necessary, use AskUserQuestion to make entering arguments easier.

1. Parse query and namespace arguments
2. If arguments are missing:
   - Run `/moorcheh:namespaces` to list available namespaces
   - Use AskUserQuestion to prompt user to select
3. Run the answer generation script:
   ```bash
   uv run ${SKILL_ROOT}/skills/moorcheh/scripts/generate_answer.py --namespace "NAMESPACE" --query "USER_QUERY"
   ```
4. Display the generated answer

## Examples

```
/moorcheh:answer query "What are the key features?" namespace "product-docs"
/moorcheh:answer query "How do I reset my password?" namespace "customer-support"
```

## For Raw Search Results

Use `/moorcheh:search` instead to get raw results without a generated answer.

## Environment

Requires:
- `MOORCHEH_API_KEY`: Moorcheh API key
