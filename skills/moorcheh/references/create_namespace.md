# Create Namespace

Create a new namespace to organize and store your data. Namespaces can be text-based (automatic embedding) or vector-based (pre-computed embeddings).

## API

```
POST https://api.moorcheh.ai/v1/namespaces
```

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | string | Yes | Unique name for the namespace |
| `type` | string | Yes | `"text"` or `"vector"` |
| `vector_dimension` | integer | When type=vector | Dimension of vector embeddings (e.g. 1536) |

### Text Namespace (automatic embedding)

```bash
curl -X POST "https://api.moorcheh.ai/v1/namespaces" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "namespace_name": "my-documents",
    "type": "text"
  }'
```

### Vector Namespace (pre-computed embeddings)

```bash
curl -X POST "https://api.moorcheh.ai/v1/namespaces" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "namespace_name": "my-vectors",
    "type": "vector",
    "vector_dimension": 1536
  }'
```

### Response

```json
{
  "status": "success",
  "message": "Namespace 'my-documents' created successfully. ✅",
  "namespace_name": "my-documents"
}
```

## Python SDK

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    # Create a text namespace
    client.namespaces.create(
        namespace_name="my-documents",
        type="text"
    )

    # Create a vector namespace
    client.namespaces.create(
        namespace_name="my-vectors",
        type="vector",
        vector_dimension=1536
    )
```

## Script

```bash
uv run skills/moorcheh/scripts/create_namespace.py \
  --name "my-documents" \
  --type "text"
```

## Important Notes

- Namespace type cannot be changed after creation
- Vector dimension must be specified for vector namespaces and cannot be modified later
- Namespace names must be unique within your account
- Namespace creation counts toward your tier limits
