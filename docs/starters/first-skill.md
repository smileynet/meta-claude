# Create Your First Skill

This walkthrough guides you through creating a working Claude Code skill from scratch.

## Objective

Build a skill that solves ONE real problem you have. By the end, you'll have:
- A working skill that triggers correctly
- Understanding of the skill creation process
- A template for creating future skills

## Step 1: Identify Your Pain Point

Think about something that annoys you when coding:

| Pain Point | Potential Skill |
|------------|-----------------|
| Forgetting test coverage | `test-reminder` - Prompts to add tests |
| Inconsistent commit messages | `commit-helper` - Guides commit format |
| Repeating same explanations | `project-context` - Explains project patterns |
| Boilerplate code | `scaffold-helper` - Generates common patterns |

**Pick ONE thing**. Start small. You can always expand later.

For this walkthrough, we'll create a `commit-helper` skill.

## Step 2: Create the Skill Directory

```bash
# Create skill directory
mkdir -p ~/.claude/skills/commit-helper

# Verify it exists
ls ~/.claude/skills/
```

## Step 3: Write SKILL.md

Create the skill file:

```bash
# Open for editing (use your preferred editor)
code ~/.claude/skills/commit-helper/SKILL.md
# or: vim ~/.claude/skills/commit-helper/SKILL.md
# or: notepad ~/.claude/skills/commit-helper/SKILL.md
```

Add this content:

```yaml
---
name: commit-helper
description: Generate commit messages from staged changes. Use when writing commits, git messages, or preparing changes for review.
---

# Commit Message Helper

Generate clear, conventional commit messages from staged changes.

## Instructions

1. Run `git diff --staged` to see the changes
2. Analyze what was changed and why
3. Generate a commit message following the format below

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type (required)
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code change that neither fixes nor adds
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Scope (optional)
Component or area affected: `auth`, `api`, `ui`, etc.

### Subject (required)
- Imperative mood: "Add feature" not "Added feature"
- No period at the end
- Under 50 characters

### Body (optional)
- Explain what and why, not how
- Wrap at 72 characters

### Footer (optional)
- Reference issues: `Fixes #123`
- Breaking changes: `BREAKING CHANGE: description`

## Examples

### Simple fix
```
fix(auth): correct password validation regex

The previous regex allowed passwords under 8 characters.
```

### Feature with breaking change
```
feat(api): add pagination to user list endpoint

BREAKING CHANGE: page parameter now required for /users
```

## Best Practices

- One logical change per commit
- If you need "and" in the subject, split the commit
- Reference related issues
- Explain WHY the change was needed
```

## Step 4: Test Discovery

Verify Claude finds your skill:

```bash
claude --debug -p "list your skills"
```

Look for output mentioning `commit-helper`. If not found:
- Check SKILL.md exists in the right location
- Verify YAML frontmatter starts with `---` on line 1
- Ensure `name` and `description` fields are present

## Step 5: Test Activation

Test that your skill triggers on the right keywords:

```bash
claude --debug -p "help me write a commit message"
```

Watch the debug output for:
```
Loading skill: commit-helper
```

If wrong skill activates or no skill activates:
- Make description more specific
- Add more trigger keywords
- Check for overlapping descriptions with other skills

## Step 6: Test Functionality

Use the skill for real:

```bash
# Stage some changes
git add -A

# Ask for help
claude -p "generate a commit message for my staged changes"
```

Verify:
- Claude runs `git diff --staged`
- Output follows your format
- Message is appropriate for the changes

## Step 7: Iterate

Based on usage, you might want to:

### Add More Context
```yaml
description: Generate commit messages from staged changes. Use when writing commits, git messages, preparing changes for review, or needing help with conventional commits format.
```

### Split Into Files
If the skill grows, use progressive disclosure:

```
commit-helper/
├── SKILL.md           # Essential instructions
├── reference.md       # Detailed type definitions
├── examples.md        # More examples
└── sources.md         # Links to conventional commits spec
```

### Add Tool Restrictions
If the skill should be read-only:
```yaml
---
name: commit-helper
description: Generate commit messages...
allowed-tools: Read, Grep, Glob, Bash
---
```

## Graduation Criteria

Your skill is ready when:

- [ ] Triggers correctly on expected keywords
- [ ] Provides helpful guidance for your use case
- [ ] Doesn't interfere with other skills
- [ ] You've used it successfully multiple times

## Common Issues

### Skill Not Found

```bash
# Check file exists
ls -la ~/.claude/skills/commit-helper/SKILL.md

# Check YAML syntax
head -10 ~/.claude/skills/commit-helper/SKILL.md
# Should start with ---
```

### Wrong Skill Activating

Make your description more specific:
```yaml
# Too vague - might conflict with other skills
description: Help with git

# Specific - clear trigger
description: Generate commit messages from staged changes. Use when writing commits.
```

### Skill Too Slow

If your skill file is large (>500 lines), split it:
```markdown
## Quick Start
[Essential info only]

## Reference
For complete details, see [reference.md](reference.md).
```

## Next Steps

1. Create a [command](first-command.md) that invokes your skill
2. Try [linking multiple skills](../patterns/skill-linking.md)
3. Add your skill to [chezmoi](../technical-bootstrap.md#deployment-via-chezmoi) for sync
