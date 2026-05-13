# List Namespaces

Retrieve every namespace for the authenticated account, including **type**, **item counts**, and **creation time**. Use this before uploads, search, or deletes to confirm names and types.

There are **no query parameters**; the response lists all namespaces for your API key.

Response objects use **snake_case** keys (for example `item_count`, `created_at`).

Documentation index: [llms.txt](https://docs.moorcheh.ai/llms.txt).

## API

```
GET https://api.moorcheh.ai/v1/namespaces
```

**Headers:** `x-api-key: <your-api-key>` (required). `Content-Type` is optional for `GET` with no body.

## Example

```bash
curl -X GET "https://api.moorcheh.ai/v1/namespaces" \
  -H "x-api-key: $MOORCHEH_API_KEY"
```

## Response

### 200 Success

The top-level object is usually `{ "namespaces": [ ... ] }`. Some versions may also include `status` or `message`; treat the **`namespaces`** array as the source of truth.

```json
{
  "namespaces": [
    {
      "namespace_name": "my_documents",
      "type": "text",
      "vector_dimension": null,
      "item_count": 1247,
      "created_at": "2024-01-15T10:30:00.000Z"
    },
    {
      "namespace_name": "product_embeddings",
      "type": "vector",
      "vector_dimension": 1536,
      "item_count": 5683,
      "created_at": "2024-01-20T14:22:15.000Z"
    },
    {
      "namespace_name": "customer_support",
      "type": "text",
      "vector_dimension": null,
      "item_count": 892,
      "created_at": "2024-02-01T09:15:30.000Z"
    }
  ]
}
```

**Empty account (no namespaces yet):**

```json
{
  "namespaces": []
}
```

### Namespace object fields

| Field | Type | Description |
|---|---|---|
| `namespace_name` | string | Unique namespace name |
| `type` | string | `"text"` or `"vector"` |
| `vector_dimension` | number \| null | Set for vector namespaces; `null` for text |
| `item_count` | number | Total items in the namespace |
| `created_at` | string | ISO 8601 creation time |

### 401 Unauthorized- missing key

```json
{
  "message": "Unauthorized: Missing API key"
}
```

```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing API key. Please check your x-api-key header."
}
```

### 401 Unauthorized- invalid key

```json
{
  "message": "Unauthorized: API key verification failed - Invalid API key ID"
}
```

### 401 Unauthorized- disabled key

```json
{
  "message": "Unauthorized: API key is disabled"
}
```

### 403 Forbidden

```json
{
  "status": "failure",
  "message": "Forbidden"
}
```

### 429 Rate limited

```json
{
  "status": "failure",
  "message": "API request limit reached for Professional plan (1000000 requests). Current usage: 1000000. Please upgrade your subscription for higher limits.",
  "current_usage": 1000000,
  "limit": 1000000
}
```

### 429 Subscription expired

```json
{
  "status": "failure",
  "message": "Your Community subscription expired on 8/15/2025. Please renew your subscription to continue using the service."
}
```

### 500 Server Error

```json
{
  "status": "failure",
  "message": "Internal Server Error fetching namespaces."
}
```

## Python SDK

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    data = client.namespaces.list()
    for ns in data.get("namespaces", []):
        print(
            f"{ns['namespace_name']}: type={ns['type']}, "
            f"items={ns['item_count']}, created={ns['created_at']}"
        )
```

**Returns:** `dict[str, Any]` with a `namespaces` array. **Raises:** `AuthenticationError`, `APIError`, etc.

## Script

```bash
uv run skills/moorcheh/scripts/list_namespaces.py
```

## Use cases

- Dashboards and admin UIs  
- Choosing a namespace before search or RAG  
- Monitoring growth and limits  
- Verifying that a delete or create has completed  

## Related

- [Create Namespace](create_namespace.md)  
- [Delete Namespace](delete_namespace.md)  
- [Upload Text Data](upload_text.md)  

## Official references

- [List Namespaces (REST)](https://docs.moorcheh.ai/api-reference/namespaces/list.md)
- [List Namespaces (Python SDK)](https://docs.moorcheh.ai/python-sdk/namespaces/list.md)
