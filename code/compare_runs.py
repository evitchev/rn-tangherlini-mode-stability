"""Compare two certificate JSON records (RULES.md D).

    python compare_runs.py REFERENCE.json CANDIDATE.json

Masks run-dependent fields (timings, host, platform, commit label) and requires every other
value to be identical: verdicts, counts, winding balls, enclosures, margins.  Exit 0 if
identical after masking, 1 otherwise (the differences are printed).
"""
import json
import sys

MASK_KEYS = {"timing", "host", "platform", "git_commit", "t_backward_s", "t_total_s", "t_design_s", "t_verify_s"}


def walk(a, b, path, diffs):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k in MASK_KEYS:
                continue
            if k not in a or k not in b:
                diffs.append(f"{path}/{k}: present in only one record")
                continue
            walk(a[k], b[k], f"{path}/{k}", diffs)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            diffs.append(f"{path}: list lengths {len(a)} != {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f"{path}[{i}]", diffs)
    elif a != b:
        diffs.append(f"{path}: {a!r} != {b!r}")


def main(argv):
    ref, cand = (json.load(open(p)) for p in argv[1:3])
    diffs = []
    walk(ref, cand, "", diffs)
    for d in diffs:
        print("DIFF", d)
    print("IDENTICAL after masking" if not diffs else f"{len(diffs)} difference(s)")
    return 0 if not diffs else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
