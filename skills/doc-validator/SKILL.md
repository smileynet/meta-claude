---
name: doc-validator
description: Validate markdown documentation against meta-agentic best practices. Use when validating skills, commands, checking broken links, validating frontmatter, auditing documentation structure, or running compliance checks.
allowed-tools: Read, Grep, Glob, Bash
---

# Documentation Validator

Validate markdown documentation for compliance with meta-agentic best practices including progressive disclosure, lazy loading references, and proper structure.

## Quick Start

```bash
# Validate a skill directory
/validate-docs ~/.claude/skills/my-skill/

# Validate with auto-fix
/validate-docs --fix ~/.claude/skills/

# Dry run (show what would be fixed)
/validate-docs --fix --dry-run ~/.claude/skills/

# Use the Python script directly
python scripts/validate_docs.py ~/.claude/skills/my-skill/
```

## What It Validates

### Structure Checks
- SKILL.md exists in skill directories
- File sizes under 500 lines (progressive disclosure)
- Directory organization follows conventions
- File naming (lowercase, hyphens)

### Link Checks
- Internal links resolve to existing files
- @file references in commands point to valid paths
- Orphaned files (not referenced from main docs)
- No circular references

### Content Checks
- YAML frontmatter present and valid
- Required fields: `name`, `description`
- Description contains trigger keywords
- Formatting: tabs, whitespace, newlines

## Auto-Fix Behavior

| Category | Auto-Fix? | Examples |
|----------|-----------|----------|
| **Safe formatting** | Yes | Tabs→spaces, trailing whitespace, final newline |
| **YAML syntax** | Yes | Quote special characters |
| **Missing structure** | With notice | Add frontmatter, generate name from folder |
| **Content decisions** | Report only | Broken links, file structure, descriptions |

For detailed auto-fix rules, see [auto-fix.md](auto-fix.md).

## Output Format

```
Validating: ~/.claude/skills/my-skill/

~/.claude/skills/my-skill/SKILL.md
  [ERROR]   Line 1: Missing YAML frontmatter
  [WARNING] Line 45: Broken link: [examples](examples.md)
  [INFO]    Line 12: Tab character found
  → Auto-fixed: Tab → spaces

SUMMARY
───────────────────────────────────────────────────────────────
Files checked:    2
Errors:           1 (require manual fix)
Warnings:         1 (recommended fix)
Info:             1 (optional polish)
Auto-fixed:       1 issues
```

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **ERROR** | Critical issue preventing proper function | Must fix |
| **WARNING** | Recommended improvement | Should fix |
| **INFO** | Optional polish | Nice to fix |

## Invocation Modes

### Single File
```bash
/validate-docs path/to/file.md
```

### Skill Directory
```bash
/validate-docs ~/.claude/skills/my-skill/
```

### Batch (All User Skills)
```bash
/validate-docs --all ~/.claude/skills/
```

## Reference Documentation

| Guide | Purpose |
|-------|---------|
| [checks.md](checks.md) | Complete list of validation checks |
| [auto-fix.md](auto-fix.md) | Auto-fix behaviors and safety classification |
| [examples.md](examples.md) | Example validation outputs |
| [sources.md](sources.md) | External documentation links |

## Integration

### With Python Script

```bash
# Basic validation
python scripts/validate_docs.py path/

# With auto-fix
python scripts/validate_docs.py --fix path/

# JSON output for tooling
python scripts/validate_docs.py --format json path/

# Strict mode (exit 1 on any issue)
python scripts/validate_docs.py --strict path/
```

### With Agent

For comprehensive validation with intelligent auto-fix:
```
Use the doc-validator agent to validate ~/.claude/skills/
```

## Patterns Validated

This validator checks compliance with patterns from:
- [Progressive Disclosure](../../docs/patterns/progressive-disclosure.md)
- [Skill-Linking](../../docs/patterns/skill-linking.md)
- [Single Source of Truth](../../docs/patterns/single-source-truth.md)
- [Validation Workflows](../../docs/patterns/validation-workflows.md)
