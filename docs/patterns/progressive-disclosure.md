# Pattern: Progressive Disclosure

Essential information first, details on demand.

## The Principle

Don't front-load everything. Present the minimum needed to get started, then provide paths to deeper knowledge when needed.

## Why It Matters

- **Reduces cognitive load**: Users aren't overwhelmed on first encounter
- **Faster activation**: AI tools load less context initially
- **Scales with complexity**: Simple tasks stay simple; complex tasks have depth available
- **Maintainable**: Changes to details don't require editing the main file

## Implementation Across Tools

### Claude Code

**File Structure**:
```
my-skill/
├── SKILL.md           # Essential (~150 lines)
├── reference.md       # Detailed API docs
├── examples.md        # Usage patterns
└── sources.md         # External links
```

**Linking Pattern**:
```markdown
## Quick Start
[Essential instructions here]

## Reference
For complete API details, see [reference.md](reference.md).
For practical examples, see [examples.md](examples.md).
```

**Target Sizes**:
- SKILL.md: < 500 lines (ideally ~150)
- Supporting files: As needed
- Total skill: Any size, layered appropriately

### Cursor

**File Structure**:
```
.cursor/rules/
├── core.mdc           # Always-on essentials
├── testing.mdc        # Loaded for test files
└── api.mdc            # Loaded for API routes
```

**Activation Pattern**:
```yaml
---
description: Core coding standards
globs: ["**/*"]
alwaysApply: true
---
# Minimal essential rules
```

```yaml
---
description: Testing patterns
globs: ["**/*.test.*", "**/*.spec.*"]
---
# Detailed testing guidance (only loads for test files)
```

### Kiro

**Spec Structure**:
```
.kiro/
├── steering.md        # Global guidance (brief)
├── specs/
│   ├── requirements.md   # What to build
│   ├── design.md         # How to build
│   └── tasks.md          # Step-by-step
```

Each spec level adds detail. Requirements are brief; tasks are comprehensive.

### OpenCode

**Agent Definitions**:
```yaml
# agent.yaml - Brief system prompt
system: "You are a code reviewer. Focus on security and performance."

# Detailed guidelines loaded via tool calls when needed
```

**Command Structure**:
```
~/.config/opencode/commands/
├── review.md          # Simple command
└── review-detailed/
    ├── command.md     # Entry point
    └── checklist.md   # Loaded when comprehensive review requested
```

## Examples

### Good: Layered Skill

```markdown
# Git Commit Helper

## Quick Start
Run `git diff --staged`, then generate a message following conventional commits.

## Format
- Type: feat|fix|docs|style|refactor|test|chore
- Scope: optional, in parentheses
- Description: imperative, < 50 chars

## Deep Dive
For edge cases and advanced patterns, see [reference.md](reference.md).
```

### Bad: Everything Upfront

```markdown
# Git Commit Helper

## Quick Start
[20 lines of basic instructions]

## Format
[50 lines of format rules]

## Edge Cases
[100 lines of edge case handling]

## History
[50 lines of why these conventions exist]

## Examples
[200 lines of examples]

## Troubleshooting
[100 lines of troubleshooting]
```

The bad example overwhelms. Most users need Quick Start + Format. The rest should be in separate files.

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Monolithic SKILL.md | Slow to load, hard to navigate | Split into main + supporting files |
| No links to depth | Users can't find details | Add "For more, see..." sections |
| Over-splitting | Too many tiny files | Combine related content |
| Duplicated content | Updates needed in multiple places | Single source, reference from others |

## Metrics

**Good progressive disclosure**:
- Main file readable in < 2 minutes
- Supporting files findable via clear links
- Most tasks completable with main file alone
- Complex tasks have documented paths to depth

## Related Patterns

- [Single Source of Truth](single-source-truth.md) - Where knowledge lives
- [Skill-Linking](skill-linking.md) - Commands reference skills
