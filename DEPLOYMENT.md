# Meta-Agentic System Deployment Guide

This guide documents how to bootstrap a meta-agentic system—a configuration layer that uses AI coding tools to improve AI coding tool configurations.

## Who This Is For

- Developers setting up AI coding tools on a new machine
- Users wanting to grow their personal AI toolkit systematically
- Those seeking portable, cross-tool configuration patterns

## Two Paths

Choose based on your preference:

### Path A: Technical Bootstrap (Get Running Now)

1. [Machine Setup](docs/technical-bootstrap.md) - Install chezmoi, clone repos, apply configs
2. [Verify Installation](docs/technical-bootstrap.md#verification)
3. [Create Your First Skill](docs/starters/first-skill.md)

### Path B: Conceptual Bootstrap (Understand First)

1. [Philosophy](docs/philosophy.md) - Mental model for meta-agentic thinking
2. [Universal Patterns](docs/patterns/) - Cross-tool principles
3. [Tool-Specific Implementation](docs/tools/) - How patterns manifest in each tool

## Quick Reference

### Existing Resources

| Resource | Location | Purpose |
|----------|----------|---------|
| meta-claude skill | `~/.claude/skills/meta-claude/` | Runtime knowledge for AI tools |
| Dotfiles | `~/code/dotfiles/` | Chezmoi-managed configs |
| This repo | `~/code/meta-claude/` | Research and improvements |

### Universal Patterns

| Pattern | Description | Guide |
|---------|-------------|-------|
| Progressive Disclosure | Essential info first, details on demand | [docs/patterns/progressive-disclosure.md](docs/patterns/progressive-disclosure.md) |
| Skill-Linking | Commands load skills via references | [docs/patterns/skill-linking.md](docs/patterns/skill-linking.md) |
| Single Source of Truth | Knowledge lives in ONE place | [docs/patterns/single-source-truth.md](docs/patterns/single-source-truth.md) |
| Validation Workflows | Quality assurance before deployment | [docs/patterns/validation-workflows.md](docs/patterns/validation-workflows.md) |

### Tool-Specific Guides

| Tool | Config Location | Guide |
|------|-----------------|-------|
| Claude Code | `~/.claude/` | [docs/tools/claude-code.md](docs/tools/claude-code.md) |
| Cursor | `.cursor/rules/` | [docs/tools/cursor.md](docs/tools/cursor.md) |
| Kiro | `.kiro/` | [docs/tools/kiro.md](docs/tools/kiro.md) |
| OpenCode | `~/.config/opencode/` | [docs/tools/opencode.md](docs/tools/opencode.md) |

### Getting Started Walkthroughs

| First Step | Time | Guide |
|------------|------|-------|
| Create a skill | ~15 min | [docs/starters/first-skill.md](docs/starters/first-skill.md) |
| Create a command | ~10 min | [docs/starters/first-command.md](docs/starters/first-command.md) |
| Create an agent | ~20 min | [docs/starters/first-agent.md](docs/starters/first-agent.md) |

## Repository Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                    meta-claude Repository                        │
│                 (Research & Development Workspace)               │
│                                                                  │
│  You are here: DEPLOYMENT.md, docs/, templates/                 │
└──────────────────────────────────┬──────────────────────────────┘
                                   │
                                   │ Stabilized content merges to
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    dotfiles Repository                           │
│                 (Chezmoi-managed deployables)                    │
│                                                                  │
│  dot_claude/skills/*, dot_claude/agents/*, etc.                 │
└──────────────────────────────────┬──────────────────────────────┘
                                   │
                                   │ chezmoi apply
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                       ~/.claude/                                 │
│                   (Runtime configuration)                        │
│                                                                  │
│  What Claude actually uses during conversations                  │
└─────────────────────────────────────────────────────────────────┘
```

**Key distinction**:
- **This repo** (`meta-claude`) = Development workspace for research and testing
- **dotfiles repo** = Production configurations (chezmoi-managed)
- **~/.claude/** = Runtime destination where Claude reads configurations

## Templates

Ready-to-use scaffolding in [templates/](templates/):

| Template | Use Case |
|----------|----------|
| [skill-simple/](templates/skill-simple/) | Single-file skill |
| [skill-complex/](templates/skill-complex/) | Multi-file skill with progressive disclosure |
| [command-basic.md](templates/command-basic.md) | Standalone command |
| [command-skill-linked.md](templates/command-skill-linked.md) | Command that loads a skill |
| [agent-specialist.md](templates/agent-specialist.md) | Custom subagent |

## Next Steps

1. **New to this?** Start with [Philosophy](docs/philosophy.md)
2. **Want to get running?** Jump to [Technical Bootstrap](docs/technical-bootstrap.md)
3. **Ready to create?** Try [Your First Skill](docs/starters/first-skill.md)
