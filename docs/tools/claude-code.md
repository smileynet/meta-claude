# Claude Code: Deployment & Idioms

This guide covers Claude Code deployment patterns and idiomatic usage. For general meta-patterns, see the [meta-claude skill](~/.claude/skills/meta-claude/).

## Directory Structure

```
~/.claude/                    # User-level configuration
├── skills/                   # Auto-activated knowledge
│   └── my-skill/
│       ├── SKILL.md         # Required: main entry point
│       ├── reference.md     # Optional: detailed docs
│       ├── examples.md      # Optional: usage examples
│       └── sources.md       # Optional: external links
├── commands/                 # Manual /slash invocation
│   └── my-command.md
├── agents/                   # Custom subagents
│   └── my-agent.md
├── hooks/                    # Post-tool automation
│   └── my-hook.py
├── scripts/                  # Helper scripts (not loaded as context)
│   └── helper.sh
├── settings.json            # Global preferences
└── plans/                   # Active planning files

.claude/                     # Project-level configuration
└── [same structure as above]
```

## Skills

### SKILL.md Format

```yaml
---
name: skill-name              # Required: identifier
description: Brief description with trigger keywords.  # Required
allowed-tools: Read, Grep, Glob  # Optional: restrict tools
---

# Skill Title

[Markdown content with guidance]
```

### Idiomatic Skill Patterns

**Focused purpose**: One skill = one domain.

```yaml
# Good: focused
---
name: commit-helper
description: Generate commit messages. Use when writing commits.
---

# Bad: kitchen sink
---
name: dev-helper
description: Help with commits, testing, debugging, deployment, and more.
---
```

**Trigger-rich descriptions**: Include words users actually say.

```yaml
# Good: specific triggers
description: Generate commit messages. Use when writing commits, git messages, or preparing changes for review.

# Bad: vague
description: Helps with version control.
```

**Progressive disclosure**: Essential info in SKILL.md, depth in supporting files.

```markdown
## Quick Start
[Essential steps]

## Reference
For API details, see [reference.md](reference.md).
For examples, see [examples.md](examples.md).
```

## Commands

### Command Format

```markdown
---
description: What this command does  # Required for discovery
---

[Instructions or skill reference]

$ARGUMENTS  # Placeholder for user input
```

### Skill-Linking Pattern

Commands should reference skills, not duplicate knowledge:

```markdown
---
description: Generate a commit message
---

Follow the guidelines in:
@~/.claude/skills/commit-helper/SKILL.md

Generate a commit message for: $ARGUMENTS
```

### Command Variables

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | Everything after the command name |
| `$SELECTION` | Currently selected text (IDE integration) |
| `@filepath` | Load file content into context |

## Agents

### Agent Format

```yaml
---
name: agent-name                    # Required
description: When to use this agent # Required for discovery
model: sonnet                       # Optional: sonnet, opus, haiku
allowed-tools: Read, Grep, Glob     # Optional: restrict tools
---

You are a specialist in [domain].

[System prompt with detailed instructions]
```

### Model Selection

| Model | Use For |
|-------|---------|
| `haiku` | Quick, simple tasks; low latency |
| `sonnet` | Balanced capability; most tasks |
| `opus` | Complex reasoning; architectural decisions |

### Idiomatic Agent Patterns

**Specialist focus**: Agents excel at specific domains.

```yaml
---
name: security-reviewer
description: Security-focused code review. Use for security audits, vulnerability assessment.
model: opus
allowed-tools: Read, Grep, Glob
---

You are a security specialist. Focus exclusively on:
- OWASP Top 10 vulnerabilities
- Authentication/authorization flaws
- Input validation issues
- Secrets exposure
```

**Tool restrictions**: Grant minimum necessary permissions.

```yaml
# Read-only agent (safe for sensitive contexts)
allowed-tools: Read, Grep, Glob

# Can modify files
allowed-tools: Read, Grep, Glob, Edit, Write

# Full access (use sparingly)
# [no allowed-tools field = all tools]
```

## Hooks

### Hook Format

```python
#!/usr/bin/env python3
"""
Hook: post-tool processing
Triggered after: Edit, Write
"""

import json
import sys

def main():
    # Read hook input from stdin
    input_data = json.load(sys.stdin)

    tool_name = input_data.get("tool_name")
    tool_input = input_data.get("tool_input", {})
    tool_output = input_data.get("tool_output", {})

    # Process...

    # Output: continue, block, or modify
    result = {
        "decision": "continue",  # or "block"
        "reason": "Processed successfully"
    }
    print(json.dumps(result))

if __name__ == "__main__":
    main()
```

### Hook Configuration

In `settings.json`:
```json
{
  "hooks": {
    "post_tool": [
      {
        "matcher": "Edit|Write",
        "path": "~/.claude/hooks/formatter.py"
      }
    ]
  }
}
```

### Idiomatic Hook Patterns

**Auto-formatting**: Format files after edits.

```python
# Run ruff on Python files after Edit/Write
if tool_name in ["Edit", "Write"]:
    file_path = tool_input.get("file_path", "")
    if file_path.endswith(".py"):
        subprocess.run(["ruff", "format", file_path])
```

**Validation**: Block dangerous operations.

```python
# Prevent editing sensitive files
if tool_name == "Edit":
    file_path = tool_input.get("file_path", "")
    if ".env" in file_path or "secrets" in file_path:
        print(json.dumps({
            "decision": "block",
            "reason": "Cannot edit sensitive files"
        }))
        return
```

## Validation

### Debug Mode

```bash
# See skill discovery
claude --debug -p "list your skills"

# Test specific trigger
claude --debug -p "help me write a commit"
# Watch for: "Loading skill: commit-helper"

# Dry-run (read-only)
claude --debug -p "review this" --allowedTools "Read,Grep,Glob"
```

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Skill not found | Missing SKILL.md | Create SKILL.md in skill directory |
| Skill not triggering | Vague description | Add specific trigger keywords |
| Wrong skill activating | Overlapping keywords | Make descriptions more specific |
| YAML parse error | Tabs instead of spaces | Use spaces, start with `---` |

### Validation Checklist

- [ ] SKILL.md exists with valid YAML frontmatter
- [ ] `name` and `description` fields present
- [ ] Description contains trigger keywords
- [ ] Supporting files are linked correctly
- [ ] `claude --debug` shows skill discovery
- [ ] Test prompt activates correct skill

## Deployment via Chezmoi

Skills are deployed via chezmoi from the dotfiles repository:

```
~/code/dotfiles/
└── dot_claude/
    ├── skills/
    │   └── my-skill/
    │       └── SKILL.md
    └── agents/
        └── my-agent.md
```

After editing:
```bash
cd ~/code/dotfiles
chezmoi add ~/.claude/skills/my-skill/
git add -A && git commit -m "Add my-skill"
git push
chezmoi apply  # On other machines
```

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Skills Reference](~/.claude/skills/claude-skills/SKILL.md)
- [Commands Reference](~/.claude/skills/claude-commands/SKILL.md)
