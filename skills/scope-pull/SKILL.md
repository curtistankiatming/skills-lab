---
name: scope-pull
description: Use this skill if asked to pull project scope, compare progress with agreed commitments, reconcile scope changes, or assess proposed expansion, including non-software projects. Report source-backed scope, evidenced progress, gaps and proposed next work; reconciliation does not approve or dispatch work.
---

# Scope Pull

## When to use and invoke

**Use this skill if** the user wants a project's scope pulled together, delivery compared with commitments, scope changes reconciled, or proposed additions assessed.

**Agent invocation:** select the matching entry from the available skill catalog, read this `SKILL.md` using its supplied path, and follow the workflow below with the available project evidence and current authority.

**Portable explicit invocation:** "Use the Scope Pull skill to reconcile [project]'s agreed scope, progress and proposed next work from [sources] through [cutoff]."

**Codex selector example:** `Use $scope-pull to compare [project]'s progress with its agreed scope and assess the proposed next work.`

In ChatGPT, select Scope Pull with `@` where the host offers it, or use the plain-language instruction above. Use the installed name or namespace supplied by the host. A `$skill-name` mention is a Codex selector, not an API tool or a guarantee of host support or execution. With another agent, supply this file through its skill loader or supported context mechanism. Selecting the skill adds no authority.

Give the user a concise, source-backed account of where a project stands against its scope, what changed during the lifecycle covered by the evidence, and what is proposed next. Use the project's own terms and completion criteria.

## Establish the basis

Identify the project, requested time horizon and relevant authoritative sources from the supplied context and accessible project records. If different plausible projects or baselines would materially change the answer, ask one focused clarification; continue any useful reconciliation that does not depend on it.

Start with the governing scope or brief, recorded decisions and changes, and current delivery/status evidence. Follow relevant references only as needed to explain material changes or close a consequential gap. Prefer a bounded history trace over an exhaustive archive scan. State which baseline and period you could establish; incomplete history is not full lifecycle coverage.

Apply the project's actual source hierarchy. A newer status summary does not automatically override an approved decision. When no formal hierarchy exists, distinguish agreed commitments, working plans, reported progress and observed results using their provenance rather than inventing approval rules.

## Reconcile commitments with evidence

Map the main deliverables, outcomes and boundaries to evidence of progress. Distinguish:

- The original agreed baseline, current agreed scope, and approved or agreed changes between them.
- Work evidenced as completed under the project's completion criteria, with its relevant limitations.
- Work in progress, outstanding, blocked, or unverifiable; preserve the difference between lack of evidence and evidence of noncompletion.
- Scope changed, deferred, removed or superseded, without counting it as delivered.
- Upcoming work already committed versus proposed additions, alternatives or replacements that are still undecided.

Keep claims, decisions, implementation, validation, acceptance and observed outcomes separate wherever those distinctions matter. Do not infer one from another, count overlapping work twice, or equate a task's completion with achievement of the project's outcome.

Resolve apparent differences against the controlling sources where possible. Otherwise identify the specific missing, stale or conflicting evidence, its effect on the affected conclusion, and the smallest useful clarification or record to consult. Continue supported conclusions instead of making the entire report contingent on unrelated gaps.

## Report and advise

Default to a report in the invoking chat. Lead with current state and the next useful action. Use a compact table when it clarifies the comparison, for example: scope item, commitment/change, evidenced state, source/gap, proposed next step. Group related work; do not create a row for every historical event.

Link material claims to inspectable sources and distinguish project-record claims from your inference. Include relevant scope changes, unresolved gaps and separately labelled upcoming proposals. State the evidence's as-of date or cutoff and coverage limits. Give a completion percentage only when a sourced, meaningful denominator and consistent completion criteria support it; otherwise describe progress without one.

Recommend retaining, narrowing, deferring or rejecting proposed work when the evidence warrants it. Explain the benefit, relevant dependencies or feasibility constraints, and tradeoff; compare with doing less or finishing existing commitments first. Label estimates and assumptions, and do not invent savings or turn one incident into a universal process requirement.

Reading and reconciliation do not approve scope, dispatch work, implement changes or establish acceptance. External sending, saving reports or updating project records requires the user's applicable authorization. Use existing records and tools; add no dashboards, ledgers, scripts or recurring workflow merely to produce this report.
