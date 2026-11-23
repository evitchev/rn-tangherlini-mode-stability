"""Development tests of hdx.pilot, run before registration.  Synthetic inputs only: for a band (n, l),
W_syn = (n - 1)^2 c x/2 + 12 (1 - x/2) in place of S5's U_-/(64 H_-^2) (hdx.devtest_scert's), which has the band's c at the
extremal horizon (so C-EXACT holds) and is otherwise unrelated; at n = 4 it is A2's W = 12 - 7x.  PG-HDS and PG-T3 need
S5's potential and are not run.  Each run is made twice and the records compared after masking; the cancellation-free
f is compared with hd.pilot's at small z.

    python -m hdx.devtest_pilot [--band D,l ...]
"""
import argparse
import json
import math
import subprocess
import sys
import tempfile

from hdx import pilot
from hdx.devtest_scert import COMPARE, synthetic


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--band", action="append", default=None)
    a = ap.parse_args(argv)
    bands = [(int(s.split(",")[0]) - 2, int(s.split(",")[1])) for s in (a.band or ["7,3", "11,7"])]
    ok = []
    with tempfile.TemporaryDirectory() as tmp:
        for args, n, ell in [(["--gate-a2"], 4, 2)] + [(["--band", f"{n + 2},{ell}"], n, ell) for n, ell in bands]:
            funcs = synthetic(n, ell)[0]
            outs = []
            for k in range(2):
                out = f"{tmp}/{n}-{ell}-{k}"
                code = pilot.main(["--out", out] + args, funcs=funcs)
                rec = json.load(open(f"{out}/result.json"))
                if "bands" in rec:
                    gates = {lab: {g: v["ok"] for g, v in b["gates"].items()} for lab, b in rec["bands"].items()}
                else:
                    gates = {g: v["ok"] for g, v in rec.get("gates", {}).items()}
                good = rec["verdict"].startswith("VALID") and code == 0
                ok.append(good)
                print(f"{'ok  ' if good else 'FAIL'} synthetic D={n + 2} l={ell} run {k}: exit {code}, {rec['verdict']!r}, "
                      f"gates {gates}", flush=True)
                outs.append(f"{out}/result.json")
            cmp = subprocess.run([sys.executable, COMPARE] + outs, capture_output=True, text=True)
            last = cmp.stdout.strip().splitlines()[-1] if cmp.stdout.strip() else cmp.stderr.strip()[-200:]
            ok.append(last == "IDENTICAL after masking")
            print(f"{'ok  ' if ok[-1] else 'FAIL'} compare_runs: {last}", flush=True)
    # the cancellation-free f against hd.pilot's, and against a series: 1 - (1 - z)^(n-1) = (n - 1) z - ...
    for n, ell in [(4, 2)] + bands:
        for mu in (0.0, 1e-3):
            A, L = pilot.Acc(n, ell, mu), pilot.Legacy(n, ell, mu)
            worst_new = worst_old = 0.0
            for e in range(4, 15):
                zz = 10.0 ** (-e)
                oy = sum((-1) ** (j + 1) * math.comb(n - 1, j) * zz ** j for j in range(1, n))
                ref = oy * (A.dt + A.k * oy)
                worst_new = max(worst_new, abs(A.f(zz) / ref - 1))
                worst_old = max(worst_old, abs(L.f(zz) / ref - 1))
            good = worst_new < 1e-12
            ok.append(good)
            print(f"{'ok  ' if good else 'FAIL'} f at n = {n}, mu = {mu}: max relative error over z = 1e-4..1e-14: "
                  f"new {worst_new:.1e}, hd.pilot's {worst_old:.1e}", flush=True)
    print(f"{sum(ok)}/{len(ok)} as expected")
    print("DEVTEST PASS" if all(ok) else "DEVTEST FAIL")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
