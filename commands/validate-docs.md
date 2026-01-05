---
description: Validate documentation against meta-agentic best practices. Use to check skills, commands, agents, or any markdown documentation for compliance.
allowed-tools: Read, Grep, Glob, Bash
---

Follow the documentation validation guidelines in:
@./skills/doc-validator/SKILL.md

## Task

Validate the documentation at: $ARGUMENTS

## Validation Process

1. **Discover files**: Find all markdown files in the target path
2. **Check structure**: Verify SKILL.md presence, file sizes, organization
3. **Check links**: Validate internal links and @file references
4. **Check content**: Verify frontmatter, required fields, formatting

## Output

For each issue found, report:
- File path and line number
- Severity: [ERROR], [WARNING], or [INFO]
- Issue description
- Whether it can be auto-fixed

## Auto-Fix

If `--fix` is in the arguments:
- Apply safe formatting fixes (tabs, whitespace, newlines)
- Apply generative fixes (missing frontmatter, name, description)
- Report all other issues for manual resolution

If `--dry-run` is also specified:
- Show what would be fixed without modifying files

## Examples

```
/validate-docs ~/.claude/skills/my-skill/
/validate-docs --fix ~/.claude/skills/
/validate-docs --fix --dry-run .claude/
```
