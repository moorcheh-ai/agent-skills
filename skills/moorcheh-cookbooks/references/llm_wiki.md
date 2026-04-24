# LLM Wiki + Moorcheh Cookbook

Build a **self-maintaining personal knowledge base** using Karpathy's LLM Wiki pattern, extended with Moorcheh's Information-Theoretic Search for persistent, scalable semantic memory.

> Based on Andrej Karpathy's [llm-wiki.md](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) idea file (April 2026).
> Starter repo: [github.com/moorcheh-ai/llm-wiki](https://github.com/moorcheh-ai/llm-wiki)

---

## The Core Idea

Most AI knowledge tools use RAG: upload documents, retrieve chunks at query time, generate an answer. Nothing accumulates. Every question re-derives the same knowledge from scratch.

LLM Wiki flips this. The agent **builds and maintains a structured wiki** from your sources — once — and queries that instead. The wiki is a persistent, compounding artifact. Moorcheh adds the search layer that makes it work at any scale.

```
Traditional RAG:   Question → Search raw docs → Generate answer → Forgotten
LLM Wiki:          New source → Agent writes wiki → Wiki compounds over time
                   Question → Search Moorcheh → Read wiki pages → Cited answer → Saved back
```

---

## What You're Building

A project folder with this structure:

```
project/
├── CLAUDE.md       ← Agent schema (instructions for this wiki)
├── AGENTS.md       ← Same schema for non-Claude agents
├── raw/            ← Your source documents (immutable — agent reads, never writes)
│   └── assets/     ← Downloaded images
└── wiki/           ← Agent-generated knowledge base
    ├── index.md    ← Master catalog of all pages
    ├── log.md      ← Append-only activity log
    ├── overview.md ← Big-picture synthesis
    ├── glossary.md ← Terms, definitions, style rules
    └── sources/    ← One summary page per source document
```

The agent owns `wiki/`. You own `raw/`. Neither crosses into the other's territory.

---

## Setup

### Step 1 — Clone the starter repo

```bash
git clone https://github.com/moorcheh-ai/llm-wiki
cd llm-wiki
```

Or start from scratch: copy `CLAUDE.md` and `AGENTS.md` from the repo into an empty folder.

### Step 2 — Create your Moorcheh namespace

```python
import moorcheh

client = moorcheh.Client()

# Create a namespace for this wiki
# Convention: wiki-<topic>
client.namespaces.create(name="wiki-research", type="text")
```

Or via the agent skill:

```
/moorcheh:namespaces
```

Name your namespace after your topic: `wiki-research`, `wiki-product`, `wiki-competitive`, `wiki-personal`, `wiki-team`.

### Step 3 — Open in your agent + Obsidian

Open the project in your agent (Claude Code, Cursor, Codex, etc.). The agent reads `CLAUDE.md` or `AGENTS.md` automatically.

Open the same folder as an Obsidian vault for graph view visualization.

---

## Core Operations

### Ingest

**Trigger:** `ingest raw/<filename>`

```
ingest raw/quarterly-report.pdf
```

The agent:
1. Reads the source document
2. Discusses key takeaways with you
3. Creates `wiki/sources/<slug>.md`
4. Creates or updates entity and concept pages; flags contradictions
5. Updates `wiki/glossary.md`, `wiki/index.md`, `wiki/overview.md`
6. Syncs all new/updated pages to Moorcheh using the **delete-then-upload** pattern (see [Sync on Update](#sync-on-update) below).

7. Logs the run: `## [2026-04-16] ingest | Source Title`

One source typically touches 10–15 wiki pages. Stay involved — read the summaries, guide the agent on what to emphasize.

### Query

**Trigger:** Ask any question in natural language

The agent searches Moorcheh first with ITS scoring:

```python
results = client.search(
    query="main risks identified across all sources",
    namespaces=["wiki-research"],
    top_k=8
)
```

With metadata filters:

```python
# Filter by page type
results = client.search(
    query="competitor analysis #type:entity",
    namespaces=["wiki-research"],
    top_k=5
)

# Filter by tag
results = client.search(
    query="pricing strategy #tags:competitive",
    namespaces=["wiki-research"]
)
```

The agent reads the returned pages and synthesizes a cited answer. Valuable answers are saved as `wiki/analysis/<slug>.md` and uploaded to Moorcheh — your questions compound the wiki just like sources do.

### Generate (RAG-powered answer)

**Trigger:** `answer: <question>`

```python
response = client.generate(
    query="What are the main architectural tradeoffs discussed?",
    namespace="wiki-research"
)
```

Or via skill:
```
/moorcheh:answer query "What are the main architectural tradeoffs?" namespace "wiki-research"
```

### Sync on Update

Whenever a wiki page is created or modified, the agent must sync it to Moorcheh. Because Moorcheh documents are immutable once uploaded, **updating a page requires deleting the old version first, then uploading the new one.**

The `moorcheh_doc_id` in frontmatter is the stable key that connects a local file to its backend document.

**Sync rules:**
1. Every wiki page gets a deterministic `moorcheh_doc_id`: `{namespace}--{type}--{slug}`
2. On **new page**: upload with that ID, set `moorcheh_uploaded: true`
3. On **updated page**: delete the old doc by ID, upload the new content with the same ID, keep `moorcheh_uploaded: true`
4. On **deleted page**: delete the doc by ID, remove the local file
5. Never leave stale versions on the backend — always delete before re-upload

```python
import pathlib
import re
import moorcheh

client = moorcheh.Client()
NAMESPACE = "wiki-research"

def sync_page(page_path: str):
    """Delete old version (if any) and upload current content."""
    content = pathlib.Path(page_path).read_text()
    assert len(content.strip()) > 0, f"Refusing to sync empty file: {page_path}"

    # Extract moorcheh_doc_id from frontmatter
    match = re.search(r"moorcheh_doc_id:\s*(.+)", content)
    if not match:
        raise ValueError(f"Missing moorcheh_doc_id in {page_path}")
    doc_id = match.group(1).strip()

    # Step 1: Delete the old version (ignore errors if it doesn't exist yet)
    try:
        client.documents.delete(namespace_name=NAMESPACE, ids=[doc_id])
    except Exception:
        pass  # First upload — nothing to delete

    # Step 2: Upload the new version with the same stable ID
    metadata = {"source_file": page_path, "wiki_namespace": NAMESPACE}
    client.documents.upload(
        namespace_name=NAMESPACE,
        documents=[{"id": doc_id, "text": content, **metadata}]
    )

    # Step 3: Ensure the flag is set (safe targeted replace)
    if "moorcheh_uploaded: false" in content:
        updated = content.replace("moorcheh_uploaded: false", "moorcheh_uploaded: true", 1)
        assert len(updated) >= len(content) - 20
        pathlib.Path(page_path).write_text(updated)
```

The agent calls `sync_page()` for every file it creates or modifies during ingest, query-save, or manual edits.

### Lint

**Trigger:** `lint`

The agent health-checks the wiki:
- Contradictions (pages with `⚠️ CONTRADICTION:` markers)
- Orphan pages with no inbound links
- Stale claims superseded by newer sources
- Concept gaps: entities mentioned but lacking their own page
- Moorcheh sync gaps: pages with `moorcheh_uploaded: false`

Run every 10 ingests.

---

## Page Schema

Every wiki page includes YAML frontmatter:

```yaml
---
type: entity | concept | source | comparison | analysis | overview | glossary
title: Page Title
created: 2026-04-16
updated: 2026-04-16
sources: [source-file.pdf, other-source.md]
tags: [competitive, pricing, 2026-q2]
moorcheh_doc_id: wiki-research--entity--page-title   # deterministic ID for sync
moorcheh_uploaded: false   # agent flips to true after upload
---
```

The `moorcheh_doc_id` is the **stable identifier** that ties a local file to its Moorcheh document. Convention: `{namespace}--{type}--{slug}`. This ID must stay constant across updates — it is how the agent knows which backend document to delete before re-uploading.

The `moorcheh_uploaded` flag is the sync status tracker. The agent maintains it. Run `lint` to catch any pages that slipped through.

---

## File Safety Rules (Critical)

**These rules prevent data loss.** The flag-update step (`moorcheh_uploaded: false → true`) has caused agents to wipe wiki files to 0 bytes. Follow these rules without exception:

1. **Read-before-write.** Always read the full file content into a variable before modifying anything. Never open a file for writing without holding its contents in memory first.
2. **Validate before flush.** After composing the new content, assert that its length is ≥ the original length minus a small tolerance (e.g. 20 chars for whitespace changes). If the new content is shorter than 50% of the original, **abort the write and log a warning.**
3. **Atomic flag updates.** When updating only frontmatter flags, use a targeted replacement (e.g. regex or string replace on the YAML block) — never rewrite the entire file body.
4. **Never write empty content.** Before any file write, check: `if len(new_content.strip()) == 0: abort`.
5. **Batch flag updates carefully.** When flipping `moorcheh_uploaded` across many files in a loop, process one file at a time and verify each write before moving to the next.

```python
# Safe flag update pattern
def safe_update_flag(path: str):
    content = pathlib.Path(path).read_text()
    assert len(content) > 0, f"Refusing to touch empty file: {path}"

    updated = content.replace("moorcheh_uploaded: false", "moorcheh_uploaded: true", 1)
    assert len(updated) >= len(content) - 20, f"Content shrank unexpectedly: {path}"

    pathlib.Path(path).write_text(updated)
```

---

## Namespace Convention

| Wiki purpose | Namespace |
|---|---|
| Research topic | `wiki-<topic>` (e.g. `wiki-llm-agents`) |
| Product knowledge | `wiki-product` |
| Competitive intelligence | `wiki-competitive` |
| Personal knowledge | `wiki-personal` |
| Team / internal | `wiki-team` |

For multiple parallel wikis, one namespace per topic. They stay completely isolated in Moorcheh.

---

## Why Moorcheh Over Flat Files

Karpathy's original design uses `index.md` as the navigation layer — read the index, drill into relevant pages. This works well up to ~300 pages. Beyond that:

| Scale | File-based index | Moorcheh ITS |
|---|---|---|
| 0–300 pages | Works fine | Works fine |
| 300–500 pages | Navigation degrades | Works fine |
| 500+ pages | Genuinely painful | Works fine |
| Metadata filtering | Not supported | Full support |
| Relevance scoring | None | ITS semantic scoring |
| Session persistence | Lost on agent restart | Permanent namespace |
| Multi-hop queries | Re-reads many files | Single ranked search |

---

## Full Working Example

```python
import moorcheh
import pathlib
import re

client = moorcheh.Client()
NAMESPACE = "wiki-research"

def sync_page(page_path: str):
    """Delete-then-upload: keeps local files and Moorcheh backend in sync."""
    content = pathlib.Path(page_path).read_text()
    assert len(content.strip()) > 0, f"Refusing to sync empty file: {page_path}"

    match = re.search(r"moorcheh_doc_id:\s*(.+)", content)
    if not match:
        raise ValueError(f"Missing moorcheh_doc_id in {page_path}")
    doc_id = match.group(1).strip()

    # Delete old version, then upload new
    try:
        client.documents.delete(namespace_name=NAMESPACE, ids=[doc_id])
    except Exception:
        pass
    metadata = {"source_file": page_path, "wiki_namespace": NAMESPACE}
    client.documents.upload(
        namespace_name=NAMESPACE,
        documents=[{"id": doc_id, "text": content, **metadata}]
    )

def delete_page(page_path: str):
    """Remove a page from both local disk and Moorcheh."""
    content = pathlib.Path(page_path).read_text()
    match = re.search(r"moorcheh_doc_id:\s*(.+)", content)
    if match:
        client.documents.delete(namespace_name=NAMESPACE, ids=[match.group(1).strip()])
    pathlib.Path(page_path).unlink()

def query_wiki(question: str, top_k: int = 8):
    return client.search(
        query=question,
        namespaces=[NAMESPACE],
        top_k=top_k
    )

def answer_question(question: str):
    return client.generate(
        query=question,
        namespace=NAMESPACE
    )
```

---

## Tips

**Ingest one source at a time.** Stay involved during ingestion — read summaries, guide emphasis. The wiki gets better when you participate.

**Save your best questions.** Tell the agent to save valuable answers as wiki pages. Analysis compounds the same way sources do.

**Use Obsidian graph view** (Cmd+G) to see hubs, orphans, and how your knowledge connects.

**Edit the schema.** `CLAUDE.md` is yours to modify. If your domain needs new page types (`api-endpoint`, `customer-segment`, `experiment-result`) — add them.

**Check the glossary before writing.** `wiki/glossary.md` has canonical terms, deprecated names, and style rules. Always check it before producing content from the wiki.

---

## Resources

- [Starter repo](https://github.com/moorcheh-ai/llm-wiki) — full project with Obsidian config and starter wiki pages
- [Moorcheh Python SDK](https://docs.moorcheh.ai/python-sdk/introduction)
- [Karpathy's original gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Moorcheh Console](https://console.moorcheh.ai)
