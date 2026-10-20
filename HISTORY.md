# Skills Lab history

This file keeps the distribution notes that earlier README, CATALOG, RELEASING and inventory.json versions carried, so the current files can describe the current collection. The text below is copied from those files as they stood at commit 4e12d40, before version 2.0.0. It describes each snapshot as it was then; statements such as "not yet published" are historical, not current. Links are relative to the repository root.

## 2.0.0 (2026-10-20)

- Every skill was revised for use on any host: plain "Use this skill when … Do not use it for …" descriptions, numbered steps, stop rules and a short example in each `SKILL.md`, and host-specific text removed from skill bodies.
- Verify Exact Candidate 1.3.0: the checker no longer keeps every file open on Linux (a 1,500-file package used to fail under a 1,024 open-file limit), common error codes get a hint, `ctypes` is imported only by the Windows adapter, and the tests moved to `tests/verify-exact-candidate/`.
- Governed Task Lifecycle 1.1.0: `SKILL.md` is a step-by-step checklist; the detailed rules moved to `references/detailed-rules.md`.
- Integrate Approved PR 1.1.0: a seven-step checklist.
- Scope Pull 1.2.0, Lean History Reporting 1.1.0 and Node Workflow Batcher 1.1.0: plainer triggers, and Lean History Reporting and Node Workflow Batcher no longer depend on one host's tools.
- Offline Usage Reporter 1.1.0 moved to `examples/` and is no longer part of the installed set. That removal is why the collection version moved to 2.0.0.
- Harder evaluation cases (`evaluations/harder-cases/`): 12 cases covering all six skills, 25 skill-selection tests and a standard-library runner for OpenAI-compatible endpoints, so local models can be tested. They had not been run on a model at release.
- Published as the GitHub release v2.0.0. The previous release was v1.1.0.

## Earlier README introduction (1.5.0 snapshot, 18 October 2026)

Six portable instruction skills for governed work, exact candidate checks, approved PR integration, scope reconciliation, task-history reporting and local Node workflow batching, plus one [example](examples/README.md) skill for offline receipt reporting. Prepared distribution snapshot, 18 October 2026: collection 1.5.0 proposes Lean History Reporting 1.0.0 and the Offline Usage Reporter 1.0.2 output-preservation correction. Offline Usage Reporter 1.0.1 and Node Workflow Batcher 1.0.0 are already published in integrated source 1.4.0. The four existing skill resource sets are unchanged from integrated source 1.3.0. The latest observed issued release is 1.1.0. This new candidate is not yet published or installed. Earlier preparation labels in distribution history describe their original snapshots; the two existing additions were published under the recorded 1.4.0 delivery. New installation is outside this task. See [RIGHTS.md](RIGHTS.md).

## Earlier README sections

### Evidence and maintenance

Earlier trials remain evidence for their exact tested workloads and source bytes. Predecessor Reporter token results do not certify successor savings; Batcher's earlier tested-name results do not establish new-name loading or universal gains. No new performance or effectiveness claim is made for the combined package.

The unchanged [evaluation guide](EVALUATING.md), [executed fictional comparison](evaluations/2026-10-07/README.md) and [local checker reference](skills/verify-exact-candidate/references/local-checker.md) retain their original scopes and coverage gaps. Published and revised Verify/Scope instructions tied in that comparison. They do not evaluate these two additions or prove Lifecycle behavior.

See [maintenance](CONTRIBUTING.md), [release preparation](RELEASING.md), [rights](RIGHTS.md) and [repository instructions](AGENTS.md). Possession or publication supplies no merge, deployment, spending, live-operation or other-project authority.

### Lean History Reporting

This one-file skill defaults to compact task-history retrieval, attributes reported counts and preserves identity, revision, owner, uncertainty, applicable stops, authority and next action. Obtain detailed evidence for missing requested facts, contradictions, requested diagnostics or independent verification; omitted output never proves success. Retrieved history grants no new authority.

It requires authorized history access but no particular tool: it uses an outputs-omitted or summary view when the host offers one (for example Codex's `includeOutputs=false`) and otherwise reads messages first and skips long output blocks. If the needed output is unavailable, it reports the gap. Intended invocation, if the host exposes it: Use $lean-history-reporting for the named task's status or diagnostic request. Otherwise supply the complete SKILL.md. Host discovery and this new name's runtime are unverified. The package adds no history connector or plugin.

The earlier O1 method and tiny packaging comparison cover different bounded workloads. They do not establish a large general saving, universal effectiveness, money or account allowance; no saving is claimed for publication. See [catalogue boundaries](CATALOG.md).

Reporter 1.0.2 changes output creation to refuse an existing destination, including an existing same-file alias. It preserves the receipt and old reports instead of truncating them. Its entrypoint and gate remain unchanged, and focused fictional file-preservation checks cover the corrected helper; earlier native-token comparisons do not certify this successor's savings. Published 1.0.1 remains the observed baseline until this candidate completes protected delivery.

## Earlier CATALOG notes (1.5.0 snapshot)

Prepared distribution snapshot, 18 October 2026: collection 1.5.0 proposes Lean History Reporting 1.0.0 with five unchanged existing skill resource sets from integrated source 1.4.0 and the focused Reporter 1.0.2 correction. Reporter 1.0.1 and Batcher 1.0.0 are already published; this new source candidate does not establish installation, discovery or universal effectiveness. See [rights](RIGHTS.md) and the final [inventory](inventory.json).

Lean History Reporting contains only [SKILL.md](skills/lean-history-reporting/SKILL.md). Version 1.1.0 is host-neutral: use any outputs-omitted or summary view the history reader offers (such as an includeOutputs flag), otherwise read messages first; preserve the required evidence boundary. Its packaged scope is task-history reporting/diagnosis, not plugin removal, general tool pruning or an independent audit engine. Prior method percentages must not be added or attributed to this package.

The 1.5.0 candidate also selects Offline Usage Reporter 1.0.2: output creation is exclusive, so existing reports and same-file aliases are refused without truncation. Reporter 1.1.0 moves the package to `examples/`, adds STOP-LATCHED to the stdout line, rounds displayed percentages, rejects a flag given in place of a value, and adds fixtures and tests. This corrected successor is distinct from the observed published 1.0.1 baseline and has no renewed token-saving claim.

## Earlier RELEASING notes (1.5.0 snapshot)

Prepared distribution snapshot, 18 October 2026: proposed collection 1.5.0 contains 39 files. It adds Lean History Reporting 1.0.0 as one complete instruction file; Offline Usage Reporter 1.0.2 supplies the focused output-preservation correction to the published 1.0.1 baseline. Node Workflow Batcher 1.0.0 remains unchanged from its already-published 1.4.0 selection. Four existing skill resource sets remain unchanged from integrated source 1.3.0. The latest observed issued release remains 1.1.0. Source, tag/release, local discovery and runtime states are separate. New MIT inclusion, protected integration, publication and installation are not authorized by this preparation.

For these additions, the eventual exact decision must include permission to distribute their five selected resource bytes under MIT and the named repository effects. A reviewable archive includes one root, all 39 files and the unchanged full LICENSE. Its raw SHA-256 is recorded outside the archive, alongside the inventory digest. A local archive is not a tag, uploaded asset, plugin package or installation. Freshly reconcile refs, version/tag collisions and controls before any later authorized writes; a failed tags listing is no evidence of tag absence. Do not install or execute candidate helpers to check packaging.

The current O1–O3 review prepares source publication only. Tags, releases, uploaded assets, installations and plugin effects remain excluded. The new O1 resource stays exact to its selected source; do not transfer method or predecessor comparison savings into a claim for this collection. Reuse current O2/O3 resources rather than duplicate their historical handovers.

## Earlier inventory.json records

These top-level fields were removed from `inventory.json` in 2.0.0. They are reproduced exactly.

```json
{
  "record_semantics": "Prepared snapshot dated 2026-10-18. Existing 1.4.0 source inclusion of Reporter/Batcher was verified at the observed base; older preparation fields retain history. This new candidate is not integration, installation or runtime proof.",
  "maintenance_snapshot_history": [
    {
      "client_date": "2026-10-08",
      "captured_utc": "2026-10-08 04:43:23 UTC",
      "state": "DRAFT_CANDIDATE_RECORD_UPKEEP_NOT_RELEASED",
      "observed_public_branch_basis": "7ca5cc0ad913d600990f08e63662ffc665cb8eda",
      "observed_public_main": "9f3ac78f1a091fee177a2dcbce3038d8b8a03c73",
      "last_observed_release": {
        "tag": "v1.1.0",
        "target": "9f3ac78f1a091fee177a2dcbce3038d8b8a03c73"
      },
      "source_alignment": "All four selected resource sets have matching source/distribution Git blobs and 100644 modes at the captured bases; restricted controller locators and records are withheld.",
      "evaluation_record": "evaluations/2026-10-07/README.md",
      "paired_evidence": [
        {
          "path": "cases.json",
          "bytes": 13409,
          "sha256": "2428f08c818cd44512baf057f58188c2253a50d9ab895b43745afdd7be51f8e0"
        },
        {
          "path": "rubric.json",
          "bytes": 3372,
          "sha256": "f860f1ac83b05e47bf9cac9c51ba91ad9ed9198ea2fd049edfc10f3bf3bfdd5b"
        },
        {
          "path": "answers.json",
          "bytes": 33587,
          "sha256": "68ef268033e4a3435c9dbaf351770a08046d2228d8a428ac794b7bc96ed35548"
        },
        {
          "path": "results.json",
          "bytes": 11333,
          "sha256": "72d67ea53db1e3481bbfcfdf4d919c29d7e6132e00c7b7d94718d5602883cff0"
        }
      ],
      "behavioral_improvement_established": false,
      "record_limits": "This snapshot predates its containing upkeep commit. It is not current approval, integration, installed state or qualification. Final delivery identities are recorded outside this inventory."
    }
  ],
  "reconciliation": {
    "date": "2026-10-08",
    "state": "PREPARED_DRAFT_REVIEW_CANDIDATE",
    "public_input_heads": [
      "0e183ba54421c1046f8d7a40eaa5b2bde8aea77c",
      "535336f10b4c4aab55eca4322d5f09f9272f4ebe"
    ],
    "public_base": "9f3ac78f1a091fee177a2dcbce3038d8b8a03c73",
    "branch": "codex/improve-governed-task-lifecycle",
    "source_alignment": "All four complete selected resource sets match their controlling prepared source bytes and modes. Restricted source locators are withheld.",
    "evaluation_scope": "evaluations/2026-10-07 covers the historical fictional Verify/Scope comparison. No Lifecycle behavioral comparison is included here; no gain is established.",
    "history": "Earlier metadata snapshots retain their evaluated revision meaning. Current files/skills inventories bind the reconciled selection; final remote delivery identities are recorded externally."
  },
  "combined_preparation": {
    "date": "2026-10-18",
    "collection_version": "1.4.0",
    "state": "LOCAL_CANDIDATE_ONLY",
    "integrated_base": "75226ac38f2b4875db7a65cb84881d39020227e4",
    "integrated_source_version": "1.3.0",
    "last_observed_issued_release": "1.1.0",
    "new_resource_count": 5,
    "existing_resource_sets_unchanged": 4,
    "rights": "Two new MIT inclusions proposed; existing terms/notices retained",
    "runtime": "No new tests, model trials, discovery, installation or plugin execution",
    "tag_absence_established": false
  },
  "o1_o3_review": {
    "date": "2026-10-18",
    "source_version": "1.5.0",
    "base": "bd6230d3cea0c9efe8db870079ab4ac9c4170985",
    "additions": [
      "lean-history-reporting"
    ],
    "unchanged_existing_skills": 5,
    "existing_O2_O3_publication": "VERIFIED_AT_BASE",
    "current_effect_scope": "Source publication through protected PRs only; no new installation, runtime activation, benchmark, release or plugin",
    "new_behavioral_tests": 0,
    "source_correction": {
      "skill": "offline-usage-reporter",
      "version": "1.0.2",
      "scope": "Exclusive output creation and contract clarification; original gate and entrypoint unchanged",
      "native_performance": "UNVERIFIED_FOR_SUCCESSOR"
    },
    "corrected_existing_skills": 1,
    "candidate": "C4"
  }
}
```
