# List Files

List **raw file objects** in document storage (S3) for a namespace: `file_name`, `size` (bytes), and `last_modified`. This is **storage inventory**- not the same as [Fetch Text Data](fetch_text_data.md) (indexed text/summary chunks) or [Search](search.md) (semantic hits over processed content). For **indexed documents by ID**, use [Get Documents](get_documents.md) (`documents.get`).

Documentation index: [llms.txt](https://docs.moorcheh.ai/llms.txt).

## API

```
GET https://api.moorcheh.ai/v1/namespaces/{namespace_name}/list-files
```

**Headers:** `x-api-key: <your-api-key>`  
**Body / query:** none.

## Path parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | string | Yes | Namespace you own (URL segment) |

## Example

```bash
curl -X GET "https://api.moorcheh.ai/v1/namespaces/my-namespace/list-files" \
  -H "x-api-key: $MOORCHEH_API_KEY"
```

## Response (200)

```json
{
  "success": true,
  "namespace": "my-namespace",
  "file_count": 2,
  "files": [
    {
      "file_name": "report.pdf",
      "size": 245678,
      "last_modified": "2026-05-10T14:22:11.000Z"
    },
    {
      "file_name": "notes.txt",
      "size": 1204,
      "last_modified": "2026-05-09T09:01:00.000Z"
    }
  ]
}
```

### Fields

| Field | Type | Description |
|---|---|---|
| `success` | boolean | `true` when listing succeeds |
| `namespace` | string | Namespace that was listed |
| `file_count` | integer | Number of objects in `files` |
| `files` | array | Each element: `file_name`, `size` (bytes), `last_modified` (ISO 8601 from storage) |

### Empty storage (no files yet)

```json
{
  "success": true,
  "namespace": "my-namespace",
  "file_count": 0,
  "files": []
}
```

### Errors (examples)

```json
{ "error": "namespace_name is required in the URL path" }
```

```json
{ "error": "Unauthorized: API key is required" }
```

```json
{ "error": "Namespace 'unknown' not found" }
```

```json
{
  "error": "Forbidden",
  "message": "You do not have access to this namespace."
}
```

```json
{
  "error": "API request limit reached for your plan (100000 requests). Current usage: 100000."
}
```

## Notes

- **`size`** is the object size in **bytes** (S3 / `Content-Length` sense).
- **Empty prefix:** `files` may be `[]` and `file_count` **0**.
- **Ordering:** not guaranteed stable; sort client-side if needed.
- **Usage:** counts toward API quota / credits like other authenticated routes.

---

## Python SDK: `documents.list_files`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | `str` | Yes | Namespace to list |

**Returns:** `dict[str, Any]`- commonly `success`, `namespace`, `file_count`, `files` (each: `file_name`, `size`, `last_modified`). Keys are **snake_case** after SDK normalization.

**Raises:** `NamespaceNotFound`, `InvalidInputError`, `AuthenticationError`, `APIError`, `MoorchehError`, etc.

### Example (sync)

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    status = client.documents.list_files(namespace_name="my-faq-documents")
    print(status)
```

### Example (async)

```python
import asyncio
from moorcheh_sdk import AsyncMoorchehClient

async def main():
    async with AsyncMoorchehClient(api_key="your-api-key") as client:
        status = await client.documents.list_files(namespace_name="my-faq-documents")
        print(status.get("file_count"), status.get("files"))

asyncio.run(main())
```

### Complete workflow

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    listing = client.documents.list_files(namespace_name="my-data")
    print(f"Namespace: {listing.get('namespace')}")
    print(f"File count: {listing.get('file_count')}")
    for f in listing.get("files", []):
        print(f["file_name"], f["size"], f.get("last_modified"))
```

## Important notes

- **Raw storage**- entries reflect objects in storage (e.g. after [Upload File](upload_file.md) / pre-signed upload), not solely “rows” from the text indexing pipeline.
- **Do not assume sort order** from the API.

## Best practices

- Use for audits, cleanup, or file-picker UIs; use **Search** / **Fetch Text Data** for content discovery over processed text.
- Sort or filter **client-side** when you need deterministic ordering.
- To remove storage objects by name, use [Delete Files](delete_files.md) (`documents.delete_files`).

## Script

```bash
uv run skills/moorcheh/scripts/list_files.py --namespace "my-namespace"
```

## Related

- [Upload File](upload_file.md)
- [Create Namespace](create_namespace.md)
- [Get Documents](get_documents.md)
- [Fetch Text Data](fetch_text_data.md)
- [Search](search.md)
- [Delete Data](delete_data.md)

## Official references

The **List Files** HTTP route may not yet appear as a standalone page in [llms.txt](https://docs.moorcheh.ai/llms.txt); confirm path and fields in the [OpenAPI spec](https://docs.moorcheh.ai/api-reference/openapi.json) (search for `list-files`). Related published pages:

- [Upload File URL (REST)](https://docs.moorcheh.ai/api-reference/data/upload-file-url.md)
- [Delete File (REST)](https://docs.moorcheh.ai/api-reference/data/delete-file.md)
- [Data management (Python SDK)](https://docs.moorcheh.ai/python-sdk/data.md)
