# LangChain Integration

Use Moorcheh as a LangChain vector store for building chains and agents.

## Installation

```bash
pip install langchain-moorcheh moorcheh-sdk
```

## Quick Start

```python
from langchain_moorcheh import MoorchehVectorStore

# Initialize vector store
vectorstore = MoorchehVectorStore(
    api_key="your-api-key",
    namespace="my-documents",
    namespace_type="text"  # or "vector"
)
```

## Adding Documents

```python
from langchain.schema.document import Document

documents = [
    Document(
        page_content="Moorcheh provides semantic search with ITS scoring.",
        metadata={"source": "docs", "category": "technology"}
    ),
    Document(
        page_content="RAG combines retrieval with LLM generation.",
        metadata={"source": "blog", "category": "ai"}
    )
]

vectorstore.add_documents(documents)
```

## Similarity Search

```python
# Basic search
results = vectorstore.similarity_search("semantic search", k=5)

# Search with score
results = vectorstore.similarity_search_with_score("semantic search", k=5)
for doc, score in results:
    print(f"Score: {score:.4f} | {doc.page_content[:80]}")
```

## Use in RAG Chain

```python
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Build RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4"),
    chain_type="stuff",
    retriever=retriever
)

answer = qa_chain.invoke("How does ITS scoring work?")
print(answer)
```

## Configuration Options

| Parameter | Type | Default | Description |
|---|---|---|---|
| `api_key` | str | env var | Moorcheh API key |
| `namespace` | str | required | Namespace name |
| `namespace_type` | str | "text" | "text" or "vector" |
| `base_url` | str | api.moorcheh.ai | API base URL |

## Resources

- [LangChain Integration Docs](https://docs.moorcheh.ai/integrations/langchain/overview)
- [Moorcheh Python SDK](https://docs.moorcheh.ai/python-sdk/introduction)
