---
name: integrate-approved-pr
description: Use this skill when asked to check whether a pull request can merge, or to mark ready or merge a PR the owner explicitly approved. Bind checks to the exact approved head and verify the result. Do not treat a review pass or design approval as permission to merge.
---

# Integrate approved PR

## When to use

**Use this skill when** the request is to inspect a pull request's integration prerequisites, mark it ready under exact approval, or perform and verify an explicitly approved protected merge.

**Skip it** for a general code review. Never infer merge permission from a review pass, a source or design approval, or a generic request to review a PR. Without integration approval, stay read-only.

## Steps

1. **Bind the approval.** Find the owner's actual instruction. Record the PR, the exact approved head SHA and which effects it covers: inspect only, mark ready, merge, or more. If approval is missing or ambiguous, inspect read-only, prepare the decision, and ask only for what is missing. If it already covers readiness and merge, do not ask again.
2. **Check your access read-only.** Confirm which tools and permissions you actually have, without a test write.
3. **Preflight just before each action.** Re-read the PR's base, head SHA, draft state, changed files, required reviews and checks, and bind the check results to that head. Check automatic effects, such as CI runs, deployments and branch deletion on merge, against what was approved.
4. **Mark ready** if that is included, then confirm the PR actually left draft.
5. **Merge** if that is included: refresh the head, base and required conditions, then merge with the permitted method and an expected-head guard (for example the `sha` parameter of GitHub's merge API).
6. **Verify the result:** merged state, the integration commit, the resulting files, and history of the right shape for the method (merge commit, squash or rebase).
7. **Close out:** report the approved and integrated identities and, for each effect, whether it is verified complete, failed, outcome unknown, held or not attempted.

**Stop and report** if the head changed since approval (hold), the base changed (re-evaluate first), required checks or protection rules can't be seen (a gap, not proof they're off), an automatic effect would exceed the grant, a call times out (the outcome is unknown, so read the state before any retry), or access is denied (do not bypass it).

**Example:** the owner says "squash-merge PR #12 at `abc123`". Preflight shows head `abc123`, not draft, required checks passing on `abc123`, and branch deletion on merge off. Merge with method squash and `sha=abc123`. Then confirm the PR is merged and the squash commit on main changes exactly the PR's files. If preflight had shown head `def456`, hold and ask instead.

The sections below give the detailed rules for each step. Complete only the PR effects the authorized owner actually granted, following the destination's integration rules. This skill is self-contained: it needs no other skill, approval ritual or particular provider. Owner, repository, PR, base, head, method, writer and limits are current inputs.

## Bind the approved operation

Resolve the repository and sole intended PR, actual owner instruction, exact approved head/candidate, validated basis and disclosed effect envelope. Distinguish substantive approval, required assurance acceptance, readiness and merge. One explicit decision may combine these; a local design approval, candidate-written approval flag or review PASS cannot substitute for it.

Recognize unchanged, unexpired and unrevoked authority. If it already includes readiness and merge, complete both after current checks without asking for the same approval again. Reuse an existing decision record by reference instead of manufacturing another assent. If approval is absent or ambiguous, inspect and prepare the concrete reviewable decision interface within authority, then ask only for the missing decision. Do not perform the ungranted mutation.

Resolve the accountable writer and any concurrent work. Do not infer capability from account labels, an old tool inventory or the existence of an API. Inspect supported tools and the usable permission/readback path without an unauthorized write probe. If needed, use a suitable authorized alternative only when it preserves the required safeguards and payload fidelity.

## Preflight immediately before each included mutation

Read current repository/PR identity, base/head, draft/state, actual change set and required rules, reviews and checks. Bind check results to the required evaluated revision. Verify accepted bytes, paths and modes at the remote destination when exact transfer is a prerequisite; compare the expected tree or baseline remainder when that claim requires it. Local hashes and prospective merge objects do not establish stored remote state.

Missing protection details or required-check evidence is a visibility/prerequisite gap, not evidence that rules are disabled. If no check is required under the actual applicable rules, report that fact without claiming CI passed. Do not dispatch hosted jobs, incur spending or change settings merely to clear a gate unless those effects are expressly in scope.

Where the current assignment excludes or bounds automatic effects, inspect the relevant current triggers and default effects before readiness or merge, including automatic CI or deployment, resulting spending and branch deletion on merge. Reconcile those effects with the exact grant and limits. Hold a mutation that would cause an excluded effect or could exceed a bound; missing material configuration evidence is a prerequisite gap. Do not infer permission from readiness/merge approval or silently change settings, disable triggers, skip safeguards or choose another route to avoid the conflict. Treat normal CI according to destination rules and the current grant.

A changed head holds integration against the old exact approval. A changed base requires reevaluating the affected compatibility, validation and approval basis; an expected-head guard does not lock it. Preserve unaffected evidence and return only affected work for the required review/decision. Do not silently extend approval to a materially changed target.

## Execute and verify

Record the intended operation and exact guards before issuing it. Use the destination's supported protected PR path and permitted merge method. Preserve required rules; do not infer bypass, force push, direct main writes, auto-merge, branch deletion, cleanup or rollback authority.

Perform only the included steps in dependency order. If readiness is included, verify the actual draft-to-ready transition. Refresh head/base and required conditions again before merge. Use a supported expected-head safeguard and any destination-required base safeguard. If the available mechanism cannot supply a mandatory guarantee, hold that action and report the exact gap.

After merge, verify the actual PR state and integration commit, resulting tree/files/modes, relevant refs and method-appropriate topology. Merge-commit parents, squash or rebase lineage have different shapes; compare with the accepted method. Confirm the accepted change and absence of unintended differences at the granularity required by the envelope. If main has advanced further, establish the integration commit's actual reachability and relevant resulting changes rather than assuming main must still equal it.

Keep approval, readiness, merge and post-action verification as separate results. A merge response alone is not verified integration. Deployment, release, publication, migration, activation, access/spending changes and other operations have their own explicitly named scope and checks, even when the same approval includes them. Complete any such included handoff through its authorized executor; do not treat merge as operational release or omit a remaining included effect from closeout.

## Reconcile failures and close out

Preserve the attempt, request identity, result and any completed effects. A timeout or missing acknowledgement is outcome unknown. Inspect actual PR/ref/object state read-only before retrying; if the effect already completed, verify and continue rather than repeat it. Retry only after reconciliation establishes it is appropriate and within the actual remaining grant and limits. Do not escalate or bypass a denial merely to force completion; report the exact limitation and seek only a genuinely necessary new authority or capability decision. Do not inherit retries from an earlier task or reset allowances on handover.

Hold dependent actions on failure or uncertainty while continuing independent authorized work where safe. Report provider/evidence problems separately from missing approval; do not request an unchanged grant again to solve a tool problem.

Complete only the required evidence/status/handoff updates under their assigned writer authority, then release ownership. Use the optional [integration receipt](assets/integration-receipt.md) when no destination format already covers these facts. Return exact approved and integrated identities, verified effects, failed/unknown/held steps, limits and remaining actions. Keep history intact and do not start a successor target.
