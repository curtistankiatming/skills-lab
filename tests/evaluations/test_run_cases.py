"""Tests for evaluations/harder-cases/run.py against a local stub endpoint.

Run: python3 -I -B tests/evaluations/test_run_cases.py
"""
import importlib.util
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
        elif "These skills are available" in system:
            content = "<think>maybe scope-pull</think>integrate-approved-pr" if "ready to merge" in user else "None."
        else:
            content = "Holding; nothing was merged." if "<skill" in system else "Done, it merges fine."
        data = json.dumps({"choices": [{"message": {"content": content}}]}).encode()
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

    def test_endpoint_error_is_recorded_not_raised(self):
        out = self.tmp / "a.jsonl"
        run.main(["answers", "--base-url", self.url, "--model", "broken", "--condition", "none",
                  "--only", "H1", "--out", str(out)])
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
        run.main(["answers", "--base-url", self.url, "--model", "broken", "--condition", "none",
                  "--only", "H1", "--out", str(answers)])
        run.main(["score", "--answers", str(answers), "--judge-base-url", self.url, "--judge-model", "j",
                  "--out", str(scored)])
        record = run.read_jsonl(scored)[0]
        self.assertNotIn("score", record)
        self.assertTrue(record["judge_error"].startswith("answer missing"))

    def test_triggers_list_descriptions_and_parse_choice(self):
        out = self.tmp / "t.jsonl"
        run.main(["triggers", "--base-url", self.url, "--model", "m", "--only", "T3,T4", "--out", str(out)])
        records = {r["case"]: r for r in run.read_jsonl(out)}
        self.assertEqual(records["T4"]["choice"], "integrate-approved-pr")
        self.assertTrue(records["T4"]["correct"])
        self.assertEqual(records["T3"]["choice"], "none")
        self.assertTrue(records["T3"]["correct"])
        self.assertIn("- scope-pull: Use this skill when", Stub.seen[0]["messages"][0]["content"])

    def test_parse_choice(self):
        names = ["scope-pull", "lean-history-reporting"]
        self.assertEqual(run.parse_choice("`scope-pull`", names), "scope-pull")
        self.assertEqual(run.parse_choice("None", names), "none")
        self.assertEqual(run.parse_choice("I'd pick the history one", names), "unparsed")

    def test_prompts_and_summary(self):
        run.main(["prompts", "--only", "H6", "--out", str(self.tmp / "p")])
        text = (self.tmp / "p" / "H6.txt").read_text(encoding="utf-8")
        self.assertIn("MANIFEST.json", text)
        self.assertNotIn("<skill", text)
        out = self.tmp / "t.jsonl"
        run.main(["triggers", "--base-url", self.url, "--model", "m", "--only", "T4", "--out", str(out)])
        run.main(["summary", str(out)])


if __name__ == "__main__":
    unittest.main(argv=sys.argv[:1], verbosity=1)
