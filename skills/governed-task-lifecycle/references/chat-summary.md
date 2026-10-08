# Owner-facing command summary

Use the same compact order for final results, including incomplete or partial work. Follow current user instructions and destination formatting. Expand only for material facts; this format adds no commands, gates, evidence files, test jobs or schemas.

```text
<Command> <exact task/revision; link when available, otherwise plain-text identifier> — <plain result>.

Scope: <work type, main implications and bounds>.
Done:
- [x] <verified completed work>.
Now:
- [ ] <actual stage and included unfinished work; reason for any hold>.
Next:
- [ ] <plain-language next action or prerequisite; put an exact user-command prompt only in Your decision>.
Checks / limits: <meaningful checks actually run; material gaps, reduced assurance, exclusions and non-claims>.
Upcoming: <separate proposed scope, not started; or None>.
Evidence: <exact candidate/PR and supporting record links when available>.
Your decision: <one genuinely needed exact command, acceptance or approval request; or None>.
```

| Command | Done / Now and genuinely needed next prompt |
| --- | --- |
| Initialize / Initiate | Report actual built, researched or designed artifacts and any unfinished work. When ready and invocation is needed, request `Validate <actual task ID>`. |
| Validate | Report checks of actual work, corrections, open findings and assurance. When ready and needed, request the exact required acceptance and/or `Approve <actual task ID>` against the exact basis. |
| Approve | Done / Now form the adaptable In Scope Checklist. Continue remaining included work under unchanged authority. When complete, Next is None; suggest `Initialize <known proposed ID>` only for a genuine upcoming target. |

Explain the work type and its main implications in Scope where required, using plain terms such as design, implementation or integration. Use `[x]` only for verified complete work; ongoing, held, unknown or future rows stay `[ ]`. If a field has no work, replace its entire checkbox list with plain None.

For Approve, label Done / Now as its In Scope Checklist and list each included owner-decision, readiness, merge, release or other meaningful effect once in the appropriate group. Unfinished effects carry IN PROGRESS / FAILED / UNKNOWN / HELD / NOT ATTEMPTED and a reason. Do not print a second duplicate checklist. Excluded/NA work is outside unfinished scope; approval or a successful call alone is not verified completion.

Explain actual stage and holds; separate approval, integration and operational results where material. Keep logs/hashes behind evidence links, but supply the full digest or command needed for exact acceptance or approval. Never abbreviate that subject or hide a blocker.

Next states the permitted action or blocker; place any needed exact user-command prompt once in the final Your decision line. If blocked, request only the smallest real prerequisite. Do not re-ask unchanged approval or require user commands for authorized internal work. Upcoming is proposed/not started, not permission or an automatic priority change; never invent its ID or treat an illustrative command as an assignment.

## Adaptation examples

These fictional examples illustrate the existing rules; they grant no actions and do not replace a destination contract.

| Situation | Appropriate result |
| --- | --- |
| Initialize permits only analysis | Produce the authorized analysis, not implementation. If the current instruction also grants implementation, complete it without seeking the same grant again. |
| A public invitation is the deliverable | Save the invitation in its audience's format. Put the lifecycle status in the separate owner reply when that workflow applies. |
| Candidate content materially changes | Complete the affected destination-required validation before its new approval request. Preserve independent authorized work and applicable evidence. |
| One approved effect times out | Read resulting state before any permitted retry. Preserve completed effects; ask no duplicate approval merely to solve a tool problem. |

For an Initialize result, Next can say “Review the completed candidate”; Your decision contains `Validate <actual target>` once, when that command is needed. For an unvalidated changed candidate, Next states the affected validation; Your decision does not imply it is already ready to approve. Use the destination's required vocabulary and fields where they differ.

Label identities by kind: a source revision locates the evaluated material; a raw file hash binds file bytes; an evidence-storage revision locates a report. None authenticates owner assent or proves an external effect completed. Use only the identities the task needs, in its existing format.
