# Generate AI Answer

Generate AI-powered answers from your data using Retrieval-Augmented Generation (RAG), or call the model directly without a namespace. The API supports **Search Mode** (with namespace) and **Direct AI Mode** (empty namespace).

Documentation index: [llms.txt](https://docs.moorcheh.ai/llms.txt).

## API

```
POST https://api.moorcheh.ai/v1/answer
```

**Headers:** `Content-Type: application/json`, `x-api-key: <MOORCHEH_API_KEY>`

### Naming (snake_case)

Use **snake_case** for all JSON request and response fields. Legacy camelCase aliases were removed in **platform version 1.5.10** (May 2026). Send only snake_case in curl, backends, and the Python SDK.

## Body parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `query` | string | Yes | The user's question |
| `namespace` | string | Yes | Namespace for Search Mode, or `""` for Direct AI Mode |
| `top_k` | number | No | Top relevant chunks (default: 10) |
| `threshold` | number | No | Minimum ITS relevance (0–1). Required when `kiosk_mode` is true |
| `temperature` | number | No | Creativity 0.0–2.0 (default: 0.7) |
| `type` | string | No | Search type: `"text"` (default) |
| `ai_model` | string | No | Model ID (see table below). Prefer setting explicitly- some SDK defaults can hit Bedrock errors |
| `kiosk_mode` | boolean | No | When true, filter low-relevance chunks; `threshold` is then required |
| `chat_history` | array | No | Prior turns: `{ "role": "user"|"assistant", "content": "..." }` |
| `header_prompt` | string | No | Custom instruction / system-style behavior |
| `footer_prompt` | string | No | Appended instruction (default behavior similar to “clear and concise answer”) |
| `structured_response` | object | No | `{ "enabled": true, ... }` for JSON in `structured_data` |

### Field restrictions

**Direct AI Mode** (`namespace: ""`): only these fields are allowed: `namespace`, `query`, `temperature`, `chat_history`, `footer_prompt`, `header_prompt`, `ai_model`, `structured_response`.

**Search Mode** (non-empty namespace): all fields above are allowed, including `top_k`, `threshold`, `type`, `kiosk_mode`.

## Available models

| Model ID | Name | Provider | Credits |
|---|---|---|---|
| `anthropic.claude-sonnet-4-6` | Claude Sonnet 4.6 | Anthropic | 3 |
| `anthropic.claude-opus-4-6-v1` | Claude Opus 4.6 | Anthropic | 3 |
| `meta.llama4-maverick-17b-instruct-v1:0` | Llama 4 Maverick 17B | Meta | 3 |
| `amazon.nova-pro-v1:0` | Amazon Nova Pro | Amazon | 2 |
| `deepseek.r1-v1:0` | DeepSeek R1 | DeepSeek | 1 |
| `deepseek.v3.2` | DeepSeek V3.2 | DeepSeek | 2 |
| `openai.gpt-oss-120b-1:0` | OpenAI GPT OSS 120B | OpenAI | 3 |
| `qwen.qwen3-32b-v1:0` | Qwen 3 32B | Qwen | 2 |
| `qwen.qwen3-next-80b-a3b` | Qwen3 Next 80B A3B | Qwen | 1 |

## Examples

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

### Direct AI Mode (empty namespace)

```bash
curl -X POST "https://api.moorcheh.ai/v1/answer" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "namespace": "",
    "query": "Explain quantum computing in simple terms",
    "ai_model": "deepseek.r1-v1:0",
    "temperature": 0.7,
    "chat_history": [
      {"role": "user", "content": "What is AI?"},
      {"role": "assistant", "content": "AI is artificial intelligence..."}
    ],
    "header_prompt": "You are a science teacher.",
    "footer_prompt": "Use simple language and examples."
  }'
```

### With chat history (Search Mode)

```bash
curl -X POST "https://api.moorcheh.ai/v1/answer" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "namespace": "my-documents",
    "query": "Can you elaborate on the second point?",
    "chat_history": [
      { "role": "user", "content": "What are key features?" },
      { "role": "assistant", "content": "The key features are..." }
    ]
  }'
```

### Structured output (default schema)

```bash
curl -X POST "https://api.moorcheh.ai/v1/answer" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "namespace": "my-documents",
    "query": "Summarize the key points",
    "structured_response": { "enabled": true }
  }'
```

## Response fields

| Field | Type | Description |
|---|---|---|
| `answer` | string | Generated answer |
| `model` | string | Model ID used |
| `context_count` | number | Chunks used for RAG |
| `query` | string | Echo of the submitted query |
| `used_context` | boolean | When structured output is used: whether RAG context was applied |
| `structured_data` | object | Present when `structured_response.enabled` is true |

### Structured output

With `structured_response: { "enabled": true }`, `structured_data` follows your schema or the **default schema** (snake_case keys), including e.g. `answer`, `confidence`, `sources`, `summary`, `topics`, `follow_up_questions`. Optional keys on `structured_response`: `schema`, `tool_name`, `tool_description`.

### Example responses (HTTP 200)

#### Unstructured answer

```json
{
  "answer": "Serverless architecture offers reduced ops cost, automatic scaling, and faster delivery...",
  "model": "deepseek.r1-v1:0",
  "context_count": 3,
  "query": "What are the main benefits of using serverless architecture?"
}
```

#### Structured output (`structured_response.enabled`)

```json
{
  "answer": "The main answer to the user's query",
  "model": "deepseek.r1-v1:0",
  "context_count": 3,
  "query": "What are the system requirements?",
  "used_context": true,
  "structured_data": {
    "answer": "The main answer to the user's query",
    "confidence": 0.92,
    "sources": [
      { "id": "chunk-1", "relevance": "high" },
      { "id": "chunk-3", "relevance": "medium" }
    ],
    "summary": "Short summary under 200 chars.",
    "topics": ["requirements", "compatibility", "hardware"],
    "follow_up_questions": ["Does it support Windows 11?", "What about Mac M1?"]
  }
}
```

### Common errors

```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing API key. Please check your x-api-key header.",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

```json
{
  "status": "failure",
  "message": "Bad Request: kiosk_mode requires threshold to be set."
}
```

```json
{
  "error": "Namespace not found",
  "message": "No text namespace found with the name 'my-documents' in your account.",
  "namespace_name": "my-documents"
}
```

```json
{
  "status": "failure",
  "message": "API request limit reached for Professional plan (1000000 requests). Current usage: 1000000.",
  "current_usage": 1000000,
  "limit": 1000000
}
```

```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred while generating the answer.",
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "req_1234567890"
}
```

## ITS relevance labels (threshold tuning)

| Label | Score range |
|---|---|
| Close Match | score ≥ 0.894 |
| Very High Relevance | 0.632 ≤ score < 0.894 |
| High Relevance | 0.447 ≤ score < 0.632 |
| Good Relevance | 0.316 ≤ score < 0.447 |
| Low Relevance | 0.224 ≤ score < 0.316 |
| Very Low Relevance | 0.1 ≤ score < 0.224 |
| Irrelevant | score < 0.1 |

## Temperature guide

- **0.0–0.5**: Conservative, factual- technical documentation
- **0.5–1.0**: Balanced- general Q&A
- **1.0–2.0**: More creative- use carefully for factual content

## Python SDK

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    response = client.answer.generate(
        namespace="my-documents",
        query="What are the main benefits of Moorcheh?",
        ai_model="anthropic.claude-sonnet-4-6",
    )
    print(response["answer"])

    response = client.answer.generate(
        namespace="my-documents",
        query="Tell me more about the second point",
        chat_history=[
            {"role": "user", "content": "What are key features?"},
            {"role": "assistant", "content": "The key features are..."},
        ],
    )
```

## Script

```bash
uv run skills/moorcheh/scripts/generate_answer.py \
  --namespace "my-documents" \
  --query "What are the main benefits of Moorcheh?"
```

## Use cases

- Customer support from documentation
- Internal Q&A over knowledge bases
- Educational / research assistants
- Technical support from docs

## Related

- [Semantic Search](search.md)- retrieve context only
- [Upload Text Data](upload_text.md)- add documents for RAG
- [List Namespaces](list_namespaces.md)- discover namespaces

## Official references

- [Generate AI Answer (REST)](https://docs.moorcheh.ai/api-reference/ai/generate.md)
- [Generate AI Answer (Python SDK)](https://docs.moorcheh.ai/python-sdk/ai/generate.md)
