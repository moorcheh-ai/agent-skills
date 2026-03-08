---
description: Interactive onboarding — set up environment, create namespace, upload sample data, and explore Moorcheh
argument-hint:
allowed-tools: Bash(uv:*), Bash(pip:*), Bash(python:*), AskUserQuestion, Skill
---

# Moorcheh Quickstart

Interactive onboarding for new Moorcheh users. Guides through environment setup, namespace creation, sample data upload, and first search.

## Workflow

1. Check if `MOORCHEH_API_KEY` is set:
   ```bash
   echo $MOORCHEH_API_KEY
   ```
   - If not set, ask the user for their API key
   - Direct them to [console.moorcheh.ai](https://console.moorcheh.ai) if they don't have one

2. Check Python dependencies:
   ```bash
   pip show moorcheh-sdk
   ```
   - If not installed: `pip install moorcheh-sdk requests`

3. List existing namespaces:
   ```bash
   uv run ${SKILL_ROOT}/skills/moorcheh/scripts/list_namespaces.py
   ```

4. Ask the user if they want to:
   - **a)** Create a demo namespace with sample data
   - **b)** Use an existing namespace

5. If creating demo data:
   ```bash
   uv run ${SKILL_ROOT}/skills/moorcheh/scripts/example_data.py --namespace "demo-namespace"
   ```

6. Run a test search:
   ```bash
   uv run ${SKILL_ROOT}/skills/moorcheh/scripts/search.py --query "artificial intelligence" --namespaces "demo-namespace"
   ```

7. Run a test AI answer:
   ```bash
   uv run ${SKILL_ROOT}/skills/moorcheh/scripts/generate_answer.py --namespace "demo-namespace" --query "What is AI used for?"
   ```

8. Show the user available commands:
   - `/moorcheh:search` — Semantic search
   - `/moorcheh:answer` — AI-powered answers
   - `/moorcheh:namespaces` — Manage namespaces
   - `/moorcheh:upload` — Upload data
   - `/moorcheh:explore` — Explore data
