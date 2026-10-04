# Git custody for an exact candidate

Read this reference when the claim concerns Git source identity, a prepared transfer or remote publication. Use authorized inspection tools; these are evidence criteria, not commands granting a write.

Select the checks needed for the actual claim. A local three-file hash comparison does not require proving an entire remote repository, while an exact transfer or protected integration claim needs its complete relevant topology and change boundary.

| Property | Evidence that supports it | Limit |
| --- | --- | --- |
| Evaluated source | Repository identity, base and exact evaluated commit or pinned file set | A receipt's storage commit may be different |
| Exact files | Raw bytes, lengths, digests; destination paths, blob identities and modes where material | Rendered text, a PR body or local hash alone cannot prove remote bytes |
| Commit topology | Actual stored commit, tree and parent list | An API success or prospective merge SHA does not prove the object exists |
| Intended delta | Actual base-to-head changed set, additions/deletions/renames/modes and no unintended changes | A changed-file subset cannot prove an entire delta |
| Complete transfer | Expected tree composed from the accepted baseline and allowed changes, compared with the actual destination tree | Matching changed blobs alone does not establish unchanged remainder |
| PR binding | Actual repository, base/head branches and SHAs, draft/state and delta | An expected-head guard does not lock base or prevent later drift |
| Freshness | Query/source and observation time, then recheck relevant refs before consequential use | A captured result is historical after relevant state changes |

For exact transfer, reconcile local raw-byte SHA-256 values with destination objects and the expected tree; Git blob identities include Git framing and are not interchangeable with raw-byte digests. Include deletions and mode changes in the expected result. Check parent topology against the authorized method rather than universally requiring one parent.

Do not change Git configuration or take a new execution route merely to bypass a blocked read. Report the exact missing capability or source. If the candidate, base or relevant rules change, identify the affected evidence and hold dependent use for the required reevaluation. Retain prior observations and distinguish them from current facts.
