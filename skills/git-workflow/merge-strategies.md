# Merge Strategies

Guide to merge, rebase, and fast-forward operations.

## Three Integration Strategies

### 1. Merge (with merge commit)

```bash
git checkout main
git merge feature-branch
```

Creates a merge commit that combines histories:

```
      A---B---C  (feature)
     /         \
D---E-----------M  (main, merge commit)
```

**Use when**:
- Preserving exact history of branch divergence
- Working on shared branches
- Auditing and traceability matter
- You want easy revert of entire feature (`git revert -m 1 M`)

### 2. Rebase

```bash
git checkout feature
git rebase main
```

Replays commits on top of target branch:

```
Before:
      A---B---C  (feature)
     /
D---E---F  (main)

After:
              A'--B'--C'  (feature, rebased)
             /
D---E---F  (main)
```

**Use when**:
- Working alone on a private branch
- Keeping feature branch up-to-date with main
- Cleaning up messy local commits before sharing
- Preparing for a clean fast-forward merge

### 3. Fast-Forward

```bash
git checkout main
git merge --ff-only feature
# or after rebase:
git merge feature  # automatically fast-forwards
```

Moves branch pointer forward (no merge commit):

```
Before:
D---E  (main)
     \
      A---B---C  (feature)

After:
D---E---A---B---C  (main, feature)
```

**Use when**:
- Feature is directly ahead of main
- You want clean linear history
- After rebasing to prepare

## The Golden Rule

> **Never rebase commits that exist outside your repository and that people may have based work on.**

If you've pushed commits and others have pulled them, rebasing rewrites history and causes divergence. Merge instead.

## Recommended Workflows

### Solo Developer / Private Branch

```bash
# Keep feature up-to-date
git checkout feature
git rebase main

# When ready, merge cleanly
git checkout main
git merge --ff-only feature
```

### Team Collaboration

```bash
# Update feature with main's changes
git checkout feature
git merge main  # creates merge commit, preserves history

# When feature complete, merge to main
git checkout main
git merge --no-ff feature  # explicit merge commit
```

### Squash Before Merge

For messy commit history on feature branch:

```bash
# Interactive rebase to squash
git checkout feature
git rebase -i main
# Mark commits as 'squash' or 'fixup'

# Then fast-forward
git checkout main
git merge --ff-only feature
```

## Common Scenarios

### Sync Feature Branch with Main

**Option A: Merge (safer)**
```bash
git checkout feature
git merge main
```

**Option B: Rebase (cleaner history)**
```bash
git checkout feature
git rebase main
# Resolve any conflicts, then:
git rebase --continue
```

### Resolve Merge Conflicts

```bash
# During merge or rebase
git status  # shows conflicted files
# Edit files to resolve
git add <resolved-files>
git merge --continue  # or git rebase --continue
```

### Undo a Rebase

```bash
# Find original commit
git reflog
# Reset to before rebase
git reset --hard HEAD@{n}
```

### Undo a Merge

```bash
# Before pushing
git reset --hard HEAD~1

# After pushing (creates revert commit)
git revert -m 1 <merge-commit>
```

## Force Push Safely

After rebasing a pushed branch:

```bash
# ONLY if you're sure no one else is using the branch
git push --force-with-lease  # safer than --force
```

`--force-with-lease` fails if remote has commits you don't have locally.

## Decision Flowchart

```
Is the branch shared/public?
├─ Yes → Use merge (never rebase)
└─ No (private branch) →
   ├─ Want clean linear history? → Rebase, then fast-forward
   └─ Want to preserve branch history? → Merge with --no-ff
```
