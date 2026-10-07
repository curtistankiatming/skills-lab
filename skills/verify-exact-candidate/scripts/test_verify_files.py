"""Run explicitly with --scratch DIR outside candidates; stdlib, no hosted effects."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock

sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
spec = importlib.util.spec_from_file_location("checker", HERE / "verify_files.py")
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
SCRATCH = None


class CheckerTests(unittest.TestCase):
    def setUp(self):
        self.home = SCRATCH / self._testMethodName
        self.home.mkdir(parents=True, exist_ok=False)
        self.root = self.home / "candidate"
        self.root.mkdir()
        self.manifest = self.home / "reference.json"
        self.write("a.txt", b"hello\n")
        self.reference(["a.txt"])

    def write(self, name, data):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def reference(self, paths):
        files = []
        for path in paths:
            raw = (self.root / path).read_bytes()
            files.append({"path": path, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
        self.manifest.write_text(json.dumps({"schema_version": 1, "files": files}), encoding="utf-8")

    def check(self, **kw):
        return c.check(str(self.root), str(self.manifest), **kw)

    def bad_entry(self, **kw):
        obj = json.loads(self.manifest.read_text())
        obj["files"][0].update(kw)
        self.manifest.write_text(json.dumps(obj), encoding="utf-8")

    def test_match_and_no_writes(self):
        self.write("nested/crlf.txt", b"hello\r\n")
        self.write("nested/empty.bin", b"")
        self.reference(["a.txt", "nested/crlf.txt", "nested/empty.bin"])
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = self.check()
        self.assertEqual(result["status"], "VERIFIED", result)
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_hash_mismatch(self):
        self.write("a.txt", b"other\n")
        self.assertEqual(self.check()["status"], "MISMATCH")

    def test_size_and_newline_mismatch(self):
        self.write("a.txt", b"hello\r\n")
        r = self.check()
        self.assertEqual(r["status"], "MISMATCH")
        self.assertEqual(r["files"][0]["actual"]["bytes"], 7)

    def test_missing_and_extra(self):
        (self.root / "a.txt").unlink()
        self.write("extra.txt", b"x")
        r = self.check()
        self.assertEqual(r["status"], "MISMATCH", r)
        self.assertEqual(r["membership"]["missing"], ["a.txt"])
        self.assertEqual(r["membership"]["extra"], ["extra.txt"])

    def test_empty_set_and_empty_directory(self):
        (self.root / "a.txt").unlink()
        (self.root / "empty").mkdir()
        self.reference([])
        self.assertEqual(self.check()["status"], "VERIFIED")

    def test_duplicate_json_keys(self):
        self.manifest.write_text('{"schema_version":1,"schema_version":1,"files":[]}', encoding="utf-8")
        self.assertEqual(self.check()["status"], "INCONCLUSIVE")

    def test_duplicate_case_paths_and_prefixes(self):
        obj = json.loads(self.manifest.read_text())
        obj["files"].append(dict(obj["files"][0], path="A.txt"))
        with self.assertRaises(c.Unavailable):
            c.manifest_entries(json.dumps(obj).encode())
        obj["files"] = [dict(obj["files"][0], path="Dir/a"), dict(obj["files"][0], path="dir/b")]
        with self.assertRaises(c.Unavailable):
            c.manifest_entries(json.dumps(obj).encode())

    def test_path_escape_and_device_aliases(self):
        for path in ("../canary.txt", "/tmp/escape", "C:/escape", "a\\b", "a:stream", "CON.txt",
                     "a./b", "a /b", "a//b", "a/./b", "COM¹.txt", "e\u0301.txt"):
            with self.subTest(path=path):
                self.bad_entry(path=path)
                self.assertEqual(self.check()["status"], "INCONCLUSIVE")

    def test_invalid_types_and_schema(self):
        for field, value in (("bytes", True), ("bytes", -1), ("bytes", "6"), ("sha256", "A" * 64),
                             ("sha256", 7), ("path", None)):
            self.reference(["a.txt"])
            self.bad_entry(**{field: value})
            self.assertEqual(self.check()["status"], "INCONCLUSIVE")
        for raw in (b"[]", b"{", b"\xff", b'{"schema_version":true,"files":[]}',
                    b'{"schema_version":1,"files":[],"extra":0}', b'{"schema_version":1,"files":[NaN]}'):
            self.manifest.write_bytes(raw)
            self.assertEqual(self.check()["status"], "INCONCLUSIVE")

    def test_manifest_inside_root_and_relative_root(self):
        self.assertEqual(c.check(str(self.root), str(self.root / "ref.json"))["status"], "INCONCLUSIVE")
        self.assertEqual(c.check("candidate", str(self.manifest))["status"], "INCONCLUSIVE")

    def test_atomic_requirement(self):
        r = self.check(require_atomic=True)
        self.assertEqual(r["status"], "INCONCLUSIVE")
        self.assertEqual(r["files"][0]["status"], "VERIFIED")

    def test_size_and_entry_limits(self):
        with mock.patch.object(c, "MAX_FILE", 5):
            self.assertEqual(self.check()["status"], "INCONCLUSIVE")
        with mock.patch.object(c, "MAX_ENTRIES", 0):
            self.assertEqual(self.check()["status"], "INCONCLUSIVE")
        with mock.patch.object(c, "MAX_MANIFEST", 8):
            self.assertEqual(self.check()["status"], "INCONCLUSIVE")

    def test_failed_read_consumes_aggregate_budget(self):
        class Fake:
            def __init__(self):
                self.reads = 0
            def read(self, handle, amount):
                self.reads += 1
                return b"abcd" if self.reads == 1 else b""
            def info(self, handle):
                return (1, 2, 0, 4, 99, 0, 1)
        fs, budget = Fake(), [6]
        with self.assertRaises(c.Unavailable):
            c.read_bounded(fs, 1, (1, 2, 0, 4, 0, 0, 1), 6, budget=budget)
        self.assertEqual(budget, [2])
        reads = fs.reads
        with self.assertRaises(c.Unavailable):
            c.read_bounded(fs, 2, (1, 3, 0, 3, 0, 0, 1), 6, budget=budget)
        self.assertEqual(fs.reads, reads)

    @unittest.skipUnless(os.name == "nt", "Windows attribute admission injection")
    def test_windows_reparse_cloud_and_special_admission(self):
        import contextlib
        import ctypes
        with contextlib.ExitStack() as stack:
            fs = c.WindowsFS(stack)
            for flag in (0x400, 0x1000, 0x40000, 0x400000):
                def metadata(handle, pointer):
                    ctypes.cast(pointer, ctypes.POINTER(fs.INFO)).contents.attrs = flag
                    return 1
                with mock.patch.object(fs.k, "GetFileInformationByHandle", metadata), mock.patch.object(fs.k, "GetFileType", return_value=1):
                    with self.assertRaises(c.Unavailable):
                        fs.info(1)

    def test_hardlink_not_followed_as_new_identity(self):
        try:
            os.link(self.root / "a.txt", self.home / "canary.txt")
        except OSError as exc:
            self.skipTest("hardlink creation unavailable: %s" % exc)
        self.assertEqual(self.check()["status"], "INCONCLUSIVE")

    def test_unsupported_hardlink_identity_observation(self):
        cls = c.WindowsFS if os.name == "nt" else c.PosixFS
        original = cls.info
        def linked(fs, handle):
            info = original(fs, handle)
            return info if fs.directory(info) or info[3] != 6 else info[:6] + (2,)
        with mock.patch.object(cls, "info", linked):
            self.assertEqual(self.check()["status"], "INCONCLUSIVE")
        def linked_manifest(fs, handle):
            info = original(fs, handle)
            return info if fs.directory(info) or info[3] == 6 else info[:6] + (2,)
        with mock.patch.object(cls, "info", linked_manifest), mock.patch.object(cls, "read") as reader:
            self.assertEqual(self.check()["status"], "INCONCLUSIVE")
            reader.assert_not_called()

    def test_unknown_type_in_partial_scan(self):
        self.write("unsupported", b"x")
        cls = c.WindowsFS if os.name == "nt" else c.PosixFS
        original = cls.child
        def unavailable(fs, parent, name):
            if name == "unsupported":
                raise c.Unavailable("excluded reparse observation")
            return original(fs, parent, name)
        with mock.patch.object(cls, "child", unavailable):
            r = self.check()
            self.assertEqual(r["status"], "INCONCLUSIVE")
            self.assertEqual(r["membership"]["status"], "INCONCLUSIVE")
            self.assertEqual(r["files"][0]["status"], "VERIFIED")

    def test_changed_membership_observation(self):
        cls = c.WindowsFS if os.name == "nt" else c.PosixFS
        original = cls.names
        count = 0
        def changed(fs, handle):
            nonlocal count
            count += 1
            return original(fs, handle) + (["appeared.txt"] if count > 1 else [])
        with mock.patch.object(cls, "names", changed):
            self.assertEqual(self.check()["status"], "INCONCLUSIVE")

    def test_symlink_escape(self):
        canary = self.home / "canary.txt"
        canary.write_bytes(b"must not be read")
        try:
            os.symlink(canary, self.root / "link.txt")
        except OSError as exc:
            self.skipTest("symlink creation unavailable: %s" % exc)
        r = self.check()
        self.assertEqual(r["status"], "INCONCLUSIVE")
        self.assertTrue(any(x["path"] == "link.txt" for x in r["issues"]))

    @unittest.skipUnless(os.name == "nt", "Windows junction fixture")
    def test_junction_escape(self):
        outside = self.home / "outside"
        outside.mkdir()
        (outside / "canary.txt").write_bytes(b"must not be read")
        # Literal disposable paths built within the explicitly supplied scratch directory.
        p = subprocess.run(["cmd", "/c", "mklink", "/J", str(self.root / "junction"), str(outside)], capture_output=True)
        if p.returncode:
            self.skipTest("junction creation unavailable")
        r = self.check()
        self.assertEqual(r["status"], "INCONCLUSIVE")
        self.assertNotIn("junction/canary.txt", [x["path"] for x in r["files"]])

    def test_unreadable_and_interrupted(self):
        cls = c.WindowsFS if os.name == "nt" else c.PosixFS
        with mock.patch.object(cls, "read", side_effect=PermissionError(13, "denied")):
            self.assertEqual(self.check()["status"], "INCONCLUSIVE")
        with mock.patch.object(cls, "read", side_effect=KeyboardInterrupt):
            self.assertEqual(self.check()["status"], "INCONCLUSIVE")

    def test_change_during_read(self):
        cls = c.WindowsFS if os.name == "nt" else c.PosixFS
        original = cls.info
        count = 0
        def changed(fs, handle):
            nonlocal count
            info = original(fs, handle)
            if not fs.directory(info):
                count += 1
                if count >= 2:
                    return info[:4] + (info[4] + count,) + info[5:]
            return info
        with mock.patch.object(cls, "info", changed):
            self.assertEqual(self.check()["status"], "INCONCLUSIVE")

    def test_no_candidate_execution(self):
        self.write("repair.py", b"raise RuntimeError('must never execute')\n")
        self.reference(["a.txt", "repair.py"])
        self.assertEqual(self.check()["status"], "VERIFIED")

    def test_cli_codes_match_json(self):
        for wanted, change in (("VERIFIED", None), ("MISMATCH", b"wrong"), ("INCONCLUSIVE", b"INVALID")):
            self.write("a.txt", b"hello\n")
            self.reference(["a.txt"])
            if change == b"INVALID":
                self.manifest.write_bytes(change)
            elif change:
                self.write("a.txt", change)
            p = subprocess.run([sys.executable, "-I", "-B", str(HERE / "verify_files.py"), "--root", str(self.root),
                                "--manifest", str(self.manifest)], capture_output=True, text=True)
            self.assertEqual(json.loads(p.stdout)["status"], wanted, p.stderr)
            self.assertEqual(p.returncode, {"VERIFIED": 0, "MISMATCH": 1, "INCONCLUSIVE": 2}[wanted])

    def test_cli_refuses_unisolated_shadow_module(self):
        marker = self.home / "shadow-executed.txt"
        (self.home / "argparse.py").write_text("open(%r, 'w').write('executed')" % str(marker), encoding="utf-8")
        env = dict(os.environ, PYTHONPATH=str(self.home))
        p = subprocess.run([sys.executable, "-B", str(HERE / "verify_files.py"), "--root", str(self.root),
                            "--manifest", str(self.manifest)], env=env, capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertFalse(marker.exists())
        p = subprocess.run([sys.executable, "-I", "-B", str(HERE / "verify_files.py"), "--root", str(self.root),
                            "--manifest", str(self.manifest)], env=env, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertFalse(marker.exists())

    def test_stdout_failure_returns_inconclusive_exit(self):
        with mock.patch.object(c.sys, "stdout") as out:
            out.flush.side_effect = OSError("unavailable output")
            self.assertEqual(c.main(["--root", str(self.root), "--manifest", str(self.manifest)]), 2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch", required=True)
    args = parser.parse_args()
    SCRATCH = Path(args.scratch)
    if not SCRATCH.is_absolute() or SCRATCH.exists():
        parser.error("scratch must be an absolute, new disposable directory")
    SCRATCH.mkdir(parents=True)
    unittest.main(argv=[sys.argv[0]], verbosity=2)
