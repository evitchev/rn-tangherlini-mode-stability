#!/usr/bin/env python3
"""Exact checks of HD-S's claimed q-intervals (reading only; no certificate is re-run).

For every band record results/hd/s/runs/record/<D>-<l>/result.json:
  1. recompute q(mu)^2 = 1 - (B mu / A)^2, A = (l+n) + (l-1) mu^2, B = 2l + n - 1, n = D - 2
     (TARGET_HD.md section 1) from the record's mu_a, mu_b; compare with the record's strings;
  2. q(mu_a)^2 >= (99/100)^2; for onset bands q(mu_b)^2 <= q_split^2, and HD-E's E2 box
     [mu_lo, 1] has mu_lo <= mu_b (so the two exact ranges overlap);
  3. the inward decimals in the JSON and in RESULT.md's table: lower decimal >= exact lower end,
     upper decimal <= exact upper end (compared as squares of exact rationals);
  4. the registered boxes are contiguous from mu_a to mu_b and every box verified.
Usage: python3 -I check_intervals.py <bh-modes root>
"""
import json
import re
import sys
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])
srec = root / "results/hd/s/runs/record"
erec = json.load(open(root / "results/hd/elementary/runs/record/main/result.json"))
E2 = {(x["D"], x["ell"]): x for x in erec["E2"]}

# RESULT.md table rows: | D | l | kind | [lo, hi] | ...
res_rows = {}
for line in open(root / "results/hd/s/RESULT.md", encoding="utf-8"):
    m = re.match(r"\|\s*(\d+)\s*\|\s*(\d+)\s*\|[^|]*\|\s*\[([0-9.]+),\s*([0-9.]+)\]\s*\|", line)
    if m:
        res_rows[(int(m.group(1)), int(m.group(2)))] = (m.group(3), m.group(4))


def q2(mu, n, l):
    A = (l + n) + (l - 1) * mu * mu
    B = 2 * l + n - 1
    w = B * mu / A
    return 1 - w * w


def parse_sqrt_interval(s):
    m = re.match(r"\[sqrt\(([0-9/]+)\), sqrt\(([0-9/]+)\)\]", s)
    return F(m.group(1)), F(m.group(2))


QMAX2 = F(99, 100) ** 2
allok = True
print("D l | exact q_lo..q_hi (float) | JSON inward | RESULT.md | inward ok | cover ok | mu_lo(HD-E) <= mu_b")
for d in sorted(srec.iterdir(), key=lambda p: [int(t) if t.isdigit() else t for t in p.name.split("-")]):
    if not re.fullmatch(r"\d+-\d+", d.name):
        continue
    r = json.load(open(d / "result.json"))
    D, l = r["D"], r["l"]
    n = D - 2
    cov = r["coverage"]
    mua, mub = F(cov["mu_a"]), F(cov["mu_b"])
    qa2, qb2 = F(cov["q(mu_a)^2"]), F(cov["q(mu_b)^2"])
    ok_recomp = (q2(mua, n, l) == qa2) and (q2(mub, n, l) == qb2)
    lo2, hi2 = parse_sqrt_interval(r["claim_q"]["exact"])
    ok_claim = (lo2 == qb2) and (hi2 == qa2)
    ok_qmax = qa2 >= QMAX2
    kind = r["kind"]
    if kind == "onset":
        qs = F(r["q_lo"])
        ok_lo = qb2 <= qs * qs
        e2 = E2[(D, l)]
        mulo = F(e2["mu_lo"])
        ok_e2 = (mulo <= mub) and (F(e2["q_at_mu_lo_squared"]) >= qs * qs) and (q2(mulo, n, l) == F(e2["q_at_mu_lo_squared"]))
        e2s = f"{e2['mu_lo']} <= {cov['mu_b']}: {ok_e2}"
    else:
        ok_lo = (mub == 1) and (qb2 == 0)
        ok_e2 = True
        e2s = "n/a (from 0+)"
    inward = r["claim_q"]["inward"]
    jl, jh = F(inward[0]), F(inward[1])
    ok_in_json = (jl >= 0) and (jl * jl >= qb2) and (jh * jh <= qa2)
    rl, rh = res_rows.get((D, l), (None, None))
    ok_in_res = rl is not None and F(rl) ** 2 >= qb2 and F(rh) ** 2 <= qa2 and F(rl) == jl and F(rh) == jh
    # contiguity of registered boxes
    boxes = [(F(a), F(b)) for a, b in r["boxes_registered"]]
    ok_contig = boxes[0][0] == mua and boxes[-1][1] == mub and all(boxes[i][1] == boxes[i + 1][0] for i in range(len(boxes) - 1))
    ok_ver = all(b["verified"] for b in r["boxes"]) and r["verdict"] == "VERIFIED"
    ok = ok_recomp and ok_claim and ok_qmax and ok_lo and ok_e2 and ok_in_json and ok_in_res and ok_contig and ok_ver
    allok &= ok
    print(f"{D} {l} | {float(qb2)**0.5:.9f}..{float(qa2)**0.5:.9f} | {inward} | [{rl}, {rh}] | json {ok_in_json} res {ok_in_res} | "
          f"recomp {ok_recomp} claim {ok_claim} qmax {ok_qmax} lo {ok_lo} contig {ok_contig} ({len(boxes)} boxes) verified {ok_ver} | {e2s}")
print("ALL OK" if allok else "SOME CHECK FAILED")
