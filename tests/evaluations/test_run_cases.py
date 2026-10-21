"""Tests for evaluations/harder-cases/run.py against a local stub endpoint.

Run: python3 -I -B tests/evaluations/test_run_cases.py
"""
import contextlib
import importlib.util
import io
import json
import re
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EVAL = REPO / "evaluations" / "harder-cases"
spec = importlib.util.spec_from_file_location("run_cases", EVAL / "run.py")
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)


class Stub(BaseHTTPRequestHandler):
    """Answers like a chat model: judge prompts get a verdict, trigger prompts a skill name."""
    seen = []

    def log_message(self, *args):
        pass

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        Stub.seen.append(body)
        system, user = body["messages"][0]["content"], body["messages"][1]["content"]
        if body["model"] == "broken":
            self.send_response(500)
            self.end_headers()
            return
        if "scoring one answer" in user:
            n_req = len(re.findall(r"^\d+\. ", user.split("Fail conditions")[0], re.M))
            n_fail = len(re.findall(r"^\d+\. ", user.split("Fail conditions")[1], re.M))
            fail = "merges" in user.split("<answer>")[1].split("</answer>")[0]
            content = json.dumps({"requirements": [True] * n_req, "fail_if": [fail] + [False] * (n_fail - 1),
                                  "notes": "stub"})
            content = "Here is my verdict:\n" + content
        elif "These skills are available" in system and "every skill" in system:
            content = "integrate-approved-pr, scope-pull" if "PR #88 go in" in user else "None"
            if "foo to bar" in user:
                content = "I'd load the editing one"
        elif "These skills are available" in system:
            content = "<think>maybe scope-pull</think>integrate-approved-pr" if "PR #88 go in" in user else "None."
        else:
            content = "Holding; nothing was merged." if "<skill" in system else "Done, it merges fine."
        reply = {"choices": [{"message": {"content": content}, "finish_reason": "stop"}],
                 "usage": {"prompt_tokens": (len(system) + len(user)) // 3, "completion_tokens": 20}}
        if body["model"] == "tiny-context":
            reply["usage"]["prompt_tokens"] = 300
        if body["model"] == "cut-off":
            reply["choices"][0].update(finish_reason="length", message={"content": "<think>still going"})
        if body["model"] == "cached-prompt":
            reply["usage"]["prompt_tokens"] = 0
        if body["model"] == "no-usage":
            del reply["usage"]
        data = json.dumps(reply).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


class RunCasesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), Stub)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.url = f"http://127.0.0.1:{cls.server.server_address[1]}/v1"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        Stub.seen.clear()

    def test_case_files_are_consistent(self):
        cases = run.load("cases.json")["cases"]
        rubric = run.load("rubric.json")["cases"]
        self.assertEqual([c["id"] for c in cases], list(rubric))
        skills = {n for n, _ in run.skill_names(REPO / "skills")}
        self.assertEqual(len(skills), 6)
        for case in cases:
            self.assertIn(case["skill"], skills)
            self.assertTrue(rubric[case["id"]]["requirements"] and rubric[case["id"]]["fail_if"])
        for case in run.load("triggers.json")["cases"]:
            self.assertIn(case["expected"], skills | {"none"})

    def test_answers_skill_condition_sends_the_skill(self):
        out = self.tmp / "a.jsonl"
        run.main(["answers", "--base-url", self.url, "--model", "m", "--condition", "skill",
                  "--only", "H1,H5", "--repeat", "2", "--out", str(out)])
        records = run.read_jsonl(out)
        self.assertEqual([(r["case"], r["repeat"]) for r in records], [("H1", 0), ("H1", 1), ("H5", 0), ("H5", 1)])
        system = Stub.seen[0]["messages"][0]["content"]
        self.assertIn('<skill name="integrate-approved-pr">', system)
        self.assertIn("name: integrate-approved-pr", system)
        self.assertIn("release-bot", Stub.seen[0]["messages"][1]["content"])
        self.assertEqual(Stub.seen[0]["temperature"], 0.0)

    def test_answers_none_condition_has_no_skill(self):
        out = self.tmp / "a.jsonl"
        run.main(["answers", "--base-url", self.url, "--model", "m", "--condition", "none",
                  "--only", "H1", "--out", str(out)])
        self.assertEqual(Stub.seen[0]["messages"][0]["content"], run.NONE_SYSTEM)

    def test_endpoint_error_is_recorded_and_exits_1(self):
        out = self.tmp / "a.jsonl"
        with self.assertRaises(SystemExit) as stop:
            run.main(["answers", "--base-url", self.url, "--model", "broken", "--condition", "none",
                      "--only", "H1", "--out", str(out)])
        self.assertEqual(stop.exception.code, 1)
        record = run.read_jsonl(out)[0]
        self.assertIn("HTTPError", record["error"])
        self.assertEqual(record["answer"], "")

    def test_score_applies_fail_conditions(self):
        answers, scored = self.tmp / "a.jsonl", self.tmp / "s.jsonl"
        run.main(["answers", "--base-url", self.url, "--model", "m", "--condition", "none",
                  "--only", "H1,H3", "--out", str(answers)])
        run.main(["score", "--answers", str(answers), "--judge-base-url", self.url, "--judge-model", "j",
                  "--out", str(scored)])
        records = run.read_jsonl(scored)
        self.assertEqual([r["score"] for r in records], [0, 0])
        self.assertEqual([r["max"] for r in records], [3, 3])
        self.assertTrue(all(r["fail_if"][0] for r in records))
        judge_prompt = Stub.seen[-1]["messages"][1]["content"]
        self.assertNotIn("<skill", judge_prompt)

    def test_score_without_failures_sums_requirements(self):
        answers, scored = self.tmp / "a.jsonl", self.tmp / "s.jsonl"
        run.main(["answers", "--base-url", self.url, "--model", "m", "--condition", "skill",
                  "--only", "H9", "--out", str(answers)])
        run.main(["score", "--answers", str(answers), "--judge-base-url", self.url, "--judge-model", "j",
                  "--out", str(scored)])
        record = run.read_jsonl(scored)[0]
        self.assertEqual((record["score"], record["max"]), (5, 5))

    def test_unanswered_case_is_not_scored(self):
        answers, scored = self.tmp / "a.jsonl", self.tmp / "s.jsonl"
        with self.assertRaises(SystemExit):
            run.main(["answers", "--base-url", self.url, "--model", "broken", "--condition", "none",
                      "--only", "H1", "--out", str(answers)])
        run.main(["score", "--answers", str(answers), "--judge-base-url", self.url, "--judge-model", "j",
                  "--out", str(scored)])
        record = run.read_jsonl(scored)[0]
        self.assertNotIn("score", record)
        self.assertTrue(record["judge_error"].startswith("answer missing"))

    def test_cut_off_answer_is_not_judged(self):
        answers, scored = self.tmp / "a.jsonl", self.tmp / "s.jsonl"
        run.main(["answers", "--base-url", self.url, "--model", "cut-off", "--condition", "skill",
                  "--only", "H6", "--out", str(answers)])
        judged_before = len(Stub.seen)
        run.main(["score", "--answers", str(answers), "--judge-base-url", self.url, "--judge-model", "j",
                  "--out", str(scored)])
        self.assertEqual(len(Stub.seen), judged_before)
        self.assertEqual(run.read_jsonl(scored)[0]["judge_error"], "answer missing: no final answer")

    def test_summary_counts_missing_answers_as_failures(self):
        answers, scored = self.tmp / "a.jsonl", self.tmp / "s.jsonl"
        with open(answers, "w", encoding="utf-8") as f:
            for case, model in [("H1", "m"), ("H3", "broken")]:
                f.write(json.dumps({"case": case, "skill": "integrate-approved-pr", "condition": "none",
                                    "model": model, "repeat": 0, "answer": "" if model == "broken" else
                                    "Done, it merges fine.", "error": "HTTPError: 500" if model == "broken" else None,
                                    "context_check": None}) + "\n")
        run.main(["score", "--answers", str(answers), "--judge-base-url", self.url, "--judge-model", "j",
                  "--out", str(scored)])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            run.main(["summary", str(scored)])
        text = out.getvalue()
        self.assertIn("0/6 points (3/6 before fail-zeroing), 2 failed cases (1 with no answer), 0 unscored", text)
        self.assertIn("H1 rep 0: 0/3 (raw 3) FAIL", text)
        self.assertIn("H3 rep 0: no answer, 0/3 FAIL", text)

    def test_judge_endpoint_error_exits_1(self):
        answers, scored = self.tmp / "a.jsonl", self.tmp / "s.jsonl"
        run.main(["answers", "--base-url", self.url, "--model", "m", "--condition", "none",
                  "--only", "H1", "--out", str(answers)])
        with self.assertRaises(SystemExit) as stop:
            run.main(["score", "--answers", str(answers), "--judge-base-url", self.url, "--judge-model", "broken",
                      "--out", str(scored)])
        self.assertEqual(stop.exception.code, 1)
        self.assertTrue(run.read_jsonl(scored)[0]["judge_endpoint_error"])

    def test_trigger_summary_counts_unparsed(self):
        out = self.tmp / "m.jsonl"
        run.main(["triggers", "--multi", "--base-url", self.url, "--model", "m", "--only", "T3,T15",
                  "--out", str(out)])
        text = io.StringIO()
        with contextlib.redirect_stdout(text):
            run.main(["summary", str(out)])
        self.assertIn("1 unparsed, 0 errors", text.getvalue())

    def test_answer_instructions_ask_to_stop_for_missing_tool_results(self):
        text = run.load("cases.json")["answer_instructions"]
        self.assertIn("name that call and stop there; report only facts you have", text)

    def test_triggers_list_descriptions_and_parse_choice(self):
        out = self.tmp / "t.jsonl"
        run.main(["triggers", "--base-url", self.url, "--model", "m", "--only", "T3,T4", "--out", str(out)])
        records = {r["case"]: r for r in run.read_jsonl(out)}
        self.assertEqual(records["T4"]["choice"], "integrate-approved-pr")
        self.assertTrue(records["T4"]["correct"])
        self.assertEqual(records["T3"]["choice"], "none")
        self.assertTrue(records["T3"]["correct"])
        self.assertIn("- scope-pull: Use when", Stub.seen[0]["messages"][0]["content"])

    def test_multi_select_counts_extra_loads(self):
        out = self.tmp / "m.jsonl"
        run.main(["triggers", "--multi", "--base-url", self.url, "--model", "m", "--only", "T3,T4,T15",
                  "--out", str(out)])
        records = {r["case"]: r for r in run.read_jsonl(out)}
        self.assertIn("list every skill", Stub.seen[0]["messages"][0]["content"])
        self.assertEqual(records["T4"]["loaded"], ["integrate-approved-pr", "scope-pull"])
        self.assertEqual(records["T4"]["extras"], ["scope-pull"])
        self.assertTrue(records["T4"]["found"])
        self.assertFalse(records["T4"]["correct"])
        self.assertEqual((records["T3"]["loaded"], records["T3"]["extras"], records["T3"]["correct"]), ([], [], True))
        self.assertIsNone(records["T15"]["loaded"])
        self.assertFalse(records["T15"]["correct"])
        run.main(["summary", str(out)])

    def test_parse_choices(self):
        names = ["scope-pull", "lean-history-reporting", "node-workflow-batcher"]
        self.assertEqual(run.parse_choices("node-workflow-batcher, `scope-pull`", names),
                         ["node-workflow-batcher", "scope-pull"])
        self.assertEqual(run.parse_choices("None of these; scope-pull is closest", names), [])
        self.assertEqual(run.parse_choices("**None**", names), [])
        self.assertIsNone(run.parse_choices("the history one", names))

    def test_parse_choice(self):
        names = ["scope-pull", "lean-history-reporting"]
        self.assertEqual(run.parse_choice("`scope-pull`", names), "scope-pull")
        self.assertEqual(run.parse_choice("None", names), "none")
        self.assertEqual(run.parse_choice("I'd pick the history one", names), "unparsed")

    def test_parse_choice_abstentions(self):
        names = ["scope-pull", "lean-history-reporting", "node-workflow-batcher"]
        for reply in ["No skill fits.", "N/A", "no", "**None**", "Nothing here fits", "None of these; scope-pull is closest"]:
            self.assertEqual(run.parse_choice(reply, names), "none", reply)
        self.assertEqual(run.parse_choice("node-workflow-batcher", names), "node-workflow-batcher")
        self.assertEqual(run.parse_choice("Skill: lean-history-reporting.", names), "lean-history-reporting")

    def test_strip_thinking(self):
        self.assertEqual(run.strip_thinking("<think>a</think>answer"), "answer")
        self.assertEqual(run.strip_thinking("answer <think>cut off mid-thought"), "answer")
        self.assertEqual(run.strip_thinking("reasoning only</think>answer"), "answer")
        self.assertEqual(run.strip_thinking("plain"), "plain")

    def test_context_check_flags(self):
        expected = {"m": "ok", "tiny-context": "prompt_short", "cut-off": "answer_cut_off", "no-usage": "unknown",
                    "cached-prompt": "unknown"}
        for model, check in expected.items():
            out = self.tmp / f"{model}.jsonl"
            run.main(["answers", "--base-url", self.url, "--model", model, "--condition", "skill",
                      "--only", "H6", "--out", str(out)])
            record = run.read_jsonl(out)[0]
            self.assertEqual(record["context_check"], check, model)
        self.assertEqual(run.read_jsonl(self.tmp / "cut-off.jsonl")[0]["answer"], "")
        self.assertIsNone(run.read_jsonl(self.tmp / "no-usage.jsonl")[0]["prompt_tokens"])

    def test_refuses_to_overwrite_results(self):
        out = self.tmp / "a.jsonl"
        out.write_text("earlier results\n", encoding="utf-8")
        args = ["answers", "--base-url", self.url, "--model", "m", "--condition", "none", "--only", "H1",
                "--out", str(out)]
        with self.assertRaises(SystemExit):
            run.main(args)
        self.assertEqual(out.read_text(encoding="utf-8"), "earlier results\n")
        run.main(args + ["--overwrite"])
        self.assertEqual(run.read_jsonl(out)[0]["case"], "H1")

    def test_records_survive_an_interrupted_run(self):
        out = self.tmp / "a.jsonl"
        real_call, calls = run.call, []

        def interrupt_second(*a):
            calls.append(1)
            if len(calls) == 2:
                raise KeyboardInterrupt
            return real_call(*a)

        run.call = interrupt_second
        try:
            with self.assertRaises(KeyboardInterrupt):
                run.main(["answers", "--base-url", self.url, "--model", "m", "--condition", "none",
                          "--only", "H1,H2", "--out", str(out)])
        finally:
            run.call = real_call
        self.assertEqual([r["case"] for r in run.read_jsonl(out)], ["H1"])

    def test_prompts_and_summary(self):
        run.main(["prompts", "--only", "H6", "--out", str(self.tmp / "p")])
        text = (self.tmp / "p" / "H6.txt").read_text(encoding="utf-8")
        self.assertIn("MANIFEST.json", text)
        self.assertNotIn("<skill", text)
        self.assertIn("Take no actions except loading skills:", text)
        self.assertNotIn("You have no tools", text)
        out = self.tmp / "t.jsonl"
        run.main(["triggers", "--base-url", self.url, "--model", "m", "--only", "T4", "--out", str(out)])
        run.main(["summary", str(out)])


if __name__ == "__main__":
    unittest.main(argv=sys.argv[:1], verbosity=1)
