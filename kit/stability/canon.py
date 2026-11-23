#!/usr/bin/env python3
"""The paper kit's canonical form of a certificate record, and its comparison with the registered records.

bh-modes, kit/stability (the operator's ruling BHM-182, item 4; registered in results/paperkit/PREREG.md).

A record (result.json) is canonicalised by dropping, at every depth, the keys that differ between two runs by
construction:
  - compare_runs.MASK_KEYS: timing, host, platform, git_commit and the per-box timings (code/compare_runs.py,
    RULES.md D);
  - archive_sha256: the archive a run came from. A run from another commit's archive has another value.
For p3's records only (the pieces flagged "p3" in pieces.tsv), a top-level key "design_rule" whose value is the
integer 1 is also dropped. p3's code has written that key since commit 094591c (design rule 2), after the records of
T1-T3 were made at 782fc56; rule 1 is the rule those records were made under.
Everything else is kept: every verdict, every exact value, and the tool versions in "provenance". The canonical form is
json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\\n" in UTF-8, and its SHA-256 is the
record's canonical hash.

  canon.py hash FILE [--p3]                          print FILE's canonical hash
  canon.py build PIECES_TSV ROOT                     print expected.tsv: the canonical hash of every registered record
  canon.py compare EXPECTED_TSV ROOT OUTDIR PART     compare PART's new records (PART = A1, A2, HD, HDX, Z or all)
  canon.py selftest EXPECTED_TSV ROOT WORKDIR        the kit's own controls KC1-KC6 (README.md)

compare exits 0 only if every registered record listed for PART still has its expected hash, and every cited job's new
record has that hash too. Control jobs and run.log files are compared as well, and reported as information.
"""
import hashlib
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "code"))
from compare_runs import MASK_KEYS  # noqa: E402  (the masks of RULES.md D, one definition)

EXTRA_MASK = frozenset({"archive_sha256"})
PARTS = ("A1", "A2", "HD", "HDX", "Z")
COLS = ("part", "piece", "job", "class", "p3", "sha256", "record")


def strip(obj):
    """obj without the masked keys, at every depth."""
    if isinstance(obj, dict):
        return {k: strip(v) for k, v in obj.items() if k not in MASK_KEYS and k not in EXTRA_MASK}
    if isinstance(obj, list):
        return [strip(v) for v in obj]
    return obj


def canonical_bytes(path, p3=False):
    with open(path, encoding="utf-8") as f:
        obj = json.load(f)
    if p3 and isinstance(obj, dict) and type(obj.get("design_rule")) is int and obj["design_rule"] == 1:
        obj = {k: v for k, v in obj.items() if k != "design_rule"}
    text = json.dumps(strip(obj), sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n"
    return text.encode("utf-8")


def canonical_hash(path, p3=False):
    return hashlib.sha256(canonical_bytes(path, p3)).hexdigest()


def read_tsv(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            rows.append(line.rstrip("\n").split("\t"))
    return rows


def build(pieces_tsv, root):
    """expected.tsv on stdout: one row per registered record under each piece's record directory."""
    print("# " + "\t".join(COLS))
    for part, piece, _command, recdir, cited, p3 in read_tsv(pieces_tsv):
        pat = None if cited == "(none)" else re.compile(cited)
        base = os.path.join(root, recdir)
        jobs = []
        for dirpath, _dirs, files in os.walk(base):
            if "result.json" in files:
                jobs.append(os.path.relpath(dirpath, base))
        if not jobs:
            raise SystemExit(f"no records under {recdir}")
        for job in sorted(jobs):
            cls = "cited" if pat is not None and pat.fullmatch(job) else "control"
            rec = os.path.join(recdir, job, "result.json")
            h = canonical_hash(os.path.join(root, rec), p3 == "p3")
            print("\t".join((part, piece, job, cls, p3, h, rec)))


def compare(expected_tsv, root, outdir, part):
    rows = [dict(zip(COLS, r)) for r in read_tsv(expected_tsv)]
    rows = [r for r in rows if part == "all" or r["part"] == part]
    if not rows:
        print(f"no expected rows for part {part}")
        return 1
    bad = 0
    tally = {"cited": [0, 0], "control": [0, 0]}
    logs = [0, 0]
    for r in rows:
        p3 = r["p3"] == "p3"
        rec = os.path.join(root, r["record"])
        new = os.path.join(outdir, r["part"], r["piece"], r["job"], "result.json")
        tag = f'{r["part"]} {r["piece"]} {r["job"]} ({r["class"]})'
        try:
            rec_h = canonical_hash(rec, p3)
        except (OSError, ValueError) as e:
            print(f"RECORD UNREADABLE  {tag}: {e}")
            bad = 1
            continue
        if rec_h != r["sha256"]:
            print(f"RECORD ALTERED  {tag}: {rec_h} != expected {r['sha256']}")
            bad = 1
            continue
        tally[r["class"]][1] += 1
        if not os.path.isfile(new):
            print(f"MISSING  {tag}")
            if r["class"] == "cited":
                bad = 1
            continue
        try:
            new_h = canonical_hash(new, p3)
        except (OSError, ValueError) as e:
            print(f"NEW UNREADABLE  {tag}: {e}")
            if r["class"] == "cited":
                bad = 1
            continue
        if new_h == r["sha256"]:
            tally[r["class"]][0] += 1
            print(f"MATCH  {tag}  {new_h[:16]}")
        else:
            print(f"MISMATCH  {tag}: {new_h} != expected {r['sha256']}")
            if r["class"] == "cited":
                bad = 1
        rl, nl = os.path.join(os.path.dirname(rec), "run.log"), os.path.join(os.path.dirname(new), "run.log")
        if os.path.isfile(rl) and os.path.isfile(nl):
            logs[1] += 1
            with open(rl, "rb") as a, open(nl, "rb") as b:
                same = a.read() == b.read()
            logs[0] += same
            if not same:
                print(f"  (information) run.log differs from the record's: {tag}")
    c, k = tally["cited"], tally["control"]
    print(f"part {part}: cited {c[0]}/{c[1]} MATCH; controls {k[0]}/{k[1]} MATCH (information); "
          f"run.log {logs[0]}/{logs[1]} byte-identical (information)")
    if c[1] == 0:
        print(f"no cited job for part {part}")
        bad = 1
    print(f"canon compare {part}: " + ("PASS" if bad == 0 else "FAIL"))
    return bad


def selftest(expected_tsv, root, work):
    """KC1-KC6: the comparison must catch what it claims to catch, and mask no more than it says."""
    rows = [dict(zip(COLS, r)) for r in read_tsv(expected_tsv)]
    cited = [r for r in rows if r["class"] == "cited" and r["p3"] == "-"]
    p3row = next(r for r in rows if r["p3"] == "p3" and r["class"] == "cited")
    one = cited[0]
    if os.path.exists(work):
        raise SystemExit(f"selftest: {work} exists; give a fresh directory")
    os.makedirs(work)
    results = []

    def case(name, rows_for_case, prepare, want_exit, want_word):
        d = os.path.join(work, name)
        os.makedirs(d)
        exp = os.path.join(d, "expected.tsv")
        with open(exp, "w", encoding="utf-8") as f:
            for r in rows_for_case:
                f.write("\t".join(r[c] for c in COLS) + "\n")
        out = os.path.join(d, "out")
        prepare(out)
        log = os.path.join(d, "compare.txt")
        stdout = sys.stdout
        with open(log, "w", encoding="utf-8") as f:
            sys.stdout = f
            try:
                code = compare(exp, root, out, rows_for_case[0]["part"])
            finally:
                sys.stdout = stdout
        with open(log, encoding="utf-8") as f:
            text = f.read()
        ok = (code != 0) == (want_exit != 0) and re.search(r"^" + re.escape(want_word) + r"\b", text, re.M) is not None
        results.append(ok)
        print(f"{name}: exit {code}, expected {'non-zero' if want_exit else '0'} with '{want_word}': "
              + ("as required" if ok else "NOT AS REQUIRED"))

    def place(out, r, mutate=None):
        src = os.path.join(root, r["record"])
        dst = os.path.join(out, r["part"], r["piece"], r["job"], "result.json")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(src, encoding="utf-8") as f:
            obj = json.load(f)
        if mutate:
            obj = mutate(obj)
        with open(dst, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=1)

    def flip_hex(h):
        return h[:-1] + ("0" if h[-1] != "0" else "1")

    def first_string_digit(obj):
        """Change one digit in the first string value that has one (an exact value of the certificate)."""
        done = [False]

        def walk(o):
            if done[0]:
                return o
            if isinstance(o, dict):
                return {k: (v if k in MASK_KEYS or k in EXTRA_MASK else walk(v)) for k, v in o.items()}
            if isinstance(o, list):
                return [walk(v) for v in o]
            if isinstance(o, str):
                m = re.search(r"[0-8]", o)
                if m:
                    done[0] = True
                    i = m.start()
                    return o[:i] + str(int(o[i]) + 1) + o[i + 1:]
            return o
        out = walk(obj)
        if not done[0]:
            raise SystemExit("selftest: no digit to change")
        return out

    def masked_only(obj):
        o = dict(obj)
        o["timing"] = {"t_total_s": 1e9, "utc_start": "1970-01-01T00:00:00Z"}
        o["archive_sha256"] = "0" * 64
        if isinstance(o.get("provenance"), dict):
            p = dict(o["provenance"])
            p["host"], p["git_commit"], p["platform"] = "elsewhere", "0000000", "other"
            o["provenance"] = p
        return o

    kc1 = dict(one, sha256=flip_hex(one["sha256"]))
    case("KC1-expected-tampered", [kc1], lambda out: place(out, one), 1, "RECORD ALTERED")
    case("KC2-value-changed", [one], lambda out: place(out, one, first_string_digit), 1, "MISMATCH")
    case("KC3-masked-fields-only", [one], lambda out: place(out, one, masked_only), 0, "MATCH")
    case("KC4-job-missing", [one], lambda out: os.makedirs(out), 1, "MISSING")
    case("KC5-p3-design-rule-1", [p3row], lambda out: place(out, p3row, lambda o: dict(o, design_rule=1)), 0, "MATCH")
    case("KC6-p3-design-rule-2", [p3row], lambda out: place(out, p3row, lambda o: dict(o, design_rule=2)), 1,
         "MISMATCH")
    case("KC6b-design-rule-outside-p3", [one], lambda out: place(out, one, lambda o: dict(o, design_rule=1)), 1,
         "MISMATCH")
    ok = all(results)
    print("canon selftest: " + ("ALL CONTROLS AS REQUIRED" if ok else "A CONTROL FAILED"))
    return 0 if ok else 1


def main(argv):
    if len(argv) >= 2 and argv[0] == "hash":
        print(canonical_hash(argv[1], p3="--p3" in argv[2:]))
        return 0
    if len(argv) == 3 and argv[0] == "build":
        build(argv[1], argv[2])
        return 0
    if len(argv) == 5 and argv[0] == "compare":
        return compare(argv[1], argv[2], argv[3], argv[4])
    if len(argv) == 4 and argv[0] == "selftest":
        return selftest(argv[1], argv[2], argv[3])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
