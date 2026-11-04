---
name: isolating-work
description: Use at the start of any task that ends in a git commit ("fix X and commit it"), before your first edit, and when the user wants new work kept separate from their own uncommitted changes. Keeps the user's uncommitted work out of your commit and untouched. Not for plain edits the user did not ask to commit or keep separate.
---
# Isolating work

**When.** The task ends in a commit, or the user wants the work kept apart from their changes. Otherwise ("just edit it", "I'll commit it myself"), edit their working copy and stop: no branch, worktree, stash or commit.

**Do this before you read or edit any code:**
1. Run `git status --short` and `git diff --cached --name-only`. Every file in the first list is the user's work: mention it in one line. The second list is what is staged (a ` D` or ` M` with a leading space is not staged).
2. Pick the place to work:
   - **Something is staged, a file you must change has the user's edits, or the commit belongs on another branch:** use a worktree. Run `git worktree add .worktrees/<task> -b <task> HEAD` (or `git worktree add .worktrees/<task> <branch>` for a branch the user named). Every path you read, edit, test and commit is under `.worktrees/<task>/`. Never edit the original file, not even once.
   - **Otherwise:** work in place. If the user asked for the current branch ("on main", "no branches"), commit there and create no branch or worktree; otherwise `git switch -c <task>` first.
3. **The user's files stay theirs**, even if they use the name or code you are changing: "everywhere" means the committed code. Never `git add` a file from step 1's list, untracked (`??`) ones included. Grep the user's files for what you changed, and in your report write one line per hit: "<file> (yours, uncommitted) still uses <old name>."
4. Never run `git stash`, `git reset`, `git restore`, `git checkout -- <file>`, `git add -A`, `git add .` or `git commit -a`. Commit with `git add <each path you changed>`, then `git commit`.
5. Leave the user's checkout exactly as found: same branch and the same modified, staged and untracked files. Do not stop to ask how to proceed: these steps are the answer.

Report where the commit is, the user's files you left alone and what they still need, and how to bring a side-branch fix in (for example `git merge <task>` once their own work is committed).
