# Technical Bootstrap: Fresh Machine Setup

This guide gets you from zero to a working meta-agentic system on any supported platform.

## Prerequisites

### All Platforms
- Git installed and configured
- 1Password account (for SSH key management)
- Terminal access

### Platform-Specific

| Platform | Requirements |
|----------|--------------|
| Windows | PowerShell 5.1+, winget |
| macOS | Homebrew |
| Linux/WSL | curl, bash |

## Step 1: Install Chezmoi

Chezmoi manages dotfiles by storing templates and applying them to target locations.

```bash
# Windows (PowerShell)
winget install twpayne.chezmoi

# macOS
brew install chezmoi

# Linux/WSL
sh -c "$(curl -fsLS get.chezmoi.io)"
```

**Note**: On Windows, restart your terminal after installation for PATH updates.

## Step 2: Initialize and Apply

```bash
chezmoi init --apply smileynet
```

This command:
1. Clones the dotfiles repository to `~/.local/share/chezmoi`
2. Processes templates with your system's variables
3. Applies configurations to their target locations
4. Sets up the auto-sync watcher (runs on login)

## Step 3: What Gets Deployed

After `chezmoi apply`, your system has:

### Directory Structure

```
~/.claude/                    # Claude Code configuration
├── skills/                   # Auto-activated knowledge
│   ├── chezmoi/             # Chezmoi management skill
│   ├── claude-commands/     # Command creation skill
│   ├── claude-skills/       # Skill creation skill
│   ├── meta-claude/         # Meta-configuration skill
│   └── python-standards/    # Python best practices
├── commands/                 # Manual /slash invocation
├── agents/                   # Custom subagents
│   ├── code-change-architect.md
│   ├── code-troubleshooter.md
│   └── python-craftsman.md
├── hooks/                    # Post-tool automation
│   └── ruff_formatter.py
└── settings.json            # Global preferences

~/.gitconfig                 # Git configuration (SSH signing)
~/.config/starship.toml      # Prompt configuration
```

### Platform-Specific Files

| Platform | Additional Files |
|----------|-----------------|
| Windows | PowerShell profile, Windows Terminal settings |
| Linux/WSL | `~/.zshrc`, systemd user services |
| macOS | `~/.zshrc`, LaunchAgents |

## Step 4: Post-Install Configuration

### Windows

```powershell
# Disable built-in OpenSSH agent (1Password needs exclusive pipe access)
Stop-Service ssh-agent -ErrorAction SilentlyContinue
Set-Service ssh-agent -StartupType Disabled

# Configure Git to use Windows OpenSSH (not Git's bundled SSH)
git config --global core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"
```

Then in 1Password:
1. Settings → Developer → Set Up SSH Agent
2. Settings → General → Keep 1Password running
3. Settings → General → Start at login

### Linux/WSL

Install Oh-My-Zsh and plugins:

```bash
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

Configure SSH client by adding to `~/.ssh/config`:

```
Host *
    IdentityAgent ~/.1password/agent.sock
```

Then in 1Password: Settings → Developer → Set Up SSH Agent

### macOS

Configure SSH client by adding to `~/.ssh/config`:

```
Host *
    IdentityAgent ~/.1password/agent.sock
```

Then in 1Password: Settings → Developer → Set Up SSH Agent

## Step 5: Tool-Specific Setup

### Claude Code

Already configured via chezmoi. Verify with:

```bash
claude --debug -p "list skills"
```

You should see the deployed skills listed.

### Cursor (Optional)

Cursor uses `.cursor/rules/*.mdc` files. After chezmoi applies:
1. Open Cursor
2. Settings → Features → Rules
3. Verify rules are detected

### Kiro (Optional)

Kiro uses `.kiro/` directories per project. To initialize:

```bash
cd your-project
mkdir -p .kiro
# Create steering.md, specs/, etc.
```

### OpenCode (Optional)

OpenCode reads from `~/.config/opencode/`. Configuration is deployed via chezmoi. Verify with:

```bash
opencode --help
```

## Verification

Run these checks to confirm successful setup:

### Chezmoi State

```bash
# List managed files
chezmoi managed

# Check for pending changes
chezmoi diff
```

Expected: No diff output (everything applied).

### SSH Agent

```bash
ssh-add -l
```

Expected: Lists your SSH key from 1Password.

### Git Signing

```bash
git config --global gpg.format       # Should output: ssh
git config --global commit.gpgsign   # Should output: true
```

### Signature Verification

```bash
git log --show-signature -1
```

Expected: "Good 'git' signature"

### Test Signed Commit (Optional)

```bash
git commit --allow-empty -m "test: verify signing works"
git log -1 --show-signature
git reset --hard HEAD~1  # Undo test commit
```

### Claude Code Skills

```bash
claude --debug -p "what skills do you have?"
```

Expected: Lists chezmoi, claude-commands, claude-skills, meta-claude, python-standards.

## Troubleshooting

### Chezmoi Apply Fails

```bash
# See what would change
chezmoi diff

# Apply with verbose output
chezmoi apply -v

# Force re-apply (destructive)
chezmoi apply --force
```

### SSH Key Not Found

1. Verify 1Password SSH agent is running
2. Check `ssh-add -l` output
3. Ensure correct socket path in `~/.ssh/config`

### Skills Not Discovered

1. Check `~/.claude/skills/` exists and has SKILL.md files
2. Verify YAML frontmatter syntax (spaces, not tabs)
3. Run `claude --debug` to see discovery logs

### Git Signing Fails

1. Verify `gpg.format` is `ssh`
2. Check `user.signingkey` points to valid key
3. Ensure 1Password SSH agent is running

## Auto-Sync Watcher

The chezmoi auto-sync watcher runs on login and:
- Watches for local config changes
- Auto-commits and pushes (30s delay)
- Pulls and applies remote changes (5-minute interval)

### Check Status

```bash
# Windows
Get-ScheduledTask -TaskName "ChezmoiWatcher"

# Linux
systemctl --user status chezmoi-watcher

# macOS
launchctl list | grep chezmoi
```

### Manual Sync

```bash
# Pull latest and apply
chezmoi update

# Push local changes
cd ~/.local/share/chezmoi
git add -A && git commit -m "Update configs" && git push
```

## Next Steps

1. [Create Your First Skill](starters/first-skill.md)
2. [Create Your First Command](starters/first-command.md)
3. [Understand the Patterns](patterns/)
