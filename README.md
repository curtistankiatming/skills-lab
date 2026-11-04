# Skills Lab

Fourteen instruction skills that help an AI agent do careful, checkable work. The first seven are governance and reporting skills: run a task through Initialize, Validate and Approve; verify exact files against a pinned baseline; merge only a PR the owner approved; check a project against its agreed scope; report on earlier work from its history; batch local tool work into one code call; and keep drafts and temp files in a scratch folder that is cleaned up after the task. The other seven are development-discipline skills for everyday coding: design before building, test first, keep work apart from the user's uncommitted changes, check claims before making them, merge carefully, pause before irreversible actions, and write skills properly. Each skill is a folder with a `SKILL.md` in the common Agent Skills format (only `name` and `description` frontmatter), so the same files work in Claude, Codex, Hermes and plain-prompt local models.

Source version 3.2.0 (latest release v3.1.0); released versions are on the [Releases page](https://github.com/curtistankiatming/skills-lab/releases). The collection is MIT licensed; see [RIGHTS.md](RIGHTS.md).

## Choose a skill

| Skill | Use it when | Entry point |
| --- | --- | --- |
| Governed Task Lifecycle | The owner says Initialize (or Initiate), Validate or Approve for a named task, or the project requires that lifecycle. Not for ordinary requests such as git init or design sign-off. | [governed-task-lifecycle](skills/governed-task-lifecycle/SKILL.md) |
| Verify Exact Candidate | Exact files, hashes or revisions must match a pinned candidate or approved baseline, in a review, transfer or handoff. Not for general code review. | [verify-exact-candidate](skills/verify-exact-candidate/SKILL.md) |
| Integrate Approved PR | You need to check whether a PR can merge, or mark ready or merge a PR the owner explicitly approved. Not for code review or merging branches locally. | [integrate-approved-pr](skills/integrate-approved-pr/SKILL.md) |
| Scope Pull | You're asked whether a project is on track, what is left against the plan, whether scope has crept, or whether new work should be added to the project's agreed scope. Works for non-software projects too. | [scope-pull](skills/scope-pull/SKILL.md) |
| Lean History Reporting | You're asked for a status report on, or a diagnosis of, earlier work recorded in a chat, session, thread or task history. | [lean-history-reporting](skills/lean-history-reporting/SKILL.md) |
| Node Workflow Batcher | A task needs many separate file reads and calculations that one script could do in a code tool (Node, Python or similar). Not for ordinary coding, editing or running a test suite. | [node-workflow-batcher](skills/node-workflow-batcher/SKILL.md) |
| Scratch Folder | A task makes drafts, logs, test output or other temporary files. They go in `.scratch`; at the end only what matters is moved to a permanent place and the rest is deleted. | [scratch-folder](skills/scratch-folder/SKILL.md) |

Scope Pull and Lean History Reporting point to each other: progress against a plan is Scope Pull, and what a single recorded run did is Lean History Reporting. The [catalog](CATALOG.md) lists each skill's resources and boundaries. [examples/](examples/README.md) holds an example skill that is not part of the installed set.

### Development discipline

| Skill | Use it when | Entry point |
| --- | --- | --- |
| Designing Before Building | Building a feature or changing existing behaviour when there are real choices to make, even if it sounds small or the user says to skip the design. | [designing-before-building](skills/designing-before-building/SKILL.md) |
| Test-First Changes | Adding or changing behaviour in code that has tests, and every bugfix, even a one-character fix or "no ceremony". | [test-first-changes](skills/test-first-changes/SKILL.md) |
| Isolating Work | A task ends in a git commit, or the user wants new work kept apart from their uncommitted changes. Not for plain edits the user did not ask to commit. | [isolating-work](skills/isolating-work/SKILL.md) |
| Checking Claims | Writing a changelog, release notes or docs about what code does; before saying anything is done, fixed or passing; before repeating someone else's claim that it is. | [checking-claims](skills/checking-claims/SKILL.md) |
| Finishing and Merging | Merging or wrapping up a branch, opening or merging a pull request, or acting on an approval to merge or ship. | [finishing-and-merging](skills/finishing-and-merging/SKILL.md) |
| Before Irreversible Actions | Deleting data, sending, deploying, migrating, paying, publishing or touching production, even when it was requested or "already checked". | [before-irreversible-actions](skills/before-irreversible-actions/SKILL.md) |
| Authoring Skills | Any task that touches a SKILL.md or a skill's scenarios, even a two-line change. | [authoring-skills](skills/authoring-skills/SKILL.md) |

These seven helped most with a short routing list shown at the start of each session. [adapters/](adapters/README.md) holds that list and how to load it in Claude Code, Codex, Cursor, OpenCode and Gemini CLI. Finishing and Merging covers local merges and the checks before any merge; for merging a hosted PR, Integrate Approved PR also applies.

## Install

Copy the whole skill folder, not only `SKILL.md`: some skills link to files in their `references/`, `assets/` or `scripts/` folders.

- **Claude Code:** copy the folder to `~/.claude/skills/<skill-name>/` for all projects, or `.claude/skills/<skill-name>/` inside one project.
- **Claude apps:** zip the skill folder and upload it under Settings → Capabilities → Skills.
- **Codex:** copy the folder to `~/.codex/skills/<skill-name>/`. The optional `agents/openai.yaml` files are Codex metadata; other hosts ignore them.
- **Hermes:** install or copy the folder into Hermes's skills directory (by default `~/.hermes/skills/<skill-name>/`). Hermes scans skills on install. Verify Exact Candidate ships an optional Python checker in `scripts/`; if the scan blocks it, the skill still works from its Markdown alone.
- **Local models without skill support** (for example Gemma 12B or Qwen 27B in Ollama, LM Studio or llama.cpp): paste the skill's `SKILL.md` into the system prompt or the first message, and add a referenced file only when a step calls for it. Load one skill at a time. Each `SKILL.md` is about 2.5 to 4 KB, except Governed Task Lifecycle at about 8 KB. The longer rules each skill links to in `references/` are needed only for edge cases.

Selecting or installing a skill grants no new permissions. The skills tell the agent to stop and ask when a step needs approval.

## Use

Most hosts pick a skill from its description, so an ordinary request is enough: "Initialize TASK-7: build the export and stop ready for Validate", "Is PR #123 ready to merge? Don't change anything", or "Where is the website project against the plan?". To name a skill explicitly:

```text
Use the governed-task-lifecycle skill. Initialize TASK-001: build the authorized deliverable and stop ready for Validate.
Use the verify-exact-candidate skill to compare the supplied files with the pinned manifest. Read and hash only.
Use the integrate-approved-pr skill to inspect OWNER/REPO PR #123. Make no changes.
Use the scope-pull skill to check the project's progress against its agreed scope, using the sources I provide.
Use the lean-history-reporting skill to report the status of yesterday's migration task.
Use the node-workflow-batcher skill for this local job in the available code tool. Stop at decisions or approvals.
Use the scratch-folder skill: keep drafts in .scratch and clean it up when you finish.
```

In Codex, `$skill-name` also works as a selector. Replace the example identifiers with real ones; an example is not an authorization.

## Requirements and limits

- Governed Task Lifecycle, Integrate Approved PR, Scope Pull and Lean History Reporting are instructions only. They need whatever access the task itself needs (for example a GitHub tool to merge a PR, or a history reader).
- Verify Exact Candidate includes an optional Python standard-library checker, `scripts/verify_files.py`. Its tests live outside the skill folder in `tests/verify-exact-candidate/`. Run the checker only with a trusted interpreter and when the task allows it.
- Node Workflow Batcher needs a code-execution tool: a persistent Node or Python REPL, a notebook kernel, or a one-shot script runner. It supplies no runtime of its own.
- Scratch Folder needs only file access in the working folder. Its cleanup commands are given for both Linux or macOS and Windows PowerShell.
- Lean History Reporting needs authorized access to the history it reports on. It uses a summary or outputs-omitted view when the host offers one.
- No skill includes an installer, hooks, server, credentials or hosted workflow. The optional development-discipline adapters include a session-start hook for Claude Code, which you add yourself. A skill's instructions don't enforce themselves; how faithfully an agent follows them depends on the host and model.

## Evaluation

The [evaluation guide](EVALUATING.md) describes how to compare a revision against its baseline. The [2026-10-07 comparison](evaluations/2026-10-07/README.md) tested earlier versions of Verify Exact Candidate and Scope Pull only, and found no measurable difference between them. The [harder cases](evaluations/harder-cases/README.md) cover the six earlier skills (Scratch Folder has trigger tests only) and can run against a local model through any OpenAI-compatible endpoint; no results are recorded here yet, so no claim is made about how much the skills help any particular model.

## Maintenance

See [CONTRIBUTING.md](CONTRIBUTING.md) for changes, [RELEASING.md](RELEASING.md) for releases, [RIGHTS.md](RIGHTS.md) for licensing and provenance, and [AGENTS.md](AGENTS.md) for repository instructions. [inventory.json](inventory.json) records the size and SHA-256 of every tracked file. Earlier distribution snapshots and their notes are kept in [HISTORY.md](HISTORY.md).
