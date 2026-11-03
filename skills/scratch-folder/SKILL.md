---
name: scratch-folder
description: Use for drafts and temp files: work in scratch, clean up. Keep only files the project or user needs and delete the rest. Not for files the user asked for by name or path, or for deleting anything outside the scratch folder.
---

# Scratch folder

Keep drafts and temporary files in one scratch folder. When the task ends, move only what matters to a permanent place and delete the rest, so files don't pile up.

## When to use

- A task makes working files: drafts, notes, logs, test output, downloads or one-off scripts.
- The user asks you to avoid clutter or to clean up temporary files.
- Skip it for a file the user asked for by name or path. Write that file where they asked.

## Steps

1. **Make the folder.** Use `.scratch` in the folder you work in. Create it if it is missing. If that folder is a git repository, add the line `.scratch/` to `.git/info/exclude`, so scratch files are never committed.
2. **Write working files there.** Drafts, notes, logs, test output, downloads and temporary scripts all go in `.scratch`.
3. **Before you finish, check each file you made in `.scratch`.** Keep it only if:
   - the user asked for it, or
   - the project needs it to build, run or test, or
   - it records a decision or result someone will need later.
4. **Move each kept file** to its permanent place, next to similar files in the project. Check before you replace an existing file. In a cloud container, a kept file is safe only once it is committed or saved where the user can reach it.
5. **Delete the other files you made in `.scratch`.** Delete the folder when it is empty: `rmdir .scratch` on Linux or macOS, `Remove-Item .scratch` in Windows PowerShell, or your host's delete tool.
6. **Report in one line:** which files you kept and where, and that scratch was cleaned up.

## Rules

- Delete only files you made inside `.scratch`. Never delete anything outside it as cleanup.
- If you are unsure whether a file matters, leave it in `.scratch` and ask the user.
- If `.scratch` already holds files you did not make, leave them and mention them in your report.
- If the task stops early, for example on an error or while waiting for approval, leave `.scratch` as it is and say so.
- If the user says to keep scratch files, keep them.

## Example

Task: fix a failing build. You save the build log, two draft patches and a test script in `.scratch`. The fix goes into the project. The test script reproduces the bug, so you move it to `tests/`. You delete the log and the drafts, then remove the empty folder. Report: "Kept tests/test_build_bug.py; deleted the log and drafts; scratch cleaned up."
