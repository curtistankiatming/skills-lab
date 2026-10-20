# Supported receipt

Use the O2 replay JSON schema: phase screening/confirmation; mode baseline/candidate; account, authority, fixtureSha256, cases and totals. Each case has an id and events. Each event records at, expectedDue, bucket, reset, fault (null means NONE), readings and worker decisions. Each reading identifies callId and actor, then a result or supported failure. The fictional meter uses rateLimitsByLimitId.ordinary.primaryWindow, not the live Codex schema. Worker decisions preserve worker, trigger, action, reason and deadline.

The pinned replay checks scheduled timestamps exactly. WORK requires matching account, bucket, reset, a fresh source reading and known ordinary permission/primary usage. Missing required evidence is HOLD. At 10% remaining or less, STOP latches across resets. Optional secondary UNKNOWN alone is allowed. This schema encodes the tested policy, not a universal monitoring schedule or permission to act on workers.

The formatter checks source gates but is not a general hostile-input validator. Unsupported inputs require review or a separately validated adapter. Its process can exit zero while its report status is HOLD. Its single stdout line starts with MATCHED or HOLD, then the report path and SHA256 hash, and ends with STOP-LATCHED whenever any worker's stop is latched, so a caller reading only stdout still sees the stop. Counters describe the replay; they are not token savings.

Required reading identity: callId is an integer (the form used by the supplied replay fixtures) or a nonblank string; actor is a nonblank string. Missing or invalid values require HOLD. No type coercion is used to validate these identifiers.

Next-action guidance uses the computed gate and receipt/case/event checks as well as the preserved recorded decisions. A rejected event cannot recommend Continue. Computed or recorded STOP is retained conservatively across later decisions and resets within its case; it cannot be cleared by a reset. Raw recorded actions, reasons and deadlines remain visible, and mismatches identify the computed gate. This is reporting of fictional receipts, not operational restart authority.

The output must be a new file. The formatter creates it exclusively and refuses any existing destination, including an existing path alias, so an old report or raw receipt cannot be overwritten. Preserve the failed attempt and choose a newly authorized output only after resolving the failure; never retry unchanged.
