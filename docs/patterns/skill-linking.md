# Pattern: Skill-Linking

Commands are thin wrappers that load skills via references.

## The Principle

Separate **what to know** (skills) from **how to invoke** (commands). Commands don't contain knowledge—they point to it.

## Why It Matters

- **Single source of truth**: Update skill once, all linked commands benefit
- **Consistency**: Same guidance regardless of invocation method
- **Flexibility**: Multiple commands can reference the same skill
- **Maintainability**: Knowledge centralized, invocation distributed

## Implementation Across Tools

### Claude Code

**Skill** (`~/.claude/skills/commit-helper/SKILL.md`):
```yaml
---
name: commit-helper
description: Generate commit messages. Use when writing commits.
---

# Commit Helper

[All the knowledge about good commits]
```

**Command** (`~/.claude/commands/commit.md`):
```markdown
Follow the guidelines in:
@~/.claude/skills/commit-helper/SKILL.md

Generate a commit message for the staged changes.
```

**Key syntax**: `@filepath` loads the file into context.

### Cursor

**Rule** (`.cursor/rules/testing.mdc`):
```yaml
---
description: Testing standards
globs: ["**/*.test.*"]
---

# Testing Guidelines
[All the knowledge]
```

**Reference from another rule**:
```yaml
---
description: Integration tests
globs: ["**/*.integration.*"]
---

Follow the core testing guidelines above, with these additions for integration tests:
[Integration-specific guidance]
```

Cursor auto-loads matching rules, so linking is implicit via glob patterns.

### Kiro

**Steering** (`.kiro/steering.md`):
```markdown
# Project Standards
[Core knowledge]
```

**Spec references steering**:
```markdown
# Feature Spec

Follow the project standards in steering.md.

## Requirements
[Feature-specific requirements]
```

### OpenCode

**Agent** (`~/.config/opencode/agents/reviewer.yaml`):
```yaml
name: reviewer
system: |
  You are a code reviewer.
  Load and follow: ~/.config/opencode/knowledge/review-checklist.md
```

**Knowledge file** (`~/.config/opencode/knowledge/review-checklist.md`):
```markdown
# Code Review Checklist
[All review criteria]
```

## Examples

### Good: Linked Command

```markdown
# /review command

Follow the code review guidelines in:
@~/.claude/skills/code-review/SKILL.md

Review the changes in this PR: $ARGUMENTS
```

The command is 4 lines. All knowledge lives in the skill.

### Bad: Duplicated Knowledge

```markdown
# /review command

## Code Review Guidelines
[100 lines of review criteria copied from somewhere]

Review the changes in this PR: $ARGUMENTS
```

If guidelines change, you must update every command that copied them.

### Good: Multiple Commands, One Skill

```markdown
# /review-security
@~/.claude/skills/code-review/SKILL.md
Focus specifically on security vulnerabilities.

# /review-performance
@~/.claude/skills/code-review/SKILL.md
Focus specifically on performance issues.

# /review-full
@~/.claude/skills/code-review/SKILL.md
Comprehensive review of all aspects.
```

Three commands, one source of truth. Update the skill, all three improve.

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Knowledge in commands | Duplicated, hard to update | Move to skill, link with @file |
| No skill for common knowledge | Repeated in multiple places | Create skill, link from all uses |
| Deep nesting | Hard to follow reference chain | Keep to 1-2 levels of reference |
| Circular references | Infinite loops | Skills should not reference commands |

## Finding Linked Commands

When updating a skill, find commands that reference it:

```bash
# Claude Code
grep -r "@.*skills/my-skill" ~/.claude/commands/
grep -r "@.*skills/my-skill" .claude/commands/

# Check project-level too
grep -r "@.*skills/my-skill" .
```

## Best Practices

1. **Skills contain knowledge**: Guidelines, rules, best practices
2. **Commands contain invocation**: What action to take, what arguments to use
3. **Commands add context**: "Focus on X" or "Apply to $ARGUMENTS"
4. **One level of linking**: Command → Skill (avoid Skill → Skill → Skill)
5. **Document the link**: In both skill and command, note the relationship

## Related Patterns

- [Single Source of Truth](single-source-truth.md) - The principle behind linking
- [Progressive Disclosure](progressive-disclosure.md) - How to structure the skill content
