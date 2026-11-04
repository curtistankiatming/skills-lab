# Adapters for the development-discipline skills

The seven development-discipline skills (designing-before-building, test-first-changes, isolating-work, checking-claims, finishing-and-merging, before-irreversible-actions, authoring-skills) work as ordinary skills on their own. In testing they helped most when the agent also saw a short routing list at the start of each session, telling it which skill to open and to open it even when a task looks tiny or the user asks to skip steps. [routing.md](routing.md) is that list. It is the only file here with instructions; each adapter below just puts it in front of the agent.

These adapters are optional and are not skills. Nothing here installs itself.

## Claude Code

1. Copy the seven skill folders to `~/.claude/skills/`.
2. Copy this `adapters/` folder to `~/.claude/skills-lab-adapters/`.
3. Add the `SessionStart` entry from [claude-code/hooks.json](claude-code/hooks.json) to the `hooks` section of `~/.claude/settings.json`.

The hook runs [claude-code/session-start](claude-code/session-start), a two-line shell script that prints `routing.md`. On Windows without a POSIX shell, use `type` on `routing.md` as the command instead.

## Codex, Cursor and OpenCode

These hosts read `AGENTS.md`. Copy the skill folders where the host looks for skills (for Codex, `~/.codex/skills/`; for Cursor and OpenCode, the skills folder their documentation names), then paste the contents of `routing.md` into the project's `AGENTS.md` (or the host's global instructions file). If the host has no skill loader, keep the skill folders in the project and the routing list's last line tells the agent to read `<skills folder>/<skill-name>/SKILL.md`; replace `<skills folder>` with the real path.

## Gemini CLI

Paste the contents of `routing.md` into `GEMINI.md` (project or `~/.gemini/GEMINI.md`) and keep the skill folders in a known path, replacing `<skills folder>` in the last line with it. Where Gemini CLI's own skill support is enabled, copy the folders there instead.

## Tested hosts

All recorded results come from Claude Code with Claude Haiku 4.5. The other hosts are untested. See [the evaluation record](../evaluations/dev-discipline/README.md).
