# Get Documents

Retrieve **indexed text documents** by **ID** from a namespace (up to **100** IDs per request). Missing IDs do not fail the whole call- you get **`207`** / `status: "partial"` with `not_found_ids` when some IDs are absent.

For **semantic** retrieval over a natural-language query, use [Search](search.md). To **list chunks** (including summaries) without knowing IDs, use [Fetch Text Data](fetch_text_data.md). For **raw S3 file names**, use [List Files](list_files.md).

Documentation index: [llms.txt](https://docs.moorcheh.ai/llms.txt).

## API

```
POST https://api.moorcheh.ai/v1/namespaces/{namespace_name}/documents/get
```

**Headers:** `Content-Type: application/json`, `x-api-key: <your-api-key>`

## Path parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | string | Yes | Namespace containing the documents |

## Body

| Field | Type | Required | Description |
|---|---|---|---|
| `ids` | array | Yes | Non-empty list of document IDs (max **100**). Use the same IDs you set when uploading via [Upload Text Data](upload_text.md). |

## Examples

```bash
curl -X POST "https://api.moorcheh.ai/v1/namespaces/demo_docs/documents/get" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ids": ["doc1"]}'
```

```bash
curl -X POST "https://api.moorcheh.ai/v1/namespaces/demo_docs/documents/get" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ids": ["doc1", "doc2", "doc3"]}'
```

## Responses

### 200- Success

```json
{
  "status": "success",
  "message": "Successfully retrieved 1 items from namespace 'demo_docs'.",
  "namespace_name": "demo_docs",
  "requested_ids": 1,
  "found_items": 1,
  "items": [
    {
      "id": "doc1",
      "metadata": {},
      "text": "This is the first document about Moorcheh."
    }
  ]
}
```

### 207- Partial success

```json
{
  "status": "partial",
  "message": "Retrieval partially completed. Requested: 2, Found: 1, Not found: 1.",
  "namespace_name": "demo_docs",
  "requested_ids": 2,
  "found_items": 1,
  "not_found_ids": ["doc12"],
  "items": [
    {
      "id": "doc1",
      "metadata": {},
      "text": "This is the first document about Moorcheh."
    }
  ]
}
```

### Fields

| Field | Type | Description |
|---|---|---|
| `status` | string | `"success"` or `"partial"` |
| `message` | string | Human-readable summary |
| `namespace_name` | string | (optional) Namespace queried |
| `requested_ids` | number | Count of IDs in the request |
| `found_items` | number | Number of documents returned in `items` |
| `items` | array | `{ "id", "text", "metadata" }` objects |
| `not_found_ids` | array | Present when some IDs were missing |

### Errors (examples)

```json
{ "status": "failure", "message": "Bad Request: ..." }
```

```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing API key.",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

```json
{ "status": "failure", "message": "Unauthorized" }
```

```json
{ "status": "failure", "message": "Namespace 'demo-docs' not found." }
```

```json
{
  "error": "Invalid request parameters",
  "message": "ids must be a non-empty array with at most 100 elements.",
  "details": { "field": "ids", "max": 100 }
}
```

## Key behavior

- **Batch:** up to **100** IDs per call.
- **Partial success:** unknown IDs → `not_found_ids`; existing ones still in `items`.
- **IDs:** strings or numbers (coerced as by the API).
- Backend uses efficient batch reads (e.g. DynamoDB `BatchGetItem` per Moorcheh docs).

---

## Python SDK: `documents.get`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | `str` | Yes | Namespace |
| `ids` | `list[str \| int]` | Yes | Up to **100** document IDs |

**Returns:** `dict[str, Any]` with `status`, `message`, optional `namespace_name`, `requested_ids`, `found_items`, `items`, optional `not_found_ids`.

**Raises:** `NamespaceNotFound`, `InvalidInputError`, etc.

### Example

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    result = client.documents.get(
        namespace_name="my-faq-documents",
        ids=["faq-1", "faq-2", "faq-3"],
    )

    for item in result.get("items", []):
        print(f"ID: {item['id']}")
        print(f"Text: {item['text']}")
        print(f"Metadata: {item.get('metadata', {})}")
```

### Full workflow

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    namespace = "my-documents"
    result = client.documents.get(
        namespace_name=namespace,
        ids=["doc-1", "doc-2", "doc-3", "doc-4", "doc-5"],
    )

    print(f"Requested: {result.get('requested_ids', 0)}")
    print(f"Found: {result.get('found_items', 0)}")

    for item in result.get("items", []):
        print(f"\nDocument ID: {item['id']}")
        print(f"Text: {item['text'][:100]}...")
        if item.get("metadata"):
            print(f"Metadata: {item['metadata']}")

    if result.get("status") == "partial":
        not_found = result.get("not_found_ids", [])
        if not_found:
            print(f"\nDocuments not found: {not_found}")
```

## Best practices

- Batch up to **100** IDs when possible.
- Compare **`found_items`** to **`requested_ids`**; handle **`partial`** and `not_found_ids`.
- Cache hot documents client-side if appropriate.

## Script

```bash
uv run skills/moorcheh/scripts/get_documents.py \
  --namespace "demo_docs" \
  --ids "doc1,doc2,doc3"
```

## Related

- [Upload Text Data](upload_text.md)
- [Fetch Text Data](fetch_text_data.md)
- [Search](search.md)
- [Delete Data](delete_data.md)
- [List Files](list_files.md)

## Official references

- [Get Documents (REST)](https://docs.moorcheh.ai/api-reference/data/get-documents.md)
- [Get Documents (Python SDK)](https://docs.moorcheh.ai/python-sdk/data/get-documents.md)
