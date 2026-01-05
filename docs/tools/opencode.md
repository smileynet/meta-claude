# OpenCode: Deployment & Idioms

This guide covers OpenCode deployment patterns and idiomatic usage. For general patterns, see the [meta-claude skill](~/.claude/skills/meta-claude/tools/opencode.md).

## Directory Structure

```
~/.config/opencode/           # User-level configuration
├── config.yaml              # Main configuration
├── .env                     # API keys
├── commands/                # Custom commands
│   └── review.md
├── agents/                  # Custom agents
│   └── architect.yaml
├── prompts/                 # Agent system prompts
│   └── architect-prompt.md
└── knowledge/               # Shared knowledge files
    └── standards.md

.opencode/                   # Project-level configuration
├── config.yaml             # Project overrides
└── commands/               # Project-specific commands
```

## Configuration

### Main Config

```yaml
# ~/.config/opencode/config.yaml

# Default model
model: claude-sonnet-4-20250514

# TUI settings
tui:
  theme: dark
  show_tokens: true

# Tool permissions
permissions:
  bash:
    allow:
      - "git *"
      - "npm *"
      - "pytest *"
    deny:
      - "rm -rf *"
      - "sudo *"

# Default agent
default_agent: coder
```

### API Keys

```bash
# ~/.config/opencode/.env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...

# Optional: custom endpoints
ANTHROPIC_BASE_URL=https://...
```

## Commands

### Command Format

```markdown
# ~/.config/opencode/commands/review.md

Review this code for best practices and potential issues.

Focus on:
- Error handling
- Performance implications
- Security vulnerabilities
- Code clarity

Code to review:
$CODE
```

### Command Variables

| Variable | Description |
|----------|-------------|
| `$CODE` | Selected/provided code |
| `$FILE` | Current file path |
| `$SELECTION` | Selected text |
| `$ARGUMENTS` | Command arguments |

### Idiomatic Command Patterns

**Simple command**:
```markdown
# explain.md
Explain this code in simple terms:
$CODE
```

**Agent-linked command**:
```markdown
# security-review.md
@agent:security-reviewer

Perform a security-focused review of:
$CODE
```

**Parameterized command**:
```markdown
# refactor.md
Refactor this code with focus on: $ARGUMENTS

Code:
$CODE
```

## Agents

### Agent Format

```yaml
# ~/.config/opencode/agents/architect.yaml
name: architect
description: System design and architecture decisions
model: claude-opus-4-20250514
prompt: prompts/architect-prompt.md
tools:
  - read
  - search
  - web
```

### Agent Prompt File

```markdown
# ~/.config/opencode/prompts/architect-prompt.md

You are a senior software architect. Your role is to:

## Responsibilities
- Design scalable system architectures
- Make technology selection decisions
- Define component boundaries
- Establish patterns and conventions

## Approach
1. Understand requirements thoroughly
2. Consider multiple approaches
3. Evaluate trade-offs explicitly
4. Recommend with clear reasoning

## Output Format
- Start with a summary of the decision
- List key trade-offs considered
- Provide implementation guidance
- Note any risks or dependencies
```

### Model Selection

```yaml
# Quick tasks - use haiku
name: quick-helper
model: claude-3-5-haiku-20241022
# Fast responses, lower cost

# Standard tasks - use sonnet
name: coder
model: claude-sonnet-4-20250514
# Balanced capability and speed

# Complex tasks - use opus
name: architect
model: claude-opus-4-20250514
# Maximum reasoning capability
```

### Tool Permissions

```yaml
# Read-only agent
tools:
  - read
  - search

# Can modify files
tools:
  - read
  - search
  - edit
  - write

# Full access (use sparingly)
tools:
  - read
  - search
  - edit
  - write
  - bash
  - web
```

### Idiomatic Agent Patterns

**Specialist agent**:
```yaml
name: security-reviewer
description: Security-focused code analysis
model: claude-opus-4-20250514
prompt: prompts/security.md
tools:
  - read
  - search
# Read-only - security reviewers shouldn't modify code
```

**Worker agent**:
```yaml
name: test-writer
description: Generate unit tests for code
model: claude-sonnet-4-20250514
prompt: prompts/test-writer.md
tools:
  - read
  - search
  - write
# Can write test files
```

**Research agent**:
```yaml
name: researcher
description: Research technologies and best practices
model: claude-sonnet-4-20250514
prompt: prompts/researcher.md
tools:
  - read
  - search
  - web
# Can search web for current info
```

## Knowledge Files

Shared knowledge referenced by agents:

```markdown
# ~/.config/opencode/knowledge/python-standards.md

# Python Coding Standards

## Style
- Follow PEP 8
- Use type hints for all public functions
- Maximum line length: 88 (Black default)

## Testing
- Use pytest for all tests
- Aim for >80% coverage
- Mock external dependencies

## Documentation
- Docstrings for all public functions
- Use Google-style docstring format
```

Reference in agent prompts:
```markdown
# architect-prompt.md

Follow the standards in:
~/.config/opencode/knowledge/python-standards.md

[Rest of prompt]
```

## Validation

### List Available

```bash
# List agents
opencode agents list

# List commands
opencode commands list
```

### Test Agent

```bash
# Simple test
opencode -a architect "hello"

# With dry-run (see what tools would be used)
opencode -a architect --dry-run "design a caching layer"
```

### Test Command

```bash
# Run command
opencode run review "def add(a, b): return a + b"
```

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Agent not found | Wrong path or name | Check `agents list` output |
| API error | Invalid/missing key | Check `.env` file |
| Permission denied | Tool not in allowed list | Add tool to agent's `tools:` |
| Prompt not loading | Path error | Use relative path from config dir |

## Deployment Patterns

### User Setup

```bash
# Create directory structure
mkdir -p ~/.config/opencode/{commands,agents,prompts,knowledge}

# Create config
cat > ~/.config/opencode/config.yaml << 'EOF'
model: claude-sonnet-4-20250514
default_agent: coder
permissions:
  bash:
    allow: ["git *", "npm *"]
    deny: ["rm -rf *"]
EOF

# Add API keys
cat > ~/.config/opencode/.env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-...
EOF
chmod 600 ~/.config/opencode/.env
```

### Project Override

```yaml
# .opencode/config.yaml

# Override default model for this project
model: claude-opus-4-20250514

# Project-specific permissions
permissions:
  bash:
    allow:
      - "python *"
      - "pip *"
      - "pytest *"
```

### Team Sharing

```
.opencode/
├── config.yaml      # Project settings (commit)
├── commands/        # Project commands (commit)
└── .env             # API keys (DO NOT COMMIT)
```

Add to `.gitignore`:
```
.opencode/.env
```

## CLI Usage

### Basic Commands

```bash
# Interactive TUI
opencode

# Single prompt
opencode "explain this code"

# With specific agent
opencode -a architect "design a caching layer"

# Run saved command
opencode run review code.py
```

### Common Flags

| Flag | Purpose |
|------|---------|
| `-a, --agent` | Use specific agent |
| `--dry-run` | Show what would happen |
| `--no-tools` | Disable tool use |
| `-v, --verbose` | Verbose output |

## Resources

- [OpenCode Documentation](https://opencode.ai/docs/)
- [GitHub Repository](https://github.com/opencode-ai/opencode)
- [Agents Guide](https://opencode.ai/docs/agents/)
- [Meta-claude OpenCode Patterns](~/.claude/skills/meta-claude/tools/opencode.md)
