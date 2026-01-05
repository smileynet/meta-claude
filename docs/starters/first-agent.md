# Create Your First Agent

This walkthrough guides you through creating a custom Claude Code subagent for specialized tasks.

## Objective

Build an agent that:
- Specializes in a specific domain
- Uses appropriate model and tools
- Can be invoked by the main Claude instance

## When to Create an Agent

| Use Case | Solution |
|----------|----------|
| Knowledge/guidelines | Skill |
| Explicit invocation | Command |
| Autonomous specialized task | **Agent** |
| Complex multi-step work | **Agent** |
| Different model needed | **Agent** |

Agents are best for tasks requiring:
- Specialized expertise
- Different capability levels (opus for complex, haiku for simple)
- Restricted tool access
- Autonomous multi-step execution

## Step 1: Choose Your Specialty

Good agent specialties:

| Agent | Purpose | Model |
|-------|---------|-------|
| `security-reviewer` | Security-focused code review | opus |
| `test-writer` | Generate comprehensive tests | sonnet |
| `documentation` | Write/update documentation | sonnet |
| `quick-helper` | Simple questions, fast responses | haiku |
| `architect` | System design decisions | opus |

For this walkthrough, we'll create a `security-reviewer` agent.

## Step 2: Create the Agent File

```bash
# Create agents directory if needed
mkdir -p ~/.claude/agents

# Create agent file
code ~/.claude/agents/security-reviewer.md
```

Add this content:

```yaml
---
name: security-reviewer
description: Security-focused code review. Use for security audits, vulnerability assessment, and secure coding guidance.
model: opus
allowed-tools: Read, Grep, Glob
---

You are a security specialist focused on identifying vulnerabilities and security issues in code.

## Your Expertise

- OWASP Top 10 vulnerabilities
- Authentication and authorization flaws
- Input validation and sanitization
- Cryptographic weaknesses
- Secrets and credential exposure
- SQL injection, XSS, CSRF
- Insecure dependencies

## Review Process

1. **Understand Context**: What does this code do? What's its attack surface?

2. **Check Input Handling**:
   - All user input validated?
   - Proper sanitization for output context?
   - Type coercion handled safely?

3. **Verify Authentication/Authorization**:
   - Auth checks on all protected routes?
   - Authorization verified for each action?
   - Session management secure?

4. **Examine Data Handling**:
   - Secrets hardcoded anywhere?
   - Sensitive data logged?
   - Encryption used appropriately?

5. **Review Dependencies**:
   - Known vulnerable packages?
   - Outdated security-critical dependencies?

## Output Format

For each finding:

```
## [SEVERITY] Finding Title

**Location**: file:line
**Category**: OWASP category or type
**Risk**: What could happen if exploited

**Issue**:
Description of the vulnerability

**Recommendation**:
How to fix it

**Example Fix**:
Code showing the fix
```

Severity levels:
- **CRITICAL**: Immediate exploitation possible
- **HIGH**: Significant risk, prioritize fix
- **MEDIUM**: Should be addressed
- **LOW**: Minor issue or best practice
- **INFO**: Informational finding

## Guidelines

- Be thorough but focused on security
- Provide actionable recommendations
- Include code examples for fixes
- Don't overwhelm with low-severity noise
- Prioritize findings by actual risk
```

## Step 3: Understand the Format

### Frontmatter Fields

```yaml
---
name: security-reviewer           # Required: identifier
description: Security-focused...  # Required: when to use
model: opus                       # Optional: opus, sonnet, haiku
allowed-tools: Read, Grep, Glob   # Optional: tool restrictions
---
```

### Model Selection

| Model | Use For | Trade-off |
|-------|---------|-----------|
| `haiku` | Quick, simple tasks | Fast, cheap, less capable |
| `sonnet` | Balanced tasks | Good capability, reasonable speed |
| `opus` | Complex reasoning | Most capable, slower, expensive |

For security review, we use `opus` because:
- Security requires careful reasoning
- Missing vulnerabilities is costly
- Quality matters more than speed

### Tool Restrictions

```yaml
allowed-tools: Read, Grep, Glob
```

This agent is read-only because:
- Security reviewers observe, don't modify
- Reduces risk of unintended changes
- Focuses the agent on analysis

Common tool sets:

| Tools | Use Case |
|-------|----------|
| `Read, Grep, Glob` | Read-only analysis |
| `Read, Grep, Glob, Edit, Write` | Can modify files |
| `Read, Grep, Glob, Bash` | Can run commands |
| (no field) | All tools available |

## Step 4: Test the Agent

Agents are invoked by the main Claude instance, not directly. Test by asking Claude to use it:

```bash
claude -p "use the security-reviewer agent to review src/auth.py"
```

Or mention the specialty:
```bash
claude -p "do a security audit of the authentication module"
```

Claude should recognize the need and invoke your agent.

## Step 5: Create Supporting Skills

Agents can benefit from linked skills. Create a skill with detailed knowledge:

```bash
mkdir -p ~/.claude/skills/security-review
```

```yaml
# ~/.claude/skills/security-review/SKILL.md
---
name: security-review
description: Security code review guidelines and checklists.
---

# Security Review Guidelines

[Detailed checklists, patterns, and references]
```

Reference in your agent:

```yaml
---
name: security-reviewer
description: Security-focused code review...
model: opus
allowed-tools: Read, Grep, Glob
---

You are a security specialist. Follow the guidelines in:
@~/.claude/skills/security-review/SKILL.md

[Rest of agent prompt]
```

## Step 6: Iterate Based on Usage

### Add More Context

```yaml
---
name: security-reviewer
description: Security-focused code review. Use for security audits, vulnerability assessment, secure coding guidance, OWASP checks, or penetration testing preparation.
---
```

### Adjust Model

If reviews are taking too long or costing too much:
```yaml
model: sonnet  # Faster, cheaper, still capable
```

### Expand Tools

If the agent needs to check configs or dependencies:
```yaml
allowed-tools: Read, Grep, Glob, Bash
```

## Example Agents

### Quick Helper (Fast, Cheap)

```yaml
---
name: quick-helper
description: Quick answers to simple questions. Use for brief explanations or simple lookups.
model: haiku
allowed-tools: Read, Grep, Glob
---

You provide quick, concise answers. Be brief and direct.
```

### Test Writer (Balanced)

```yaml
---
name: test-writer
description: Generate comprehensive unit tests. Use when adding tests or improving coverage.
model: sonnet
allowed-tools: Read, Grep, Glob, Write
---

You are a testing specialist. Generate thorough unit tests.

## Guidelines
- Test edge cases
- Use descriptive names
- Mock external dependencies
- Aim for high coverage
```

### Architect (Powerful)

```yaml
---
name: architect
description: System design and architecture decisions. Use for major design questions.
model: opus
allowed-tools: Read, Grep, Glob, WebSearch
---

You are a senior software architect. Make well-reasoned design decisions.

## Approach
1. Understand requirements
2. Consider alternatives
3. Evaluate trade-offs
4. Recommend with reasoning
```

## Validation Checklist

- [ ] Agent file has valid YAML frontmatter
- [ ] `name` and `description` present
- [ ] Model appropriate for task complexity
- [ ] Tools restricted to what's needed
- [ ] System prompt is clear and focused
- [ ] Agent invokes correctly via main Claude

## Common Issues

### Agent Not Invoked

Make description specific to trigger correctly:
```yaml
# Vague - might not trigger
description: Reviews code

# Specific - clear when to use
description: Security-focused code review. Use for security audits, vulnerability assessment.
```

### Wrong Model Used

Check `model` field is valid:
```yaml
model: opus    # Valid
model: sonnet  # Valid
model: haiku   # Valid
model: gpt-4   # Invalid - use Anthropic model names
```

### Agent Too Slow

- Switch to `sonnet` or `haiku`
- Reduce scope of task
- Use read-only tools if possible

## Next Steps

1. Review [validation workflows](../patterns/validation-workflows.md)
2. Learn about [progressive disclosure](../patterns/progressive-disclosure.md) for complex agents
3. Add agents to [chezmoi](../technical-bootstrap.md#deployment-via-chezmoi) for sync
