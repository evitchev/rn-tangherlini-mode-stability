#!/usr/bin/env python3
"""HD-E reading checks (exact, Fractions only).

1. E3: the stage report's quoted bounds (STAGE_REPORT.md line 31) and HD-E RESULT's (E3 table) against the
   exact rationals in results/hd/elementary/runs/record/main/result.json: a quoted lower bound is inward iff <= exact.
2. E1 / E2 coverage: recompute q(mu_lo)^2 = 1 - (B mu/A)^2 from mu_lo; check q(mu_lo)^2 >= q_hi^2.
3. E2: quoted "certified lower bound of U_-" (approximate, with the sign "≈") vs the exact U_lower_bound.
Usage: python3 -I check_hde.py <bh-modes root>
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])
e = json.load(open(root / "results/hd/elementary/runs/record/main/result.json"))

print("== E3: quoted bounds vs exact")
stage = {5: "38.6", 6: "23.6", 7: "7.19", 8: "4.84", 9: "3.03"}       # STAGE_REPORT.md l. 31 (D = 7..11)
result = {5: "38.57", 6: "23.61", 7: "7.187", 8: "4.842", 9: "3.029"}  # elementary/RESULT.md l. 51-55
for r in e["E3"]:
    n = r["n"]
    ex = F(r["bound"])
    s, t = F(stage[n]), F(result[n])
    print(f"D = {n + 2}: exact {r['bound']} = {float(ex):.6f}; stage report '>= {stage[n]}' inward: {s <= ex}; "
          f"HD-E RESULT '>= {result[n]}' inward: {t <= ex}")


def q2(mu, n, l):
    A = (l + n) + (l - 1) * mu * mu
    B = 2 * l + n - 1
    return 1 - (B * mu / A) ** 2


print("\n== E1 coverage (q <= 99/100) and E2 coverage (q <= q_split)")
bad = 0
for key in ("E1", "E2"):
    for r in e[key]:
        n, l = r["n"], r["ell"]
        mu = F(r["mu_lo"])
        qq = q2(mu, n, l)
        qhi = F(r["q_hi"])
        ok = (qq == F(r["q_at_mu_lo_squared"])) and qq >= qhi * qhi and r["covers"]
        bad += not ok
        if key == "E2":
            print(f"E2 D = {r['D']} l = {l}: mu_lo {r['mu_lo']}, q(mu_lo) = {float(qq) ** 0.5:.6f} >= q_hi {r['q_hi']}: {ok}; "
                  f"U lower bound {float(F(r['U_lower_bound'])):.6g}; leaves {r['bernstein_leaves']}")
print(f"E1 entries: {len(e['E1'])}; E2 entries: {len(e['E2'])}; failures: {bad}")
print("verdict:", e["verdict"])
