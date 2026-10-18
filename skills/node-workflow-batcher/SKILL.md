---
name: node-workflow-batcher
description: Group local read, derive and validate work in a persistent Node REPL while keeping job and revision state explicit.
---

Before calling Node, identify any approval or decision that requires external inspection. If none must intervene, perform the authorized read, derive and validate phases in one Node call, awaiting dependencies in order. Check routine phase outcomes inside that call; returning a phase result is not itself a reason for another call. Use `Promise.allSettled` for independent reads and inspect every result.

Before each dependent phase, check the preceding result against its documented schema and inspect every item for unexpected errors. Implement these checks in the call; serializing results alone is not inspection. Handle documented partial outcomes explicitly. Do not guess field locations. If the schema is unknown, inspect it first and group only the remaining understood phases.

Split at an approval, unresolved decision or provider limit, preserving state for continuation. Honor stop requests before loading or processing, and between phases when a stop signal is available. Grouping grants no permission to execute downstream effects.

Store state by job. Before reuse, check schema version, job, task and caller-supplied input revision. Rebuild missing or mismatched read/derive state from authorized inputs; do not replay side effects. A revision label does not detect unannounced file changes. Clear only the affected job when needed; avoid resetting the shared kernel.

Preserve each input failure with its file, error code and message. Partial results, withheld approval and stopped work must remain explicit. Validate the declared final output schema; intermediate phase fields need not exist in a final result.

For JSON-compatible results, emit `nodeRepl.write(JSON.stringify(result))` in the producing call. Object inspection can hide nested errors and counters as `[Object]` or `[Array]`. Preserve every required field. If serialization fails, report the failure without replaying the work.

Return a compact result with identity, revision, outcome, errors and next action. Save full evidence when required for review. On provider access denial, stop and report it; do not reroute around the denial.
