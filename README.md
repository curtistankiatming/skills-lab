# Skills Lab

Six portable instruction skills for governed work, exact candidate checks, approved PR integration, scope reconciliation, offline receipt reporting and local Node workflow batching. Prepared distribution snapshot, 18 October 2026: collection 1.4.0 adds Offline Usage Reporter 1.0.1 and Node Workflow Batcher 1.0.0. The four existing skill resource sets are unchanged from integrated source 1.3.0. The latest observed issued release is 1.1.0. This candidate is not published or installed; inclusion of the two new packages under MIT is proposed in [RIGHTS.md](RIGHTS.md).

The existing collection retains the [MIT License](LICENSE), copyright and notices. Source acceptance, selected distribution, host discovery, invocation and actual execution are separate states.

## Choose a skill

| Skill | Use this skill if... | Complete entry point |
| --- | --- | --- |
| Governed Task Lifecycle | Initialize, Initiate, Validate or Approve is requested, or the destination requires that lifecycle. | [governed-task-lifecycle](skills/governed-task-lifecycle/SKILL.md) |
| Verify Exact Candidate | Exact files, hashes, revisions or evidence need comparison with a pinned basis. | [verify-exact-candidate](skills/verify-exact-candidate/SKILL.md) |
| Integrate Approved PR | Integration prerequisites need inspection, or explicitly approved readiness/merge needs completion. | [integrate-approved-pr](skills/integrate-approved-pr/SKILL.md) |
| Scope Pull | Agreed scope, evidenced progress, changes or proposed expansion needs reconciliation. | [scope-pull](skills/scope-pull/SKILL.md) |
| Offline Usage Reporter | Supplied fictional O2 replay receipts need one offline report. | [offline-usage-reporter](skills/offline-usage-reporter/SKILL.md) |
| Node Workflow Batcher | Authorized local read, derive and validate phases can be grouped in a persistent Node REPL. | [node-workflow-batcher](skills/node-workflow-batcher/SKILL.md) |

The [catalog](CATALOG.md) explains examples, resources and boundaries. The [inventory](inventory.json) binds the complete selection. This collection is a selected distribution; it does not replace the maintained controller of any skill or expand an existing plugin bundle.

## Use the complete skill

Give the agent the complete selected folder and follow the host's supported loading procedure. If the host exposes an installed selector, examples are:

```text
Use $governed-task-lifecycle. Initialize TASK-001: build the authorized deliverable and stop ready for Validate.
Use $verify-exact-candidate to compare the supplied files with the pinned manifest. Read and hash only.
Use $integrate-approved-pr to inspect OWNER/REPO PR #123. Make no changes.
Use $scope-pull to reconcile agreed scope and evidenced progress from the sources I provide.
Use $offline-usage-reporter for the supplied fictional O2 receipt and named new output file. Preserve HOLD, unknowns and STOP latches.
Use $node-workflow-batcher for the authorized local job in a supported persistent Node REPL. Stop at unresolved decisions or approvals.
```

Replace example identifiers with actual authorized inputs. For manual use, say “Use Offline Usage Reporter at <skill-folder>/SKILL.md” or “Use Node Workflow Batcher at <skill-folder>/SKILL.md” and supply every resource. An example or selector grants no extra authority. New-name discovery, automatic selection, phone/plugin availability and runtime are unverified for this distribution.

Lifecycle consumers retain the [owner-facing summary](skills/governed-task-lifecycle/references/chat-summary.md) and the destination's command meanings. Keep owner status separate from an audience-facing deliverable unless requested.

## Dependencies and limits

- Offline Usage Reporter includes SKILL.md, the [receipt contract](skills/offline-usage-reporter/references/receipt-contract.md), and both Node.js helpers. It requires an available Node.js runtime and authorized fictional O2 receipts. Preserve the exact stdout and process status: HOLD may accompany exit zero, and reset grants no restart authority. It has no live schema adapter, polling, worker messaging or enforcement. It is not a hostile-input validator.
- Node Workflow Batcher is a one-file instruction skill. It needs a host-provided persistent Node REPL with the documented job/state and output facilities. A standalone Node executable is insufficient evidence of that host capability. Group only understood authorized phases, inspect every result and stop on provider denial. This package adds no REPL implementation, connector or permission.
- Verify Exact Candidate retains its optional Python standard-library checker and fixture suite. Execution needs a trusted interpreter and task authority. No additional software is needed to read Markdown. PyYAML is not a runtime dependency of either new skill.

The four existing agent metadata files retain their declarations. The two new packages add no agent metadata, installer, hooks, server, credentials or hosted workflow. Instructions and exact files do not establish backend identity, runtime enforcement, independent assurance or destination adoption.

## Evidence and maintenance

Earlier trials remain evidence for their exact tested workloads and source bytes. Predecessor Reporter token results do not certify successor savings; Batcher's earlier tested-name results do not establish new-name loading or universal gains. No new performance or effectiveness claim is made for the combined package.

The unchanged [evaluation guide](EVALUATING.md), [executed fictional comparison](evaluations/2026-10-07/README.md) and [local checker reference](skills/verify-exact-candidate/references/local-checker.md) retain their original scopes and coverage gaps. Published and revised Verify/Scope instructions tied in that comparison. They do not evaluate these two additions or prove Lifecycle behavior.

See [maintenance](CONTRIBUTING.md), [release preparation](RELEASING.md), [rights](RIGHTS.md) and [repository instructions](AGENTS.md). Possession or publication supplies no merge, deployment, spending, live-operation or other-project authority.
