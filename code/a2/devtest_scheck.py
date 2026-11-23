"""Development tests of A2-S addendum 1 (results/a2/s/PREREG_ADDENDUM_1.md section 5): the new controls of a2.scert
on the synthetic potential W = 12 - 7x with its own design (as code/a2/devtest_scert.py), and a2.scheck's exact
decimals and record comparison on synthetic values.  S5's potential is not evaluated, except by G-RES's symbolic
comparison on U_- + x^4 (td-gres), which the reading's drill D3 already ran.

    python -m a2.devtest_scheck
"""
import json
import os
import re
import tempfile

from a2 import pilot, scert, scheck
from a2.devtest_scert import SYN_E, SYN_F
from hd.pilot import Setting
from ki.potentials import x
from qnm1c.common import CertificateError

OK = []


def expect(name, cond, info=""):
    OK.append(bool(cond))
    print(f"{'ok  ' if cond else 'FAIL'} {name} {info}"[:300], flush=True)


def main():
    S1 = Setting(4, 2, 0.0, funcs=SYN_F)
    c = S1.W(0.0) / 9
    beta0 = 9 * (c - float(pilot.A_RES) * (float(pilot.A_RES) + 1))
    rec = {"a": "-2/5", "b_pole": "1/2", "degree": 12,
           "cheb": [float.hex(v) for v in pilot.p0_fit(S1, float(pilot.A_RES), beta0, 12)]}
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    want = {"td-H": "REJECT: H", "td-param": "REJECT: PARAM", "td-L": "REJECT: L", "td-divT": "REJECT: DIV-T, POS-T",
            "td-divC": "REJECT: DIV-C, POS-C", "d0": "REJECT: POS-C", "td-S": None, "d6": None, "none": "VERIFIED"}
    with tempfile.TemporaryDirectory() as tmp:
        for ctl, w in want.items():
            out = f"{tmp}/{ctl}"
            scert.main(["--out", out, "--control", ctl], UH=SYN_E, design_rec=rec)
            r = json.load(open(f"{out}/result.json"))
            v = r["verdict"]
            if ctl == "td-S":
                good = v.startswith("REJECT: S") and all(t.strip() in ("POS-O", "POS-O'", "POS-T", "POS-C")
                                                          for t in v[len("REJECT: "):].split(",")[1:])
            elif ctl == "d6":
                det = r["checks"].get("POS-T", {}).get("detail", "")
                good = v.startswith("REJECT: ") and "POS-T" in v and re.match(r"at \([^,]+, [^0][^)]*\);", det)
            elif ctl == "d0":
                good = v == w and r["checks"]["POS-C"]["detail"].startswith("at (0, 0); POS-C: sign*p = 0 <= 0")
            else:
                good = v == w
            expect(f"synthetic {ctl}:", good, v)
        out = f"{tmp}/design"
        scert.main(["--out", out], UH=SYN_E, design_rec={**rec, "a": "-1/2"})
        expect("a design outside the registered family:", json.load(open(f"{out}/result.json"))["verdict"] == "REJECT: DESIGN")
    try:
        scert.design(root, None, tamper=True)
        expect("td-design's changed hash refuses the sealed pilot record:", False)
    except CertificateError as exc:
        expect("td-design's changed hash refuses the sealed pilot record:", "not the sealed one" in str(exc))
    expect("the untampered design reads the sealed pilot record:", scert.design(root, None)[1] == 12)
    ok, det = scert.g_res(x ** 4)
    expect("G-RES's comparison on U + x^4 fails:", not ok, det[:120])
    expect("decimal(2, 5, up) = 1.41422:", scheck.decimal(2, 5, True) == "1.41422")
    expect("decimal(2, 5, down) = 1.41421:", scheck.decimal(2, 5, False) == "1.41421")
    expect("decimal(1/4, 3, up) = 0.500 (exact):", scheck.decimal(scheck.Fraction(1, 4), 3, True) == "0.500")
    a = {"verdict": "VERIFIED", "timing": {"t": 1}, "provenance": {"host": "a"}, "archive_sha256": "x", "checks": {}}
    b = {**a, "timing": {"t": 2}, "provenance": {"host": "b"}, "archive_sha256": "y"}
    expect("strip ignores timing, provenance, archive:", scheck.strip(a) == scheck.strip(b))
    expect("strip keeps a changed verdict:", scheck.strip(a) != scheck.strip({**a, "verdict": "REJECT: X"}))
    print(f"{sum(OK)}/{len(OK)} as expected")
    print("DEVTEST PASS" if all(OK) else "DEVTEST FAIL")


if __name__ == "__main__":
    main()
