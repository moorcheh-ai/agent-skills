# AI Q&A System

Build a question-answering system with structured output, custom prompts, multi-namespace search, and temperature control.

## Architecture

```
Multiple Data Sources → Multiple Namespaces → User Question → AI Answer with Structured Output → JSON Response
```

## Prerequisites

- [Project Setup](project_setup.md)
- [Environment Requirements](environment_requirements.md)

## Implementation

### Step 1: Set Up Multi-Namespace Data

```python
from moorcheh_sdk import MoorchehClient
import time

client = MoorchehClient(api_key="your-api-key")

# Create separate namespaces for different knowledge domains
for ns in ["docs-api", "docs-guides", "docs-faq"]:
    client.namespaces.create(namespace_name=ns, type="text")

# Upload API reference docs
client.documents.upload(namespace_name="docs-api", documents=[
    {"id": "api-1", "text": "POST /v1/search — Semantic search endpoint...", "section": "api"},
    {"id": "api-2", "text": "POST /v1/answer — AI generation endpoint...", "section": "api"}
])

# Upload guides
client.documents.upload(namespace_name="docs-guides", documents=[
    {"id": "guide-1", "text": "Getting started with Moorcheh in 5 minutes...", "section": "guide"},
    {"id": "guide-2", "text": "Best practices for semantic search...", "section": "guide"}
])

time.sleep(5)
```

### Step 2: Build Q&A with Structured Output

```python
def qa_structured(question: str, namespace: str = "docs-api") -> dict:
    """Get a structured answer with confidence and sources."""
    response = client.answer.generate(
        namespace=namespace,
        query=question,
        temperature=0.2,  # Low temperature for factual answers
        structuredResponse={"enabled": True},
        headerPrompt="You are a technical documentation assistant. Provide accurate, specific answers.",
        footerPrompt="Include relevant code examples when applicable."
    )

    structured = response.get("structuredData", {})
    return {
        "answer": structured.get("answer", response.get("answer")),
        "confidence": structured.get("confidence", "unknown"),
        "sources": structured.get("sources", []),
        "topics": structured.get("topics", []),
        "follow_up": structured.get("followUpQuestions", [])
    }

result = qa_structured("How do I perform a semantic search?")
print(f"Answer: {result['answer']}")
print(f"Confidence: {result['confidence']}")
print(f"Suggested follow-ups: {result['follow_up']}")
```

### Step 3: Multi-Namespace Q&A Router

```python
def smart_qa(question: str) -> dict:
    """Route questions to the most appropriate namespace."""
    # First, search all namespaces to find the best context
    search_results = client.similarity_search.query(
        namespaces=["docs-api", "docs-guides", "docs-faq"],
        query=question,
        top_k=3
    )

    # Determine best namespace from top results
    results = search_results.get("results", [])
    if not results:
        # Fallback to direct AI mode
        response = client.answer.generate(
            namespace="",
            query=question
        )
        return {"answer": response.get("answer"), "source": "general_ai"}

    # Use the namespace where the best result came from
    best_namespace = "docs-api"  # Default
    # Generate answer
    response = client.answer.generate(
        namespace=best_namespace,
        query=question,
        top_k=5,
        temperature=0.3
    )

    return {
        "answer": response.get("answer"),
        "source": best_namespace,
        "context_count": response.get("contextCount", 0)
    }
```

### Step 4: FastAPI Q&A Service

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Q&A System")

class QARequest(BaseModel):
    question: str
    namespace: str = "docs-api"
    structured: bool = True

class QAResponse(BaseModel):
    answer: str
    confidence: str = None
    sources: list = []
    follow_up: list = []

@app.post("/qa", response_model=QAResponse)
async def qa(request: QARequest):
    if request.structured:
        result = qa_structured(request.question, namespace=request.namespace)
    else:
        response = client.answer.generate(
            namespace=request.namespace,
            query=request.question
        )
        result = {"answer": response.get("answer")}

    return QAResponse(**result)
```

## Temperature Guide

| Temperature | Use Case |
|---|---|
| 0.0–0.3 | Technical documentation, API references |
| 0.3–0.7 | General Q&A, guides |
| 0.7–1.0 | Creative content, brainstorming |
