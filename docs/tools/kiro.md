# Kiro: Deployment & Idioms

This guide covers Kiro deployment patterns and idiomatic usage. For general patterns, see the [meta-claude skill](~/.claude/skills/meta-claude/tools/kiro.md).

## Directory Structure

```
.kiro/                        # Project-level configuration
├── steering.md              # Global AI guidance
├── specs/                   # Feature specifications
│   ├── requirements.md      # What to build (EARS syntax)
│   ├── design.md            # How to build it
│   └── tasks.md             # Implementation steps
├── hooks/                   # Event-driven automation
│   └── on-save.yaml
└── rules/                   # Coding standards
    └── coding-standards.md
```

## Specs (Specifications)

### The Spec Flow

Kiro uses structured specifications to guide development:

```
Requirements → Design → Tasks → Implementation
     ↓            ↓         ↓
  WHAT         HOW      STEPS    CODE
```

### Requirements (EARS Syntax)

EARS (Easy Approach to Requirements Syntax) provides structured requirements:

```markdown
# requirements.md

## User Authentication

### Ubiquitous Requirements
- The system shall encrypt all passwords using bcrypt

### Event-Driven Requirements
- When a user submits valid credentials, the system shall create a session
- When a user submits invalid credentials, the system shall display an error

### State-Driven Requirements
- While a user is logged in, the system shall display their dashboard
- While a user session is expired, the system shall redirect to login

### Optional Requirements
- Where two-factor authentication is enabled, the system shall require a verification code

### Unwanted Behavior
- The system shall not store passwords in plain text
- The system shall not allow more than 5 failed login attempts per hour
```

### EARS Keywords

| Keyword | Type | Use For |
|---------|------|---------|
| `shall` | Ubiquitous | Always-true requirements |
| `When` | Event-driven | Triggered by events |
| `While` | State-driven | Active during states |
| `Where` | Optional | Conditional features |
| `shall not` | Unwanted | Explicitly forbidden |

### Design Document

```markdown
# design.md

## Architecture

### Tech Stack
- Frontend: React 18 with TypeScript
- Backend: Node.js with Express
- Database: PostgreSQL 15
- Auth: JWT with refresh tokens

### Component Structure
```
src/
├── components/    # React components
├── services/      # Business logic
├── api/           # API routes
└── utils/         # Shared utilities
```

### Key Decisions
- Using repository pattern for data access
- JWT stored in httpOnly cookies
- Rate limiting via Redis
```

### Tasks Document

```markdown
# tasks.md

## Phase 1: Setup
- [x] Initialize project structure
- [x] Configure TypeScript strict mode
- [ ] Set up database connection

## Phase 2: Authentication
- [ ] Create user model with password hashing
- [ ] Implement registration endpoint
- [ ] Implement login endpoint
- [ ] Add JWT middleware
- [ ] Create session management

## Phase 3: Testing
- [ ] Unit tests for auth service
- [ ] Integration tests for auth flow
- [ ] E2E tests for login/register
```

## Steering Rules

### Global Guidance

```markdown
# .kiro/steering.md

# Project Guidance

## Code Style
- Use TypeScript strict mode
- Prefer functional components
- Handle all errors explicitly

## Architecture
- Follow the repository pattern
- Keep business logic in services
- API routes are thin wrappers

## Testing
- Every public function needs tests
- Use descriptive test names
- Mock external dependencies

## Security
- Validate all user input
- Use parameterized queries
- Never log sensitive data
```

Steering rules apply to ALL Kiro operations in the project.

### Focused Rules

```markdown
# .kiro/rules/testing.md

# Testing Standards

## Naming
Use "should [expected] when [condition]" format:
- `should return user when valid id`
- `should throw error when user not found`

## Structure
```typescript
describe('ServiceName', () => {
  describe('methodName', () => {
    it('should handle normal case', () => {});
    it('should handle edge case', () => {});
  });
});
```

## Mocking
- Mock at service boundaries
- Use dependency injection for testability
- Never mock the thing you're testing
```

## Hooks

### Hook Format

```yaml
# .kiro/hooks/format-on-save.yaml
name: format-on-save
trigger: onSave
pattern: "**/*.ts"
action: |
  Format the saved file using the project's prettier configuration.
  Report any formatting changes made.
```

### Trigger Types

| Trigger | Fires When | Use For |
|---------|------------|---------|
| `onSave` | File saved | Formatting, linting, testing |
| `onCreate` | File created | Scaffolding, templates |
| `onDelete` | File deleted | Cleanup, dependency checks |
| `manual` | Explicit invocation | On-demand operations |

### Idiomatic Hook Patterns

**Auto-test on save**:
```yaml
name: auto-test
trigger: onSave
pattern: "**/*.ts"
action: |
  Find and run tests related to this file.
  If tests fail, suggest fixes.
```

**Lint on save**:
```yaml
name: lint-check
trigger: onSave
pattern: "**/*.{ts,tsx}"
action: |
  Run eslint on this file.
  Fix auto-fixable issues.
  Report remaining issues.
```

**Generate tests for new files**:
```yaml
name: scaffold-tests
trigger: onCreate
pattern: "src/**/*.ts"
exclude: "**/*.test.ts"
action: |
  Create a corresponding test file in the same directory.
  Add basic test scaffolding for exported functions.
```

## Autonomous Agent

Kiro's autonomous agent (Pro/Pro+ feature):
- Maintains context across sessions
- Learns from feedback patterns
- Works independently on assigned tasks

### Configuring Autonomy

In Kiro settings:
- Set task scope boundaries
- Define confirmation requirements
- Configure auto-commit rules

### Best Practices

1. **Start supervised**: Review agent actions initially
2. **Establish patterns**: Give consistent feedback
3. **Expand gradually**: Increase autonomy as trust builds
4. **Set boundaries**: Define what requires human approval

## Validation

### Spec Validation

```bash
# Check spec syntax
cat .kiro/specs/requirements.md
# Look for EARS keyword usage

# Verify task status
grep -c "\[x\]" .kiro/specs/tasks.md  # Completed
grep -c "\[ \]" .kiro/specs/tasks.md  # Pending
```

### Hook Testing

```bash
# Trigger onSave hook manually
touch src/test-file.ts
# Check Kiro logs for hook execution

# Verify hook configuration
cat .kiro/hooks/format-on-save.yaml
```

## Deployment Patterns

### Project Initialization

```bash
# Create Kiro structure
mkdir -p .kiro/specs .kiro/hooks .kiro/rules

# Create steering file
cat > .kiro/steering.md << 'EOF'
# Project Guidance

## Code Style
- TypeScript strict mode
- Functional React components
- Explicit error handling
EOF

# Create initial requirements
cat > .kiro/specs/requirements.md << 'EOF'
# Requirements

## Core Features
- The system shall [describe feature]
EOF

# Add to git
git add .kiro/
git commit -m "Initialize Kiro configuration"
```

### Team Sharing

```
.kiro/
├── steering.md       # Team-wide guidance (commit)
├── specs/            # Shared specifications (commit)
├── hooks/            # Shared automation (commit)
└── rules/            # Shared standards (commit)
```

All `.kiro/` files should be version-controlled for team consistency.

### Feature Development Flow

1. **Write requirements** (EARS syntax)
2. **Create design** (architecture, decisions)
3. **Generate tasks** (Kiro helps create these)
4. **Implement** (Kiro guides based on specs)
5. **Validate** (tests against requirements)

## Resources

- [Kiro Home](https://kiro.dev/)
- [Introducing Kiro Blog](https://kiro.dev/blog/introducing-kiro/)
- [Autonomous Agent Guide](https://kiro.dev/blog/introducing-kiro-autonomous-agent/)
- [Meta-claude Kiro Patterns](~/.claude/skills/meta-claude/tools/kiro.md)
