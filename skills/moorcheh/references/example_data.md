# Example Data

Create sample data for demos and testing when no data is available or the user wants to test Moorcheh functionality.

## Usage

Run the example data script to create a namespace and populate it with sample documents:

```bash
uv run skills/moorcheh/scripts/example_data.py --namespace "demo-namespace"
```

## What Gets Created

The script creates a text namespace called `demo-namespace` (or your chosen name) and uploads sample documents covering:

- **Technology** — Articles about AI, machine learning, cloud computing
- **Science** — Documents about physics, biology, chemistry
- **Business** — Content about startups, marketing, finance

Each document includes metadata fields (`category`, `author`, `difficulty`) for demonstrating filtered search.

## Python SDK Example

```python
import time
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    namespace = "demo-namespace"

    # 1. Create namespace
    client.namespaces.create(namespace_name=namespace, type="text")

    # 2. Upload sample documents
    docs = [
        {
            "id": "demo-1",
            "text": "Artificial intelligence is transforming healthcare through improved diagnostics and personalized treatment plans.",
            "category": "technology",
            "author": "Dr. Chen",
            "difficulty": "beginner"
        },
        {
            "id": "demo-2",
            "text": "Quantum computing leverages quantum mechanical phenomena to process information in fundamentally new ways.",
            "category": "science",
            "author": "Prof. Johnson",
            "difficulty": "advanced"
        },
        {
            "id": "demo-3",
            "text": "Effective startup growth requires a balance of product-market fit, user acquisition, and sustainable unit economics.",
            "category": "business",
            "author": "Sarah Kim",
            "difficulty": "intermediate"
        }
    ]
    client.documents.upload(namespace_name=namespace, documents=docs)

    # 3. Wait for indexing
    time.sleep(5)

    # 4. Test search
    results = client.similarity_search.query(
        namespaces=[namespace],
        query="How is AI used in medicine?"
    )
    for r in results.get("results", []):
        print(f"[{r['label']}] {r['text'][:80]}... (Score: {r['score']:.3f})")
```
