#!/usr/bin/env python3
"""(1) The zeta-design bracket in code/hd/scert.py (Exact.NL, lines 176-179), checked symbolically:
    with P = g/s^e, s = z + delta, the code's br must equal s^(2e) * [(1-z) f_z P + f(-P + (1-z) P_z + P^2)].
    g, f, f_z are arbitrary functions of z; checked for e = 1, 2, 20, 24 (the zeta degrees used are 20 and 24).
(2) Scan of HD-S records: verdicts of the 34 records, attempts per box (fallback used?), G-S6, control outcomes,
    zeta-band delta_b values, and record vs repro-host-2 equality after masking 'timing' and 'provenance'.
Usage: python -I check_mobius_and_records.py <bh-modes root>
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path

import sympy as sp

z, dl = sp.symbols("z delta", positive=True)
g, f, fz = sp.Function("g")(z), sp.Function("f")(z), sp.Function("fz")(z)
print("== (1) zeta-design bracket")
for e in (1, 2, 20, 24):
    s = z + dl
    P = g / s**e
    bracket = (1 - z) * fz * P + f * (-P + (1 - z) * sp.diff(P, z) + P**2)
    Pz = sp.diff(g, z)
    code_br = (1 - z) * fz * g * s**e + f * (-g * s**e + (1 - z) * (Pz * s - e * g) * s**(e - 1) + g**2)
    diff = sp.simplify(sp.expand(bracket * s**(2 * e) - code_br))
    print(f"e = {e}: s^(2e)*bracket - code_br = {diff}")

root = Path(sys.argv[1])
rec = root / "results/hd/s/runs/record"
rep = root / "results/hd/s/runs/repro-host-2"


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in ("timing", "provenance")}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o


print("\n== (2) HD-S records")
names = sorted(p.name for p in rec.iterdir())
print("records:", len(names))
for nm in names:
    a = json.load(open(rec / nm / "result.json"))
    b = json.load(open(rep / nm / "result.json"))
    same = strip(a) == strip(b)
    logs_same = (rec / nm / "run.log").read_bytes() == (rep / nm / "run.log").read_bytes()
    plan_same = None
    if (rec / nm / "planning.jsonl").exists():
        plan_same = (rec / nm / "planning.jsonl").read_bytes() == (rep / nm / "planning.jsonl").read_bytes()
    extra = ""
    if "boxes" in a:
        nbox = len(a["boxes_registered"])
        natt = len(a["boxes"])
        allv = all(r["verified"] for r in a["boxes"])
        degs = sorted({r["degree"] for r in a["boxes"]})
        dbs = sorted({r["delta_b"] for r in a["boxes"] if r["delta_b"] is not None}, key=lambda t: F(t))
        gs6 = [k for k in a["checks"] if k.startswith("G-S6")]
        extra = (f"boxes {nbox}, attempts {natt}, all verified {allv}, degrees {degs}"
                 + (f", delta_b in [{dbs[0]}, {dbs[-1]}] (min {float(F(dbs[0])):.4f})" if dbs else "")
                 + (f", {gs6[0]}: {a['checks'][gs6[0]]['ok']}" if gs6 else ""))
    if "nc-bound" in a:
        nb = a["nc-bound"]
        extra = f"K {nb['K']}, Q {nb['Q_phi0']}, (a) {nb['bound_state_certified']}, rejected {nb['certificate_rejected_on_planted']}"
    print(f"{nm:16s} {a['control']:12s} {a['verdict'][:60]:60s} repro-equal {same} log-equal {logs_same} plan-equal {plan_same} | {extra}")
