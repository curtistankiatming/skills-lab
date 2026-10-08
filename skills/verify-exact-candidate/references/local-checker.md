# Optional local file checker

Use `scripts/verify_files.py` only for an authorized comparison of an ordinary local directory with an independently selected reference. It checks primary-stream raw bytes, sizes, SHA-256 and the complete file set. It does not authenticate the reference, approve work, compare Git modes or commits, establish correctness, or evaluate test applicability. Generating a manifest from the candidate is inventory, not approved-baseline proof.

## Inputs and launch

Use a trusted Python 3.10+ interpreter and the trusted shipped script. No dependency installation is needed. Start with **`-I -B`**: isolated imports prevent the script directory, current directory and `PYTHONPATH` from supplying modules. The checker refuses ordinary CLI startup before its own non-builtin imports; that refusal cannot undo code already executed by an improperly launched interpreter. Programmatic importing is outside this CLI assurance.

Supply literal absolute local paths. The manifest must be outside the candidate directory, including outside any alias of that directory selected by the operator. Keep the directory quiescent where feasible. The checker opens existing objects only and emits one JSON result to stdout; it has no report-file or repair option. Any output redirection is a separate operator write and must be authorized outside the candidate.

```text
python -I -B scripts/verify_files.py --root ABSOLUTE_CANDIDATE_DIRECTORY --manifest ABSOLUTE_REFERENCE_JSON
```

The strict UTF-8 JSON reference is exactly this shape; replace the example with the trusted complete set. Empty file sets are valid. Unknown keys, duplicate keys or malformed entries are inconclusive.

```json
{"schema_version":1,"files":[{"path":"note.txt","bytes":6,"sha256":"5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03"}]}
```

Paths use `/` between relative components. No absolute paths, traversal, empty components, backslashes, streams, control characters, Windows device names, trailing dots/spaces or non-NFC spellings. Case-fold collisions, conflicting directory spellings and file/directory collisions are rejected even on case-sensitive hosts. This deliberately conservative portable-path policy can exclude otherwise legitimate projects; do not rename or normalize them merely to obtain a pass. Raw content is never normalized. The collection's `inventory.json` has a different schema and excludes itself: it is not directly a complete checker reference.

## Results and coverage

| Exit | JSON status | Meaning |
| --- | --- | --- |
| 0 | VERIFIED | Every declared primary file stream matched and observed membership matched within the stated limits. |
| 1 | MISMATCH | A completed comparison found missing/extra files or differing sizes/hashes, with no unresolved coverage. |
| 2 | INCONCLUSIVE | Invalid, unreadable, unstable, interrupted, unsupported or incomplete input prevents an overall conclusion. |

Valid evaluated invocations emit JSON. CLI argument/launch errors report to stderr and exit 2; unavailable stdout exits 2 without a delivered result. Inspect the embedded status, individual file results, membership, issues and limits as well as the exit code. An overall inconclusive result may retain verified or mismatched independent observations; `missing` during incomplete membership coverage means not observed, not proven absent.

The defaults cap the manifest at 2 MiB, each candidate file at 16 MiB, aggregate candidate reads at 256 MiB (including failed reads), entries at 4,096 and relative depth at 32. A file read may consume one extra detection byte against its per-file limit; the aggregate budget remains bounded. Local I/O can still stall; no hard time limit is supplied. Large manifests or incompatible filenames need another adequate authorized method, not a relaxed silent retry.

Windows uses existing handles with read access, no-follow reparse opens and no-recall options; it rejects every reparse/offline/recall object before reading its content, including locally resident Cloud Files. Only fixed local Windows drives are supported. Read-only sharing can temporarily deny competing write/delete opens until handles close; do not run against an actively changing project. No privilege adjustment or backup-intent access is requested. Linux uses retained directory descriptors and no-follow child opens; links and special files are unsupported. Other platforms fail inconclusive before adapter I/O. Linux/WSL behavior has not been run in this validation; the Linux adapter is provisional.

The operator must establish that filesystem/provider I/O is authorized and local. The checker makes no network API calls, but filesystem filters, mounts, cloud providers, access timestamps and OS auditing remain outside its control. It is not an I/O sandbox or a no-side-effect guarantee. It does not hydrate/reclassify unsupported inputs or execute candidate content. Hard-linked files are rejected. Empty directories, permissions, alternate data streams, extended attributes, origin/approval, destination acceptance and environment qualification are outside byte coverage.

Before/after handle metadata and a second directory observation detect demonstrated changes; they do not prove an atomic whole-package snapshot, defeat undetected change-and-revert races, or establish one shared observation instant. If that property is required, use an adequate authorized snapshot mechanism; `--require-atomic` explicitly returns inconclusive while preserving bounded file observations.

## Reproduce fixture checks

Run the bundled fixture suite only when creation of a new disposable directory is authorized. Select a new absolute scratch path outside every candidate. It preserves its fixtures and never recursively deletes them. Some link creation needs host permissions; skips must be retained as coverage gaps. Injected denial/change/attribute tests are not actual link, Cloud Files or concurrency qualification.

```text
python -I -B scripts/test_verify_files.py --scratch ABSOLUTE_NEW_DISPOSABLE_DIRECTORY
```

This helper remains optional. Adequate existing authorized tools can satisfy the skill. Its limitations do not impose a universal ban on Cloud Files or add a repository lifecycle, model, network, installation or approval requirement.

Implementation basis: [Windows existing and relative-handle opens](https://learn.microsoft.com/en-us/windows/win32/api/winternl/nf-winternl-ntcreatefile), [Windows handle directory information](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_both_dir_info), [Windows no-follow and sharing semantics](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew), and [Python descriptor operations](https://docs.python.org/3/library/os.html). These documents support API choices, not qualification of this implementation.
