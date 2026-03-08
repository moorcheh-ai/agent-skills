---
description: Upload text documents or JSON data to a Moorcheh namespace
argument-hint: namespace [NamespaceName] file [path/to/data.json]
allowed-tools: Bash(uv:*), AskUserQuestion, Skill, Read
---

# Upload Data

Upload text documents or JSON data to a Moorcheh namespace.

## Usage

```
/moorcheh:upload namespace "my-documents" file "data.json"
```

## Workflow

When necessary, use AskUserQuestion to make entering arguments easier.

1. Parse namespace and file arguments
2. If arguments are missing:
   - Use AskUserQuestion to prompt for namespace name and file path
3. Verify the file exists and is valid JSON
4. Run the upload script:
   ```bash
   uv run ${SKILL_ROOT}/skills/moorcheh/scripts/upload_text.py --namespace "NAMESPACE" --file "FILE_PATH"
   ```
5. Display upload results

## Supported Formats

The JSON file should contain either:
- An array of document objects: `[{"id": "...", "text": "...", ...}]`
- An object with documents key: `{"documents": [{"id": "...", "text": "...", ...}]}`

Each document must have `id` and `text` fields. Additional fields become metadata.

## Examples

```
/moorcheh:upload namespace "product-docs" file "./data/products.json"
/moorcheh:upload namespace "support-faq" file "./faq.json"
```

## Environment

Requires:
- `MOORCHEH_API_KEY`: Moorcheh API key
