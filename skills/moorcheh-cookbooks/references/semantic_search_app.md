# Semantic Search App

Build a semantic search application with Moorcheh's ITS scoring, metadata filtering, and relevance-labeled results.

## Architecture

```
Data Sources → Upload to Namespace → User searches → Semantic Search with ITS → Filtered, Labeled Results
```

## Prerequisites

- [Project Setup](project_setup.md)
- [Environment Requirements](environment_requirements.md)

## Implementation

### Step 1: Set Up the Search Namespace

```python
from moorcheh_sdk import MoorchehClient
import time

client = MoorchehClient(api_key="your-api-key")

# Create namespace
client.namespaces.create(namespace_name="search-app", type="text")

# Upload searchable content
articles = [
    {
        "id": "article-1",
        "text": "Introduction to vector databases and their role in modern AI applications.",
        "title": "Vector Databases 101",
        "category": "technology",
        "author": "Alice",
        "published": "2024-06-15"
    },
    {
        "id": "article-2",
        "text": "How semantic search differs from keyword search and why it matters for user experience.",
        "title": "Semantic vs Keyword Search",
        "category": "technology",
        "author": "Bob",
        "published": "2024-07-20"
    }
]
client.documents.upload(namespace_name="search-app", documents=articles)
time.sleep(5)
```

### Step 2: Build Search with Filters

```python
def search(query: str, category: str = None, top_k: int = 10, threshold: float = None) -> list:
    """Perform semantic search with optional metadata filtering."""
    # Build query with metadata filters
    search_query = query
    if category:
        search_query = f"{query} #category:{category}"

    kwargs = {
        "namespaces": ["search-app"],
        "query": search_query,
        "top_k": top_k
    }
    if threshold is not None:
        kwargs["threshold"] = threshold

    results = client.similarity_search.query(**kwargs)

    return [{
        "id": r["id"],
        "text": r["text"],
        "score": r["score"],
        "label": r["label"],
        "metadata": r.get("metadata", {})
    } for r in results.get("results", [])]

# Examples
results = search("how do vector databases work")
results = search("AI applications", category="technology")
results = search("best practices", threshold=0.5)  # Only high-relevance
```

### Step 3: Multi-Namespace Search

```python
def search_all(query: str, namespaces: list = None) -> list:
    """Search across multiple namespaces simultaneously."""
    if namespaces is None:
        # Get all namespaces
        ns_list = client.namespaces.list()
        namespaces = [ns["namespace_name"] for ns in ns_list]

    results = client.similarity_search.query(
        namespaces=namespaces,
        query=query,
        top_k=20
    )
    return results.get("results", [])
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
    threshold: Optional[float] = None
):
    results = search(q, category=category, top_k=top_k, threshold=threshold)
    return {
        "query": q,
        "count": len(results),
        "results": results
    }

# Run with: uvicorn main:app --reload
```

## ITS Scoring Labels

Moorcheh's ITS system provides human-readable relevance labels:

| Label | Meaning |
|---|---|
| Close Match | Very high semantic similarity |
| High Relevance | Strong topical match |
| Moderate Relevance | Related content |
| Low Relevance | Loosely related |
