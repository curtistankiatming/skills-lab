---
name: before-irreversible-actions
description: Use before deleting data, sending messages or emails, deploying, migrating, paying, publishing, or touching production or shared systems, even when the step was requested, agreed earlier, or the user says they already checked.
---
# Before an irreversible action

Immediately before the step, every time:

1. **Exact target.** Read the config, env files, flags, current branch and defaults the command uses. Do not trust its name or what was said earlier.
2. **Fresh data.** `ls` the data folders and read the other files about the same people or items (payments, cancellations, status, build info). Look for anything saying the action is no longer needed or points elsewhere. Exported or "synced weekly" data may be stale. Name each target you would skip and why.
3. **Matches the approval?** Approval covers the exact target approved: "staging" does not cover production; "main" does not cover a work-in-progress branch.
4. **Undo and blast radius.** Can it be undone? Who else is affected?

If any check fails or is unknown, do not run it. Say what you found (file and value), what would happen, and ask one precise question or offer the safe alternative.

Not irreversible: local edits to git-tracked files and deleting unused code in a working copy. Just do those.
