# Fetch Text Data

List stored **text and summary chunks** in a **text** namespace (up to **100** items per response). Use this for export, UI previews, or RAG-style listing. For similarity ranking over a query string, use [Search](search.md) instead.

**HTTP:** `GET https://api.moorcheh.ai/v1/namespaces/{namespace_name}/documents/fetch-text-data`

Documentation index: [llms.txt](https://docs.moorcheh.ai/llms.txt).

## Overview

- **Text namespaces only**- vector namespaces return an error for this route.
- **Up to 100 items** per successful response (no pagination parameters in the public API today; for full history beyond that, use other product flows or [Get Documents](get_documents.md) when you know document IDs).
- Responses use **snake_case** keys (`items`, `is_summary`, `created_at`, `execution_time`, etc.).
- Successful calls consume **credits** and count toward your plan’s **API request** usage.

## Authentication

- Header **`x-api-key`**: required.

## Path parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | string | Yes | Text namespace to read from (URL path segment) |

## REST example

```bash
curl -X GET "https://api.moorcheh.ai/v1/namespaces/my-docs/documents/fetch-text-data" \
  -H "x-api-key: $MOORCHEH_API_KEY"
```

## Response (200)

```json
{
  "status": "success",
  "message": "Fetched 3 text items from namespace 'my-docs'.",
  "namespace": "my-docs",
  "statistics": {
    "total_items": 3,
    "total_text_chunks": 2,
    "total_summary_chunks": 1,
    "created_at_min": 1234567890123,
    "created_at_max": 1234567890456,
    "source_counts": {
      "upload": 2,
      "api": 1
    }
  },
  "items": [
    {
      "id": "chunk-id-or-doc-id",
      "text": "The actual text content of the chunk.",
      "metadata": {
        "source": "document.pdf",
        "page": "1",
        "summary_chunk_id": "my-docs#doc_summary_0"
      },
      "created_at": 1234567890123,
      "is_summary": false
    },
    {
      "id": "doc_summary_0",
      "text": "Summary of the document content.",
      "metadata": {
        "source": "document.pdf",
        "page": "summary_0_chunks_0_2"
      },
      "created_at": 1234567890123,
      "is_summary": true
    }
  ],
  "execution_time": 0.123
}
```

### No chunks yet (empty `items`)

```json
{
  "status": "success",
  "message": "Fetched 0 text items from namespace 'my-docs'.",
  "namespace": "my-docs",
  "statistics": {
    "total_items": 0,
    "total_text_chunks": 0,
    "total_summary_chunks": 0,
    "created_at_min": null,
    "created_at_max": null,
    "source_counts": {}
  },
  "items": [],
  "execution_time": 0.018
}
```

### Top-level fields

| Field | Type | Description |
|---|---|---|
| `status` | string | `"success"` on 200 |
| `message` | string | Human-readable summary |
| `namespace` | string | Namespace that was queried |
| `statistics` | object | Aggregates for the returned `items` |
| `items` | array | Chunk list (length ≤ 100) |
| `execution_time` | number | Seconds spent processing the request |

### `statistics` (typical)

| Field | Type | Description |
|---|---|---|
| `total_items` | number | Count of objects in `items` |
| `total_text_chunks` | number | Non-summary chunks |
| `total_summary_chunks` | number | Summary chunks |
| `created_at_min` | number \| null | Earliest `created_at` among items (often Unix **ms**) |
| `created_at_max` | number \| null | Latest `created_at` among items |
| `source_counts` | object | Map of source label → count (`upload`, `api`, file names, etc.) |

### `items[]` fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Chunk / item id |
| `text` | string | Chunk body |
| `metadata` | object | Optional metadata (`source`, `page`, `summary_chunk_id`, …) |
| `created_at` | number \| string \| null | Backend-dependent; may be Unix ms or ISO string |
| `is_summary` | boolean | `true` for summary chunks when present |

**`created_at` in clients:** If the value is Unix **seconds**, multiply by 1000 for `Date` in JavaScript; if already **milliseconds**, pass through directly.

## Errors (examples)

```json
{ "status": "failure", "message": "Bad Request: Missing namespace name in URL path." }
```

```json
{ "status": "failure", "message": "Bad Request: Namespace 'your-namespace' is not a text-based namespace." }
```

```json
{ "status": "failure", "message": "Unauthorized: Missing API key" }
```

```json
{ "status": "failure", "message": "Unauthorized: Invalid API key ID" }
```

```json
{ "status": "failure", "message": "Namespace 'your-namespace' not found." }
```

```json
{ "status": "failure", "message": "Internal Server Error during namespace validation." }
```

## Limits

- **100** items maximum per response (`items.length` ≤ 100).
- Each successful call uses **credits** and API quota.

## Python SDK: `documents.fetch_text_data`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | `str` | Yes | Target **text** namespace |

**Returns:** `dict[str, Any]` with snake_case keys (`status`, `message`, `namespace`, `statistics`, `items`, `execution_time`, …).

**Raises:** `NamespaceNotFound`, `InvalidInputError`, `AuthenticationError`, `APIError`, etc.

### Sync example

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    data = client.documents.fetch_text_data(namespace_name="my-faq-documents")

    print(data.get("status"), data.get("message"))
    for item in data.get("items", []):
        print(item.get("id"), item.get("is_summary"), (item.get("text") or "")[:80])
```

### Async example

```python
from moorcheh_sdk import AsyncMoorchehClient
import asyncio

async def main():
    async with AsyncMoorchehClient(api_key="your-api-key") as client:
        data = await client.documents.fetch_text_data(namespace_name="my-faq-documents")
        print(len(data.get("items", [])), "items")

# asyncio.run(main())
```

### Full listing walkthrough

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    listing = client.documents.fetch_text_data(namespace_name="my-faq-documents")
    print(listing.get("status"), listing.get("statistics"))
    for item in listing.get("items", []):
        print(item.get("id"), (item.get("text") or "")[:120])
```

## vs. Get Documents

| Operation | When to use |
|---|---|
| **Fetch Text Data** | **List** chunks in a text namespace (up to 100). |
| **Get Documents** (`documents.get` with `ids`) | Fetch **specific** documents when you already know their IDs. |

## Best practices

- Treat `items` as **read-only** slices for display or export; use **Search** for semantic queries.
- Rely on **snake_case** everywhere in JSON and Python.

## Script

```bash
uv run skills/moorcheh/scripts/fetch_text_data.py --namespace "my-faq-documents"
```

## Related

- [Upload Text Data](upload_text.md)
- [Get Documents](get_documents.md)- fetch specific indexed documents by ID
- [List Files](list_files.md)- raw objects in storage (vs indexed chunks here)
- [Search](search.md)
- [List Namespaces](list_namespaces.md)

## Official references

- [Fetch Text Data (REST)](https://docs.moorcheh.ai/api-reference/data/fetch-text-data.md)
- [Fetch Text Data (Python SDK)](https://docs.moorcheh.ai/python-sdk/data/fetch-text-data.md)
