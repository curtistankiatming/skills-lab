# Skills Lab catalog

Collection version: 1.0.1. [MIT licence](LICENSE). This catalog summarizes the three unchanged skill declarations. The [inventory](inventory.json) binds their complete files to raw hashes; the skill bodies control their detailed meaning.

| Folder | Use if | Boundary | Complete entry point |
| --- | --- | --- | --- |
| governed-task-lifecycle | The owner invokes Initialize/Initiate, Validate or Approve, or the destination requires that contract. | Do not impose a lifecycle on ordinary work. Initialize builds; author checks do not finish Validate; approval covers only its named effects. | [SKILL.md](skills/governed-task-lifecycle/SKILL.md) |
| verify-exact-candidate | Exact identity, custody or evidence must be checked against a pinned candidate or baseline. | Byte identity is not semantic acceptance, live capability, owner approval or integration authority. | [SKILL.md](skills/verify-exact-candidate/SKILL.md) |
| integrate-approved-pr | Integration prerequisites need inspection, or exact approved readiness/merge effects need completion. | A review pass or design approval supplies no merge authority. Changes and unknown outcomes require reconciliation. | [SKILL.md](skills/integrate-approved-pr/SKILL.md) |

## Explicit examples

```text
Use $governed-task-lifecycle. Initialize TASK-001: prepare the implementation described in the supplied assignment.
Use $verify-exact-candidate to verify the three named files against the supplied SHA-256 manifest. Read and hash only.
Use $integrate-approved-pr to inspect OWNER/REPO PR #123 without changes.
```

These examples are invocation patterns, not task authorizations. For an agent without a skill selector, name the skill in ordinary language and provide its complete files. Do not execute the integration example against an invented destination.

## Included resources

- Lifecycle: [chat-summary reference](skills/governed-task-lifecycle/references/chat-summary.md), [optional task record](skills/governed-task-lifecycle/assets/task-record.md), and agent metadata.
- Verification: [Git custody reference](skills/verify-exact-candidate/references/git-custody.md), [optional verification record](skills/verify-exact-candidate/assets/verification-record.md), and agent metadata.
- Integration: [optional integration receipt](skills/integrate-approved-pr/assets/integration-receipt.md) and agent metadata.

The metadata permits implicit invocation; actual discovery remains host-dependent. Resource completeness and source identity do not prove the agent will enforce a workflow.
