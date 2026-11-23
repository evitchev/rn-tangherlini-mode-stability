"""Development tests of hdx.scert, run before registration.  Synthetic inputs only, apart from the gates' own direct
tests below.  For a band (n, l): W_syn = (n - 1)^2 c x/2 + 12 (1 - x/2) (U = 64 m^2 W_syn, H = m) replaces S5's potential.
It has the band's extremal throat coefficient c at x = x_H = 2, hence the band's residue window, and is otherwise
unrelated; at n = 4 it is A2's synthetic W = 12 - 7x.  The design is built on it with hdx.pilot's functions (the same
rule).  E0n, G-RES and THROAT need S5's potential and are not run on it.  Every control path and the record writer are
exercised, with the verdict rules of the kit.  Direct tests: DESIGN's seal and family checks (on A2-PILOT's sealed
record and on a missing one), G-RES and its tamper at n = 5, the refusal of a critical band.

    python -m hdx.devtest_scert [--band D,l ...] [--root REPO]
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time

import sympy as sp

from hdx import pilot, scert
from hdx.bands import B_POLE, MU1, residues
from hdx.verdicts import judge
from ki.potentials import m, x
from qnm1c.common import CertificateError

COMPARE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "compare_runs.py")


def synthetic(n, ell):
    """(float funcs, exact (U, H)) of W_syn = (n - 1)^2 c x/2 + W_inf (1 - x/2), U = 64 m^2 W_syn, H = m, with W_inf =
    m + n(n + 2)/4, S5's value at infinity (x = 0).  At n = 4, l = 2 this is A2's synthetic W = 12 - 7x."""
    c = residues(n, ell)[0]
    winf = sp.Rational((ell - 1) * (ell + n)) + sp.Rational(n * (n + 2), 4)
    k, wf = float((n - 1) ** 2 * c), float(winf)
    funcs = (lambda mm, dd, xx: 64 * mm * mm * (k * xx / 2 + wf * (1 - xx / 2)), lambda mm, dd, xx: mm)
    W = sp.Rational((n - 1) ** 2 * c.numerator, c.denominator) * x / 2 + winf * (1 - x / 2)
    return funcs, (sp.expand(64 * m ** 2 * W), m)


def band_suite(n, ell, tmp, ok):
    funcs, UH = synthetic(n, ell)
    a = residues(n, ell)[3]
    S1 = pilot.Acc(n, ell, 0.0, funcs=funcs)
    c = S1.W(0.0) / (n - 1) ** 2
    beta0 = (n - 1) ** 2 * (c - float(a) * (float(a) + 1))
    cheb = pilot.p0_fit(S1, float(a), beta0, 12)
    drec = {"a": str(a), "b_pole": str(B_POLE), "degree": 12, "mu1": str(MU1), "cheb": [float.hex(v) for v in cheb]}
    outs = []
    for ctl in scert.CONTROLS:
        out = f"{tmp}/{n}-{ell}-{ctl}"
        t0 = time.time()
        scert.main(["--out", out, "--band", f"{n + 2},{ell}", "--control", ctl], UH=UH, design_rec=drec)
        rec = json.load(open(f"{out}/result.json"))
        good = judge(ctl, rec, synthetic=True)
        ok.append(good)
        print(f"{'ok  ' if good else 'FAIL'} D={n + 2} l={ell} {ctl}: {rec['verdict'][:160]} ({time.time() - t0:.0f} s)",
              flush=True)
        if ctl == "none":
            outs.append(f"{out}/result.json")
    out2 = f"{tmp}/{n}-{ell}-none2"
    scert.main(["--out", out2, "--band", f"{n + 2},{ell}"], UH=UH, design_rec=drec)
    outs.append(f"{out2}/result.json")
    cmp = subprocess.run([sys.executable, COMPARE] + outs, capture_output=True, text=True)
    last = cmp.stdout.strip().splitlines()[-1] if cmp.stdout.strip() else cmp.stderr.strip()[-200:]
    ok.append(last == "IDENTICAL after masking")
    print(f"{'ok  ' if ok[-1] else 'FAIL'} D={n + 2} l={ell} compare_runs: {last}", flush=True)


def direct(root, ok):
    def expect(label_, fn, exc_type, text=None):
        try:
            fn()
            good = exc_type is None
            msg = "no exception"
        except Exception as exc:  # noqa: BLE001
            good = exc_type is not None and isinstance(exc, exc_type) and (text is None or text in str(exc))
            msg = f"{type(exc).__name__}: {str(exc)[:120]}"
        ok.append(good)
        print(f"{'ok  ' if good else 'FAIL'} {label_}: {msg}", flush=True)

    expect("DESIGN on A2-PILOT's sealed record (gate band)", lambda: scert.design(root, 4, 2), None)
    expect("DESIGN, td-design's changed hash", lambda: scert.design(root, 4, 2, tamper=True), CertificateError,
           "is not the sealed one")
    expect("DESIGN, a design outside the family", lambda: scert.design(root, 5, 3, design_rec={
        "a": "-1/2", "b_pole": "1/2", "degree": 12, "mu1": "1/8", "cheb": ["0x0p+0"]}), CertificateError,
        "not the registered family")
    hdx_rec = os.path.join(root, scert.PILOT_RECORD)
    if not os.path.exists(hdx_rec):
        expect("DESIGN before HD-X-PILOT's record exists", lambda: scert.design(root, 5, 3), CertificateError,
               "cannot be read")
    expect("a critical band is refused (D = 8, l = 2)", lambda: residues(6, 2), ValueError, "critical band")
    expect("--band 8,2 is refused", lambda: scert.parse_band("8,2"), ValueError, "not a band")
    t0 = time.time()
    g, det = scert.g_res(5)
    ok.append(g)
    print(f"{'ok  ' if g else 'FAIL'} G-RES at n = 5: {det} ({time.time() - t0:.0f} s)", flush=True)
    g2, det2 = scert.g_res(5, x ** 4)
    ok.append(not g2)
    print(f"{'ok  ' if not g2 else 'FAIL'} td-gres at n = 5 (must fail): {det2[:160]}", flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--band", action="append", default=None)
    ap.add_argument("--root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    a = ap.parse_args(argv)
    bands = [(int(s.split(",")[0]) - 2, int(s.split(",")[1])) for s in (a.band or ["7,3", "11,7"])]
    ok = []
    with tempfile.TemporaryDirectory() as tmp:
        for n, ell in bands:
            try:
                band_suite(n, ell, tmp, ok)
            except Exception as exc:  # noqa: BLE001
                ok.append(False)
                print(f"FAIL D={n + 2} l={ell}: the suite stopped: {type(exc).__name__}: {exc}", flush=True)
    direct(a.root, ok)
    print(f"{sum(ok)}/{len(ok)} as expected")
    print("DEVTEST PASS" if all(ok) else "DEVTEST FAIL")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
