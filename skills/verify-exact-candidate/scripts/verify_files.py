#!/usr/bin/env python3
"""Optional, bounded raw-file comparison. Python 3.10+, standard library only."""
import sys

# Refuse ordinary CLI startup before importing modules that could be shadowed.
# Isolated mode removes script/CWD/PYTHONPATH injection; the interpreter itself must be trusted.
if __name__ == "__main__" and not sys.flags.isolated:
    sys.stderr.write("Use a trusted Python interpreter with -I -B for isolated imports.\n")
    sys.exit(2)
sys.dont_write_bytecode = True

import argparse
import contextlib
import ctypes
import hashlib
import json
import ntpath
import os
import re
import stat
import unicodedata

MAX_MANIFEST = 2 * 1024 * 1024
MAX_FILE = 16 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
MAX_ENTRIES = 4096
MAX_DEPTH = 32
CHUNK = 65536
LIMITS = [
    "Sequential observations, not an atomic package snapshot or hostile-filesystem proof.",
    "Ordinary files only. Windows reparse/offline/recall objects and POSIX links/special files are unsupported.",
    "No network API, install, repair, candidate import or execution. Filesystem/provider I/O is not isolated.",
    "Caller must select an authorized local filesystem; no approval, provenance or test applicability is established.",
    "Portable path policy; primary file streams only. Empty directories and alternate streams are outside byte coverage.",
]


class Unavailable(Exception):
    pass


def component(name):
    if (not isinstance(name, str) or not name or name in (".", "..")
            or name != unicodedata.normalize("NFC", name)
            or any(ord(c) < 32 or ord(c) == 127 or 0xD800 <= ord(c) <= 0xDFFF for c in name)
            or any(c in '<>:"/\\|?*' for c in name) or name.endswith((".", " "))
            or re.fullmatch(r"(?i)(CON|PRN|AUX|NUL|COM[1-9¹²³]|LPT[1-9¹²³])(?:\..*)?", name)):
        raise Unavailable("unsupported or ambiguous path component")
    return name


def relative(path):
    if not isinstance(path, str) or len(path) > 4096:
        raise Unavailable("invalid manifest path")
    parts = path.split("/")
    if len(parts) > MAX_DEPTH:
        raise Unavailable("path depth limit")
    for part in parts:
        component(part)
    return parts


def absolute(path):
    if not isinstance(path, str):
        raise Unavailable("absolute literal path required")
    if os.name == "nt":
        if not re.match(r"^[A-Za-z]:[\\/]", path) or path.startswith(("\\\\", "//")):
            raise Unavailable("local drive absolute path required; UNC/device paths unsupported")
        drive, tail = ntpath.splitdrive(path)
        parts = re.split(r"[\\/]", tail[1:]) if tail[1:] else []
        if parts and parts[-1] == "":
            parts.pop()
        if len(parts) > 128:
            raise Unavailable("absolute path depth limit")
        for part in parts:
            component(part)
        return drive.upper() + "\\", parts
    if not path.startswith("/") or path.startswith("//"):
        raise Unavailable("absolute literal local path required")
    parts = path[1:].split("/") if path != "/" else []
    if parts and parts[-1] == "":
        parts.pop()
    if len(parts) > 128:
        raise Unavailable("absolute path depth limit")
    for part in parts:
        component(part)
    return "/", parts


class PosixFS:
    def __init__(self, stack):
        self.stack = stack
        if (os.open not in os.supports_dir_fd or os.listdir not in os.supports_fd
                or not hasattr(os, "O_NOFOLLOW")):
            raise Unavailable("handle-relative no-follow operations unavailable")

    def hold(self, fd):
        self.stack.callback(os.close, fd)
        return fd

    def anchor(self, base):
        return self.hold(os.open(base, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW))

    def child(self, parent, name):
        component(name)
        return self.hold(os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent))

    def info(self, handle):
        s = os.fstat(handle)
        if not (stat.S_ISREG(s.st_mode) or stat.S_ISDIR(s.st_mode)):
            raise Unavailable("unsupported file type")
        return (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink)

    def directory(self, info):
        return stat.S_ISDIR(info[2])

    def names(self, handle):
        names = []
        with os.scandir(handle) as entries:
            for entry in entries:
                names.append(entry.name)
                if len(names) > MAX_ENTRIES:
                    raise Unavailable("directory entry limit")
        return names

    def read(self, handle, amount):
        return os.read(handle, amount)


class WindowsFS:
    """Open existing objects relative to retained handles, without following reparses."""
    def __init__(self, stack):
        from ctypes import wintypes as w
        self.stack = stack
        self.k = ctypes.WinDLL("kernel32", use_last_error=True)
        self.n = ctypes.WinDLL("ntdll")
        class US(ctypes.Structure):
            _fields_ = [("length", w.USHORT), ("maximum", w.USHORT), ("buffer", w.LPWSTR)]
        class OA(ctypes.Structure):
            _fields_ = [("length", w.ULONG), ("root", w.HANDLE), ("name", ctypes.POINTER(US)),
                        ("attributes", w.ULONG), ("security", w.LPVOID), ("quality", w.LPVOID)]
        class IOS(ctypes.Structure):
            _fields_ = [("status", w.LPVOID), ("information", ctypes.c_size_t)]
        class INFO(ctypes.Structure):
            _fields_ = [("attrs", w.DWORD), ("created", w.FILETIME), ("accessed", w.FILETIME),
                        ("written", w.FILETIME), ("volume", w.DWORD), ("size_hi", w.DWORD),
                        ("size_lo", w.DWORD), ("links", w.DWORD), ("id_hi", w.DWORD), ("id_lo", w.DWORD)]
        class DIR(ctypes.Structure):
            _fields_ = [("next", w.DWORD), ("index", w.DWORD),
                        ("creation", ctypes.c_int64), ("access", ctypes.c_int64),
                        ("write", ctypes.c_int64), ("change", ctypes.c_int64),
                        ("end", ctypes.c_int64), ("allocation", ctypes.c_int64),
                        ("attrs", w.DWORD), ("length", w.DWORD), ("ea", w.DWORD),
                        ("short_length", ctypes.c_byte), ("short_name", w.WCHAR * 12),
                        ("file_id", ctypes.c_int64), ("name", w.WCHAR * 1)]
        self.US, self.OA, self.IOS, self.INFO, self.DIR = US, OA, IOS, INFO, DIR
        self.n.NtCreateFile.argtypes = [ctypes.POINTER(w.HANDLE), w.ULONG, ctypes.POINTER(OA),
                                       ctypes.POINTER(IOS), w.LPVOID, w.ULONG, w.ULONG,
                                       w.ULONG, w.ULONG, w.LPVOID, w.ULONG]
        self.n.NtCreateFile.restype = ctypes.c_long
        self.n.RtlNtStatusToDosError.argtypes = [ctypes.c_long]
        self.n.RtlNtStatusToDosError.restype = w.ULONG
        self.k.CloseHandle.argtypes = [w.HANDLE]
        self.k.GetFileInformationByHandle.argtypes = [w.HANDLE, ctypes.POINTER(INFO)]
        self.k.GetFileInformationByHandleEx.argtypes = [w.HANDLE, ctypes.c_int, w.LPVOID, w.DWORD]
        self.k.ReadFile.argtypes = [w.HANDLE, w.LPVOID, w.DWORD, ctypes.POINTER(w.DWORD), w.LPVOID]
        self.k.GetDriveTypeW.argtypes = [w.LPCWSTR]
        self.k.GetFileType.argtypes = [w.HANDLE]

    def open(self, parent, name):
        from ctypes import wintypes as w
        buf = ctypes.create_unicode_buffer(name)
        length = len(name.encode("utf-16-le"))
        if length > 65532:
            raise Unavailable("native path length limit")
        us = self.US(length, length + 2, ctypes.cast(buf, w.LPWSTR))
        oa = self.OA(ctypes.sizeof(self.OA), parent, ctypes.pointer(us), 0, None, None)
        handle, ios = w.HANDLE(), self.IOS()
        # READ_DATA/LIST_DIRECTORY, READ_ATTRIBUTES, SYNCHRONIZE; share read only.
        # FILE_OPEN existing; synchronous, OPEN_REPARSE_POINT, OPEN_NO_RECALL.
        status = self.n.NtCreateFile(ctypes.byref(handle), 0x100081, ctypes.byref(oa),
                                    ctypes.byref(ios), None, 0, 1, 1, 0x00600020, None, 0)
        if status < 0:
            raise ctypes.WinError(self.n.RtlNtStatusToDosError(status))
        self.stack.callback(self.k.CloseHandle, handle)
        return handle

    def anchor(self, base):
        if self.k.GetDriveTypeW(base) != 3:
            raise Unavailable("helper supports fixed local Windows drives only")
        return self.open(None, "\\??\\" + base)

    def child(self, parent, name):
        return self.open(parent, component(name))

    def info(self, handle):
        value = self.INFO()
        if not self.k.GetFileInformationByHandle(handle, ctypes.byref(value)):
            raise ctypes.WinError(ctypes.get_last_error())
        if self.k.GetFileType(handle) != 1 or value.attrs & (0x400 | 0x1000 | 0x40000 | 0x400000):
            raise Unavailable("reparse, offline, recall or non-disk object unsupported")
        return (value.volume, (value.id_hi << 32) | value.id_lo, value.attrs,
                (value.size_hi << 32) | value.size_lo,
                (value.written.dwHighDateTime << 32) | value.written.dwLowDateTime,
                (value.created.dwHighDateTime << 32) | value.created.dwLowDateTime, value.links)

    def directory(self, info):
        return bool(info[2] & 0x10)

    def names(self, handle):
        buf = ctypes.create_string_buffer(CHUNK)
        names, first = [], True
        while True:
            if not self.k.GetFileInformationByHandleEx(handle, 11 if first else 10, buf, CHUNK):
                code = ctypes.get_last_error()
                if code == 18:
                    return names
                raise ctypes.WinError(code)
            first, offset = False, 0
            while True:
                if offset + ctypes.sizeof(self.DIR) > CHUNK:
                    raise Unavailable("invalid directory buffer")
                entry = self.DIR.from_buffer(buf, offset)
                end = offset + self.DIR.name.offset + entry.length
                if entry.length % 2 or end > CHUNK:
                    raise Unavailable("invalid directory name buffer")
                name = buf.raw[offset + self.DIR.name.offset:end].decode("utf-16-le")
                if name not in (".", ".."):
                    names.append(name)
                if len(names) > MAX_ENTRIES:
                    raise Unavailable("directory entry limit")
                if not entry.next:
                    break
                if entry.next < self.DIR.name.offset + entry.length or entry.next % 8:
                    raise Unavailable("invalid directory entry offset")
                offset += entry.next

    def read(self, handle, amount):
        from ctypes import wintypes as w
        buf, count = ctypes.create_string_buffer(amount), w.DWORD()
        if not self.k.ReadFile(handle, buf, amount, ctypes.byref(count), None):
            raise ctypes.WinError(ctypes.get_last_error())
        return buf.raw[:count.value]


def open_absolute(fs, path, directory):
    base, parts = absolute(path)
    handle = fs.anchor(base)
    info = fs.info(handle)
    if not fs.directory(info):
        raise Unavailable("anchor is not a directory")
    for i, part in enumerate(parts):
        handle = fs.child(handle, part)
        info = fs.info(handle)
        if (i < len(parts) - 1 or directory) and not fs.directory(info):
            raise Unavailable("expected directory")
    if fs.directory(info) != directory:
        raise Unavailable("wrong input type")
    return handle, info


def read_bounded(fs, handle, before, limit, collect=False, budget=None):
    if before[3] > limit:
        raise Unavailable("file size limit")
    if budget is not None and before[3] > budget[0]:
        raise Unavailable("total read byte limit")
    digest, size, chunks = hashlib.sha256(), 0, []
    while True:
        amount = min(CHUNK, limit - size + 1)
        if budget is not None:
            if budget[0] == 0:
                if size == before[3]:
                    break
                raise Unavailable("total read byte limit")
            amount = min(amount, budget[0])
        chunk = fs.read(handle, amount)
        if not chunk:
            break
        if budget is not None:
            budget[0] -= len(chunk)  # Charge failed/unstable reads as well as successful reads.
        size += len(chunk)
        if size > limit:
            raise Unavailable("read size limit")
        digest.update(chunk)
        if collect:
            chunks.append(chunk)
    if fs.info(handle) != before or size != before[3]:
        raise Unavailable("file changed during read")
    return size, digest.hexdigest(), b"".join(chunks)


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise Unavailable("duplicate JSON key")
        obj[key] = value
    return obj


def manifest_entries(raw):
    obj = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                     parse_constant=lambda x: (_ for _ in ()).throw(Unavailable("non-JSON constant")))
    if (not isinstance(obj, dict) or set(obj) != {"schema_version", "files"}
            or type(obj["schema_version"]) is not int or obj["schema_version"] != 1
            or not isinstance(obj["files"], list) or len(obj["files"]) > MAX_ENTRIES):
        raise Unavailable("invalid manifest schema")
    found, names, total = {}, {}, 0
    for entry in obj["files"]:
        if not isinstance(entry, dict) or set(entry) != {"path", "bytes", "sha256"}:
            raise Unavailable("invalid file entry")
        path = entry["path"]
        parts = relative(path)
        if (type(entry["bytes"]) is not int or not 0 <= entry["bytes"] <= MAX_FILE
                or not isinstance(entry["sha256"], str)
                or not re.fullmatch("[0-9a-f]{64}", entry["sha256"])):
            raise Unavailable("invalid file size or SHA-256")
        if path.casefold() in found:
            raise Unavailable("duplicate or case-ambiguous file path")
        found[path.casefold()] = entry
        for i in range(1, len(parts) + 1):
            prefix = "/".join(parts[:i])
            folded = prefix.casefold()
            kind = "file" if i == len(parts) else "directory"
            if folded in names and names[folded] != (prefix, kind):
                raise Unavailable("ambiguous path spelling or file/directory collision")
            names[folded] = (prefix, kind)
        total += entry["bytes"]
    if total > MAX_TOTAL:
        raise Unavailable("manifest total byte limit")
    return {e["path"]: e for e in found.values()}


def failure_text(exc):
    if isinstance(exc, OSError):
        return "I/O unavailable (code %s)" % (getattr(exc, "winerror", None) or exc.errno)
    return str(exc)[:240] or type(exc).__name__


def check(root, manifest, require_atomic=False):
    report = {"schema_version": 1, "status": "INCONCLUSIVE", "root": root, "manifest": manifest,
              "manifest_sha256": None, "files": [], "membership": {"status": "INCONCLUSIVE"},
              "issues": [], "limits": list(LIMITS), "policy": {
                  "max_manifest_bytes": MAX_MANIFEST, "max_file_bytes": MAX_FILE,
                  "max_total_bytes": MAX_TOTAL, "max_entries": MAX_ENTRIES, "max_depth": MAX_DEPTH}}
    try:
        # Validate literal paths before opening. Manifest must sit outside the candidate.
        root_base, root_parts = absolute(root)
        manifest_base, manifest_parts = absolute(manifest)
        fold = (lambda x: x.casefold()) if os.name == "nt" else (lambda x: x)
        if (fold(root_base) == fold(manifest_base)
                and list(map(fold, manifest_parts[:len(root_parts)])) == list(map(fold, root_parts))):
            raise Unavailable("manifest must be outside candidate root")
        with contextlib.ExitStack() as stack:
            if os.name == "nt":
                fs = WindowsFS(stack)
            elif sys.platform == "linux":
                fs = PosixFS(stack)
            else:
                raise Unavailable("unsupported platform; only Windows and Linux adapters supplied")
            mh, mi = open_absolute(fs, manifest, False)
            if mi[6] != 1:
                raise Unavailable("hard-linked manifest identity unsupported")
            _, report["manifest_sha256"], raw = read_bounded(fs, mh, mi, MAX_MANIFEST, True)
            expected = manifest_entries(raw)
            rh, ri = open_absolute(fs, root, True)
            dirs, observed, issues, aliases = [], {}, [], {}
            entry_count = 0

            def scan(handle, prefix, before, depth):
                nonlocal entry_count
                names = fs.names(handle)
                if len(names) > MAX_ENTRIES:
                    raise Unavailable("directory entry limit")
                dirs.append((handle, prefix, before, sorted(names)))
                for name in sorted(names):
                    entry_count += 1
                    if entry_count > MAX_ENTRIES or depth >= MAX_DEPTH:
                        raise Unavailable("observed entry or depth limit")
                    path = prefix + name
                    try:
                        component(name)
                        folded = path.casefold()
                        if folded in aliases:
                            raise Unavailable("case-ambiguous observed path")
                        aliases[folded] = path
                        child = fs.child(handle, name)
                        info = fs.info(child)
                        if fs.directory(info):
                            scan(child, path + "/", info, depth + 1)
                        else:
                            if info[6] != 1:
                                raise Unavailable("hard-linked file identity unsupported")
                            observed[path] = (child, info)
                    except (OSError, Unavailable, UnicodeError) as exc:
                        issues.append({"path": path, "reason": failure_text(exc)})

            scan(rh, "", ri, 0)
            missing, extra = sorted(set(expected) - set(observed)), sorted(set(observed) - set(expected))
            report["membership"] = {"status": "INCONCLUSIVE" if issues else
                                    ("MISMATCH" if missing or extra else "VERIFIED"),
                                    "missing": missing, "extra": extra}
            read_budget = [MAX_TOTAL]
            for path, entry in sorted(expected.items()):
                row = {"path": path, "status": "INCONCLUSIVE", "expected": entry}
                if path not in observed:
                    row["status"] = "INCONCLUSIVE" if issues else "MISMATCH"
                    row["reason"] = "not observed; see membership coverage"
                else:
                    handle, info = observed[path]
                    try:
                        size, digest, _ = read_bounded(fs, handle, info, MAX_FILE, budget=read_budget)
                        row["actual"] = {"bytes": size, "sha256": digest}
                        row["status"] = "VERIFIED" if size == entry["bytes"] and digest == entry["sha256"] else "MISMATCH"
                    except (OSError, Unavailable) as exc:
                        row["reason"] = failure_text(exc)
                report["files"].append(row)
            for handle, prefix, before, names in dirs:
                try:
                    if fs.info(handle) != before or sorted(fs.names(handle)) != names:
                        raise Unavailable("directory changed between observations")
                except (OSError, Unavailable, UnicodeError) as exc:
                    issues.append({"path": prefix or ".", "reason": failure_text(exc)})
            for path, (handle, before) in observed.items():
                try:
                    if fs.info(handle) != before:
                        raise Unavailable("file changed between observations")
                except (OSError, Unavailable) as exc:
                    issues.append({"path": path, "reason": failure_text(exc)})
                    for row in report["files"]:
                        if row["path"] == path:
                            row["status"], row["reason"] = "INCONCLUSIVE", failure_text(exc)
            if fs.info(mh) != mi:
                issues.append({"path": "manifest", "reason": "manifest changed between observations"})
            if require_atomic:
                issues.append({"path": ".", "reason": "atomic package snapshot required but not supplied"})
            report["issues"] = issues
            if issues:
                report["membership"]["status"] = "INCONCLUSIVE"
            statuses = [report["membership"]["status"]] + [r["status"] for r in report["files"]]
            if issues or "INCONCLUSIVE" in statuses:
                report["status"] = "INCONCLUSIVE"
            else:
                report["status"] = "MISMATCH" if "MISMATCH" in statuses else "VERIFIED"
    except (OSError, Unavailable, ValueError, UnicodeError, RecursionError) as exc:
        report["issues"].append({"path": "input", "reason": failure_text(exc)})
        report["status"] = "INCONCLUSIVE"
    except KeyboardInterrupt:
        report["issues"].append({"path": "input", "reason": "interrupted; completed observations only"})
        report["status"] = "INCONCLUSIVE"
        report["membership"]["status"] = "INCONCLUSIVE"
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="literal absolute local candidate directory")
    parser.add_argument("--manifest", required=True, help="literal absolute JSON reference outside root")
    parser.add_argument("--require-atomic", action="store_true", help="report inconclusive: this helper supplies no atomic snapshot")
    args = parser.parse_args(argv)
    report = check(args.root, args.manifest, args.require_atomic)
    try:
        print(json.dumps(report, ensure_ascii=True, sort_keys=True), flush=True)
    except (OSError, KeyboardInterrupt):
        sys.stdout = None  # Prevent CPython shutdown from retrying a failed buffered flush.
        return 2  # No successful-output claim if stdout cannot be delivered.
    return {"VERIFIED": 0, "MISMATCH": 1, "INCONCLUSIVE": 2}[report["status"]]


if __name__ == "__main__":
    sys.exit(main())
