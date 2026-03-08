# Knowledge Base RAG

Build a document Q&A system that ingests documents into Moorcheh and generates AI-powered answers with source citations.

## Architecture

```
Documents → Upload to Moorcheh → User asks question → Semantic Search → Context Retrieval → AI Generation → Answer with Sources
```

## Prerequisites

- [Project Setup](project_setup.md)
- [Environment Requirements](environment_requirements.md)

## Implementation

### Step 1: Create Namespace

```python
from moorcheh_sdk import MoorchehClient

client = MoorchehClient(api_key="your-api-key")

# Create a text namespace for the knowledge base
client.namespaces.create(
    namespace_name="knowledge-base",
    type="text"
)
```

### Step 2: Ingest Documents

```python
import os
import json

def load_documents(directory: str) -> list:
    """Load documents from a directory of text/JSON files."""
    documents = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filename.endswith(".txt"):
            with open(filepath, "r") as f:
                documents.append({
                    "id": filename,
                    "text": f.read(),
                    "source": filename,
                    "type": "document"
                })
        elif filename.endswith(".json"):
            with open(filepath, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    documents.extend(data)
    return documents

# Upload documents
docs = load_documents("./data")
client.documents.upload(
    namespace_name="knowledge-base",
    documents=docs
)
print(f"Uploaded {len(docs)} documents")
```

### Step 3: Build the Q&A Function

```python
import time

def ask_knowledge_base(question: str, chat_history: list = None) -> dict:
    """Ask a question against the knowledge base."""
    kwargs = {
        "namespace": "knowledge-base",
        "query": question,
        "top_k": 5,
        "temperature": 0.3  # Low temp for factual answers
    }
    if chat_history:
        kwargs["chatHistory"] = chat_history

    response = client.answer.generate(**kwargs)
    return {
        "answer": response.get("answer"),
        "model": response.get("model"),
        "context_count": response.get("contextCount", 0)
    }

# Wait for indexing
time.sleep(5)

# Ask a question
result = ask_knowledge_base("What are the key features of our product?")
print(f"Answer: {result['answer']}")
print(f"Based on {result['context_count']} source documents")
```

### Step 4: Add Structured Output

```python
def ask_structured(question: str) -> dict:
    """Get a structured answer with sources and confidence."""
    response = client.answer.generate(
        namespace="knowledge-base",
        query=question,
        structuredResponse={"enabled": True}
    )
    return response

result = ask_structured("Summarize the main topics in our knowledge base")
structured = result.get("structuredData", {})
print(f"Answer: {structured.get('answer')}")
print(f"Confidence: {structured.get('confidence')}")
print(f"Topics: {structured.get('topics')}")
print(f"Follow-up questions: {structured.get('followUpQuestions')}")
```

### Step 5: Build a FastAPI Server

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Knowledge Base Q&A")

class Question(BaseModel):
    query: str
    chat_history: list = None

class Answer(BaseModel):
    answer: str
    context_count: int

@app.post("/ask", response_model=Answer)
async def ask(question: Question):
    result = ask_knowledge_base(
        question.query,
        question.chat_history
    )
    return Answer(
        answer=result["answer"],
        context_count=result["context_count"]
    )

# Run with: uvicorn main:app --reload
```

## Deployment

1. Set `MOORCHEH_API_KEY` in your deployment environment
2. Upload your documents to the `knowledge-base` namespace
3. Deploy the FastAPI server
4. Optionally add a [Frontend Interface](frontend_interface.md)
