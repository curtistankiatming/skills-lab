"""Run the harder evaluation cases against any OpenAI-compatible chat endpoint.

Standard library only. Works with Ollama, LM Studio, llama.cpp server, vLLM and
hosted OpenAI-compatible APIs. See README.md in this folder for usage.
"""
import argparse
import hashlib
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
NONE_SYSTEM = "You are a careful assistant."
# A prompt whose reported token count falls below this share of a rough
# characters/4 estimate was probably cut to fit a small context window.
SHORT_PROMPT_RATIO = 0.8


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def skill_text(skills_dir, name):
    return (Path(skills_dir) / name / "SKILL.md").read_text(encoding="utf-8")


def frontmatter(text):
    m = re.match(r"---\r?\n(.*?)\r?\n---", text, re.S)
    fields = {}
    for line in (m.group(1) if m else "").splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def strip_thinking(text):
    """Drop reasoning blocks, including one left open when the model hit its token limit."""
    if "</think>" in text and "<think>" not in text.split("</think>", 1)[0]:
        text = text.split("</think>", 1)[1]  # templates that put the opening tag in the prompt
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    return text.split("<think>", 1)[0].strip()


def chat(args, base_url, model, system, user):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": args.temperature,
    }).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    key = os.environ.get("EVAL_API_KEY")
    if key:
        headers["Authorization"] = "Bearer " + key
    req = urllib.request.Request(base_url.rstrip("/") + "/chat/completions", body, headers)
    with urllib.request.urlopen(req, timeout=args.timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def context_check(estimate, prompt_tokens, finish_reason):
    if finish_reason == "length":
        return "answer_cut_off"
    if not prompt_tokens:  # missing, or 0 from servers that don't count cached prompt tokens
        return "unknown"
    return "prompt_short" if prompt_tokens < estimate * SHORT_PROMPT_RATIO else "ok"


def call(args, base_url, model, system, user):
    """Return a result dict. Endpoint and network errors are recorded, never raised."""
    start = time.monotonic()
    estimate = (len(system) + len(user)) // 4
    result = {"answer": "", "raw": "", "error": None, "prompt_tokens": None, "completion_tokens": None,
              "estimated_prompt_tokens": estimate, "finish_reason": None}
    try:
        data = chat(args, base_url, model, system, user)
        choice = data["choices"][0]
        raw = choice["message"]["content"] or ""
        usage = data.get("usage") or {}
        result.update(answer=strip_thinking(raw), raw=raw, finish_reason=choice.get("finish_reason"),
                      prompt_tokens=usage.get("prompt_tokens"), completion_tokens=usage.get("completion_tokens"))
    except (urllib.error.URLError, http.client.HTTPException, OSError, ValueError, KeyError, IndexError,
            TypeError) as exc:
        if isinstance(exc, urllib.error.HTTPError):
            exc.close()
        result["error"] = f"{type(exc).__name__}: {exc}"
    result["context_check"] = None if result["error"] else context_check(
        estimate, result["prompt_tokens"], result["finish_reason"])
    result["seconds"] = round(time.monotonic() - start, 2)
    return result


def case_prompt(cases, case):
    docs = json.dumps(case["documents"], indent=2, ensure_ascii=False)
    return (f"{cases['answer_instructions']}\n\nRequest:\n{case['request']}\n\n"
            f"Documents:\n{docs}")


def system_prompt(args, case):
    if args.condition == "none":
        return NONE_SYSTEM
    text = skill_text(args.skills_dir, case["skill"])
    return (f"{NONE_SYSTEM} You have the following skill. Follow it when it applies.\n\n"
            f"<skill name=\"{case['skill']}\">\n{text}\n</skill>")


def selected(items, only):
    wanted = set(only.split(",")) if only else None
    return [c for c in items if wanted is None or c["id"] in wanted]


def open_out(args):
    """Open --out for appending one record per line, refusing to replace earlier results."""
    try:
        return open(args.out, "w" if args.overwrite else "x", encoding="utf-8")
    except FileExistsError:
        sys.exit(f"{args.out} already exists; choose another --out or pass --overwrite")


def emit(out, record):
    out.write(json.dumps(record, ensure_ascii=False) + "\n")
    out.flush()


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def warn(record):
    check = record.get("context_check")
    return "" if check in (None, "ok") else f" [{check}]"


def cmd_answers(args):
    cases = load("cases.json")
    with open_out(args) as out:
        for case in selected(cases["cases"], args.only):
            system, user = system_prompt(args, case), case_prompt(cases, case)
            for rep in range(args.repeat):
                result = call(args, args.base_url, args.model, system, user)
                emit(out, {"case": case["id"], "skill": case["skill"], "condition": args.condition,
                           "model": args.model, "repeat": rep, "system_sha256": sha(system),
                           "user_sha256": sha(user), **result})
                status = "ERROR " + result["error"] if result["error"] else "ok"
                print(f"{case['id']} rep {rep}: {status}{warn(result)}", file=sys.stderr)


JUDGE = """You are scoring one answer against a fixed rubric. You do not know which model or setup wrote it.

Request and documents given to the answerer:
{prompt}

Answer to score:
<answer>
{answer}
</answer>

Requirements (true if the answer clearly meets it):
{requirements}

Fail conditions (true if the answer does or says this):
{fail_if}

Reply with JSON only, in this shape:
{{"requirements": [true or false for each requirement, in order], "fail_if": [true or false for each fail condition, in order], "notes": "one sentence"}}"""


def parse_json_object(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("no JSON object in judge reply")
    return json.loads(m.group(0))


def judge_one(args, cases, rubric, record):
    rules = rubric["cases"][record["case"]]
    case = {c["id"]: c for c in cases["cases"]}[record["case"]]
    prompt = JUDGE.format(
        prompt=case_prompt(cases, case),
        answer=record["answer"],
        requirements="\n".join(f"{i + 1}. {r}" for i, r in enumerate(rules["requirements"])),
        fail_if="\n".join(f"{i + 1}. {r}" for i, r in enumerate(rules["fail_if"])))
    result = call(args, args.judge_base_url, args.judge_model, NONE_SYSTEM, prompt)
    scored = {"judge_model": args.judge_model, "judge_raw": result["raw"], "judge_error": result["error"],
              "judge_context_check": result["context_check"]}
    if result["error"] is None:
        try:
            verdict = parse_json_object(result["answer"])
            req = [bool(v) for v in verdict["requirements"]][:len(rules["requirements"])]
            fail = [bool(v) for v in verdict["fail_if"]][:len(rules["fail_if"])]
            if len(req) != len(rules["requirements"]) or len(fail) != len(rules["fail_if"]):
                raise ValueError("judge reply has the wrong number of items")
            scored.update(requirements=req, fail_if=fail, notes=verdict.get("notes", ""),
                          score=0 if any(fail) else sum(req), max=len(req))
        except (ValueError, KeyError, TypeError) as exc:
            scored["judge_error"] = f"unparsed judge reply: {exc}"
    return scored


def cmd_score(args):
    rubric, cases = load("rubric.json"), load("cases.json")
    records = read_jsonl(args.answers)
    with open_out(args) as out:
        for record in records:
            if record.get("error"):
                record["judge_error"] = "answer missing: " + record["error"]
            else:
                record.update(judge_one(args, cases, rubric, record))
            emit(out, record)
            print(f"{record['case']} rep {record['repeat']}: {record.get('score', record.get('judge_error'))}",
                  file=sys.stderr)


def skill_names(skills_dir):
    found = []
    for path in sorted(Path(skills_dir).glob("*/SKILL.md")):
        fields = frontmatter(path.read_text(encoding="utf-8"))
        found.append((fields.get("name", path.parent.name), fields.get("description", "")))
    return found


def parse_choice(text, names):
    """Map a picker reply to a skill name, "none" or "unparsed". A leading abstention wins."""
    lowered = re.sub(r"[`*_\"'.]", " ", text.lower()).strip()
    if re.match(r"(none|no\b|n/a|nothing\b)", lowered):
        return "none"
    hits = sorted((lowered.find(n), n) for n in names if n in lowered)
    if hits:
        return hits[0][1]
    return "none" if re.search(r"\bnone\b", lowered) else "unparsed"


def cmd_triggers(args):
    skills = skill_names(args.skills_dir)
    names = [n for n, _ in skills]
    listing = "\n".join(f"- {n}: {d}" for n, d in skills)
    system = (f"{NONE_SYSTEM} These skills are available:\n{listing}\n\n"
              "For the user's request, reply with exactly one skill name from the list, "
              "or none if no skill fits. Reply with the name only.")
    with open_out(args) as out:
        for case in selected(load("triggers.json")["cases"], args.only):
            for rep in range(args.repeat):
                result = call(args, args.base_url, args.model, system, case["request"])
                choice = None if result["error"] else parse_choice(result["answer"], names)
                emit(out, {"case": case["id"], "model": args.model, "repeat": rep, "expected": case["expected"],
                           "choice": choice, "correct": choice == case["expected"], **result})
                print(f"{case['id']}: {choice or 'ERROR ' + result['error']}{warn(result)}", file=sys.stderr)


def cmd_prompts(args):
    """Write each case's prompt to a text file, for pasting into a host such as Hermes."""
    cases = load("cases.json")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for case in selected(cases["cases"], args.only):
        (out / f"{case['id']}.txt").write_text(case_prompt(cases, case) + "\n", encoding="utf-8")
    print(f"wrote prompts to {out}", file=sys.stderr)


def cmd_summary(args):
    for path in args.files:
        records = read_jsonl(path)
        flagged = [r for r in records if r.get("context_check") not in (None, "ok")]
        if records and "expected" in records[0]:
            done = [r for r in records if not r["error"]]
            right = sum(r["correct"] for r in done)
            print(f"{path}: triggers {right}/{len(done)} correct, {len(records) - len(done)} errors")
            for r in done:
                if not r["correct"]:
                    print(f"  {r['case']}: expected {r['expected']}, got {r['choice']}")
        else:
            scored = [r for r in records if "score" in r]
            points, top = sum(r["score"] for r in scored), sum(r["max"] for r in scored)
            fails = sum(1 for r in scored if any(r["fail_if"]))
            conditions = sorted({r["condition"] for r in records})
            print(f"{path}: {', '.join(conditions)}: {points}/{top} points, {fails} failed cases, "
                  f"{len(records) - len(scored)} unscored")
            for r in scored:
                flag = " FAIL" if any(r["fail_if"]) else ""
                print(f"  {r['case']} rep {r['repeat']}: {r['score']}/{r['max']}{flag}{warn(r)}")
        if flagged:
            print(f"  WARNING: {len(flagged)} record(s) flagged by the context check "
                  f"({', '.join(sorted({r['context_check'] for r in flagged}))}); "
                  "raise the model's context size and rerun them. See README.")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="command", required=True)

    def common(sp, endpoint=True):
        if endpoint:
            sp.add_argument("--base-url", required=True, help="for example http://localhost:11434/v1")
            sp.add_argument("--model", required=True)
            sp.add_argument("--repeat", type=int, default=1)
        sp.add_argument("--only", help="comma-separated case ids")
        sp.add_argument("--skills-dir", default=str(REPO / "skills"))
        sp.add_argument("--temperature", type=float, default=0.0)
        sp.add_argument("--timeout", type=float, default=600.0)
        sp.add_argument("--out", required=True)
        sp.add_argument("--overwrite", action="store_true", help="replace an existing --out file")

    a = sub.add_parser("answers", help="answer the cases with or without the skill")
    common(a)
    a.add_argument("--condition", choices=["none", "skill"], required=True)
    t = sub.add_parser("triggers", help="check which skill each request selects")
    common(t)
    s = sub.add_parser("score", help="score an answers file with a judge model")
    common(s, endpoint=False)
    s.add_argument("--answers", required=True)
    s.add_argument("--judge-base-url", required=True)
    s.add_argument("--judge-model", required=True)
    pr = sub.add_parser("prompts", help="write case prompts to files for manual runs")
    common(pr, endpoint=False)
    m = sub.add_parser("summary", help="print totals for scored or trigger files")
    m.add_argument("files", nargs="+")

    args = p.parse_args(argv)
    {"answers": cmd_answers, "score": cmd_score, "triggers": cmd_triggers,
     "prompts": cmd_prompts, "summary": cmd_summary}[args.command](args)


if __name__ == "__main__":
    main()
