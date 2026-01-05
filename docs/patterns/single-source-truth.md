# Pattern: Single Source of Truth

Knowledge lives in ONE place, referenced from many.

## The Principle

Every piece of knowledge should have exactly one authoritative location. Other places that need that knowledge should reference it, not duplicate it.

## Why It Matters

- **Consistency**: No conflicting versions of the same information
- **Maintainability**: Update once, propagate everywhere
- **Clarity**: Clear answer to "where is the truth?"
- **Auditability**: Changes tracked in one location

## Implementation Across Tools

### Claude Code

**Source** (`~/.claude/skills/python-standards/SKILL.md`):
```yaml
---
name: python-standards
description: Python coding standards for all projects.
---

# Python Standards
[Authoritative guidelines]
```

**References**:
```markdown
# Command that references
@~/.claude/skills/python-standards/SKILL.md

# Project CLAUDE.md that references
For Python code, follow the standards in ~/.claude/skills/python-standards/

# Another skill that references
For Python-specific guidance, see the python-standards skill.
```

### Cursor

**Source** (`.cursor/rules/python.mdc`):
```yaml
---
description: Python standards
globs: ["**/*.py"]
alwaysApply: false
---
# Python Standards
[Authoritative guidelines]
```

Other rules don't need to reference—Cursor auto-loads based on file patterns.

### Kiro

**Source** (`.kiro/steering.md`):
```markdown
# Project Standards
[Authoritative project-wide guidance]
```

**Specs reference implicitly**:
Kiro loads steering.md for all operations. Specs add feature-specific details.

### OpenCode

**Source** (`~/.config/opencode/knowledge/standards.md`):
```markdown
# Coding Standards
[Authoritative guidelines]
```

**Agent references**:
```yaml
name: coder
system: |
  Follow the standards in ~/.config/opencode/knowledge/standards.md
```

## The sources.md Pattern

For external authoritative sources, use a `sources.md` file:

```markdown
# Sources

## Primary Source
- [Official Python Style Guide](https://peps.python.org/pep-0008/)

## Secondary Sources
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Black Code Style](https://black.readthedocs.io/en/stable/the_black_code_style/)

## Conflict Resolution
When sources conflict, prefer the Primary Source.
```

This pattern:
- Documents where knowledge comes from
- Enables fetching current docs when needed
- Establishes hierarchy for conflicts

## Examples

### Good: Single Source

```
~/.claude/skills/
├── api-design/
│   └── SKILL.md         # THE source for API design guidance
└── code-review/
    └── SKILL.md         # References api-design for API-related reviews
        "For API endpoint reviews, apply the principles in
         @~/.claude/skills/api-design/SKILL.md"
```

### Bad: Multiple Sources

```
~/.claude/skills/
├── api-design/
│   └── SKILL.md         # Has API guidelines
├── code-review/
│   └── SKILL.md         # Has DIFFERENT API guidelines (copy-pasted, drifted)
└── backend/
    └── SKILL.md         # Has YET ANOTHER version of API guidelines
```

Which is correct? Nobody knows. Updates require finding all copies.

### Good: Project References User

```markdown
# Project .claude/CLAUDE.md

This project uses the team's standard Python configuration.
For Python code, follow: @~/.claude/skills/python-standards/SKILL.md

Project-specific additions:
- Use Django ORM patterns for database access
- Prefer class-based views
```

The project adds context but doesn't duplicate the standards.

## Determining the Source

Ask these questions:

1. **Who owns this knowledge?**
   - Personal preference → User scope (`~/.claude/`)
   - Team standard → Project scope (`.claude/`)
   - External standard → Link to official docs

2. **How often does it change?**
   - Frequently → Keep in one editable place
   - Rarely → Can embed, but still prefer reference

3. **Who needs to update it?**
   - Just you → User scope
   - Team → Project scope with clear ownership

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Copy-paste knowledge | Drift between copies | Reference single source |
| No clear owner | Nobody updates, becomes stale | Designate authoritative location |
| Embedded external standards | Can't update when standard changes | Link to sources.md |
| Circular references | No clear source | Establish hierarchy |

## Hierarchy When Sources Conflict

```
Enterprise Policy    (highest authority)
       ↓
  Team Standards
       ↓
 Personal Preferences
       ↓
   Tool Defaults     (lowest authority)
```

Document this hierarchy in your source files:
```markdown
## Conflict Resolution
Enterprise policies override team standards.
Team standards override personal preferences.
When in doubt, ask in #engineering-standards.
```

## Related Patterns

- [Skill-Linking](skill-linking.md) - How to reference sources
- [Progressive Disclosure](progressive-disclosure.md) - How to structure the source
