# Contributing to Moorcheh Agent Skills

Thank you for your interest in contributing! This guide will help you add new skills, references, or cookbooks.

## Structure

Each skill follows the [Agent Skills specification](https://agentskills.io/specification):

```
skills/<skill-name>/
├── SKILL.md          # Required: YAML frontmatter + instructions
├── references/       # Optional: detailed reference documents
├── scripts/          # Optional: executable helper scripts
└── assets/           # Optional: templates, images, data files
```

## Adding a Reference

1. Create a new `.md` file in the appropriate `references/` directory
2. Follow the existing reference format (purpose, usage, parameters, examples)
3. Add the reference to the parent `SKILL.md` script index
4. Include both REST API and Python SDK examples

## Creating a New Skill

1. Create a new directory under `skills/` with a lowercase, hyphenated name
2. Add a `SKILL.md` with required YAML frontmatter:

```yaml
---
name: your-skill-name
description: Clear description of what this skill does and when to use it.
---
```

3. The `name` must match the directory name exactly
4. Keep `SKILL.md` body under 5000 tokens (use references for details)
5. Add a PR with your changes

## Adding a Command

Commands go in `commands/` and follow the format:

```yaml
---
description: Short description of the command
argument-hint: param1 [value] param2 [value]
allowed-tools: Bash(uv:*), Skill
---
```

## Code Style

- Python scripts should be self-contained
- Include clear error messages with suggested fixes
- Use `argparse` for command-line arguments
- Support both `MOORCHEH_API_KEY` env var and `--api-key` flag

## Testing

Before submitting:
1. Verify SKILL.md frontmatter has valid `name` and `description`
2. Confirm all file references in SKILL.md point to existing files
3. Test Python scripts with a Moorcheh API key
4. Run `npm pack --dry-run` to verify package contents

## License

By contributing, you agree that your contributions will be licensed under the BSD-3-Clause License.
