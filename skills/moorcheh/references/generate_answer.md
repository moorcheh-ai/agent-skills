# Generate AI Answer

Generate AI-powered answers from your data using Retrieval-Augmented Generation (RAG). Searches relevant context from a namespace and synthesizes a natural-language answer.

## API

```
POST https://api.moorcheh.ai/v1/answer
```

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | Yes | The question to answer |
| `namespace` | string | Yes | Namespace to search for context (use `""` for direct AI mode) |
| `top_k` | integer | No | Number of context documents (default: 5) |
| `threshold` | float | No | Minimum relevance score for context |
| `temperature` | float | No | Response creativity (0.0–2.0, default: 0.7) |
| `type` | string | No | Namespace type: `"text"` or `"vector"` |
| `aiModel` | string | No | AI model to use (default: `anthropic.claude-sonnet-4-6`). **Important:** always pass this parameter explicitly — older SDK versions default to a model ID that returns 500 errors from Bedrock. |
| `chatHistory` | array | No | Previous conversation turns |
| `headerPrompt` | string | No | System prompt prepended to context |
| `footerPrompt` | string | No | Instructions appended after context |
| `structuredResponse` | object | No | Enable structured JSON output |

### Search Mode (with namespace)

```bash
curl -X POST "https://api.moorcheh.ai/v1/answer" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "namespace": "my-documents",
    "query": "What are the main benefits of Moorcheh?",
    "type": "text",
    "top_k": 5
  }'
```

### Direct AI Mode (no namespace)

```bash
curl -X POST "https://api.moorcheh.ai/v1/answer" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "namespace": "",
    "query": "Explain the difference between semantic and keyword search"
  }'
```

### With Chat History

```bash
curl -X POST "https://api.moorcheh.ai/v1/answer" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "namespace": "my-documents",
    "query": "Can you elaborate on the second point?",
    "chatHistory": [
      { "role": "user", "content": "What are key features?" },
      { "role": "assistant", "content": "The key features are..." }
    ]
  }'
```

### With Structured Output

```bash
curl -X POST "https://api.moorcheh.ai/v1/answer" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "namespace": "my-documents",
    "query": "Summarize the key points",
    "structuredResponse": {
      "enabled": true
    }
  }'
```

### Response

```json
{
  "answer": "The main benefits include higher accuracy through ITS scoring, better performance with MIB technology, and explainable results...",
  "model": "anthropic.claude-sonnet-4-6",
  "contextCount": 3,
  "query": "What are the main benefits of Moorcheh?"
}
```

### Structured Response

When `structuredResponse.enabled` is `true`, the response includes:
- `answer` — Plain text answer
- `confidence` — Confidence level
- `sources` — Source document references
- `summary` — Brief summary
- `topics` — Extracted topics
- `followUpQuestions` — Suggested follow-up questions

## Temperature Guide

- **0.0–0.5**: Conservative, factual — best for technical documentation
- **0.5–1.0**: Balanced — good for general Q&A
- **1.0–2.0**: Creative — use carefully for factual content

## Python SDK

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    # Basic RAG answer
    response = client.answer.generate(
        namespace="my-documents",
        query="What are the main benefits of Moorcheh?",
        ai_model="anthropic.claude-sonnet-4-6"
    )
    print(f"Answer: {response['answer']}")

    # With chat history
    response = client.answer.generate(
        namespace="my-documents",
        query="Tell me more about the second point",
        chat_history=[
            {"role": "user", "content": "What are key features?"},
            {"role": "assistant", "content": "The key features are..."}
        ]
    )
```

## Script

```bash
uv run skills/moorcheh/scripts/generate_answer.py \
  --namespace "my-documents" \
  --query "What are the main benefits of Moorcheh?"
```

## Use Cases

- **Customer Support**: Answer questions using documentation
- **Internal Q&A**: Help employees find answers in knowledge bases
- **Educational Tools**: Create AI tutors using educational content
- **Research Assistance**: Get insights from research papers
- **Technical Support**: Provide answers based on technical docs
