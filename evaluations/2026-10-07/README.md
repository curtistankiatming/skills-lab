# Bounded instruction comparison and helper checks

The published and revised instructions tied in this trial. It supports retaining the clearer instructions and investigating the optional deterministic helper, but **does not establish a behavioral improvement over the published baseline**.

| Supplied condition | Requirements met | Held-out requirements met |
| --- | --- | --- |
| No skill file (A) | 39/40 | 8/8 |
| Published baseline (B) | 40/40 | 8/8 |
| Instruction revision (C) | 40/40 | 8/8 |

Twenty fictional cases ran once in each fresh delegated context, sixty answers total. A fixed rubric was written before answers. A separate fresh scorer assessed answers under permuted labels without the condition mapping; its read set included the raw cases and rubric. The no-skill answer correctly identified the absent approved reference in V3 but omitted an explicit request for a trusted reference. That is a next-action omission, not false approval. Separately scored unsupported positives, missed material findings, unnecessary holds, invalid/missing citations and unauthorized actions were all zero in these answer records.

Inspect the [raw fictional inputs](cases.json), [prewritten rubric](rubric.json), [actual answer text](answers.json) and [scores, source hashes and coverage](results.json). Record IDs in answers cite supplied fictional records; their authenticity/observations are stipulated facts, not independently verified real project evidence. Agent paths and host transcripts are deliberately excluded from this public selection.

The revised skill's casebooks exposed the 16 seed expectations. Four additional cases were held out from those casebooks, but all conditions passed them. This single ceiling-limited batch has no statistical or causal reliability claim. Default model settings were inherited; the effective backend/settings were not independently attested. Fresh task context and declared read boundaries did not establish technical host isolation. No skill file was supplied to A, but catalog/system context and tools remained available. Results apply to the exact hashed instruction snapshots; the optional helper and subsequent integration paragraph were added later.

The helper fixture suite separately ran on Windows Python 3.12: 23 passed and 3 actual link-creation fixtures skipped under existing host permissions. Injected admission/denial/change tests are labeled in results. WSL inventory access was denied, so Linux/WSL, actual Cloud Files and concurrent mutation qualification are not claimed. The first attempt's fixture setup error is retained as an attempt limitation. An independent source-only reviewer found resource, startup and stdout issues that were corrected; this is source review plus author fixture execution, not independent runtime certification.

Public-facing limits: the helper's conservative filename/type policy may reject legitimate projects; Windows read-only sharing can obstruct writers briefly; filesystem/provider side effects and blocking I/O are outside its control. It is optional and has no repair, installation or candidate-code-execution path under its documented trusted isolated launch. Before/after observations are not an atomic snapshot. See the [helper usage and limits](../../skills/verify-exact-candidate/references/local-checker.md).

This record grants no integration, release, installation, adoption or operational permission. Case specifications remain useful examples; executed results do not turn them into universal host compatibility or model-performance evidence.
