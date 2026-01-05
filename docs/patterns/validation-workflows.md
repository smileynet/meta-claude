# Pattern: Validation Workflows

Test before deploy. Catch issues early.

## The Principle

Never deploy untested configurations. Build verification into your workflow so problems surface before they cause harm.

## Why It Matters

- **Catch syntax errors**: YAML parsing, markdown structure
- **Verify activation**: Skills trigger on expected keywords
- **Prevent regressions**: Changes don't break existing behavior
- **Build confidence**: Deploy knowing it works

## Implementation Across Tools

### Claude Code

**Debug Mode Testing**:
```bash
# Test skill discovery
claude --debug -p "list your skills"

# Test specific trigger
claude --debug -p "help me write a commit message"
# Check: Does commit-helper skill activate?

# Test with dry-run (read-only)
claude --debug -p "review this code" --allowedTools "Read,Grep,Glob"
```

**Non-Interactive Testing** (for automation):
```bash
# Test a slash command - runs without permission prompts
claude -p "/validate-docs ~/.claude/skills/" --dangerously-skip-permissions

# Test an agent by prompting for its use
claude -p "use the doc-validator-agent to validate skills/my-skill/" --dangerously-skip-permissions

# Test skill activation via trigger phrase
claude -p "help me write a commit message for these changes" --dangerously-skip-permissions

# Capture output for validation scripts
output=$(claude -p "/my-command arg1" --dangerously-skip-permissions 2>&1)
echo "$output" | grep -q "expected text" && echo "PASS" || echo "FAIL"
```

> **Note**: `--dangerously-skip-permissions` bypasses all permission prompts. Use only for testing in controlled environments, never in production or with untrusted inputs.

**Validation Commands** (if you have them):
```bash
/validate-skill my-skill --dry-run
/validate-all-skills --user
```

**Manual Checklist**:
- [ ] YAML frontmatter parses (no tabs, starts with `---`)
- [ ] Description contains trigger keywords
- [ ] File paths are correct
- [ ] Supporting files exist and are linked

### Cursor

**Rule Validation**:
1. Open Cursor
2. Settings → Features → Rules
3. Check "Rules" panel shows your rules
4. Open a file matching your glob pattern
5. Verify rule content appears in context

**Manual Testing**:
```bash
# Check MDC syntax
cat .cursor/rules/my-rule.mdc | head -20
# Verify YAML frontmatter is valid
```

### Kiro

**Spec Validation**:
```bash
# Kiro validates specs on load
# Check for parsing errors in output

# Manual review
cat .kiro/specs/requirements.md
# Verify EARS syntax is correct
```

**Hook Testing**:
```bash
# Test hooks by triggering events
touch test-file.py  # Triggers onCreate hooks
# Check hook executed correctly
```

### OpenCode

**Agent Testing**:
```bash
# List available agents
opencode agents list

# Test agent with simple prompt
opencode -a my-agent "hello"

# Check tool permissions
opencode -a my-agent --dry-run "do something"
```

**Command Testing**:
```bash
# List commands
opencode commands list

# Test command
opencode run my-command test-arg
```

## Validation Checklist

Use this before deploying any configuration:

### Syntax Validation
- [ ] YAML/frontmatter parses without errors
- [ ] Markdown renders correctly
- [ ] No invisible characters (tabs vs spaces)
- [ ] File encoding is UTF-8

### Discovery Validation
- [ ] Skill/rule appears in tool's discovery
- [ ] Description triggers on expected keywords
- [ ] Glob patterns match intended files
- [ ] No conflicts with other skills/rules

### Behavior Validation
- [ ] Basic functionality works as expected
- [ ] Edge cases handled appropriately
- [ ] No unintended side effects
- [ ] Performance acceptable (not too slow to load)

### Integration Validation
- [ ] Links to supporting files work
- [ ] Referenced skills/commands exist
- [ ] Cross-tool compatibility (if applicable)
- [ ] Sync/deployment works correctly

## Examples

### Good: Test-Deploy-Verify Workflow

```bash
# 1. Create/edit skill
vim ~/.claude/skills/my-skill/SKILL.md

# 2. Test discovery
claude --debug -p "what skills do you have?" | grep my-skill

# 3. Test activation
claude --debug -p "[trigger phrase for my-skill]"
# Verify skill content appears in context

# 4. Test functionality
claude -p "[actual task using skill]"
# Verify output is correct

# 5. Commit and sync
cd ~/.local/share/chezmoi
chezmoi add ~/.claude/skills/my-skill/
git add -A && git commit -m "Add my-skill"
chezmoi apply  # Verify still works after sync
```

### Bad: Edit-Deploy-Hope Workflow

```bash
# Edit skill
vim ~/.claude/skills/my-skill/SKILL.md

# Immediately use without testing
claude -p "do the thing"
# Fails mysteriously, unclear why
```

## Debugging Common Issues

### Skill Not Activating

```bash
# Check discovery
claude --debug -p "list skills" 2>&1 | grep -A5 "my-skill"

# Common causes:
# - Description doesn't contain trigger words
# - YAML syntax error (skill not parsed)
# - Wrong directory location
```

### Wrong Skill Activating

```bash
# Check what's activating
claude --debug -p "[your prompt]" 2>&1 | grep "Loading skill"

# Common causes:
# - Overlapping trigger keywords
# - Too-generic description
# - Higher-priority skill matching first
```

### Skill Too Slow

```bash
# Time the load
time claude --debug -p "test" 2>&1 | head -1

# Common causes:
# - SKILL.md too large (split into supporting files)
# - Too many files in skill directory
# - Complex template processing
```

## Automated Validation

For teams, consider automated checks:

```yaml
# .github/workflows/validate-claude.yml
name: Validate Claude Configs
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate YAML frontmatter
        run: |
          for f in .claude/skills/*/SKILL.md; do
            head -20 "$f" | grep -q "^---" || exit 1
          done
      - name: Check required fields
        run: |
          for f in .claude/skills/*/SKILL.md; do
            grep -q "^name:" "$f" || exit 1
            grep -q "^description:" "$f" || exit 1
          done
```

**Local Testing Script** (bash):
```bash
#!/bin/bash
# test-claude-artifacts.sh - Test commands and agents locally

set -e

echo "Testing /validate-docs command..."
output=$(claude -p "/validate-docs .claude/skills/" --dangerously-skip-permissions 2>&1)
if echo "$output" | grep -q "Status:.*PASS\|Status:.*WARN"; then
  echo "  PASS: /validate-docs works"
else
  echo "  FAIL: /validate-docs returned unexpected output"
  echo "$output"
  exit 1
fi

echo "Testing doc-validator agent..."
output=$(claude -p "use doc-validator-agent to check .claude/skills/my-skill/" --dangerously-skip-permissions 2>&1)
if [ -n "$output" ]; then
  echo "  PASS: Agent responded"
else
  echo "  FAIL: Agent produced no output"
  exit 1
fi

echo "All tests passed!"
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| No testing | Issues found in production | Always test before deploy |
| Testing only happy path | Edge cases fail | Include negative tests |
| Manual-only validation | Inconsistent, error-prone | Add automated checks |
| Skipping validation for "small" changes | Small changes can break | Validate everything |

## Related Patterns

- [Progressive Disclosure](progressive-disclosure.md) - Well-structured skills are easier to validate
- [Single Source of Truth](single-source-truth.md) - Fewer places to validate
