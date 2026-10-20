# Skills Lab catalog

Collection 2.1.1: six installable skills, plus one example skill in [examples/](examples/README.md). The [inventory](inventory.json) records every tracked file's size and SHA-256. See [rights](RIGHTS.md).

| Folder | Use when | Boundary | Entry point |
| --- | --- | --- | --- |
| governed-task-lifecycle | The owner says Initialize (or Initiate), Validate or Approve for a named task, or the project requires that lifecycle. | Not for ordinary requests. Initialize builds the authorized work; author checks don't finish Validate; Approve carries out only the effects the owner approved. | [SKILL.md](skills/governed-task-lifecycle/SKILL.md) |
| verify-exact-candidate | Exact files, hashes or revisions must match a pinned candidate or approved baseline, in a review, transfer or handoff. | Not for general code review, testing, approval or merging. Byte identity is not semantic acceptance or permission to integrate. | [SKILL.md](skills/verify-exact-candidate/SKILL.md) |
| integrate-approved-pr | Checking whether a PR can merge, or marking ready or merging a PR the owner explicitly approved. | Not for general code review. A review pass or design approval is not permission to merge. Changed heads and unknown outcomes are reconciled before any retry. | [SKILL.md](skills/integrate-approved-pr/SKILL.md) |
| scope-pull | Whether a project is on track, what is left against the plan, whether scope has crept, or whether new work should be added to the project's agreed scope, including non-software projects. | Reports only; it doesn't approve or start work. Missing evidence is not evidence of non-completion. For what a single recorded run did, use lean-history-reporting. | [SKILL.md](skills/scope-pull/SKILL.md) |
| lean-history-reporting | A status report on, or a diagnosis of, earlier work recorded in a chat, session, thread or task history. | Summaries first; fetch full outputs when a fact, contradiction or check needs them. Omitted output never proves success. For progress against a plan, use scope-pull. Doesn't repair, rerun or approve. | [SKILL.md](skills/lean-history-reporting/SKILL.md) |
| node-workflow-batcher | A task needs many separate file reads and calculations that one script could do in a code tool (Node, Python or similar). | Not for ordinary coding, editing or running a test suite. Needs a host code-execution tool. Check every result; stop at decisions, approvals or a denied provider. Not for steps that need approval or change anything outside the task. | [SKILL.md](skills/node-workflow-batcher/SKILL.md) |

## Included resources

- Lifecycle: [detailed rules](skills/governed-task-lifecycle/references/detailed-rules.md), [owner-facing summary format](skills/governed-task-lifecycle/references/chat-summary.md), [optional task record](skills/governed-task-lifecycle/assets/task-record.md), and Codex agent metadata.
- Verification: [detailed rules](skills/verify-exact-candidate/references/detailed-rules.md), [Git custody reference](skills/verify-exact-candidate/references/git-custody.md), [local checker reference](skills/verify-exact-candidate/references/local-checker.md), the optional [checker script](skills/verify-exact-candidate/scripts/verify_files.py), an [optional verification record](skills/verify-exact-candidate/assets/verification-record.md), [fictional examples and evaluation cases](skills/verify-exact-candidate/references/check-cases.md), and Codex agent metadata. The checker's tests are in `tests/verify-exact-candidate/`, outside the skill folder.
- Integration: [detailed rules](skills/integrate-approved-pr/references/detailed-rules.md), [optional integration receipt](skills/integrate-approved-pr/assets/integration-receipt.md) and Codex agent metadata.
- Scope Pull: [detailed rules](skills/scope-pull/references/detailed-rules.md), [fictional examples and evaluation cases](skills/scope-pull/references/check-cases.md) and [Codex agent metadata](skills/scope-pull/agents/openai.yaml).
- Lean History Reporting and Node Workflow Batcher are a single `SKILL.md` each.

The `agents/openai.yaml` files are optional Codex metadata that allow implicit invocation there. Other hosts read only `SKILL.md`. Whether a host discovers a skill, and whether the agent follows it, depends on the host and model.

## Example skill

[Offline Usage Reporter](examples/offline-usage-reporter/SKILL.md) is kept in `examples/` and is not part of the installed set. It shows a skill wrapping a deterministic Node.js helper: [receipt contract](examples/offline-usage-reporter/references/receipt-contract.md), [report.cjs](examples/offline-usage-reporter/scripts/report.cjs), [gate.cjs](examples/offline-usage-reporter/scripts/gate.cjs), fictional fixtures and `node:test` checks. It reports on fictional O2 usage-monitor replay receipts only.

## Evaluation

The [evaluation guide](EVALUATING.md) separates case specifications, structural checks and observed behavior. The [2026-10-07 comparison](evaluations/2026-10-07/README.md) covers earlier versions of Verify Exact Candidate and Scope Pull; the published and revised instructions tied, so no behavioral gain is claimed for the current versions. The [harder cases](evaluations/harder-cases/README.md), with trigger tests and a runner for local models, cover all six current skills and have not been run yet.

Earlier distribution snapshots are described in [HISTORY.md](HISTORY.md).
