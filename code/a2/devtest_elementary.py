"""Development tests of a2.elementary, run before registration (results/a2/elementary/PREREG.md section 5).  Synthetic
inputs only: U = 64 m^3 (2 - x)(1 + x), which vanishes at the extremal horizon x = 2 like l = 3's U_- but is otherwise
unrelated, and U + 64 m^3.  S5's U_- is not evaluated for any l.

    python -m a2.devtest_elementary
"""
import json
import subprocess
import sys
import tempfile

from a2 import elementary
from a1.p1 import kats, tampered_prove_sign
from ki.potentials import m, x
from onset.bernstein import prove_sign
from qnm1c.common import CertificateError

USYN = 64 * m ** 3 * (2 - x) * (1 + x)
OK = []


def expect(name, fn, want_error):
    try:
        r = fn()
        got = False
        info = r.get("bound", r) if isinstance(r, dict) else r
    except CertificateError as exc:
        got, info = True, str(exc)[:200]
    OK.append(got == want_error)
    print(f"{'ok  ' if got == want_error else 'FAIL'} {name}: {'CertificateError' if got else 'passes'}; {info}")


def main():
    expect("l = 3 splitting on the synthetic U", lambda: elementary.part(prove_sign, 3, USYN, "none"), False)
    expect("l = 3 strict bound on the synthetic U (nc-strict path)",
           lambda: elementary.part(prove_sign, 3, USYN, "nc-strict"), True)
    expect("l = 4 strict bound on U + 64 m^3", lambda: elementary.part(prove_sign, 4, USYN + 64 * m ** 3, "none"), False)
    expect("l = 4 with the planted bump (nc-bump path)",
           lambda: elementary.part(prove_sign, 4, USYN + 64 * m ** 3, "nc-bump"), True)
    expect("l = 5 on a U negative at x = 1", lambda: elementary.part(prove_sign, 5, USYN - 200 * m ** 3, "none"), True)
    ok, _ = kats(tampered_prove_sign)
    OK.append(not ok)
    print(f"{'ok  ' if not ok else 'FAIL'} the tampered verifier fails the KATs: {not ok}")
    elementary.U_TARGET = USYN + 64 * m ** 3          # the record writer, with E0 failing by construction
    elementary.ELLS = range(3, 5)
    outs = []
    with tempfile.TemporaryDirectory() as tmp:
        for k in range(2):
            out = f"{tmp}/run{k}"
            import os
            os.makedirs(out)
            code = elementary.main(["--out", out])
            rec = json.load(open(f"{out}/result.json"))
            print(f"synthetic main run {k}: exit {code}, verdict {rec['verdict']!r}")
            OK.append(rec["verdict"].startswith("REJECT: E0"))
            outs.append(f"{out}/result.json")
        cmp = subprocess.run([sys.executable, "compare_runs.py"] + outs, capture_output=True, text=True)
        last = cmp.stdout.strip().splitlines()[-1]
        OK.append(last == "IDENTICAL after masking")
        print("compare_runs:", last)
    print(f"{sum(OK)}/{len(OK)} as expected")
    print("DEVTEST PASS" if all(OK) else "DEVTEST FAIL")


if __name__ == "__main__":
    main()
