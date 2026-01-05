# Validation Examples

Example outputs from the doc-validator.

## Example 1: Clean Skill

A well-structured skill with no issues.

**Input**:
```
~/.claude/skills/commit-helper/
├── SKILL.md (120 lines)
├── reference.md
└── examples.md
```

**Output**:
```
Validating: ~/.claude/skills/commit-helper/

Checking structure... ✓
Checking links... ✓
Checking content... ✓

~/.claude/skills/commit-helper/SKILL.md
  ✓ All checks passed

~/.claude/skills/commit-helper/reference.md
  ✓ All checks passed

~/.claude/skills/commit-helper/examples.md
  ✓ All checks passed

SUMMARY
═══════════════════════════════════════════════════════════════
Files checked:    3
Errors:           0
Warnings:         0
Info:             0
Status:           PASS
```

## Example 2: Skill with Fixable Issues

A skill with formatting issues that can be auto-fixed.

**Input**:
```yaml
---
name:	my-skill
description: Use when: testing things
---

# My Skill

Instructions here...
```

**Output (without --fix)**:
```
Validating: ~/.claude/skills/my-skill/

~/.claude/skills/my-skill/SKILL.md
  [WARNING] Line 2: Tab character in frontmatter
  [ERROR]   Line 3: Unquoted special character ':' in description
  [INFO]    Line 6: Trailing whitespace

SUMMARY
═══════════════════════════════════════════════════════════════
Files checked:    1
Errors:           1
Warnings:         1
Info:             1
Status:           FAIL
```

**Output (with --fix)**:
```
Validating: ~/.claude/skills/my-skill/

~/.claude/skills/my-skill/SKILL.md
  [WARNING] Line 2: Tab character in frontmatter
  → Auto-fixed: Converted to spaces

  [ERROR]   Line 3: Unquoted special character ':' in description
  → Auto-fixed: Added quotes

  [INFO]    Line 6: Trailing whitespace
  → Auto-fixed: Removed

SUMMARY
═══════════════════════════════════════════════════════════════
Files checked:    1
Errors:           0 (1 fixed)
Warnings:         0 (1 fixed)
Info:             0 (1 fixed)
Auto-fixed:       3 issues
Status:           PASS (after fixes)
```

## Example 3: Skill with Broken Links

A skill with references to missing files.

**Input**:
```markdown
---
name: my-skill
description: Example skill
---

# My Skill

For examples, see [examples.md](examples.md).
For API reference, see [reference.md](reference.md).
```

**Directory**:
```
my-skill/
└── SKILL.md        # references.md doesn't exist!
```

**Output**:
```
Validating: ~/.claude/skills/my-skill/

~/.claude/skills/my-skill/SKILL.md
  [ERROR]   Line 9: Broken link: [examples.md](examples.md)
            Target file does not exist

  [ERROR]   Line 10: Broken link: [reference.md](reference.md)
            Target file does not exist

SUMMARY
═══════════════════════════════════════════════════════════════
Files checked:    1
Errors:           2
Warnings:         0
Info:             0
Status:           FAIL

Recommendation: Create missing files or remove broken links.
```

## Example 4: Missing Frontmatter

A markdown file without YAML frontmatter.

**Input**:
```markdown
# My Skill

This skill does things.
```

**Output (without --fix)**:
```
Validating: ~/.claude/skills/my-skill/

~/.claude/skills/my-skill/SKILL.md
  [ERROR]   Line 1: Missing YAML frontmatter
  [ERROR]   Line -: Missing required field: name
  [ERROR]   Line -: Missing required field: description

SUMMARY
═══════════════════════════════════════════════════════════════
Files checked:    1
Errors:           3
Warnings:         0
Info:             0
Status:           FAIL
```

**Output (with --fix)**:
```
Validating: ~/.claude/skills/my-skill/

~/.claude/skills/my-skill/SKILL.md
  [ERROR]   Line 1: Missing YAML frontmatter
  → Auto-fixed: Added frontmatter delimiters

  [ERROR]   Line -: Missing required field: name
  → Auto-fixed: Generated name: my-skill

  [ERROR]   Line -: Missing required field: description
  → Auto-fixed: Added placeholder description

SUMMARY
═══════════════════════════════════════════════════════════════
Files checked:    1
Errors:           0 (3 fixed)
Auto-fixed:       3 issues
Status:           PASS (after fixes)

Note: Please update the placeholder description with specific trigger keywords.
```

**Result**:
```yaml
---
name: my-skill
description: "TODO: Add description with trigger keywords"
---

# My Skill

This skill does things.
```

## Example 5: Large File Warning

A skill that violates progressive disclosure.

**Input**: SKILL.md with 650 lines

**Output**:
```
Validating: ~/.claude/skills/my-skill/

~/.claude/skills/my-skill/SKILL.md
  [WARNING] File is 650 lines (threshold: 500)
            Consider splitting into supporting files.

  [INFO]    No supporting files found
            Large skills should use progressive disclosure:
            - reference.md for API details
            - examples.md for usage examples
            - sources.md for external links

SUMMARY
═══════════════════════════════════════════════════════════════
Files checked:    1
Errors:           0
Warnings:         1
Info:             1
Status:           WARN

Recommendation: Split content into supporting files.
```

## Example 6: Batch Validation

Validating all user skills at once.

**Command**:
```bash
python validate_docs.py ~/.claude/skills/
```

**Output**:
```
Validating: ~/.claude/skills/

Scanning for documentation...
Found 5 skill directories, 23 markdown files

~/.claude/skills/chezmoi/
  ✓ 5 files checked, no issues

~/.claude/skills/claude-commands/
  ✓ 9 files checked, no issues

~/.claude/skills/claude-skills/
  [WARNING] troubleshooting.md:265 - Broken link: reference.md
  8 files checked, 1 warning

~/.claude/skills/meta-claude/
  ✓ 6 files checked, no issues

~/.claude/skills/python-standards/
  ✓ 5 files checked, no issues

SUMMARY
═══════════════════════════════════════════════════════════════
Directories:      5
Files checked:    33
Errors:           0
Warnings:         1
Info:             0
Status:           WARN

Issues by skill:
  claude-skills:  1 warning
```

## Example 7: JSON Output

For tooling integration.

**Command**:
```bash
python validate_docs.py --format json ~/.claude/skills/my-skill/
```

**Output**:
```json
{
  "target": "~/.claude/skills/my-skill/",
  "timestamp": "2024-01-15T10:30:00Z",
  "summary": {
    "files_checked": 3,
    "errors": 1,
    "warnings": 2,
    "info": 1,
    "auto_fixed": 0,
    "status": "FAIL"
  },
  "issues": [
    {
      "file": "SKILL.md",
      "line": 45,
      "category": "links",
      "severity": "error",
      "message": "Broken link: [missing](missing.md)",
      "auto_fixable": false
    },
    {
      "file": "SKILL.md",
      "line": 12,
      "category": "content",
      "severity": "warning",
      "message": "Tab character found",
      "auto_fixable": true
    }
  ],
  "auto_fixed": []
}
```
