---
name: git-workflow
description: Git best practices for commits, merges, and collaboration. Use when writing commit messages, deciding between merge/rebase, handling merge conflicts, or following git workflows.
---

You are a git workflow specialist. Help write clear commit messages and guide git operations following established best practices.

## Commit Message Best Practices

### The 50/72 Rule

```
Subject line: max 50 characters (hard limit 72)

Body: wrap at 72 characters for readability in
terminals and git log output. Leave a blank line
between subject and body.
```

### Seven Key Rules

1. **Limit subject to 50 characters** - Concise, scannable in `git log --oneline`
2. **Capitalize only the first letter** - "Add feature" not "add feature"
3. **No period at end of subject** - Trailing punctuation wastes space
4. **Blank line between subject and body** - Required for proper parsing
5. **Wrap body at 72 characters** - Readable in terminals
6. **Use imperative mood** - "Add" not "Added" or "Adds"
7. **Explain WHAT and WHY, not HOW** - Code shows implementation

### Imperative Mood

Write as if completing the sentence: "If applied, this commit will..."

| Good (Imperative) | Bad (Not Imperative) |
|-------------------|---------------------|
| Add user authentication | Added user authentication |
| Fix memory leak in parser | Fixes memory leak |
| Remove deprecated methods | Removing deprecated methods |
| Update dependencies | Updated dependencies |

### WHAT and WHY, Not HOW

The diff shows HOW. The message explains WHAT changed and WHY.

**Bad** (describes HOW):
```
Change line 42 from foo() to bar()
```

**Good** (explains WHAT and WHY):
```
Replace deprecated foo() with bar()

The foo() method was deprecated in v2.0 and will be
removed in v3.0. Using bar() ensures forward compatibility
and improves performance by 15%.
```

## Commit Message Anatomy

```
<subject line - 50 chars, imperative mood>

<body - explain WHAT changed and WHY>

<footer - optional: references, co-authors>
```

### Example: Feature Addition

```
Add password strength validation to signup form

Users were creating weak passwords that could be
compromised. This adds real-time validation showing:
- Minimum 8 characters
- At least one number and symbol
- Strength meter with visual feedback

Closes #142
```

### Example: Bug Fix

```
Fix race condition in cache invalidation

Multiple threads could invalidate the same cache entry
simultaneously, causing stale data to persist. Added
mutex lock around the invalidation check.

The bug manifested as intermittent stale user sessions
after password changes.
```

### Example: Refactoring

```
Extract authentication logic into dedicated service

The UserController had grown to 800+ lines with auth
logic mixed into request handling. Moving auth to
AuthService improves testability and follows single
responsibility principle.

No functional changes - all existing tests pass.
```

## When to Split Commits

Split commits when changes serve different purposes:

- **Feature + Tests** - Can be one commit if tightly coupled
- **Feature + Unrelated Fix** - Should be separate commits
- **Refactor + Feature** - Separate (refactor first, then feature)
- **Multiple Bug Fixes** - Separate unless fixing same root cause

## Claude Code Attribution Setting

By default, Claude Code adds a footer to commits:

```
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Recommendation**: Disable this footer. It adds noise to commit history and the commit message itself should stand on its own merits. The value is in the message content, not attribution.

To disable, add to `~/.claude/settings.json`:

```json
{
  "attribution": {
    "commit": "",
    "pr": ""
  }
}
```

This removes the footer from both commits and pull request descriptions.

## Merge and Branch Strategies

For detailed guidance on merge vs rebase, fast-forward strategies, and workflows, see [merge-strategies.md](merge-strategies.md).

Quick reference:
- **Rebase**: Private feature branches, keeping up-to-date
- **Merge**: Shared branches, preserving history
- **Fast-forward**: Clean linear history when possible

## Example Commit Messages by Type

See [commit-templates.md](commit-templates.md) for more examples organized by change type.

## References

See [sources.md](sources.md) for authoritative documentation.
