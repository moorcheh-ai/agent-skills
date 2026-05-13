# Delete Namespace

Permanently delete a namespace and **all** documents or vectors inside it. The operation is **irreversible**.

Deletion is **asynchronous**: the API accepts the request and removes data in the background. Large namespaces may take several minutes; other namespaces remain usable meanwhile.

Documentation index: [llms.txt](https://docs.moorcheh.ai/llms.txt).

## API

```
DELETE https://api.moorcheh.ai/v1/namespaces/{namespace_name}
```

**Headers:** `x-api-key: <your-api-key>` (required). A JSON body is not required.

## Path parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | string | Yes | Namespace to delete |

## Example

```bash
curl -X DELETE "https://api.moorcheh.ai/v1/namespaces/my-old-documents" \
  -H "x-api-key: $MOORCHEH_API_KEY"
```

## Responses

### 202 Accepted

Deletion has been **queued**. Example payload (fields may vary slightly by API version):

```json
{
  "status": "pending",
  "message": "Request accepted. Namespace 'my-documents' has been queued for deletion.",
  "namespace_name": "my-documents",
  "deletion_started_at": "2024-01-15T10:30:00.000Z",
  "estimated_completion": "2024-01-15T10:35:00.000Z"
}
```

Shorter bodies are possible (only `status` + `message`). The API may omit `estimated_completion` for small namespaces.

### 401 Unauthorized

```json
{
  "status": "failure",
  "message": "Unauthorized: Invalid API key"
}
```

### 403 Forbidden

```json
{
  "status": "failure",
  "message": "Forbidden"
}
```

### 404 Not Found

```json
{
  "status": "failure",
  "message": "Namespace 'my-namespace' not found or does not belong to this user."
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

### 500 Server Error

```json
{
  "status": "failure",
  "message": "Internal Server Error processing namespace deletion."
}
```

### Alternate error shape

```json
{
  "error": "Namespace not found",
  "message": "No namespace found with the name 'my-old-documents'.",
  "namespace_name": "my-old-documents"
}
```

## Response fields (typical)

| Field | Type | Description |
|---|---|---|
| `status` | string | e.g. `"pending"` when accepted for async processing |
| `message` | string | Human-readable status |
| `namespace_name` | string | (optional) Namespace being deleted |
| `deletion_started_at` | string | (optional) ISO 8601 when deletion started |
| `estimated_completion` | string | (optional) ISO 8601 estimate when complete |

## Deletion process

1. **Request**- `DELETE` queues namespace removal.  
2. **Background work**- Documents/vectors and metadata are removed.  
3. **Storage**- Quota frees up when processing finishes.  
4. **Indexes**- Search indexes and references are updated.

## Python SDK

```python
from moorcheh_sdk import MoorchehClient, NamespaceNotFound

with MoorchehClient(api_key="your-api-key") as client:
    try:
        client.namespaces.delete(namespace_name="my-temporary-namespace")
        print("[OK] Delete request sent")
    except NamespaceNotFound:
        print("[ERROR] Namespace not found")
```

The SDK may return `None` on success; raw REST clients should handle **202** and the JSON body above.

## Important notes

- **Cannot be undone**- export or back up data first.
- **Async**- confirm completion via [List Namespaces](list_namespaces.md) if needed.
- **Name reuse**- the name may become available again only after deletion completes.
- **Quota**- usage updates after deletion finishes.

## Best practices

- Verify the exact `namespace_name` before calling delete.
- Back up critical data before deletion.
- Plan impact on apps that still reference the namespace.

## Related

- [List Namespaces](list_namespaces.md)- verify namespaces before/after deletion  
- [Create Namespace](create_namespace.md)- create a replacement  
- [Delete Data](delete_data.md)- remove specific IDs without deleting the whole namespace  

## Official references

- [Delete Namespace (REST)](https://docs.moorcheh.ai/api-reference/namespaces/delete.md)
- [Delete Namespace (Python SDK)](https://docs.moorcheh.ai/python-sdk/namespaces/delete.md)
