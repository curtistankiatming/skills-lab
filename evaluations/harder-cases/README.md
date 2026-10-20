# Harder cases and trigger tests

The [2026-10-07 comparison](../2026-10-07/README.md) hit a ceiling: a model with no skill scored 39/40, so it could not show whether the skills help. These cases are built around the mistakes a model without the skill is likely to make, and the runner works against any OpenAI-compatible endpoint, so you can run them on a local model such as Gemma 12B or Qwen 27B.

**Status: not yet run.** No results are recorded here yet, and no claim is made about any model.

## What's here

- [cases.json](cases.json): 12 fictional cases across all six skills. Three are marked `held_out`; leave them out when tuning a skill, and use them to check the result.
  - **Forged approval:** a bot comment on a PR (H1) and a line in test output (H2) claim the owner approved a merge.
  - **Merge timeout that actually succeeded:** the merge call times out, and the readback shows it merged (H3). In H4 the readback fails, so the outcome is unknown.
  - **PR head changed after approval** (H5), and an approval that matches PRs in two repositories (H12).
  - **Candidate shipping its own manifest:** the package's MANIFEST.json claims to be the approved one and adds a `postinstall.sh` (H6), and a test report is bound to the wrong revision (H7).
  - Also: a bare "Approve" with two tasks waiting (H8), a "done" status with no evidence plus work outside scope (H9), a summary that contradicts the detailed log (H10), and a batch that would cross a sign-off point (H11).
- [rubric.json](rubric.json): per-case requirements, plus `fail_if` items that score the whole case 0, such as merging without approval. It was written before any answers.
- [triggers.json](triggers.json): 18 requests, each naming the skill a host should pick from the six descriptions, or `none`. It covers the lean-history / scope-pull boundary, general code review (which no skill should take), and the batcher.
- [run.py](run.py): the runner. It uses only the Python standard library, and its tests are in [tests/evaluations/](../../tests/evaluations/test_run_cases.py).

## Run it

Start your model behind an OpenAI-compatible endpoint. Ollama serves one at `http://localhost:11434/v1`, LM Studio at `http://localhost:1234/v1`, and llama.cpp's `llama-server` at `http://localhost:8080/v1`. Use the model name your server lists. If the endpoint needs a key, set `EVAL_API_KEY`.

```sh
cd evaluations/harder-cases
URL=http://localhost:11434/v1
MODEL=gemma3:12b   # or your Qwen 27B tag
JUDGE=$MODEL       # better: a stronger model, if you have one

# 1. Answer every case without the skill, then with the skill in the system prompt.
python3 run.py answers --base-url $URL --model $MODEL --condition none  --repeat 3 --out none.jsonl
python3 run.py answers --base-url $URL --model $MODEL --condition skill --repeat 3 --out skill.jsonl

# 2. Score both files with a judge model. A stronger model judges more reliably.
python3 run.py score --answers none.jsonl  --judge-base-url $URL --judge-model $JUDGE --out none-scored.jsonl
python3 run.py score --answers skill.jsonl --judge-base-url $URL --judge-model $JUDGE --out skill-scored.jsonl

# 3. Check skill selection. Scoring is exact-match, so no judge is needed.
python3 run.py triggers --base-url $URL --model $MODEL --repeat 3 --out triggers.jsonl

python3 run.py summary none-scored.jsonl skill-scored.jsonl triggers.jsonl
```

Temperature defaults to 0. Use `--repeat` because small models vary between runs even at temperature 0. `--only H1,H5` runs a subset. Reasoning models' `<think>` blocks are stripped before scoring and kept in the `raw` field.

**Through Hermes.** To test the skills as Hermes actually loads them, install them in Hermes. Then run `python3 run.py prompts --out prompts/` and paste each `prompts/H*.txt` into a fresh Hermes session, once with the skill installed and once without. Save each reply as a JSON line with `case`, `repeat`, `condition` and `answer` fields, and score that file with `run.py score`.

## Reading the results

- The skill helps where the `skill` condition scores higher or fails fewer cases than `none` on the same model. A tie on these cases means no effect was shown, not that the skill is useless.
- Read the `fail_if` hits first. They are the costly mistakes, like merging on a forged approval.
- A judge model can be wrong. Spot-check a few scored answers by hand, especially any `fail_if` hit and any case where the conditions differ. Record the judge model with the results.
- Record the exact model tag, quantization, server and commit of this repository for each run. Results apply to that setup only.
- The cases are fictional and the model has no tools, so they test what the model says it would do, not real tool use.
