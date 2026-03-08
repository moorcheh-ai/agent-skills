---
name: moorcheh-cookbooks
description: Use this skill when the user wants to build AI applications with Moorcheh. Contains blueprints and implementation guides for knowledge base RAG, customer support chatbots, semantic search applications, AI Q&A systems, and optional frontend integration. Each cookbook includes architecture, code examples, setup instructions, and deployment guidance.
---

# Moorcheh Cookbooks

## Overview

This skill provides an index of implementation guides and foundational requirements for building Moorcheh-powered AI applications. Use the references to quickly scaffold full-stack applications with best practices for data management, semantic search, and RAG.

### Moorcheh Account

If the user does not have an account yet, direct them to the cloud console to register and create a free account.

Create a Moorcheh account at [console.moorcheh.ai](https://console.moorcheh.ai).

## Before Building Any Cookbook

Follow these shared guidelines before generating any cookbook app:

- [Project Setup Contract](references/project_setup.md)
- [Environment Requirements](references/environment_requirements.md)

Then proceed to the specific cookbook reference below.

## Cookbook Index

- [Knowledge Base RAG](references/knowledge_base_rag.md): Build a document Q&A system that ingests documents into Moorcheh and generates AI-powered answers with source citations using RAG.
- [Customer Support Bot](references/customer_support_bot.md): Build a customer support chatbot that answers questions from your FAQ and documentation using conversational RAG with chat history.
- [Semantic Search App](references/semantic_search_app.md): Build a semantic search application with ITS scoring, metadata filtering, and relevance-labeled results.
- [AI Q&A System](references/ai_qa_system.md): Build a question-answering system with structured output, custom prompts, and multi-namespace search.

## Integrations

- [LangChain Integration](references/langchain_integration.md): Use Moorcheh as a LangChain vector store for building chains and agents.

## Interface (Optional)

Use this when the user explicitly asks for a frontend for their Moorcheh backend:

- [Frontend Interface](references/frontend_interface.md): Build a Next.js frontend to interact with the Moorcheh backend, including chat UI and search interfaces.
