# Cursor: Deployment & Idioms

This guide covers Cursor deployment patterns and idiomatic usage. For general patterns, see the [meta-claude skill](~/.claude/skills/meta-claude/tools/cursor.md).

## Directory Structure

```
.cursor/                      # Project-level configuration
├── rules/                    # Rule files
│   ├── general.mdc          # Always applied
│   ├── typescript.mdc       # *.ts, *.tsx files
│   ├── testing.mdc          # *.test.*, *.spec.*
│   └── api.mdc              # api/**/*
└── mcp.json                 # MCP server configuration

# User-level (in Cursor settings)
Cursor Settings → Rules → User Rules
```

## Rules (.mdc Files)

### MDC Format

```yaml
---
description: Brief description for discovery
globs: ["**/*.ts", "**/*.tsx"]  # File patterns
alwaysApply: false              # Always include in context?
---

# Rule Title

[Markdown content with guidance]
```

### Rule Types

| Type | Configuration | Behavior |
|------|---------------|----------|
| Always Apply | `alwaysApply: true` | Included in every conversation |
| File-Triggered | `globs: ["pattern"]` | Loaded when matching files open |
| Manual | No globs, `alwaysApply: false` | User/AI explicitly requests |

### Idiomatic Rule Patterns

**Layered rules**: General always-on, specific triggered by files.

```yaml
# .cursor/rules/general.mdc
---
description: Core project standards
alwaysApply: true
---

# Project Standards
- Follow existing code patterns
- Write self-documenting code
- Handle errors explicitly
```

```yaml
# .cursor/rules/typescript.mdc
---
description: TypeScript standards
globs: ["**/*.ts", "**/*.tsx"]
---

# TypeScript Guidelines
- Enable strict mode
- Prefer interfaces for object shapes
- Use discriminated unions for state
```

**Focused rules**: One domain per file.

```yaml
# Good: focused testing rule
---
description: Testing guidelines
globs: ["**/*.test.*", "**/*.spec.*"]
---

# Testing Standards
[Comprehensive testing guidance]
```

```yaml
# Bad: mixed concerns
---
description: Development standards
alwaysApply: true
---

# Coding Standards
[Coding patterns]

# Testing Standards  <- Should be separate file
[Testing patterns]

# API Standards  <- Should be separate file
[API patterns]
```

**Glob patterns**: Match precisely.

```yaml
# Common patterns
globs: ["**/*.ts"]                     # All TypeScript files
globs: ["**/*.test.ts", "**/*.spec.ts"]  # Test files
globs: ["src/api/**/*"]                # API directory
globs: ["**/*.{ts,tsx}"]               # TS and TSX
globs: ["!**/node_modules/**"]         # Exclude node_modules
```

## User Rules

Configured in Cursor Settings → Rules:

```markdown
# Personal Preferences

- Explain your reasoning before making changes
- Prefer simple solutions over clever ones
- Use descriptive variable names
- Ask clarifying questions when requirements are ambiguous
```

User rules:
- Apply to ALL projects
- Supplement project rules
- Good for personal workflow preferences

## MCP (Model Context Protocol)

### Configuration

```json
// .cursor/mcp.json
{
  "servers": {
    "database": {
      "command": "npx",
      "args": ["@cursor/mcp-server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["@cursor/mcp-server-filesystem"],
      "args_extra": ["--root", "./data"]
    }
  }
}
```

### Common MCP Servers

| Server | Purpose |
|--------|---------|
| `@cursor/mcp-server-postgres` | PostgreSQL database access |
| `@cursor/mcp-server-filesystem` | File system operations |
| `@cursor/mcp-server-github` | GitHub API integration |
| `@cursor/mcp-server-memory` | Persistent memory |

## Validation

### Check Rule Discovery

1. Open Cursor
2. Settings → Features → Rules
3. Verify rules appear in the list
4. Check "Auto Attached" status for glob-based rules

### Test File-Triggered Rules

1. Open a file matching your glob pattern
2. Start a conversation
3. Verify rule content appears in context
4. Check Rules panel shows rule as active

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Rule not loading | Invalid YAML | Check frontmatter syntax |
| Rule never triggers | Glob mismatch | Test glob pattern |
| Wrong rule activating | Overlapping globs | Make patterns more specific |
| Rule too slow | Too much content | Split into focused files |

## Migration from .cursorrules

If using the legacy `.cursorrules` file:

```bash
# 1. Create new structure
mkdir -p .cursor/rules

# 2. Move content
mv .cursorrules .cursor/rules/main.mdc

# 3. Add frontmatter
# Edit main.mdc to add:
# ---
# description: Main project rules
# alwaysApply: true
# ---

# 4. Split into focused files
# Extract testing rules to testing.mdc
# Extract API rules to api.mdc
# etc.

# 5. Remove legacy file
rm .cursorrules  # (if still exists)
```

## Deployment Patterns

### Project Setup

```bash
# Initialize for a new project
mkdir -p .cursor/rules

# Create core rules
cat > .cursor/rules/general.mdc << 'EOF'
---
description: Core project standards
alwaysApply: true
---

# Project Standards

- Follow existing code patterns
- Write self-documenting code
EOF

# Add to version control
git add .cursor/
git commit -m "Add Cursor rules"
```

### Team Sharing

```yaml
# .cursor/rules/team.mdc
---
description: Team coding standards
alwaysApply: true
---

# Team Standards

These rules ensure consistency across the team.

## Code Style
[Team's agreed patterns]

## Review Requirements
[What code reviews should check]
```

Add `.cursor/` to repository so team members get shared rules.

### Combining with User Rules

**Project rules** (`.cursor/rules/`):
- Team standards
- Project-specific patterns
- Shared across all team members

**User rules** (Cursor Settings):
- Personal preferences
- Workflow habits
- Not shared with team

Cursor combines both - user rules supplement project rules.

## Resources

- [Cursor Rules Documentation](https://cursor.com/docs/context/rules)
- [Rules for AI Guide](https://docs.cursor.com/context/rules-for-ai)
- [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules)
- [Meta-claude Cursor Patterns](~/.claude/skills/meta-claude/tools/cursor.md)
