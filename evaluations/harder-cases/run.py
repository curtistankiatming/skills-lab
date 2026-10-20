"""Run the harder evaluation cases against any OpenAI-compatible chat endpoint.

Standard library only. Works with Ollama, LM Studio, llama.cpp server, vLLM and
hosted OpenAI-compatible APIs. See README.md in this folder for usage.
"""
import argparse
import hashlib
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
THINK = re.compile(r"<think>.*?</think>", re.S)


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
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"] or ""


def call(args, base_url, model, system, user):
    """Return (text, raw, error, seconds). Errors are recorded, never raised."""
    start = time.monotonic()
    try:
        raw = chat(args, base_url, model, system, user)
        return THINK.sub("", raw).strip(), raw, None, round(time.monotonic() - start, 2)
    except (urllib.error.URLError, OSError, ValueError, KeyError, IndexError) as exc:
        if isinstance(exc, urllib.error.HTTPError):
            exc.close()
        return "", "", f"{type(exc).__name__}: {exc}", round(time.monotonic() - start, 2)


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


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as out:
        for r in records:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")


def read_jsonl(path):
    return [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]


def cmd_answers(args):
    cases = load("cases.json")
    records = []
    for case in selected(cases["cases"], args.only):
        system, user = system_prompt(args, case), case_prompt(cases, case)
        for rep in range(args.repeat):
            text, raw, error, secs = call(args, args.base_url, args.model, system, user)
            records.append({"case": case["id"], "skill": case["skill"], "condition": args.condition,
                            "model": args.model, "repeat": rep, "system_sha256": sha(system),
                            "user_sha256": sha(user), "answer": text, "raw": raw, "error": error,
                            "seconds": secs})
            print(f"{case['id']} rep {rep}: {'ERROR ' + error if error else 'ok'}", file=sys.stderr)
    write_jsonl(args.out, records)


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


def judge_one(args, cases_by_id, rubric, record):
    rules = rubric["cases"][record["case"]]
    prompt = JUDGE.format(
        prompt=case_prompt(load("cases.json"), cases_by_id[record["case"]]),
        answer=record["answer"],
        requirements="\n".join(f"{i + 1}. {r}" for i, r in enumerate(rules["requirements"])),
        fail_if="\n".join(f"{i + 1}. {r}" for i, r in enumerate(rules["fail_if"])))
    text, raw, error, _ = call(args, args.judge_base_url, args.judge_model, NONE_SYSTEM, prompt)
    result = {"judge_model": args.judge_model, "judge_raw": raw, "judge_error": error}
    if error is None:
        try:
            verdict = parse_json_object(text)
            req = [bool(v) for v in verdict["requirements"]][:len(rules["requirements"])]
            fail = [bool(v) for v in verdict["fail_if"]][:len(rules["fail_if"])]
            if len(req) != len(rules["requirements"]) or len(fail) != len(rules["fail_if"]):
                raise ValueError("judge reply has the wrong number of items")
            result.update(requirements=req, fail_if=fail, notes=verdict.get("notes", ""),
                          score=0 if any(fail) else sum(req), max=len(req))
        except (ValueError, KeyError, TypeError) as exc:
            result["judge_error"] = f"unparsed judge reply: {exc}"
    return result


def cmd_score(args):
    rubric = load("rubric.json")
    cases_by_id = {c["id"]: c for c in load("cases.json")["cases"]}
    records = read_jsonl(args.answers)
    for record in records:
        if record.get("error"):
            record.update(judge_error="answer missing: " + record["error"])
            continue
        record.update(judge_one(args, cases_by_id, rubric, record))
        print(f"{record['case']} rep {record['repeat']}: {record.get('score', record.get('judge_error'))}",
              file=sys.stderr)
    write_jsonl(args.out, records)


def skill_names(skills_dir):
    found = []
    for path in sorted(Path(skills_dir).glob("*/SKILL.md")):
        fields = frontmatter(path.read_text(encoding="utf-8"))
        found.append((fields.get("name", path.parent.name), fields.get("description", "")))
    return found


def parse_choice(text, names):
    lowered = text.lower()
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
    records = []
    for case in selected(load("triggers.json")["cases"], args.only):
        for rep in range(args.repeat):
            text, raw, error, secs = call(args, args.base_url, args.model, system, case["request"])
            choice = None if error else parse_choice(text, names)
            records.append({"case": case["id"], "model": args.model, "repeat": rep,
                            "expected": case["expected"], "choice": choice, "correct": choice == case["expected"],
                            "raw": raw, "error": error, "seconds": secs})
            print(f"{case['id']}: {choice or 'ERROR ' + error}", file=sys.stderr)
    write_jsonl(args.out, records)


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
        if records and "expected" in records[0]:
            done = [r for r in records if not r["error"]]
            right = sum(r["correct"] for r in done)
            print(f"{path}: triggers {right}/{len(done)} correct, {len(records) - len(done)} errors")
            for r in done:
                if not r["correct"]:
                    print(f"  {r['case']}: expected {r['expected']}, got {r['choice']}")
            continue
        scored = [r for r in records if "score" in r]
        points, top = sum(r["score"] for r in scored), sum(r["max"] for r in scored)
        fails = sum(1 for r in scored if any(r["fail_if"]))
        conditions = sorted({r["condition"] for r in records})
        print(f"{path}: {', '.join(conditions)}: {points}/{top} points, {fails} failed cases, "
              f"{len(records) - len(scored)} unscored")
        for r in scored:
            flag = " FAIL" if any(r["fail_if"]) else ""
            print(f"  {r['case']} rep {r['repeat']}: {r['score']}/{r['max']}{flag}")


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
