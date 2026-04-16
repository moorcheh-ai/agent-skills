# /moorcheh:llm-wiki

Set up and operate an LLM Wiki — a self-maintaining knowledge base using
Karpathy's pattern extended with Moorcheh ITS search.

## Usage

```
/moorcheh:llm-wiki setup
/moorcheh:llm-wiki ingest <file>
/moorcheh:llm-wiki query "<question>"
/moorcheh:llm-wiki lint
/moorcheh:llm-wiki sync
```

## Actions

### setup
Initialize a new LLM Wiki project in the current directory:
- Creates `raw/`, `wiki/`, `wiki/sources/` directories
- Copies `CLAUDE.md` and `AGENTS.md` schema files
- Creates starter wiki pages (index, log, overview, glossary)
- Prompts for Moorcheh namespace name (default: `wiki-<folder-name>`)
- Creates the Moorcheh namespace if it doesn't exist
- Configures Obsidian vault settings if `.obsidian/` is present

### ingest `<file>`
Process a source document and update the wiki:
- Reads the file from `raw/<file>`
- Extracts entities, concepts, and key claims
- Creates or updates wiki pages
- Uploads all new/updated pages to the Moorcheh namespace
- Updates `wiki/index.md`, `wiki/overview.md`, `wiki/glossary.md`
- Appends to `wiki/log.md`

### query `"<question>"`
Search the wiki and synthesize a cited answer:
- Searches the Moorcheh namespace with ITS scoring
- Reads the top-ranked wiki pages
- Synthesizes an answer with wiki page citations
- Offers to save the answer as a `wiki/analysis/` page

### lint
Health-check the wiki:
- Scans for contradiction markers (`⚠️ CONTRADICTION:`)
- Finds orphan pages (no inbound links)
- Finds pages with `moorcheh_uploaded: false`
- Reports gaps and offers fixes

### sync
Upload all unsynced wiki pages to Moorcheh:
- Finds all pages with `moorcheh_uploaded: false`
- Uploads them to the configured namespace
- Flips `moorcheh_uploaded: true` in frontmatter

## Full Documentation

See [skills/moorcheh-cookbooks/references/llm_wiki.md](../skills/moorcheh-cookbooks/references/llm_wiki.md)
and the starter repo at https://github.com/moorcheh-ai/llm-wiki
