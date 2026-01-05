# Create Your First Command

This walkthrough guides you through creating a Claude Code slash command that links to a skill.

## Objective

Build a command that:
- Invokes with `/command-name`
- Links to an existing skill (single source of truth)
- Accepts user arguments

## Prerequisites

You should have completed [Create Your First Skill](first-skill.md) or have an existing skill to link to.

## Step 1: Understand Commands vs Skills

| Aspect | Skill | Command |
|--------|-------|---------|
| Activation | Automatic (keyword matching) | Manual (`/command-name`) |
| Purpose | Knowledge/guidance | Invocation/action |
| Content | Full instructions | Reference to skill + action |
| Best for | Reusable knowledge | Explicit, repeatable actions |

Commands are thin wrappers that point to skills.

## Step 2: Create the Command

Create a command file:

```bash
# Create commands directory if needed
mkdir -p ~/.claude/commands

# Create command file
code ~/.claude/commands/commit.md
```

Add this content:

```markdown
---
description: Generate a commit message for staged changes
---

Follow the guidelines in:
@~/.claude/skills/commit-helper/SKILL.md

Generate a commit message for the currently staged changes.

$ARGUMENTS
```

## Step 3: Understand the Format

### Frontmatter

```yaml
---
description: Brief description for discovery
---
```

The description helps Claude understand when this command is relevant.

### Skill Reference

```markdown
@~/.claude/skills/commit-helper/SKILL.md
```

The `@filepath` syntax loads the skill content into context. This is the **skill-linking pattern**.

### Arguments

```markdown
$ARGUMENTS
```

Everything after `/commit` gets substituted here. For example:
- `/commit` → empty arguments
- `/commit with detailed body` → "with detailed body"

## Step 4: Test the Command

```bash
# Basic invocation
claude -p "/commit"

# With arguments
claude -p "/commit include issue reference"
```

Verify:
- Command is recognized
- Skill content is loaded
- Arguments are passed through

## Step 5: Add Variations

Create related commands that use the same skill:

### Quick Commit
```markdown
# ~/.claude/commands/commit-quick.md
---
description: Generate a brief commit message
---

Follow the guidelines in:
@~/.claude/skills/commit-helper/SKILL.md

Generate a BRIEF commit message (subject line only, no body) for the staged changes.
```

### Detailed Commit
```markdown
# ~/.claude/commands/commit-detailed.md
---
description: Generate a detailed commit message with body
---

Follow the guidelines in:
@~/.claude/skills/commit-helper/SKILL.md

Generate a DETAILED commit message with full body explanation for the staged changes.
Include:
- What changed
- Why it changed
- Any breaking changes or side effects
```

Both commands use the same skill, but add different context.

## Step 6: Project-Level Commands

Commands can also live in project directories:

```bash
# Project-specific command
mkdir -p .claude/commands
```

```markdown
# .claude/commands/commit.md
---
description: Generate project-specific commit message
---

Follow the guidelines in:
@~/.claude/skills/commit-helper/SKILL.md

Additional project conventions:
- Always reference Jira ticket: PROJECT-XXX
- Use "Component:" prefix for scope

Generate a commit message for staged changes.
```

Project commands:
- Override user commands with same name
- Contain team-specific conventions
- Are shared via version control

## Command Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `$ARGUMENTS` | Everything after command name | `/commit fix typo` → "fix typo" |
| `$SELECTION` | Selected text (IDE) | Highlighted code |
| `@filepath` | Load file content | `@README.md` |

## Best Practices

### 1. Keep Commands Thin

```markdown
# Good: references skill
@~/.claude/skills/commit-helper/SKILL.md
Generate a commit message.

# Bad: duplicates skill content
## Commit Format
<type>(<scope>): <subject>
...
[100 lines of duplicated content]
```

### 2. Add Context, Not Duplication

```markdown
# Good: skill + context
@~/.claude/skills/commit-helper/SKILL.md
Focus specifically on documenting breaking changes.

# Bad: repeating skill content
Follow conventional commits format...
[repeats what's in the skill]
```

### 3. Use Descriptive Names

```
# Good
/commit
/commit-quick
/commit-breaking

# Bad
/c
/cm
/cmt
```

### 4. Document the Relationship

In your skill, note which commands link to it:

```markdown
## Related Commands

This skill is invoked by:
- `/commit` - Standard commit message
- `/commit-quick` - Brief commit
- `/commit-detailed` - Detailed commit with body
```

## Validation Checklist

- [ ] Command file has valid frontmatter
- [ ] `@filepath` points to existing skill
- [ ] Command triggers with `/command-name`
- [ ] Arguments passed through correctly
- [ ] Skill content appears in context

## Common Issues

### Command Not Recognized

```bash
# Check file exists
ls ~/.claude/commands/

# Verify frontmatter
head -5 ~/.claude/commands/commit.md
```

### Skill Not Loading

```bash
# Check skill path is correct
ls ~/.claude/skills/commit-helper/SKILL.md

# Verify @ syntax
grep "@" ~/.claude/commands/commit.md
```

### Arguments Not Working

Ensure `$ARGUMENTS` is on its own line or clearly positioned:

```markdown
# Good
Generate for: $ARGUMENTS

# Problematic
Generate$ARGUMENTS  # No space
```

## Next Steps

1. Create an [agent](first-agent.md) for complex tasks
2. Learn about [skill-linking patterns](../patterns/skill-linking.md)
3. Add commands to [chezmoi](../technical-bootstrap.md#deployment-via-chezmoi) for sync
