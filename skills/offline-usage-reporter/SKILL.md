---
name: offline-usage-reporter
description: Produce consolidated reports from O2 offline replay receipts; excludes live monitoring.
---

For supplied O2 receipts, run once from this skill directory:

`node scripts/report.cjs --receipt <input.json> --out <new-report.md>`

The helper creates the output directory and hashes the report. Use its returned hash; do not add directory setup or another hash check unless independent verification is requested. Return exact stdout and the tool exit status. HOLD still requires review when exit is zero. Failure or truncation means INVALID; never retry unchanged. Preserve receipts; avoid loading or rewriting full reports except for requested review or diagnosis.

For unfamiliar inputs, read [the contract](references/receipt-contract.md). Unsupported schemas require review. The helper preserves evidence, gates, unknowns and STOP latches. Reset alone grants no restart authority.

Offline simulation only: no polling, schedules, worker messages, live stopping, adoption or savings claims.
