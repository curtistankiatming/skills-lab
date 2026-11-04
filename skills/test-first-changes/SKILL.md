---
name: test-first-changes
description: Use when adding or changing behaviour in code that has tests, including small additions like a new flag, option, field, or discount rule, and every bugfix, even a one-character fix. Applies even if the user says to skip tests or "no ceremony".
---
# Test first

If the task ends in a commit, open isolating-work first and do these steps where it tells you to work.

1. Write the test first, in the existing test file and style: the normal case and the edge cases. For a bug, the test reproduces it.
2. Run it and watch it fail for the right reason. If it passes, the test is wrong.
3. Make the smallest change that makes it pass. For a bug, fix the line that is actually wrong, not the symptom.
4. Run the full suite and report the result.

**Rules**
- If your test shows the code is wrong, fix the code. Never change an expected value to match what the code returns.
- "No ceremony" or "just patch it" still gets one regression test: it is the minimum. If the repo requires tests, say so in one line. Skip the test only if the user clearly says no test, and say so.
- Skip this skill for changes with no behaviour: docs, comments, formatting, version strings.
