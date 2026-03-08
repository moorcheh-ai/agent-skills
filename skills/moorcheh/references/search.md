# Semantic Search

Perform semantic search across one or multiple namespaces using text queries or vector embeddings with Moorcheh's ITS (Information-Theoretic Scoring) system.

## API

```
POST https://api.moorcheh.ai/v1/search
```

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string or array | Yes | Text query (for text namespaces) or vector (for vector namespaces) |
| `namespaces` | array[string] | Yes | List of namespace names to search across |
| `top_k` | integer | No | Number of results to return (default: 10) |
| `kiosk_mode` | boolean | No | Enable kiosk mode for streamlined results |
| `threshold` | float | No | Minimum ITS relevance score (0.0–1.0) |

### Text Search Example

```bash
curl -X POST "https://api.moorcheh.ai/v1/search" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "query": "machine learning algorithms",
    "namespaces": ["my-documents", "research-papers"],
    "top_k": 10,
    "threshold": 0.25
  }'
```

### Vector Search Example

```bash
curl -X POST "https://api.moorcheh.ai/v1/search" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "query": [0.1, 0.2, 0.3, ...],
    "namespaces": ["my-vectors"],
    "top_k": 5
  }'
```

### Response

```json
{
  "results": [
    {
      "id": "doc-123",
      "score": 0.856432,
      "label": "Close Match",
      "text": "Machine learning algorithms are computational methods...",
      "metadata": {
        "title": "Introduction to ML",
        "category": "education"
      }
    }
  ],
  "execution_time": 0.451749005
}
```

## Advanced Filtering

### Metadata Filters

Use `#key:value` syntax in the query to filter by metadata:

```
"query": "machine learning #category:education"
```

- `#category:tech` — Find documents with category = "tech"
- `#priority:high` — Find high-priority documents
- `#author:john` — Find documents by author "john"

### Keyword Filters

Use `#keyword` to require specific words:

```
"query": "algorithms #important"
```

### Combined Filters

```
"query": "authentication #category:security #important"
```

## ITS Scoring System

Moorcheh uses Information-Theoretic Scoring instead of traditional cosine similarity. ITS provides:
- More nuanced relevance measurements
- Explainable results with relevance labels (e.g., "Close Match", "High Relevance")
- Better performance than traditional vector similarity

## Python SDK

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    # Text-based semantic search
    results = client.similarity_search.query(
        namespaces=["my-documents"],
        query="What is machine learning?",
        top_k=5
    )
    for result in results.get("results", []):
        print(f"[{result['label']}] {result['text']} (Score: {result['score']})")
```

## Script

```bash
uv run skills/moorcheh/scripts/search.py \
  --query "machine learning" \
  --namespaces "my-documents,research-papers" \
  --top-k 10
```
