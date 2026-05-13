# Delete Files

Delete one or more **file objects by name** from **document storage (S3)** for a text namespace you own. This is **storage deletion**- not the same as [Delete Data](delete_data.md), which removes **indexed documents or vectors by ID** (`documents.delete` / `vectors.delete`).

**HTTP:** `DELETE https://api.moorcheh.ai/v1/namespaces/{namespace_name}/delete-file` with a JSON body (and/or query) listing names.

Documentation index: [llms.txt](https://docs.moorcheh.ai/llms.txt).

## Overview

- **Permanent**- S3 `DeleteObject`; no trash / undo.
- **Single or batch** in one request- more efficient than one call per file.
- **Per-file outcomes**- `results[]` can mix `deleted` and `error` (e.g. missing file).

## Authentication

- **`x-api-key`** (required)
- **`Content-Type: application/json`** when sending a JSON body

## Path parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | string | Yes | Namespace you own |

## Body / query inputs

Provide **at least one** of:

| Source | Field | Type | Description |
|---|---|---|---|
| Body | `file_name` | string | One file to delete |
| Body | `file_names` | array of strings | Multiple files; can be combined with `file_name` |
| Query | `file_name` | string | e.g. `?file_name=report.pdf`- can be combined with body |

Use **snake_case** (`file_name`, `file_names`). Per Moorcheh API docs, legacy camelCase (`fileName`, `fileNames`) was **removed in platform 1.5.10**- send snake_case only.

## Examples

### Single file (JSON body)

```bash
curl -X DELETE "https://api.moorcheh.ai/v1/namespaces/my-namespace/delete-file" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"file_name": "document.pdf"}'
```

### Multiple files

```bash
curl -X DELETE "https://api.moorcheh.ai/v1/namespaces/my-namespace/delete-file" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"file_names": ["doc1.pdf", "doc2.docx", "notes.txt"]}'
```

### Query parameter (single name)

```bash
curl -X DELETE "https://api.moorcheh.ai/v1/namespaces/my-namespace/delete-file?file_name=report.pdf" \
  -H "x-api-key: $MOORCHEH_API_KEY"
```

## Response (200)

```json
{
  "success": true,
  "message": "File deletion process completed.",
  "namespace": "my-namespace",
  "results": [
    {
      "file_name": "document.pdf",
      "status": "deleted",
      "message": "File deletion initiated successfully"
    },
    {
      "file_name": "missing.pdf",
      "status": "error",
      "message": "File not found"
    }
  ]
}
```

| Field | Type | Description |
|---|---|---|
| `success` | boolean | `true` when the request finished processing |
| `message` | string | Summary message |
| `namespace` | string | Namespace operated on |
| `results` | array | One row per target file: `file_name`, `status` (`deleted` \| `error`), `message` |

### Response (207)- partial HTTP success

Some deployments return **207** when every file was examined but at least one row failed (others may still use **200** with mixed `results`). Always inspect **`results[]`**:

```json
{
  "success": true,
  "message": "File deletion process completed with errors.",
  "namespace": "my-namespace",
  "results": [
    {
      "file_name": "document.pdf",
      "status": "deleted",
      "message": "File deletion initiated successfully"
    },
    {
      "file_name": "missing.pdf",
      "status": "error",
      "message": "File not found"
    }
  ]
}
```

### Errors (examples)

```json
{ "error": "Missing namespace in path or no file_name/file_names provided" }
```

```json
{ "error": "Missing or invalid API key" }
```

```json
{ "error": "Namespace not found or you do not own it" }
```

```json
{ "error": "API/credit limit exceeded" }
```

## Notes

- Only **`DELETE`** is used for this route.
- Objects live under `userId/namespace_name/file_name`; you must **own** the namespace.
- One HTTP call counts as **one** API request for quota/credits even when deleting several names.
- Some deployments may return **207** for partial success; the Python SDK may treat **200** and **207** as success- check `results` either way.

---

## Python SDK: `documents.delete_files`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | `str` | Yes | Text namespace |
| `file_names` | `list[str]` | Yes | Non-empty list of storage file names (same strings as [List Files](list_files.md) / upload) |

**Returns:** `dict[str, Any]`- typically `success`, `message`, `namespace`, `results` (snake_case).

**Raises:** `NamespaceNotFound`, `InvalidInputError`, `AuthenticationError`, `APIError`, `MoorchehError`, etc.

This is **not** `documents.delete`, which removes **indexed documents by ID**.

### Example (sync)

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    status = client.documents.delete_files(
        namespace_name="my-faq-documents",
        file_names=["old-report.pdf", "draft-notes.txt"],
    )
    print(status)
```

### Example (async)

```python
import asyncio
from moorcheh_sdk import AsyncMoorchehClient

async def main():
    async with AsyncMoorchehClient(api_key="your-api-key") as client:
        status = await client.documents.delete_files(
            namespace_name="my-faq-documents",
            file_names=["old-report.pdf"],
        )
        for row in status.get("results", []):
            print(row["file_name"], row["status"], row.get("message"))

asyncio.run(main())
```

### List then delete (workflow)

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    namespace = "my-data"
    listing = client.documents.list_files(namespace_name=namespace)
    names = [
        f["file_name"]
        for f in listing.get("files", [])
        if f["file_name"].endswith(".tmp")
    ]
    if names:
        result = client.documents.delete_files(
            namespace_name=namespace,
            file_names=names,
        )
        print(result.get("message"), result.get("results"))
```

## Best practices

- Call [List Files](list_files.md) first to confirm names.
- Inspect every `results[]` row; do not treat one `error` as total failure if others `deleted`.
- Use [Delete Data](delete_data.md) when removing **chunks/documents by ID**, not raw storage file names.

## Script

```bash
uv run skills/moorcheh/scripts/delete_files.py \
  --namespace "my-namespace" \
  --files "old.pdf,draft.txt"
```

## Related

- [List Files](list_files.md)
- [Get Documents](get_documents.md)
- [Upload File](upload_file.md)
- [Fetch Text Data](fetch_text_data.md)
- [Delete Data](delete_data.md)

## Official references

- [Delete File (REST)](https://docs.moorcheh.ai/api-reference/data/delete-file.md)
- [Data management (Python SDK)](https://docs.moorcheh.ai/python-sdk/data.md)
- [OpenAPI spec](https://docs.moorcheh.ai/api-reference/openapi.json)
