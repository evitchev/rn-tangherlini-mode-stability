"""HD-X-S's verdict rules: what each job of kit/hdx/run_s.sh must end with (the PREREG's table), applied to a record.

    python -m hdx.verdicts --control NAME --record RESULT.json [--synthetic]

"By POS charts" means REJECT with every reason one of POS-O, POS-O', POS-T, POS-C.  --synthetic: the development
tests' rules, where E0n, G-RES and the pilot record's seal are not run, so td-coeff, td-gres and td-design end VERIFIED.
Prints OK or FAIL with the verdict, and exits 0 only on OK.
"""
import argparse
import json
import re
import sys

POS = ("POS-O", "POS-O'", "POS-T", "POS-C")
EXACT = {"td-verifier": "REJECT: KAT", "td-chart": "REJECT: POS-T", "td-cover": "REJECT: COVER", "td-H": "REJECT: H",
         "td-param": "REJECT: PARAM", "td-design": "REJECT: DESIGN", "td-gres": "REJECT: G-RES", "td-L": "REJECT: L",
         "td-divT": "REJECT: DIV-T, POS-T", "td-divC": "REJECT: DIV-C, POS-C", "nc-well": "REJECT: nc-well (b)"}


def reasons(v):
    return [r.strip() for r in v[len("REJECT: "):].split(",")] if v.startswith("REJECT: ") else None


def judge(ctl, rec, synthetic=False):
    v = rec.get("verdict", "")
    rs = reasons(v)
    ck = rec.get("checks", {})
    if ctl == "none" or (synthetic and ctl in ("td-coeff", "td-gres", "td-design")):
        return v == "VERIFIED"
    if ctl in ("nc-a2", "nc-res"):
        return rs is not None and all(r in POS for r in rs)
    if ctl == "nc-well":
        return v == EXACT[ctl] and ck.get("nc-well (a)", {}).get("ok") is True
    if ctl == "d0":
        return (rs is not None and "POS-C" in rs and all(r in POS for r in rs)
                and ck.get("POS-C", {}).get("detail", "").startswith("at (0, 0); POS-C: sign*p = 0 <= 0"))
    if ctl == "d6":
        mt = re.match(r"at \(([^,]+), ([^)]+)\);", ck.get("POS-T", {}).get("detail", ""))
        return (rs is not None and "POS-T" in rs and all(r in POS for r in rs) and mt is not None
                and mt.group(2).strip() != "0")
    if ctl == "td-S":
        return rs is not None and rs[0] == "S" and all(r in POS for r in rs[1:])
    if ctl == "td-coeff":
        return rs is not None and "E0n" in rs
    return v == EXACT[ctl]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--control", required=True)
    ap.add_argument("--record", required=True)
    ap.add_argument("--synthetic", action="store_true")
    a = ap.parse_args(argv)
    try:
        with open(a.record) as fh:
            rec = json.load(fh)
        good = judge(a.control, rec, a.synthetic)
        v = rec.get("verdict", "")
    except Exception as exc:  # noqa: BLE001
        good, v = False, f"no record: {type(exc).__name__}: {exc}"
    print(f"{'OK' if good else 'FAIL'}  {a.control}: {v[:200]}")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
