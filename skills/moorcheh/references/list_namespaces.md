# List Namespaces

List all namespaces in your Moorcheh account. Use this to discover available data before performing search or upload operations.

## API

```
GET https://api.moorcheh.ai/v1/namespaces
```

### Example

```bash
curl -X GET "https://api.moorcheh.ai/v1/namespaces" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -H "Content-Type: application/json"
```

### Response

```json
{
  "namespaces": [
    {
      "namespace_name": "my-documents",
      "type": "text",
      "document_count": 150
    },
    {
      "namespace_name": "my-vectors",
      "type": "vector",
      "vector_dimension": 1536,
      "vector_count": 5000
    }
  ]
}
```

## Python SDK

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    response = client.namespaces.list()
    # SDK returns {"namespaces": [...]}
    for ns in response["namespaces"]:
        print(f"Name: {ns['namespace_name']}, Type: {ns['type']}")
```

## Script

```bash
uv run skills/moorcheh/scripts/list_namespaces.py
```
