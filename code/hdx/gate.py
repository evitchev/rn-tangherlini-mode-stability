"""HD-X's gates against A2: the general-n code on the gate band (4, 2) must reproduce A2's records of record.

    python -m hdx.gate --kind pilot|s --new RESULT.json --ref RESULT.json

pilot: hdx.pilot --gate-a2 --legacy-f against A2-PILOT's record (BHM-095): every field except claim, provenance,
       archive_sha256 and timing must be identical (the same float arithmetic, so the same bits).
s:     hdx.scert --band 6,2 against A2-S's record (BHM-101), in every field A2-S's certificate determines: design, eps,
       degrees, bernstein_leaves, min_bernstein (every chart's least Bernstein coefficient), THROAT's value, verdict,
       and the ok and detail of each check except G-RES's and E0's wording (ok compared; E0 is E0n here).
Prints IDENTICAL, or each difference, and exits 0 only if identical.
"""
import argparse
import json
import sys

PILOT_MASK = ("claim", "provenance", "archive_sha256", "timing")
S_FIELDS = ("design", "eps", "degrees", "bernstein_leaves", "min_bernstein", "verdict")
S_CHECKS_FULL = ("COVER", "DESIGN", "DIV-C", "DIV-T", "H", "KAT", "L", "PARAM", "POS-C", "POS-O", "POS-O'", "POS-T", "S")


def diff_pilot(new, ref):
    keys = (set(new) | set(ref)) - set(PILOT_MASK)
    return [f"{k}: differs" for k in sorted(keys) if new.get(k) != ref.get(k)]


def diff_s(new, ref):
    out = [f"{k}: differs" for k in S_FIELDS if new.get(k) != ref.get(k)]
    tn, tr = new.get("THROAT", {}), ref.get("THROAT", {})
    if tn.get("T(zeta, 0) - pencil limit") != tr.get("T(zeta, 0) - pencil limit"):
        out.append("THROAT value differs")
    cn, cr = new.get("checks", {}), ref.get("checks", {})
    for k in S_CHECKS_FULL:
        if cn.get(k) != cr.get(k):
            out.append(f"check {k} differs")
    if cn.get("G-RES", {}).get("ok") != cr.get("G-RES", {}).get("ok"):
        out.append("check G-RES ok differs")
    if cn.get("E0n", {}).get("ok") != cr.get("E0", {}).get("ok"):
        out.append("check E0n ok differs from A2's E0")
    extra = set(cn) - set(cr) - {"E0n"}
    missing = set(cr) - set(cn) - {"E0"}
    if extra or missing:
        out.append(f"check labels differ: extra {sorted(extra)}, missing {sorted(missing)}")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=("pilot", "s"), required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--ref", required=True)
    a = ap.parse_args(argv)
    with open(a.new) as fh:
        new = json.load(fh)
    with open(a.ref) as fh:
        ref = json.load(fh)
    d = diff_pilot(new, ref) if a.kind == "pilot" else diff_s(new, ref)
    for line in d:
        print(line)
    print("IDENTICAL" if not d else f"DIFFERENT ({len(d)})")
    return 0 if not d else 1


if __name__ == "__main__":
    sys.exit(main())
