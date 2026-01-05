# Sources

External documentation and references for documentation validation.

## Primary Source

- **[Meta-Claude Patterns](../../docs/patterns/)**
  - Progressive disclosure, skill-linking, single source of truth
  - These patterns define the standards being validated

## Claude Code Documentation

- **[Claude Code Skills Guide](https://docs.anthropic.com/en/docs/claude-code/skills)**
  - Official skill format and requirements
  - YAML frontmatter specification

- **[Claude Code Commands Guide](https://docs.anthropic.com/en/docs/claude-code/commands)**
  - Command format and variables
  - @file reference syntax

## YAML Specifications

- **[YAML 1.2 Specification](https://yaml.org/spec/1.2.2/)**
  - Official YAML syntax reference
  - Special character handling

- **[PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)**
  - Python YAML parsing library
  - Used by validate_docs.py

## Markdown Standards

- **[CommonMark Specification](https://spec.commonmark.org/)**
  - Markdown parsing standard
  - Link and reference syntax

- **[GitHub Flavored Markdown](https://github.github.com/gfm/)**
  - Extended markdown features
  - Code block language hints

## Related Skills

- **[claude-skills validation.md](~/.claude/skills/claude-skills/validation.md)**
  - Existing skill validation patterns
  - Pre-deployment checklist

- **[claude-commands validation.md](~/.claude/skills/claude-commands/validation.md)**
  - Command validation patterns
  - Batch validation commands

## Python Tools

- **[PyYAML](https://pypi.org/project/PyYAML/)**
  - YAML parsing for Python
  - Required by validate_docs.py

- **[pathlib](https://docs.python.org/3/library/pathlib.html)**
  - Path handling in Python
  - Cross-platform file operations

## Conflict Resolution

When sources disagree:

1. **Meta-Claude Patterns** take precedence for style decisions
2. **Claude Code Docs** take precedence for format requirements
3. **YAML Spec** takes precedence for syntax questions
4. **CommonMark** takes precedence for markdown parsing

## Last Verified

Sources last verified: 2024-01

Use WebFetch to get current content when needed.
