# Skills Lab

Four portable instruction skills for preparing governed work, checking exact candidates, handling explicitly approved pull request integration and reconciling project scope. Collection version: 1.3.0. Verify Exact Candidate selects source version 1.2.0 and Scope Pull 1.1.0; Governed Task Lifecycle and Integrate Approved PR remain at 1.0.1.

The collection is provided under the [MIT License](LICENSE). See [rights and attribution](RIGHTS.md) for the selected components and preserved notices.

## Choose a skill

| Skill | Use this skill if... | Start here |
| --- | --- | --- |
| Governed Task Lifecycle | Initialize, Initiate, Validate or Approve is requested, or the destination requires that lifecycle. | [governed-task-lifecycle](skills/governed-task-lifecycle/SKILL.md) |
| Verify Exact Candidate | A handoff or check must establish exact files, hashes, revisions or evidence against a pinned basis. | [verify-exact-candidate](skills/verify-exact-candidate/SKILL.md) |
| Integrate Approved PR | You need integration prerequisites checked, or already-approved readiness or protected merge completed. | [integrate-approved-pr](skills/integrate-approved-pr/SKILL.md) |
| Scope Pull | You want agreed scope, evidenced progress, changes and proposed expansion reconciled, including non-software projects. | [scope-pull](skills/scope-pull/SKILL.md) |

The [catalog](CATALOG.md) explains the boundaries and examples. The [optional evaluation guide](EVALUATING.md) and fictional casebooks support maintainers assessing revisions; their inclusion is not evidence of executed tests. The [inventory](inventory.json) records version, source relationships, file sizes and raw SHA-256 values.

## Use the complete skill

Give your agent access to the selected SKILL.md and the resources it calls for. Keep each skill folder complete, including its references, assets and agent metadata. Follow your host's documented skill-loading procedure; this repository does not install or activate anything.

If the host exposes these installed names, explicit examples are:

```text
Use $governed-task-lifecycle. Initialize TASK-001: build the deliverable within the supplied scope and stop ready for Validate.
Use $verify-exact-candidate to compare the named candidate files with the pinned manifest and report mismatches or missing evidence.
Use $integrate-approved-pr to inspect integration prerequisites for OWNER/REPO PR #123. Make no changes.
Use $scope-pull to reconcile the project's agreed scope, evidenced progress and proposed next work from the sources I identify.
```

Replace task identifiers and example destinations with your actual inputs. In another host, request the same skill in plain language and supply its files. Use the installed name or namespace the host actually exposes. Selecting a skill grants no additional permission.

For the lifecycle skill, preserve its [owner-facing chat summary](skills/governed-task-lifecycle/references/chat-summary.md), including Scope, Done, Now, Next, Checks / limits, Upcoming, Evidence and Your decision.

## What to expect

The instruction files and templates include an optional local stdlib checker and its fixture suite for Verify Exact Candidate. They need a trusted Python interpreter and explicit task authority to execute. The package has no credentials, server, installer, dependency environment or hosted workflow. An agent needs separately available tools and current authority for real file or GitHub operations. No extra software is needed simply to read the Markdown.

The four agent metadata files enable implicit invocation as a declaration. Automatic selection, effective model configuration, runtime enforcement and compatibility with every host have not been established by this package. Templates are blank formats, not evidence of completed work. Scope Pull reports and advises; it does not approve scope or dispatch work.

Publication or possession does not establish destination adoption, portfolio admission, independent assurance or permission to merge, spend, deploy or publish. Follow the current task and destination instructions.

## Maintain or release

See [contributing and maintenance](CONTRIBUTING.md), [release preparation](RELEASING.md) and [repository instructions](AGENTS.md). Keep one controlling source for each skill identity; the collection is a selected distribution, not an automatic replacement for its source.

See the [optional local checker](skills/verify-exact-candidate/references/local-checker.md) and the [executed bounded comparison](evaluations/2026-10-07/README.md). Published and revised instructions tied in this trial; no behavioral improvement is established. The helper was separately tested on Windows with explicit coverage gaps.
