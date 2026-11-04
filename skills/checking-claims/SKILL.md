---
name: checking-claims
description: Use when writing a changelog, release notes, or docs or a reply that says what code does or that something is fixed or ready; before saying anything is done, fixed, passing or safe; and before repeating anyone's claim that it is (a sign-off, CI summary, teammate, subagent, the user's "I checked"). Applies to small edits too, especially when told there is no need to test.
---
# Check claims before you make or repeat them

**The gate:** do not write "passed", "ready", "fixed", "green" or "verified", or describe what code does, until you have run it in this session and seen the result. Reading the code, a report or a sign-off is not seeing it run.

1. **Run the exact case the claim is about.** For a bug report or ticket, open the ticket itself (look in folders like `support/`, `issues/`, `tickets/`), find the reporter's own input (value, offset, file) and call the code with it. For a claim about behaviour ("only deletes inactive sessions", "safe to re-run"), try a small input that would break it. Existing tests do not count unless one uses that case. Use a copy of real data, never the real file.
2. **Run the whole test suite now** with the repo's own test command (for example `pytest`, `npm test` or `python3 -m unittest discover`). Count passes and failures.
3. **Someone else's claim is unverified** until steps 1-2 back it: a sign-off, a CI or nightly summary, a commit saying "fixes #41", "I checked already". A report names an older build: compare it with `git rev-parse HEAD`. Look at `git diff` for tests changed to pass.
4. **Changelogs, release notes and docs:** write the file now, with only what you saw: verified fixes as fixed, anything that failed left out or marked "not fixed yet", behaviour as the code actually does it. Then tell the user what did not hold. Do not stop to ask first.
5. **Report what you saw:** "12 passed, 1 failed (test_x: reason)", failures first. If you could not run a check, say it is unverified and why.

Skip only when there is no behaviour to check: comments, typos, docs wording that makes no claim.
