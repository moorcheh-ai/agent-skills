# Upload Text Data

Upload **text documents** to a **text** namespace so Moorcheh can embed and index them for [Search](search.md), [Get Documents](get_documents.md), and RAG ([Generate AI Answer](generate_answer.md)). Processing is **asynchronous**; embeddings are generated in the cloud (e.g. Amazon Bedrock per Moorcheh product docs).

Use **snake_case** in JSON bodies and prefer snake_case keys in response handling (`documents_processed`, `namespace_name`, `uploaded_documents`, `failed_documents`, etc.).

Documentation index: [llms.txt](https://docs.moorcheh.ai/llms.txt).

## API

```
POST https://api.moorcheh.ai/v1/namespaces/{namespace_name}/documents
```

**Headers:** `Content-Type: application/json`, `x-api-key: <your-api-key>`

## Path parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | string | Yes | Target **text** namespace |

## Body

| Field | Type | Required | Description |
|---|---|---|---|
| `documents` | array | Yes | Non-empty array of document objects (max **100** per request) |

### Document object (flat)

Each element of `documents` is a **flat** object:

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string \| number | Yes | Unique document id within the namespace (non-empty) |
| `text` | string | Yes | Main body text |
| *any other keys* | any | No | Treated as **metadata** (filtering, display, etc.) |

**Metadata:** every key other than `id` and `text` is metadata. Metadata is optional but recommended; keep schemas consistent across documents.

## Request examples

### Single document

```bash
curl -X POST "https://api.moorcheh.ai/v1/namespaces/demo-namespace/documents" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "documents": [
      {
        "id": "doc_001",
        "text": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.",
        "title": "Introduction to Machine Learning",
        "category": "education",
        "difficulty": "beginner",
        "author": "Dr. Smith"
      }
    ]
  }'
```

### Multiple documents

```bash
curl -X POST "https://api.moorcheh.ai/v1/namespaces/demo-namespace/documents" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "documents": [
      {
        "id": "doc_001",
        "text": "API authentication requires including your API key in the x-api-key header for all requests.",
        "title": "API Authentication Guide",
        "category": "security",
        "priority": "high"
      },
      {
        "id": "doc_002",
        "text": "Rate limiting protects our service by limiting the number of requests per hour. Premium users have higher limits.",
        "title": "Rate Limiting Policy",
        "category": "policy",
        "priority": "medium"
      }
    ]
  }'
```

## Responses

### 202 Accepted- success

```json
{
  "status": "success",
  "message": "2 documents uploaded successfully to namespace 'technical-docs'",
  "upload_id": "upload_1234567890",
  "namespace_name": "technical-docs",
  "documents_processed": 2,
  "processing_status": "in_progress",
  "estimated_completion": "2024-01-15T10:35:00Z",
  "uploaded_documents": [
    {
      "id": "doc_001",
      "status": "processing",
      "character_count": 89
    },
    {
      "id": "doc_002",
      "status": "processing",
      "character_count": 112
    }
  ]
}
```

### 207 Multi-Status- partial success

```json
{
  "status": "partial_success",
  "message": "2 out of 3 documents uploaded successfully. 1 document failed validation.",
  "upload_id": "upload_1234567891",
  "namespace_name": "my-documents",
  "documents_processed": 2,
  "documents_failed": 1,
  "uploaded_documents": [
    {
      "id": "doc_001",
      "status": "processing",
      "character_count": 156
    },
    {
      "id": "doc_002",
      "status": "processing",
      "character_count": 203
    }
  ],
  "failed_documents": [
    {
      "id": "doc_003",
      "error": "Text content too short",
      "message": "Document text must be at least 10 characters long",
      "provided_length": 3
    }
  ]
}
```

### Common error shapes

Responses may use either `status` + `message` or top-level `error` + `message` depending on route/version- always read the body and HTTP code.

```json
{
  "status": "failure",
  "message": "Bad Request: Each document in 'documents' must have a non-empty 'id' (string or number)."
}
```

```json
{
  "error": "Invalid request parameters",
  "message": "Documents array is required and must contain at least one document",
  "details": {
    "field": "documents",
    "requirement": "Array with minimum 1 document"
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
  "message": "Document upload limit reached for your current tier. Upgrade your plan or delete unused documents.",
  "details": {
    "current_count": 9985,
    "tier_limit": 10000,
    "tier": "professional",
    "documents_attempted": 25
  }
}
```

```json
{
  "error": "Namespace not found",
  "message": "No text namespace found with the name 'my-documents' in your account.",
  "namespace_name": "my-documents",
  "suggestion": "Create the namespace first or check the namespace name."
}
```

## Response fields (202)

| Field | Type | Description |
|---|---|---|
| `status` | string | e.g. `"success"` |
| `message` | string | Human-readable summary |
| `upload_id` | string | Batch / job identifier |
| `namespace_name` | string | Target namespace |
| `documents_processed` | number | Count accepted for processing |
| `processing_status` | string | e.g. `in_progress`, `completed`, `failed` |
| `estimated_completion` | string | ISO 8601 estimate (when provided) |
| `uploaded_documents` | array | Per-doc status: `id`, `status`, `character_count`, … |
| `documents_failed` | number | (207) Count that failed validation |
| `failed_documents` | array | (207) Per-doc error objects with `id`, `error`, `message`, … |

## Processing pipeline (high level)

1. **Validate**- format, size, content rules  
2. **Normalize**- text cleanup / preparation  
3. **Embed**- vector generation (e.g. Bedrock-backed)  
4. **Index**- make content available to search and RAG  
5. **Metadata**- optional enrichment / storage of extra fields  

## Document limits

| Constraint | Value |
|---|---|
| **Text length** | **Min** 10 characters; **max** 50,000 characters per document |
| **Batch size** | **Max** 100 documents per HTTP request |
| **Recommended batch** | 25–50 documents for latency and stability |
| **Metadata** | Up to ~**2KB** per document and ~**50** metadata keys (per product docs; confirm in OpenAPI if strict) |
| **Processing time** | Often seconds per doc; large batches can take longer |

**Per-request cap:** never send more than **100** documents in one `documents` array.

## Python SDK: `documents.upload`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | `str` | Yes | Text namespace |
| `documents` | `list[dict]` | Yes | Each dict: required `id`, `text`; other keys = metadata |

**Returns:** `dict[str, Any]`- queued upload status (same snake_case fields as REST when normalized by the SDK).

**Raises:** `NamespaceNotFound`, `InvalidInputError`, etc.

### Example

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    documents_to_upload = [
        {
            "id": "faq-1",
            "text": "To reset your password, go to the account settings page.",
            "category": "account",
        },
        {
            "id": "faq-2",
            "text": "Our return policy allows returns within 30 days of purchase.",
            "category": "shipping",
        },
    ]

    status = client.documents.upload(
        namespace_name="my-faq-documents",
        documents=documents_to_upload,
    )
    print(status)
```

### Rich metadata example

```python
documents = [
    {
        "id": "article-123",
        "text": "Full article content here...",
        "title": "Introduction to Machine Learning",
        "author": "Dr. Smith",
        "category": "education",
        "publish_date": "2024-01-15",
        "tags": ["ml", "ai", "tutorial"],
        "difficulty": "beginner",
    }
]
```

### End-to-end workflow

```python
from moorcheh_sdk import MoorchehClient
import time

with MoorchehClient(api_key="your-api-key") as client:
    client.namespaces.create(namespace_name="my-data", type="text")

    docs = [
        {
            "id": "doc-1",
            "text": "This is the first document with enough characters for validation.",
            "category": "tutorial",
            "author": "John Doe",
        },
        {
            "id": "doc-2",
            "text": "This is the second document with enough characters for validation.",
            "category": "guide",
            "author": "Jane Smith",
        },
    ]

    upload_result = client.documents.upload(namespace_name="my-data", documents=docs)
    print(f"Upload status: {upload_result}")

    print("[WAIT] Waiting for embedding and indexing...")
    time.sleep(5)
```

## Important notes

- **Async**- wait briefly before [Search](search.md) or [Get Documents](get_documents.md).
- **Duplicate `id`**- uploading the same `id` again typically **overwrites** the prior document in that namespace; confirm intent.
- **Partial batches**- inspect `failed_documents` / `documents_failed` when `status` is `partial_success` (207).
- **Namespace type** must be **`text`**.

## Best practices

- One main topic per document; split very long texts into multiple ids.
- Consistent metadata keys for filtering (`#category:value` in search).
- Meaningful, stable `id` values for later [Get Documents](get_documents.md) and [Delete Data](delete_data.md).
- Batch in the **25–50** range when possible; never exceed **100** per request.
- Retry transient **5xx** with backoff.

## Script

```bash
uv run skills/moorcheh/scripts/upload_text.py \
  --namespace "my-documents" \
  --file "data.json"
```

JSON file: either a top-level array of documents or `{"documents": [...]}`.

## Related

- [Create Namespace](create_namespace.md)
- [Get Documents](get_documents.md)
- [Search](search.md)
- [Delete Data](delete_data.md)
- [Upload File](upload_file.md)

## Official references

- [Upload Text Data (REST)](https://docs.moorcheh.ai/api-reference/data/upload-text.md)
- [Upload Text Data (Python SDK)](https://docs.moorcheh.ai/python-sdk/data/upload-text.md)
