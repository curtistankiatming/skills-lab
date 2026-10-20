---
name: offline-usage-reporter
description: Example skill. Use it only to turn a supplied O2 replay receipt (a fictional usage-monitor test format) into one offline Markdown report. Do not use it for live usage monitoring, real accounts or restarting work.
---

This is a worked example of a skill that wraps a deterministic helper. It is kept under `examples/` and is not meant to be installed as a working skill. "O2" is the fictional usage-monitor replay format described in [the contract](references/receipt-contract.md).

## Steps

1. Check that Node.js is available and that you were given a receipt file and a new output path.
2. From this folder, run once: `node scripts/report.cjs --receipt <input.json> --out <new-report.md>`
3. Read the single stdout line. It starts with `MATCHED` or `HOLD`, followed by `STOP-LATCHED` when any worker's stop is latched, then the report path and its SHA-256.
4. Return that exact line and the exit status. Use the returned hash; do not re-hash or reload the report unless asked to review it.

## Stop and report

- `HOLD` means the receipt needs review, even though the exit status is 0.
- `STOP-LATCHED` means work must stop at a safe checkpoint. A later reset does not clear it; only the owner can authorize a restart.
- A non-zero exit or truncated output means the run is INVALID. Do not retry unchanged. The helper never overwrites an existing file, so choose a new output path only after resolving the failure.
- An unfamiliar receipt shape needs review. Read the contract before guessing.

## Limits

Offline simulation only: no polling, schedules, worker messages, live stopping or savings claims. The fixtures in `tests/fixtures/` show the supported shape; run the checks with `node --test tests/report.test.cjs`.
