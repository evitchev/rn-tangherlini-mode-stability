"""Development tests of a2.scert, run before registration (results/a2/s/PREREG.md section 6).  Synthetic inputs only:
W = 12 - 7x (U = 64 m^2 (12 - 7x), H = m) in place of S5's potential, with its own design from a2.pilot's functions (the
same rule, on the synthetic potential).  E0, G-RES and THROAT need S5's potential and are not run.  Every control path
and the record writer are exercised.

    python -m a2.devtest_scert
"""
import json
import subprocess
import sys
import tempfile
import time

from a2 import pilot, scert
from hd.pilot import Setting
from ki.potentials import m, x

SYN_F = (lambda mm, dd, xx: 64 * mm * mm * (12 - 7 * xx), lambda mm, dd, xx: mm)
SYN_E = (64 * m ** 2 * (12 - 7 * x), m)


def main():
    S1 = Setting(4, 2, 0.0, funcs=SYN_F)
    c = S1.W(0.0) / 9
    beta0 = 9 * (c - float(pilot.A_RES) * (float(pilot.A_RES) + 1))
    cheb = pilot.p0_fit(S1, float(pilot.A_RES), beta0, 12)
    rec = {"a": "-2/5", "b_pole": "1/2", "degree": 12, "cheb": [float.hex(v) for v in cheb]}
    want = {"none": "VERIFIED", "nc-a2": "REJECT", "nc-zm": "REJECT", "nc-res": "REJECT", "nc-bound": "REJECT: nc-bound (b)",
            "td-verifier": "REJECT: KAT", "td-chart": "REJECT: POS-T", "td-cover": "REJECT: COVER", "td-coeff": None}
    ok = []
    with tempfile.TemporaryDirectory() as tmp:
        outs = []
        for k, (ctl, w) in enumerate(want.items()):
            out = f"{tmp}/{ctl}"
            t0 = time.time()
            scert.main(["--out", out, "--control", ctl], UH=SYN_E, design_rec=rec)
            v = json.load(open(f"{out}/result.json"))["verdict"]
            good = w is None or v == w or (w == "REJECT" and v.startswith("REJECT: ") and "exception" not in v)
            ok.append(good)
            print(f"{'ok  ' if good else 'FAIL'} {ctl}: {v[:200]} ({time.time() - t0:.0f} s)", flush=True)
            if ctl == "none":
                outs.append(f"{out}/result.json")
        out2 = f"{tmp}/none2"
        scert.main(["--out", out2], UH=SYN_E, design_rec=rec)
        outs.append(f"{out2}/result.json")
        cmp = subprocess.run([sys.executable, "compare_runs.py"] + outs, capture_output=True, text=True)
        last = cmp.stdout.strip().splitlines()[-1]
        ok.append(last == "IDENTICAL after masking")
        print("compare_runs:", last)
    print(f"{sum(ok)}/{len(ok)} as expected")
    print("DEVTEST PASS" if all(ok) else "DEVTEST FAIL")


if __name__ == "__main__":
    main()
