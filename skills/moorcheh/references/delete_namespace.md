# Delete Namespace

Permanently delete a namespace and all its data. This action is irreversible.

## API

```
DELETE https://api.moorcheh.ai/v1/namespaces/{namespace_name}
```

### Example

```bash
curl -X DELETE "https://api.moorcheh.ai/v1/namespaces/my-documents" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -H "Content-Type: application/json"
```

### Response

```json
{
  "status": "success",
  "message": "Namespace 'my-documents' deleted successfully."
}
```

## Python SDK

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    client.namespaces.delete("my-documents")
```

## Important Notes

- This action is **irreversible** — all data in the namespace will be permanently deleted
- Always confirm with the user before deleting a namespace
- The namespace must exist, otherwise a 404 error is returned
