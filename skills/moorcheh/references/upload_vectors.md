# Upload Vectors

Upload pre-computed vector embeddings to a vector namespace. Use this when you have your own embedding pipeline.

## API

```
POST https://api.moorcheh.ai/v1/namespaces/{namespace_name}/vectors
```

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `vectors` | array | Yes | Array of vector objects |

### Vector Object

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes | Unique vector identifier |
| `vector` | array[float] | Yes | Vector embedding (must match namespace dimension) |
| `source` | string | No | Source document identifier |
| `index` | integer | No | Position index within the source |

### Example

```bash
curl -X POST "https://api.moorcheh.ai/v1/namespaces/my-vectors/vectors" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "vectors": [
      {
        "id": "vec-1",
        "vector": [0.1, 0.2, 0.3, ...],
        "source": "document-1",
        "index": 0
      }
    ]
  }'
```

## Python SDK

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    vectors = [
        {
            "id": "vec-1",
            "vector": [0.1, 0.2, 0.3, ...],  # Must match namespace dimension
            "source": "document-1",
            "index": 0
        }
    ]
    result = client.upload_vectors(
        namespace_name="my-vectors",
        vectors=vectors
    )
    print(f"Uploaded {result['processed']} vectors")
```

## Important Notes

- Each vector must match the `vector_dimension` set at namespace creation
- The namespace must be of type `"vector"`
- A `400 Vector dimension mismatch` error occurs if dimensions don't match
- Vectors are indexed asynchronously — allow time before searching
