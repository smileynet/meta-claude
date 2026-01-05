# Validation Checks Reference

Complete list of all validation checks performed by the doc-validator.

## Structure Checks

### SKILL.md Presence

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| SKILL.md exists in skill directories | ERROR | No |
| SKILL.md filename is exactly `SKILL.md` (case-sensitive) | ERROR | No |
| Supporting files are in same directory or subdirectories | WARNING | No |

**Why**: Skills must have a SKILL.md as the entry point. Claude discovers skills by looking for this file.

### File Size (Progressive Disclosure)

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| SKILL.md under 500 lines | WARNING | No |
| Supporting files exist for large content | INFO | No |
| Main file links to supporting files | INFO | No |

**Why**: Large files slow loading and overwhelm context. Progressive disclosure keeps main files focused.

**Thresholds**:
- < 150 lines: Optimal
- 150-500 lines: Acceptable
- > 500 lines: Warning - consider splitting

### Directory Organization

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| Skill in `skills/` directory | ERROR | No |
| Command in `commands/` directory | ERROR | No |
| Agent in `agents/` directory | ERROR | No |
| No deeply nested skills (max 1 level) | WARNING | No |

**Why**: Claude looks in specific directories for each artifact type.

### File Naming

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| Filenames use lowercase | WARNING | Rename |
| Filenames use hyphens (not underscores) | INFO | No |
| No spaces in filenames | ERROR | No |
| .md extension for markdown files | WARNING | No |

**Why**: Consistent naming prevents cross-platform issues and improves discoverability.

## Link Checks

### Internal Links

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| Relative links resolve to existing files | ERROR | No |
| Linked files are readable | ERROR | No |
| Link text matches target topic | INFO | No |

**Pattern**: `[text](path/to/file.md)`

### @file References

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| @file paths resolve to existing files | ERROR | No |
| @file paths use correct path format | WARNING | No |
| Referenced skills exist | ERROR | No |

**Pattern**: `@~/.claude/skills/my-skill/SKILL.md`

### Orphaned Files

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| Supporting files are referenced from main docs | INFO | No |
| No unreachable files in skill directory | INFO | No |

**Why**: Orphaned files suggest incomplete documentation or dead code.

### Circular References

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| No circular reference chains | WARNING | No |
| Clear hierarchy of references | INFO | No |

**Why**: Circular references create confusion about the source of truth.

## Content Checks

### YAML Frontmatter

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| Frontmatter present | ERROR | Add `---\n---` |
| Frontmatter starts with `---` on line 1 | ERROR | No |
| Frontmatter ends with `---` | ERROR | No |
| Valid YAML syntax | ERROR | No |
| No tab characters in frontmatter | ERROR | Convert to spaces |

### Required Fields

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| `name` field present (skills) | ERROR | Generate from folder |
| `name` uses only lowercase, numbers, hyphens | WARNING | No |
| `description` field present | ERROR | Add placeholder |
| `description` is non-empty | ERROR | No |

### Description Quality

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| Description contains trigger keywords | WARNING | Suggest keywords |
| Description under 200 characters | INFO | No |
| Description explains when to use | INFO | No |

**Good description example**:
```yaml
description: Generate commit messages from staged changes. Use when writing commits, git messages, or preparing changes for review.
```

**Bad description example**:
```yaml
description: Helps with git
```

### Formatting

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| No tab characters (use spaces) | WARNING | Convert |
| No trailing whitespace | INFO | Remove |
| File ends with newline | INFO | Add |
| Consistent heading hierarchy | INFO | No |
| Code blocks have language specified | INFO | No |

### Special Characters

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| YAML values with `:` are quoted | ERROR | Add quotes |
| YAML values with `#` are quoted | ERROR | Add quotes |
| No unescaped special chars in descriptions | WARNING | Escape |

## Skill-Specific Checks

### allowed-tools Field

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| Tool names are valid | ERROR | No |
| Tools are comma-separated | ERROR | No |
| No duplicate tools | WARNING | Remove |

**Valid tools**: Read, Write, Edit, Grep, Glob, Bash, WebFetch, WebSearch, etc.

### model Field (Agents)

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| Model name is valid | ERROR | No |
| Model appropriate for task | INFO | No |

**Valid models**: `haiku`, `sonnet`, `opus`

## Command-Specific Checks

### Variables

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| $ARGUMENTS used correctly | INFO | No |
| $SELECTION used correctly | INFO | No |
| Variables not inside @file references | WARNING | No |

### Skill-Linking

| Check | Severity | Auto-Fix |
|-------|----------|----------|
| @file references load skill content | INFO | No |
| Command adds context, not duplication | INFO | No |

## Check Severity Guide

| Severity | When to Use | Example |
|----------|-------------|---------|
| **ERROR** | Prevents functionality | Missing SKILL.md, broken frontmatter |
| **WARNING** | Recommended fix | Large file, vague description |
| **INFO** | Optional improvement | Trailing whitespace, orphaned file |

## Running Specific Checks

```bash
# All checks
python validate_docs.py path/

# Structure checks only
python validate_docs.py --category structure path/

# Link checks only
python validate_docs.py --category links path/

# Content checks only
python validate_docs.py --category content path/
```
