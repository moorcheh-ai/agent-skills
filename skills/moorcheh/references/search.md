# Search

Perform semantic search across **one or more namespaces** using a **text query** or a **vector** (list of floats). Moorcheh ranks hits with **ITS** (Information Theoretic Similarity) and returns human-readable **labels** (for example "Close Match", "High Relevance").

Text queries support **automatic embedding**; vector queries must match **vector** namespaces whose dimension matches your vectors. In a single request, **all `namespaces` must be the same type** (all text or all vector).

Documentation index: [llms.txt](https://docs.moorcheh.ai/llms.txt).

## API

```
POST https://api.moorcheh.ai/v1/search
```

**Headers:** `Content-Type: application/json`, `x-api-key: <your-api-key>`

Use **snake_case** in JSON bodies (`namespaces`, `top_k`, `kiosk_mode`, `threshold`, …).

## Body parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `query` | string \| array of numbers | Yes | Text (with optional `#` filters) or embedding vector for vector search |
| `namespaces` | array of strings | Yes | Namespace names to search. All must be **text** or all **vector** (same type) |
| `top_k` | number | No | Max hits across namespaces (default **10**) |
| `kiosk_mode` | boolean | No | When `true`, filters low-relevance chunks; **`threshold` is then required** |
| `threshold` | number | If `kiosk_mode` | Minimum ITS score in **0–1** |

## Advanced filtering (text `query`)

### Metadata filters

Append `#key:value` to the query string (values with spaces: use **hyphens** instead of spaces in the value):

- `#category:tech`- metadata `category` equals `tech`
- `#priority:high`
- `#author:john`

### Keyword filters

Append `#word` so the match should involve that token in content:

- `#important` `#urgent`

### Combined

Example: `authentication #category:security #important`- semantic part first, filters **after**.

**Important:** Put **filter tokens at the end** of the query string. Use **hyphens** inside filter values instead of spaces (e.g. `#status:in-progress`).

## Request examples

### Basic text search (with kiosk mode)

```bash
curl -X POST "https://api.moorcheh.ai/v1/search" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "query": "machine learning algorithms",
    "namespaces": ["my-documents", "research-papers"],
    "top_k": 10,
    "kiosk_mode": true,
    "threshold": 0.15
  }'
```

### Search with metadata filter

```bash
curl -X POST "https://api.moorcheh.ai/v1/search" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "query": "authentication #category:security",
    "namespaces": ["tech-docs", "security-guides"],
    "top_k": 15,
    "kiosk_mode": true,
    "threshold": 0.2
  }'
```

### Vector search

```bash
curl -X POST "https://api.moorcheh.ai/v1/search" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "query": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
    "namespaces": ["vector-embeddings"],
    "top_k": 5,
    "kiosk_mode": false
  }'
```

### Combined semantic + filters

```bash
curl -X POST "https://api.moorcheh.ai/v1/search" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "query": "machine learning #category:research #published",
    "namespaces": ["research-papers", "academic-docs"],
    "top_k": 25,
    "kiosk_mode": true,
    "threshold": 0.15
  }'
```

## Response

### 200- Success

```json
{
  "results": [
    {
      "id": "doc-123",
      "score": 0.856432,
      "label": "Close Match",
      "text": "Machine learning algorithms are computational methods that enable systems to automatically learn and improve from experience.",
      "metadata": {
        "title": "Introduction to ML",
        "category": "education",
        "tags": ["machine-learning", "algorithms"]
      }
    },
    {
      "id": "doc-456",
      "score": 0.512345,
      "label": "High Relevance",
      "text": "Deep learning is a subset of machine learning that uses neural networks with multiple layers.",
      "metadata": {
        "author": "John Doe",
        "published": "2024-01-15"
      }
    }
  ],
  "execution_time": 0.451749005,
  "timings": {
    "authorize": 0.267880763,
    "parse_validate": 0.000720582,
    "validate_namespace": 0.01685079,
    "fetch_data": 0.037917629,
    "calculate_scores": 0.001484341,
    "total": 0.451749005
  },
  "optimization_info": {
    "fetch_strategy": "single_phase_with_early_filtering",
    "initial_fetch": "complete_data_with_early_filtering",
    "complete_fetch": "no_additional_fetch_needed"
  }
}
```

`timings` may include more phase keys than shown above; `optimization_info` describes the path the server took for that request.

### 200- No hits

```json
{
  "results": [],
  "execution_time": 0.042,
  "timings": {
    "authorize": 0.02,
    "parse_validate": 0.001,
    "validate_namespace": 0.008,
    "fetch_data": 0.01,
    "calculate_scores": 0.001,
    "total": 0.042
  },
  "optimization_info": {
    "fetch_strategy": "single_phase_with_early_filtering",
    "initial_fetch": "complete_data_with_early_filtering",
    "complete_fetch": "no_additional_fetch_needed"
  }
}
```

### Result item fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Chunk / document identifier |
| `score` | number | ITS score in **0–1** |
| `label` | string | Human-readable band for the score |
| `text` | string | Chunk text (text namespaces) |
| `metadata` | object | Custom metadata |

### Performance fields

| Field | Type | Description |
|---|---|---|
| `execution_time` | number | Wall-clock seconds for the search |
| `timings` | object | Per-phase timings; keys are **snake_case** in current docs (`parse_validate`, `validate_namespace`, …). If you see legacy camelCase (`parseValidate`, …), treat both shapes as opaque diagnostics until normalized. |
| `optimization_info` | object | Fetch / filter strategy metadata |

### Errors

```json
{ "status": "failure", "message": "Bad Request: query field is required" }
```

```json
{
  "status": "failure",
  "message": "Forbidden: Missing API Key information.",
  "timings": { "authorize": 0.001, "total": 0.002 }
}
```


Other common HTTP statuses: **403** Forbidden, **404** namespace not found, **429** rate limit, **500** server error (payload shapes similar to other Moorcheh APIs - prefer `error` + `message` or `status` + `message` depending on route).

## ITS scoring (labels)

| Label | Score range |
|---|---|
| Close Match | score ≥ 0.894 |
| Very High Relevance | 0.632 ≤ score < 0.894 |
| High Relevance | 0.447 ≤ score < 0.632 |
| Good Relevance | 0.316 ≤ score < 0.447 |
| Low Relevance | 0.224 ≤ score < 0.316 |
| Very Low Relevance | 0.1 ≤ score < 0.224 |
| Irrelevant | score < 0.1 |

## Python SDK: `similarity_search.query`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `namespaces` | `list[str]` | Yes | One or more namespaces (same type) |
| `query` | `str` \| `list[float]` | Yes | Text (with optional `#` filters) or query vector |
| `top_k` | `int` | No | Default **10** |
| `threshold` | `float` \| `None` | If `kiosk_mode=True` | Minimum ITS score **0–1** |
| `kiosk_mode` | `bool` | No | Default **False**; if `True`, pass `threshold` |

**Returns:** `dict[str, Any]` with at least `results`; often also `execution_time`, `timings`, `optimization_info`.

**Raises:** `NamespaceNotFound`, `InvalidInputError`, etc.

### Basic example

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    results = client.similarity_search.query(
        namespaces=["my-faq-documents"],
        query="How long do I have to return an item?",
        top_k=5,
    )

    for result in results.get("results", []):
        print(f"Score: {result['score']:.3f}")
        print(f"Text: {result['text'][:100]}...")
        print("---")
```

### Multi-namespace + threshold

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    results = client.similarity_search.query(
        namespaces=["faq-documents", "policy-documents"],
        query="return policy",
        top_k=5,
        threshold=0.7,
    )

    for result in results["results"]:
        print(f"ID: {result['id']}")
        print(f"Score: {result['score']:.3f}")
        print(f"Text: {result['text'][:100]}...")
        print("---")
```

### Vector query + kiosk mode

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    query_vector = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]  # length must match namespace dimension

    results = client.similarity_search.query(
        namespaces=["vector-embeddings"],
        query=query_vector,
        top_k=10,
        kiosk_mode=True,
        threshold=0.5,
    )

    for result in results.get("results", []):
        print(f"Similarity: {result['score']:.3f}")
```

### End-to-end (text namespace)

```python
from moorcheh_sdk import MoorchehClient
import time

with MoorchehClient(api_key="your-api-key") as client:
    namespace = "customer-support"

    client.namespaces.create(namespace_name=namespace, type="text")

    support_docs = [
        {
            "id": "policy-1",
            "text": "Our return policy allows returns within 30 days of purchase with original receipt.",
            "category": "returns",
        },
        {
            "id": "policy-2",
            "text": "We offer free shipping on orders over $50. Standard shipping takes 3-5 business days.",
            "category": "shipping",
        },
    ]

    client.documents.upload(namespace_name=namespace, documents=support_docs)
    print("[WAIT] Documents uploaded; waiting for indexing...")
    time.sleep(5)

    search_results = client.similarity_search.query(
        namespaces=[namespace],
        query="return policy",
        top_k=2,
    )

    for result in search_results["results"]:
        print(f"Score: {result['score']:.3f} | ID: {result['id']}")
        print(f"Text: {result['text'][:80]}...")
        print()
```

### Error handling

```python
from moorcheh_sdk import MoorchehClient, NamespaceNotFound, InvalidInputError

try:
    with MoorchehClient(api_key="your-api-key") as client:
        results = client.similarity_search.query(
            namespaces=["my-namespace"],
            query="search query",
            top_k=5,
        )
        if results["results"]:
            print(f"Found {len(results['results'])} results")
        else:
            print("No results found")
except NamespaceNotFound:
    print("One or more namespaces do not exist")
except InvalidInputError as e:
    print(f"Invalid search parameters: {e}")
```

## Best practices

- Prefer clear, specific natural-language queries.
- When using **`kiosk_mode`**, always set **`threshold`**.
- Tune **`top_k`** for latency vs coverage.
- Use multiple namespaces only when they share the same **type** (all text or all vector).

## Script

```bash
uv run skills/moorcheh/scripts/search.py \
  --query "machine learning" \
  --namespaces "my-documents,research-papers" \
  --top-k 10

# With kiosk mode (requires threshold):
uv run skills/moorcheh/scripts/search.py \
  --query "machine learning" \
  --namespaces "my-documents" \
  --top-k 10 \
  --kiosk-mode \
  --threshold 0.15
```

## Related

- [Upload Text Data](upload_text.md) / [Upload File](upload_file.md)
- [Get Documents](get_documents.md)- fetch by document ID
- [List Files](list_files.md)- storage objects after upload
- [Upload Vectors](upload_vectors.md)
- [Fetch Text Data](fetch_text_data.md)- list chunks in a text namespace (not ranked search)
- [List Namespaces](list_namespaces.md)
- [Generate AI Answer](generate_answer.md)

## Official references

- [Search (REST)](https://docs.moorcheh.ai/api-reference/search/query.md)
- [Search (Python SDK)](https://docs.moorcheh.ai/python-sdk/search/query.md)
