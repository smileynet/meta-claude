# Auto-Fix Behaviors

How the doc-validator handles automatic fixes.

## Fix Classification

Fixes are classified into three categories based on safety and reversibility.

### Safe Auto-Fix

These are purely mechanical fixes with no semantic impact. They are applied automatically when `--fix` is specified.

| Fix | What It Does | Reversible |
|-----|--------------|------------|
| Tab → spaces | Replace tab characters with 2 spaces | Yes |
| Trailing whitespace | Remove spaces/tabs at end of lines | Yes |
| Final newline | Add newline at end of file if missing | Yes |
| YAML quoting | Add quotes around values with special chars | Yes |

**Example - Tab conversion**:
```diff
- name:	my-skill
+ name: my-skill
```

**Example - Trailing whitespace**:
```diff
- description: My skill
+ description: My skill
```

**Example - YAML quoting**:
```diff
- description: Use when: testing
+ description: "Use when: testing"
```

### Generative Auto-Fix

These create new content but are deterministic and safe. They are applied with a notice in the output.

| Fix | What It Creates | Notice |
|-----|-----------------|--------|
| Missing frontmatter | `---\n---\n` at start of file | "Added frontmatter delimiters" |
| Missing `name` | Generated from folder name | "Generated name: my-skill" |
| Missing `description` | Placeholder text | "Added placeholder description" |

**Example - Missing frontmatter**:
```diff
+ ---
+ ---
+
  # My Skill

  Content here...
```

**Example - Missing name**:
```diff
  ---
+ name: my-skill
  description: Does things
  ---
```

**Example - Missing description**:
```diff
  ---
  name: my-skill
+ description: "TODO: Add description with trigger keywords"
  ---
```

### Report Only

These require human judgment and are never automatically fixed.

| Issue | Why No Auto-Fix |
|-------|-----------------|
| Broken links | May be intentional or require content creation |
| File structure | Organizational decisions need human input |
| Size warnings | Splitting content requires understanding context |
| Missing keywords | Semantic choices about trigger words |
| Orphaned files | May be intentionally unlinked |
| Progressive disclosure | Restructuring requires content decisions |

## Command Line Options

### Enable Auto-Fix

```bash
# Apply all safe and generative fixes
python validate_docs.py --fix path/

# Apply only safe fixes (no generated content)
python validate_docs.py --fix --safe-only path/
```

### Dry Run

See what would be fixed without modifying files:

```bash
python validate_docs.py --fix --dry-run path/
```

Output:
```
DRY RUN - No files modified

Would fix:
  SKILL.md:12 - Convert tab to spaces
  SKILL.md:45 - Remove trailing whitespace
  reference.md:89 - Add final newline
```

### Interactive Mode

Confirm each fix before applying:

```bash
python validate_docs.py --fix --interactive path/
```

Output:
```
SKILL.md:12 - Tab character found
  Fix: Convert to spaces? [y/n/q]: y
  → Fixed

SKILL.md:45 - Trailing whitespace
  Fix: Remove trailing whitespace? [y/n/q]: n
  → Skipped
```

## Fix Output Format

When fixes are applied, they're reported in the output:

```
~/.claude/skills/my-skill/SKILL.md
  [WARNING] Line 12: Tab character found
  → Auto-fixed: Converted tab to spaces

  [INFO]    Line 45: Trailing whitespace
  → Auto-fixed: Removed trailing whitespace

  [ERROR]   Line 1: Missing frontmatter
  → Auto-fixed: Added frontmatter delimiters
  → Auto-fixed: Generated name from folder: my-skill
  → Auto-fixed: Added placeholder description

SUMMARY
Files modified: 1
Total fixes applied: 5
  - Safe fixes: 2
  - Generated fixes: 3
```

## Backup Behavior

By default, no backups are created (fixes are reversible via git).

To create backups:

```bash
python validate_docs.py --fix --backup path/
```

Creates `filename.md.bak` before modifying.

## Undo Fixes

### With Git

```bash
# See what changed
git diff path/to/file.md

# Undo changes to a file
git checkout -- path/to/file.md

# Undo all changes
git checkout -- .
```

### With Backups

```bash
# Restore from backup
mv file.md.bak file.md
```

## Fix Priorities

When multiple fixes apply to the same line, they're applied in order:

1. Tab conversion (affects indentation)
2. Trailing whitespace removal
3. YAML quoting (depends on correct spacing)
4. Frontmatter fixes (depends on file structure)

## Edge Cases

### Already Correct

If a file passes all checks, no fixes are applied:

```
~/.claude/skills/my-skill/SKILL.md
  ✓ All checks passed

SUMMARY
Files checked: 1
Issues found: 0
Fixes applied: 0
```

### Mixed Results

Some issues fixed, others reported:

```
~/.claude/skills/my-skill/SKILL.md
  [INFO]    Line 12: Tab character found
  → Auto-fixed: Converted to spaces

  [ERROR]   Line 45: Broken link: [missing](missing.md)
  → Cannot auto-fix: File does not exist

SUMMARY
Fixes applied: 1
Issues remaining: 1 (require manual fix)
```

### Write Permission Error

If file cannot be modified:

```
~/.claude/skills/my-skill/SKILL.md
  [INFO]    Line 12: Tab character found
  → FAILED: Permission denied

Fixes attempted: 1
Fixes failed: 1
```
