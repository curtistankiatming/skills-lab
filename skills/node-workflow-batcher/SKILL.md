---
name: node-workflow-batcher
description: Use when a task needs many separate file reads and calculations that one script could do in a code tool (Node, Python or similar), instead of many tool calls. Check every result. Not for ordinary coding, editing or running a test suite, or for steps that need approval or change anything outside the task.
---

# Workflow batcher

## When to use

- A local job needs several reads, then derived results, then validation, and you have a code-execution tool: a persistent Node or Python REPL, a notebook kernel, or a one-shot script runner.
- Skip it for ordinary coding, editing or running a test suite, where one tool call already does the job.
- Skip it when a step needs an approval or decision you don't have yet, or when the work sends, writes or changes anything outside the job's own state.

## Steps

1. **Find the split points first.** Before writing code, list any approval, open decision or provider limit that has to be resolved outside the code. Batch only the phases before the first split point.
2. **Run the phases in one call**, awaiting dependencies in order. A returned phase result is not, by itself, a reason for another call.
3. **Collect every independent read's outcome**, success or failure: `Promise.allSettled` in JavaScript, `asyncio.gather(..., return_exceptions=True)` or a per-item `try/except` in Python. Inspect every result.
4. **Check each phase before the next one uses it.** Compare the result with its documented schema and look at every item for unexpected errors, in code, inside the same call. Printing results is not checking them. Handle documented partial outcomes explicitly. If you don't know the schema, inspect it first and batch only the phases you understand. Never guess where a field lives.
5. **Keep state per job.** In a persistent runtime, store state under the job's id. Before reusing it, check its schema version, job, task and the caller's input revision. Rebuild missing or mismatched read/derive state from the authorized inputs, and never replay side effects. A revision label cannot detect unannounced file changes. Clear only the affected job, and don't reset a shared runtime. If the runtime is not persistent, rebuild state from inputs on each call.
6. **Print the result as JSON** from the call that produced it (`JSON.stringify` in JavaScript, `json.dumps` in Python). Default printing hides nested errors, as in Node's `[Object]` or a truncated repr; never report, send or act on output you haven't seen in full. If serialization fails, report that failure instead of rerunning the work.
7. **Return a compact result:** identity, revision, outcome, errors and next action. Save full evidence when a reviewer needs it. Validate the declared final output schema; intermediate phase fields don't have to appear in it.

## Stop and report

- At an approval, an unresolved decision or a provider limit: stop there and keep the state needed to continue.
- On a stop request: honor it before loading or processing, and between phases when a stop signal is available.
- On provider access denial: stop and report it. Do not route around it.
- Record each input failure with its file, error code and message. Partial results, withheld approval and stopped work stay explicit in the result.
- Batching grants no permission for downstream effects.

## Example

Job: summarize three local JSON reports. One call reads all three, recording successes and failures. It checks each against the report schema, merges the valid ones and validates the summary schema, then prints `{"job":"J1","revision":"r4","outcome":"partial","errors":[{"file":"c.json","code":"ENOENT","message":"not found"}],"next":"supply c.json or accept a 2-of-3 summary"}`. A follow-up step that would post the summary is not run; it waits for approval.
