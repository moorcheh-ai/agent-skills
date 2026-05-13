# Upload Vector Data

Upload **pre-computed embeddings** to a **vector** namespace for similarity [Search](search.md). Each vector’s length must match the namespace **`vector_dimension`** set at [Create Namespace](create_namespace.md). Extra fields on each object (beyond `id`, `vector`, and optional `text`) are **metadata**.

Use **snake_case** in JSON bodies and in typical API/SDK responses (`vectors_processed`, `namespace_name`, `failed_vectors`, etc.).

Documentation index: [llms.txt](https://docs.moorcheh.ai/llms.txt).

## Overview

- **Vector namespace only**- type must be `"vector"` with a fixed dimension.
- Moorcheh describes this path as **synchronous**: validated vectors are indexed and become **searchable immediately** (no long “wait for embedding” loop like async text pipelines).
- **Dimension lock**- every `vector` array length must equal the namespace dimension.

## API

```
POST https://api.moorcheh.ai/v1/namespaces/{namespace_name}/vectors
```

**Headers:** `Content-Type: application/json`, `x-api-key: <your-api-key>`

## Path parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | string | Yes | Target **vector** namespace |

## Body

| Field | Type | Required | Description |
|---|---|---|---|
| `vectors` | array | Yes | Non-empty list of vector objects (see limits below) |

### Vector object (flat)

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes | Unique id for this embedding |
| `vector` | array of numbers | Yes | Embedding; length **must** equal namespace dimension |
| `text` | string | No | Optional source text that produced the embedding (useful in search results) |
| *other keys* | any | No | Metadata (filtering, display, model name, etc.) |

**Metadata:** any keys other than `id`, `vector`, and `text` (and you may still store model/source as metadata).

## Request examples

### Single vector

```bash
curl -X POST "https://api.moorcheh.ai/v1/namespaces/my-vectors/vectors" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "vectors": [
      {
        "id": "vec_001",
        "vector": [0.1, -0.2, 0.3, 0.4, -0.5],
        "text": "Machine learning algorithms",
        "source": "openai",
        "model": "text-embedding-3-small",
        "category": "tech"
      }
    ]
  }'
```

The example `vector` length must match how the namespace was created (here length **5** implies a 5-D namespace for demo only).

### Multiple vectors

```bash
curl -X POST "https://api.moorcheh.ai/v1/namespaces/my-vectors/vectors" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "vectors": [
      {
        "id": "prod_001",
        "vector": [0.1, -0.2, 0.3, 0.4],
        "text": "Wireless bluetooth headphones",
        "category": "electronics",
        "price": 99.99,
        "brand": "TechCorp"
      },
      {
        "id": "prod_002",
        "vector": [0.2, 0.1, -0.4, 0.3],
        "text": "Professional gaming mouse",
        "category": "electronics",
        "price": 79.99,
        "brand": "GameGear"
      }
    ]
  }'
```

## Responses

### 201 Created- success

```json
{
  "status": "success",
  "message": "2 vectors uploaded successfully to namespace 'product-embeddings'",
  "upload_id": "upload_vec_1234567890",
  "namespace_name": "product-embeddings",
  "vectors_processed": 2,
  "processing_status": "completed",
  "uploaded_vectors": [
    {
      "id": "prod_001",
      "status": "completed",
      "dimension": 4,
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "prod_002",
      "status": "completed",
      "dimension": 4,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### 207 Multi-Status- partial success

```json
{
  "status": "partial_success",
  "message": "1 out of 2 vectors uploaded successfully. 1 vector failed validation.",
  "upload_id": "upload_vec_1234567891",
  "namespace_name": "my-embeddings",
  "vectors_processed": 1,
  "vectors_failed": 1,
  "uploaded_vectors": [
    {
      "id": "vec_001",
      "status": "completed",
      "dimension": 1536
    }
  ],
  "failed_vectors": [
    {
      "id": "vec_002",
      "error": "Dimension mismatch",
      "message": "Vector dimension (768) does not match namespace dimension (1536)",
      "expected_dimension": 1536,
      "provided_dimension": 768
    }
  ]
}
```

### Errors (examples)

```json
{
  "error": "Invalid request parameters",
  "message": "Vector dimension mismatch. All vectors must have dimension 1536.",
  "details": {
    "namespace_dimension": 1536,
    "provided_dimensions": [1536, 768, 1536],
    "invalid_vectors": ["vectors[1]"]
  }
}
```

```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing API key. Please check your x-api-key header.",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

```json
{
  "error": "Forbidden",
  "message": "Vector upload limit reached for your current tier. Upgrade your plan or delete unused vectors.",
  "details": {
    "current_count": 49950,
    "tier_limit": 50000,
    "tier": "professional",
    "vectors_attempted": 100
  }
}
```

```json
{
  "error": "Namespace not found",
  "message": "No vector namespace found with the name 'my-embeddings' in your account.",
  "namespace_name": "my-embeddings",
  "suggestion": "Create a vector namespace first or check the namespace name."
}
```

## Response fields (success)

| Field | Type | Description |
|---|---|---|
| `status` | string | e.g. `"success"` |
| `message` | string | Summary |
| `upload_id` | string | Batch id |
| `namespace_name` | string | Namespace |
| `vectors_processed` | number | Count processed |
| `processing_status` | string | Often `"completed"` for this route |
| `uploaded_vectors` | array | Per-id status, `dimension`, `created_at`, … |

## Vector requirements

| Topic | Guidance |
|---|---|
| **Dimension** | Must match namespace **exactly** (common model sizes: 384, 512, 768, 1536, 3072, …) |
| **Values** | Floats; **normalized** (e.g. unit length) vectors often work best for cosine-style search |
| **Batch size** | Up to **1000** vectors per request (per Moorcheh docs); **100–500** is a reasonable default for latency |
| **Precision** | Typical **float32**-style values (several decimal places) |

## Common embedding dimensions (reference)

| Model / family | Typical dimension |
|---|---|
| OpenAI `text-embedding-3-large` | 3072 |
| OpenAI `text-embedding-3-small` | 1536 |
| OpenAI `text-embedding-ada-002` | 1536 |
| Sentence-BERT (varies) | 384 or 768 |
| Universal Sentence Encoder | 512 |

Always match the **namespace** `vector_dimension` to the model you use.

## Processing pipeline (conceptual)

1. **Validate dimension** for every vector in the batch  
2. **Validate format** (numeric list, length, etc.)  
3. **Insert into similarity index**  
4. **Store metadata** (and optional `text`)  
5. **Available for search** immediately after success  

---

## Python SDK: `vectors.upload`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | `str` | Yes | Vector namespace |
| `vectors` | `list[dict]` | Yes | Each dict: `id`, `vector` (+ optional `text` and metadata) |

**Returns:** `dict[str, Any]`- upload summary (snake_case fields when normalized by SDK).

**Raises:** `NamespaceNotFound`, `InvalidInputError`, etc.

### Example

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    vectors_to_upload = [
        {
            "id": "image_001.jpg",
            "vector": [0.12, -0.45, 0.23, 0.67],  # length == namespace dimension
            "source": "product_database",
            "category": "electronics",
        },
        {
            "id": "image_002.jpg",
            "vector": [-0.22, 0.81, -0.34, 0.12],
            "source": "product_database",
            "category": "electronics",
        },
    ]

    status = client.vectors.upload(
        namespace_name="my-image-embeddings",
        vectors=vectors_to_upload,
    )
    print(status)
```

### End-to-end (create namespace + upload)

```python
from moorcheh_sdk import MoorchehClient
import numpy as np

with MoorchehClient(api_key="your-api-key") as client:
    dim = 768
    client.namespaces.create(
        namespace_name="product-embeddings",
        type="vector",
        vector_dimension=dim,
    )

    vectors = []
    for i in range(10):
        vec = np.random.randn(dim).astype("float32")
        vec = vec / (np.linalg.norm(vec) + 1e-12)
        vectors.append(
            {
                "id": f"product_{i}",
                "vector": vec.tolist(),
                "category": "electronics",
                "price": 99.99 + i * 10,
            }
        )

    result = client.vectors.upload(
        namespace_name="product-embeddings",
        vectors=vectors,
    )
    print(result.get("message"), result.get("vectors_processed"))
```

## Important notes

- **Never mix dimensions** in one namespace.
- **207 / `partial_success`**- check `failed_vectors` and `vectors_failed`.
- For removing vectors **by id**, use [Delete Data](delete_data.md) (`vectors.delete` / REST vectors delete), not file-name delete.

## Best practices

- Normalize embeddings and keep preprocessing identical for all points in a namespace.
- Use meaningful `id` values and include **`text`** when you want human-readable snippets in UIs or debugging.
- Batch in the **100–500** range unless you have measured headroom toward **1000**.
- Smoke-test [Search](search.md) with a vector query after the first batch.

## Related

- [Create Namespace](create_namespace.md)
- [Search](search.md)
- [Delete Data](delete_data.md)
- [Get Documents](get_documents.md)- text documents by ID; vector workflows may differ by product version (see Moorcheh docs)

## Official references

- [Upload Vector Data (REST)](https://docs.moorcheh.ai/api-reference/data/upload-vector.md)
- [Upload Vector Data (Python SDK)](https://docs.moorcheh.ai/python-sdk/data/upload-vector.md)
