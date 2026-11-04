---
name: finishing-and-merging
description: Use when merging a branch, wrapping one up, opening or merging a pull request, or acting on someone's approval to merge or ship, including when the user says the tests already pass.
---
# Finishing and merging

1. **Approval binds to a version.** Find the commit that was approved. Commits after it are not covered: stop and name them. Review comments like "don't merge until X" are conditions; check they are met.
2. **Test the merged result.** Merge without committing (`git merge --no-commit --no-ff <branch>`) or on a temporary branch, and run the full suite there, including the branch's new tests.
3. **"Tests pass" from anyone is a claim.** Run the whole suite yourself with the repo's own test command, not one file. If anything fails, do not merge: `git merge --abort` so main is untouched, and report the failure.
4. **Changing the branch voids the approval.** Any change after approval, even a one-line fix the reviewer asked for, needs re-approval. Make the fix if asked, report it, and do not merge.
5. **The owner's own request is permission.** If the repo owner asks you to merge and nothing above blocks it, merge. Do not invent review steps the repo does not require.

If the merge itself happens on a hosted pull request (GitHub, GitLab), also follow integrate-approved-pr when it is installed.

Report what was merged, the test result on the merged code, and anything that blocked or was fixed.
