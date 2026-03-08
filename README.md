# Moorcheh Agent Skills

<p align="center">
  <strong>Agent Skills for building AI applications with <a href="https://moorcheh.ai">Moorcheh</a> — the Universal Memory Layer for Agentic AI.</strong>
</p>

<p align="center">
  <a href="https://docs.moorcheh.ai">Documentation</a> ·
  <a href="https://console.moorcheh.ai">Console</a> ·
  <a href="https://docs.moorcheh.ai/python-sdk/introduction">Python SDK</a> ·
  <a href="https://agentskills.io/specification">Agent Skills Spec</a>
</p>

---

Each skill is a folder containing instructions, scripts, and resources that agents like Claude Code, Cursor, GitHub Copilot, Codex, Windsurf, Antigravity, and others can discover to work more accurately and efficiently with Moorcheh.

Works with any agent that supports the [Agent Skills](https://agentskills.io/home#adoption) format.

## Installation

### Using npx skills (Cursor, Claude Code, Gemini CLI, Codex, etc.)

```bash
npx skills add moorcheh-ai/agent-skills
```

### Using Claude Code Plugin Manager

```bash
/plugin install moorcheh@moorcheh-agent-skills
```

### Manual: clone and point your agent to the directory

```bash
git clone https://github.com/moorcheh-ai/agent-skills.git
cd agent-skills
claude --plugin-dir .
```

## Quickstart

New to Moorcheh? Run the interactive onboarding to set up your environment variables, import sample data, and explore the full functionality:

```bash
/moorcheh:quickstart
```

## Configuration

### Moorcheh Account

Create a free account at [console.moorcheh.ai](https://console.moorcheh.ai).

### Required Environment Variables

```bash
export MOORCHEH_API_KEY="your-api-key"
```

## Available Skills

<details>
<summary><strong>Moorcheh</strong></summary>

Core operations for interacting with the Moorcheh platform:

- **Namespace Management** — Create, list, and delete namespaces
- **Data Operations** — Upload text documents and vector embeddings
- **Semantic Search** — Search with ITS scoring, metadata filters, and relevance labels
- **AI Generation** — Generate RAG-powered answers with structured output

</details>

<details>
<summary><strong>Cookbooks</strong></summary>

Blueprints for complete AI applications powered by Moorcheh:

- **Knowledge Base RAG** — Document Q&A with source citations
- **Customer Support Bot** — Conversational chatbot with chat history
- **Semantic Search App** — Search with ITS scoring and filtering
- **AI Q&A System** — Structured Q&A with multi-namespace routing
- **Frontend Interface** — Next.js frontend (optional)
- **LangChain Integration** — Use Moorcheh as a LangChain vector store

</details>

## Usage

### Commands (Claude Code Plugin)

```bash
# Interactive onboarding
/moorcheh:quickstart

# Semantic search across namespaces
/moorcheh:search query "machine learning" namespaces "my-documents"

# Search with metadata filters
/moorcheh:search query "best practices #category:tech" namespaces "articles" top_k 5

# Generate AI-powered RAG answers
/moorcheh:answer query "What are the key features?" namespace "product-docs"

# List all namespaces
/moorcheh:namespaces

# Upload data to a namespace
/moorcheh:upload namespace "my-documents" file "data.json"

# Explore data in a namespace
/moorcheh:explore namespace "my-documents"
```

### Skills (Any Compatible Agent)

The skill is automatically discovered by compatible agents. Simply describe what you want:

- "Search my Moorcheh namespace for information about vector databases"
- "List all my Moorcheh namespaces"
- "Upload these documents to Moorcheh for semantic search"
- "Build a knowledge base chatbot using Moorcheh"
- "Generate an AI answer from my documentation"
- "Build a customer support bot with Moorcheh"

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A [Moorcheh](https://console.moorcheh.ai) account

## Resources

- [Moorcheh Documentation](https://docs.moorcheh.ai)
- [Python SDK](https://docs.moorcheh.ai/python-sdk/introduction)
- [API Reference](https://docs.moorcheh.ai/api-reference/introduction)
- [LangChain Integration](https://docs.moorcheh.ai/integrations/langchain/overview)
- [LlamaIndex Integration](https://docs.moorcheh.ai/integrations/llamaindex/overview)
- [MCP Server](https://docs.moorcheh.ai/integrations/mcp/overview)
- [Agent Skills Specification](https://agentskills.io/specification)
