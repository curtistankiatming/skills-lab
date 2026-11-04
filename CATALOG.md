# Skills Lab catalog

Collection 3.2.0 (source): fourteen installable skills, plus one example skill in [examples/](examples/README.md). The [inventory](inventory.json) records every tracked file's size and SHA-256. See [rights](RIGHTS.md).

| Folder | Use when | Boundary | Entry point |
| --- | --- | --- | --- |
| governed-task-lifecycle | The owner says Initialize (or Initiate), Validate or Approve for a named task, or the project requires that lifecycle. | Not for ordinary requests such as git init or design sign-off. Initialize builds the authorized work; author checks don't finish Validate; Approve carries out only the effects the owner approved. | [SKILL.md](skills/governed-task-lifecycle/SKILL.md) |
| verify-exact-candidate | Exact files, hashes or revisions must match a pinned candidate or approved baseline, in a review, transfer or handoff. | Not for general code review, testing, approval or merging. Byte identity is not semantic acceptance or permission to integrate. | [SKILL.md](skills/verify-exact-candidate/SKILL.md) |
| integrate-approved-pr | Checking whether a PR can merge, or marking ready or merging a PR the owner explicitly approved. | Not for code review or merging branches locally. A review pass or design approval is not permission to merge. Changed heads and unknown outcomes are reconciled before any retry. | [SKILL.md](skills/integrate-approved-pr/SKILL.md) |
| scope-pull | Whether a project is on track, what is left against the plan, whether scope has crept, or whether new work should be added to the project's agreed scope, including non-software projects. | Reports only; it doesn't approve or start work. Missing evidence is not evidence of non-completion. For what a single recorded run did, use lean-history-reporting. | [SKILL.md](skills/scope-pull/SKILL.md) |
| lean-history-reporting | A status report on, or a diagnosis of, earlier work recorded in a chat, session, thread or task history. | Summaries first; fetch full outputs when a fact, contradiction or check needs them. Omitted output never proves success. For progress against a plan, use scope-pull. Doesn't repair, rerun or approve. | [SKILL.md](skills/lean-history-reporting/SKILL.md) |
| node-workflow-batcher | A task needs many separate file reads and calculations that one script could do in a code tool (Node, Python or similar). | Not for ordinary coding, editing or running a test suite. Needs a host code-execution tool. Check every result; stop at decisions, approvals or a denied provider. Not for steps that need approval or change anything outside the task. | [SKILL.md](skills/node-workflow-batcher/SKILL.md) |
| scratch-folder | A task makes drafts, notes, logs, test output, downloads or one-off scripts, or the user asks to avoid clutter. | Not for files the user asked for by name or path. Deletes only files it made inside `.scratch`; when unsure whether a file matters, it keeps it and asks. A task that stops early leaves `.scratch` as it is. | [SKILL.md](skills/scratch-folder/SKILL.md) |

## Development discipline

| Folder | Use when | Boundary | Entry point |
| --- | --- | --- | --- |
| designing-before-building | Building a feature or changing behaviour with real choices, including small-sounding changes to existing behaviour. | Skips changes with one obvious implementation. Does not edit code until the person agrees, except parts that depend on no open choice. | [SKILL.md](skills/designing-before-building/SKILL.md) |
| test-first-changes | Adding or changing behaviour in code that has tests; every bugfix. | Skips docs, comments, formatting and version strings. Never changes an expected value to match the code. | [SKILL.md](skills/test-first-changes/SKILL.md) |
| isolating-work | A task ends in a commit, or work must stay apart from the user's uncommitted changes. | Not for plain edits the user will commit. Never stashes, resets or adds the user's files. | [SKILL.md](skills/isolating-work/SKILL.md) |
| checking-claims | Writing about what code does, or saying or repeating that something is done, fixed or passing. | Skips text that makes no behavioural claim. Unrun checks are reported as unverified. | [SKILL.md](skills/checking-claims/SKILL.md) |
| finishing-and-merging | Merging or wrapping up a branch or PR, or acting on an approval to merge or ship. | Approval binds to the approved commit. For a hosted PR merge, integrate-approved-pr also applies. | [SKILL.md](skills/finishing-and-merging/SKILL.md) |
| before-irreversible-actions | Deleting data, sending, deploying, migrating, paying, publishing or touching production. | Local edits to git-tracked files are not irreversible. Stops and asks when a check fails or is unknown. | [SKILL.md](skills/before-irreversible-actions/SKILL.md) |
| authoring-skills | A task touches a SKILL.md or a skill's scenarios. | Renames and mechanical edits get no new content. Follows the repo's own contributing rules. | [SKILL.md](skills/authoring-skills/SKILL.md) |

These seven are single-file skills. The optional [adapters](adapters/README.md) show a routing list at session start; the [held-out scenarios](evaluations/dev-discipline/README.md) record how they were tested.

## Included resources

- Lifecycle: [detailed rules](skills/governed-task-lifecycle/references/detailed-rules.md), [owner-facing summary format](skills/governed-task-lifecycle/references/chat-summary.md), [optional task record](skills/governed-task-lifecycle/assets/task-record.md), and Codex agent metadata.
- Verification: [detailed rules](skills/verify-exact-candidate/references/detailed-rules.md), [Git custody reference](skills/verify-exact-candidate/references/git-custody.md), [local checker reference](skills/verify-exact-candidate/references/local-checker.md), the optional [checker script](skills/verify-exact-candidate/scripts/verify_files.py), an [optional verification record](skills/verify-exact-candidate/assets/verification-record.md), [fictional examples and evaluation cases](skills/verify-exact-candidate/references/check-cases.md), and Codex agent metadata. The checker's tests are in `tests/verify-exact-candidate/`, outside the skill folder.
- Integration: [detailed rules](skills/integrate-approved-pr/references/detailed-rules.md), [optional integration receipt](skills/integrate-approved-pr/assets/integration-receipt.md) and Codex agent metadata.
- Scope Pull: [detailed rules](skills/scope-pull/references/detailed-rules.md), [fictional examples and evaluation cases](skills/scope-pull/references/check-cases.md) and [Codex agent metadata](skills/scope-pull/agents/openai.yaml).
- Lean History Reporting, Node Workflow Batcher and Scratch Folder are a single `SKILL.md` each.

The `agents/openai.yaml` files are optional Codex metadata that allow implicit invocation there. Other hosts read only `SKILL.md`. Whether a host discovers a skill, and whether the agent follows it, depends on the host and model.

## Example skill

[Offline Usage Reporter](examples/offline-usage-reporter/SKILL.md) is kept in `examples/` and is not part of the installed set. It shows a skill wrapping a deterministic Node.js helper: [receipt contract](examples/offline-usage-reporter/references/receipt-contract.md), [report.cjs](examples/offline-usage-reporter/scripts/report.cjs), [gate.cjs](examples/offline-usage-reporter/scripts/gate.cjs), fictional fixtures and `node:test` checks. It reports on fictional O2 usage-monitor replay receipts only.

## Evaluation

The [evaluation guide](EVALUATING.md) separates case specifications, structural checks and observed behavior. The [2026-10-07 comparison](evaluations/2026-10-07/README.md) covers earlier versions of Verify Exact Candidate and Scope Pull; the published and revised instructions tied, so no behavioral gain is claimed for the current versions. The [harder cases](evaluations/harder-cases/README.md), with trigger tests and a runner for local models, cover the six earlier skills, with trigger tests for Scratch Folder too; no results are recorded here yet.

Earlier distribution snapshots are described in [HISTORY.md](HISTORY.md).
