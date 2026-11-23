"""Does a job's verdict match its registered form?  Used by kit/hdx/run_critical.sh (results/hdx/critical/PREREG.md
section 4).

    python -m hdx.kitcheck SPEC RESULT.json        exit 0 if the record's verdict matches SPEC, 1 otherwise

SPEC is one of:
    =TEXT            the verdict is exactly TEXT (e.g. =VERIFIED, =REJECT: COVER)
    ^TEXT            the verdict starts with TEXT (e.g. ^REJECT: E0n)
    +A,B             a REJECT, without an exception, whose failed checks include A and B
    +A,B|C,D         the same, and every failed check is one of A, B, C, D
"""
import json
import sys


def failed_checks(verdict):
    if not verdict.startswith("REJECT: ") or verdict.startswith("REJECT: exception") or \
            verdict.startswith("REJECT: record not written"):
        return None
    return [s.strip() for s in verdict[len("REJECT: "):].split(", ")]


def matches(spec, verdict):
    if spec.startswith("="):
        return verdict == spec[1:]
    if spec.startswith("^"):
        return verdict.startswith(spec[1:])
    if spec.startswith("+"):
        failed = failed_checks(verdict)
        if failed is None:
            return False
        need, _, allowed = spec[1:].partition("|")
        need = [s for s in need.split(",") if s]
        if not all(s in failed for s in need):
            return False
        if allowed:
            ok = set(need) | {s for s in allowed.split(",") if s}
            return all(s in ok for s in failed)
        return True
    raise ValueError(f"unknown spec {spec!r}")


def main(argv):
    spec, path = argv[1], argv[2]
    verdict = json.load(open(path))["verdict"]
    ok = matches(spec, verdict)
    print(f"{'match' if ok else 'NO MATCH'}: {spec} vs {verdict[:200]}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
