# Development-discipline skills: held-out scenarios

These 21 scenarios (three per skill) were written after the skills had been tuned on a separate set of 46, and were never used for tuning. Each is a small fictional git repository and one user request.

## What's here

- `scenarios/<skill>__f<n>/setup.sh` builds the fixture repository in the current directory. It calls `$GITINIT` at the end, which should point to [gitinit.sh](gitinit.sh) (it makes the initial commit).
- `prompt.txt` is the user's request, sent as the first message.
- `check.sh`, run in the same directory afterwards, prints `PASS`/`FAIL`/`INFO` lines about the resulting files and git state.
- `rubric.txt` holds the MUST and MUST NOT items a grader scores the transcript against. A scenario passes only when every item holds. `check.sh` output is evidence for the grader, not the score on its own.

Each scenario covers one of: the skill should fire, a near-miss where it should not, or a user pushing to skip the rule.

## Recorded result

Conditions: Claude Code headless (`claude -p`) with Claude Haiku 4.5 (`claude-haiku-4-5-20251001`), edits auto-accepted and Bash limited to ordinary development commands; five runs per scenario per condition; transcripts graded blind against `rubric.txt` by a separate Claude model.

| Condition | Passed (of 105 runs) |
| --- | --- |
| No skills | 36 (34%) |
| obra/superpowers, pinned release | 39 (37%) |
| This pack, earlier revision (v8) | 79 (75%) |

The skills in this collection are a later revision (v14), tuned further on weak spots: renaming on `main` with an untracked user file, "just the SKILL.md" requests and stale CI or QA sign-offs. v14 was checked on three further new scenarios (12 of 15 runs passed, against 0 of 15 with no skills) but has not been rerun on all 21 here. Stale sign-offs remain the weakest case, at about 60%.

Only Claude Code with Haiku 4.5 was tested, always with the routing list from [adapters/](../../adapters/README.md) loaded at session start. No other host, model or skills-only setup has a recorded result. Transcripts are kept outside this repository.
