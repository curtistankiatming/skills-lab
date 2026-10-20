# Skills Lab catalog

Prepared distribution snapshot, 18 October 2026: collection 1.5.0 proposes Lean History Reporting 1.0.0 with five unchanged existing skill resource sets from integrated source 1.4.0 and the focused Reporter 1.0.2 correction. Reporter 1.0.1 and Batcher 1.0.0 are already published; this new source candidate does not establish installation, discovery or universal effectiveness. See [rights](RIGHTS.md) and the final [inventory](inventory.json).

| Folder | Use if | Boundary | Complete entry point |
| --- | --- | --- | --- |
| governed-task-lifecycle | The owner invokes Initialize/Initiate, Validate or Approve, or the destination requires that contract. | Do not impose a lifecycle on ordinary work. Initialize produces the authorized analysis, design or implementation under the active destination contract; author checks do not finish Validate; approval covers only its named effects. | [SKILL.md](skills/governed-task-lifecycle/SKILL.md) |
| verify-exact-candidate | Exact identity, custody or evidence must be checked against a pinned candidate or baseline. | Byte identity is not semantic acceptance, live capability, owner approval or integration authority. | [SKILL.md](skills/verify-exact-candidate/SKILL.md) |
| integrate-approved-pr | Integration prerequisites need inspection, or exact approved readiness/merge effects need completion. | A review pass or design approval supplies no merge authority. Changes and unknown outcomes require reconciliation. | [SKILL.md](skills/integrate-approved-pr/SKILL.md) |
| scope-pull | Project scope, delivery against commitments, scope changes or proposed expansion needs reconciliation, including non-software work. | Reconciliation does not approve, dispatch, implement or establish acceptance. Missing evidence is not evidence of noncompletion. | [SKILL.md](skills/scope-pull/SKILL.md) |
| lean-history-reporting | Authorized task-history status reporting or diagnosis needs selective detailed-output retrieval. | Compact view is a default, not evidence of success; fetch required diagnostics, contradictions and verification evidence. Requires a supported history reader; no new effects or savings guarantee. | [SKILL.md](skills/lean-history-reporting/SKILL.md) |
| node-workflow-batcher | Authorized local read, derive and validate phases can be grouped into one code-tool call (Node, Python or similar). | Requires a host code-execution tool; state persists only in a persistent runtime. Inspect every outcome; stop at unresolved decisions, approvals or provider denial. No downstream authority is added. | [SKILL.md](skills/node-workflow-batcher/SKILL.md) |

## Explicit examples

```text
Use $governed-task-lifecycle. Initialize TASK-001: prepare the implementation described in the supplied assignment.
Use $verify-exact-candidate to verify the three named files against the supplied SHA-256 manifest. Read and hash only.
Use $integrate-approved-pr to inspect OWNER/REPO PR #123 without changes.
Use $scope-pull to compare PROJECT's evidenced progress with its agreed scope using the sources I provide.
```

These examples are invocation patterns, not task authorizations. For an agent without a skill selector, name the skill in ordinary language and provide its complete files. Do not execute the integration example against an invented destination.

## Included resources

- Lifecycle: [detailed rules](skills/governed-task-lifecycle/references/detailed-rules.md), [chat-summary reference](skills/governed-task-lifecycle/references/chat-summary.md), [optional task record](skills/governed-task-lifecycle/assets/task-record.md), and agent metadata.
- Verification: [Git custody reference](skills/verify-exact-candidate/references/git-custody.md), [optional verification record](skills/verify-exact-candidate/assets/verification-record.md), [fictional examples and evaluation cases](skills/verify-exact-candidate/references/check-cases.md), and agent metadata.
- Integration: [optional integration receipt](skills/integrate-approved-pr/assets/integration-receipt.md) and agent metadata.
- Scope Pull: [workflow](skills/scope-pull/SKILL.md), [fictional examples and evaluation cases](skills/scope-pull/references/check-cases.md), and [agent metadata](skills/scope-pull/agents/openai.yaml).

The metadata permits implicit invocation; actual discovery remains host-dependent. Resource completeness and source identity do not prove the agent will enforce a workflow.

The [optional maintainer evaluation guide](EVALUATING.md) distinguishes case specifications, structural checks and observed behavior. The [optional local checker](skills/verify-exact-candidate/references/local-checker.md) and [bounded executed comparison](evaluations/2026-10-07/README.md) have separate authority and coverage limits. The published and revised instructions tied; no behavioral gain is claimed.

## New package resources and use

Offline Usage Reporter is now an [example](examples/README.md), not an installed skill. It contains [SKILL.md](examples/offline-usage-reporter/SKILL.md), [receipt-contract.md](examples/offline-usage-reporter/references/receipt-contract.md), [report.cjs](examples/offline-usage-reporter/scripts/report.cjs), [gate.cjs](examples/offline-usage-reporter/scripts/gate.cjs), fictional fixtures and `node:test` checks. Batcher contains only its [SKILL.md](skills/node-workflow-batcher/SKILL.md). Keep these complete; neither package includes an installer or a runtime provider.

When a host actually exposes the names, use $node-workflow-batcher with your authorized inputs. Otherwise supply the complete folder and explicitly name its SKILL.md. See the [README examples](README.md). New-name discovery, plugin/mobile access and execution remain unverified; prior bounded trials do not establish universal savings.

Lean History Reporting contains only [SKILL.md](skills/lean-history-reporting/SKILL.md). Version 1.1.0 is host-neutral: use any outputs-omitted or summary view the history reader offers (such as an includeOutputs flag), otherwise read messages first; preserve the required evidence boundary. Its packaged scope is task-history reporting/diagnosis, not plugin removal, general tool pruning or an independent audit engine. Prior method percentages must not be added or attributed to this package.

The 1.5.0 candidate also selects Offline Usage Reporter 1.0.2: output creation is exclusive, so existing reports and same-file aliases are refused without truncation. Reporter 1.1.0 moves the package to `examples/`, adds STOP-LATCHED to the stdout line, rounds displayed percentages, rejects a flag given in place of a value, and adds fixtures and tests. This corrected successor is distinct from the observed published 1.0.1 baseline and has no renewed token-saving claim.
