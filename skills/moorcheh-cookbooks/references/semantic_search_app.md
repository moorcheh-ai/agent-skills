# Semantic Search App

Build a semantic search application with Moorcheh's ITS scoring, metadata filtering (`#key:value` on the query string), and relevance-labeled results.

For **PDF, DOCX, XLSX**, or very large text, index content via **Deep Ingest** (staging namespace + `upload_file`) before searching — see [Deep Ingest](deep_ingest.md) and `skills/moorcheh-cookbooks/scripts/deep_ingest.py`.

## Architecture

```
Data Sources → Upload to Namespace → User searches → Semantic Search with ITS → Filtered, Labeled Results
```

## Prerequisites

- [Project Setup](project_setup.md)
- [Environment Requirements](environment_requirements.md)
- API details: [Search](../../moorcheh/references/search.md)

## Implementation

Use a single `MoorchehClient` for the app lifetime. In short scripts below, `client = MoorchehClient(api_key=...)` is shown; in production prefer `with MoorchehClient(api_key=...) as client:` so connections close cleanly.

### Step 1: Set Up the Search Namespace

```python
from moorcheh_sdk import MoorchehClient
import os
import time

client = MoorchehClient(api_key=os.environ.get("MOORCHEH_API_KEY", "your-api-key"))

# Create namespace (text)
client.namespaces.create(namespace_name="search-app", type="text")

# Upload searchable content (snake_case document fields)
articles = [
    {
        "id": "article-1",
        "text": "Introduction to vector databases and their role in modern AI applications.",
        "title": "Vector Databases 101",
        "category": "technology",
        "author": "Alice",
        "published": "2024-06-15",
    },
    {
        "id": "article-2",
        "text": "How semantic search differs from keyword search and why it matters for user experience.",
        "title": "Semantic vs Keyword Search",
        "category": "technology",
        "author": "Bob",
        "published": "2024-07-20",
    },
]
client.documents.upload(namespace_name="search-app", documents=articles)
time.sleep(5)  # allow async embedding/indexing before first search
```

### Step 2: Build Search with Filters

```python
def search(
    query: str,
    category: str | None = None,
    top_k: int = 10,
    *,
    kiosk_mode: bool = False,
    threshold: float | None = None,
) -> list:
    """Semantic search with optional metadata filters (#category:value)."""
    search_query = query
    if category:
        search_query = f"{query} #category:{category}"

    kwargs: dict = {
        "namespaces": ["search-app"],
        "query": search_query,
        "top_k": top_k,
    }
    if kiosk_mode:
        kwargs["kiosk_mode"] = True
        if threshold is None:
            raise ValueError("kiosk_mode=True requires threshold (min ITS score 0–1)")
        kwargs["threshold"] = threshold
    elif threshold is not None:
        kwargs["threshold"] = threshold

    results = client.similarity_search.query(**kwargs)

    return [
        {
            "id": r["id"],
            "text": r["text"],
            "score": r["score"],
            "label": r["label"],
            "metadata": r.get("metadata", {}),
        }
        for r in results.get("results", [])
    ]


# Examples
results = search("how do vector databases work")
results = search("AI applications", category="technology")
results = search("best practices", kiosk_mode=True, threshold=0.15)
```

### Step 3: Multi-Namespace Search

`namespaces.list()` returns a **dict** with a `namespaces` array. A single search request must not mix **text** and **vector** namespaces — filter to one type (here: **text** only).

```python
def search_all(
    query: str,
    namespaces: list[str] | None = None,
    top_k: int = 20,
) -> list:
    """Search across multiple text namespaces."""
    if namespaces is None:
        listed = client.namespaces.list()
        rows = listed.get("namespaces", []) if isinstance(listed, dict) else listed or []
        namespaces = [
            ns["namespace_name"]
            for ns in rows
            if ns.get("type") == "text"
        ]
        if not namespaces:
            return []

    return client.similarity_search.query(
        namespaces=namespaces,
        query=query,
        top_k=top_k,
    ).get("results", [])
```

### Step 4: FastAPI Search Service

```python
from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI(title="Semantic Search API")


@app.get("/search")
async def search_endpoint(
    q: str = Query(..., description="Search query"),
    category: Optional[str] = None,
    top_k: int = 10,
    kiosk_mode: bool = False,
    threshold: Optional[float] = None,
):
    results = search(q, category=category, top_k=top_k, kiosk_mode=kiosk_mode, threshold=threshold)
    return {"query": q, "count": len(results), "results": results}


# Run with: uvicorn main:app --reload
```

## ITS Scoring Labels

Same bands as the core Moorcheh search reference (ITS score in **0–1**):

| Label | Score range |
|---|---|
| Close Match | score ≥ 0.894 |
| Very High Relevance | 0.632 ≤ score < 0.894 |
| High Relevance | 0.447 ≤ score < 0.632 |
| Good Relevance | 0.316 ≤ score < 0.447 |
| Low Relevance | 0.224 ≤ score < 0.316 |
| Very Low Relevance | 0.1 ≤ score < 0.224 |
| Irrelevant | score < 0.1 |

## Large or binary documents

1. Create a **staging** text namespace and upload with **`documents.upload_file`** (or run `uv run skills/moorcheh-cookbooks/scripts/deep_ingest.py --file path/to/doc.pdf --staging-namespace staging-my-corpus`).
2. [Search](../../moorcheh/references/search.md) that namespace to learn structure, then copy or summarize into your production namespace as needed.
3. Remove staging with `--cleanup` when finished. Full workflow: [Deep Ingest](deep_ingest.md).

## Related

- [Deep Ingest](deep_ingest.md)
- [Search](../../moorcheh/references/search.md)
- [Upload Text Data](../../moorcheh/references/upload_text.md)
- [Upload File](../../moorcheh/references/upload_file.md)
