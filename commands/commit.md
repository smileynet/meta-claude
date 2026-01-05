---
description: Generate a well-crafted commit message for staged changes. Analyzes diff and follows commit message best practices.
allowed-tools: Bash, Read
---

Load commit guidelines from:
@./skills/git-workflow/SKILL.md

## Task

Generate a commit message for the currently staged changes and commit them.

## Process

1. **Check for staged changes**
   - Run `git status` to see staged files
   - If nothing staged, inform user and suggest `git add`

2. **Analyze the changes**
   - Run `git diff --cached` to see what's being committed
   - Identify the nature of changes (feature, fix, refactor, etc.)
   - Note which files and areas are affected

3. **Review repository style**
   - Run `git log --oneline -5` to see recent commit style
   - Match the existing patterns where appropriate

4. **Draft commit message**
   - Subject: Max 50 characters, imperative mood, no period
   - Body: Explain WHAT changed and WHY (not how)
   - Wrap body at 72 characters
   - Focus on value to other developers reading the history

5. **Handle large commits**
   - If diff is >500 lines, suggest splitting into smaller commits
   - If changes span multiple unrelated areas, recommend separate commits

6. **Present for approval**
   - Show the proposed commit message
   - Ask if user wants to commit, edit, or cancel

7. **Execute commit**
   - Use HEREDOC format for multi-line messages

## Commit Format

```
<subject - 50 chars max, imperative mood>

<body - explain what changed and why>
<wrap at 72 characters>

<footer - co-authors, references>
```

## Example Output

```
Staged: 3 files changed

- src/auth/validator.py (+45, -12)
- tests/test_validator.py (+30, -0)
- README.md (+5, -2)

Proposed commit message:

  Add password strength validation

  Users could create weak passwords that were easily
  compromised. This adds real-time validation checking:
  - Minimum 8 characters
  - At least one number and special character
  - Visual strength indicator

  Includes unit tests for edge cases.

[Commit] [Edit] [Cancel]
```

## Notes

- Never commit files that appear to contain secrets (.env, credentials, keys)
- Respect any existing commit hooks (pre-commit, commit-msg)
- If commit fails, show the error and suggest resolution
