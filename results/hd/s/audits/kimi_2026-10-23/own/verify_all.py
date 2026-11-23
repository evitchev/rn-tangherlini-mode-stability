"""HD-S: verify every stored certificate box in all 18 bands, with exact coverage.
Kimi's own route: buildN.py + verify.py.  Only the boxes[] fields of the records are read.
"""
import json
import os
import sys
from fractions import Fraction

from flint import fmpq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rfg import Ctx
from buildN import build_N
from verify import verify_1d, verify_2d

HERE = os.path.dirname(os.path.abspath(__file__))
RECREC = os.path.join(HERE, "..", "data")

Q99 = Fraction(99, 100)
# 13 onset bands: (D, ell) -> q_split; 5 bands from 0+ have None
Q_SPLIT = {(7, 2): Fraction(948, 1000), (7, 3): Fraction(977, 1000),
           (8, 3): Fraction(944, 1000), (8, 4): Fraction(983, 1000),
           (9, 3): Fraction(921, 1000), (9, 4): Fraction(952, 1000),
           (9, 5): Fraction(987, 1000),
           (10, 3): Fraction(490, 1000), (10, 4): Fraction(920, 1000),
           (10, 5): Fraction(961, 1000),
           (11, 4): Fraction(897, 1000), (11, 5): Fraction(929, 1000),
           (11, 6): Fraction(968, 1000)}
ZERO_BANDS = [(8, 2), (9, 2), (10, 2), (11, 2), (11, 3)]
ALL_BANDS = [(7, 2), (7, 3), (8, 2), (8, 3), (8, 4), (9, 2), (9, 3), (9, 4), (9, 5),
             (10, 2), (10, 3), (10, 4), (10, 5), (11, 2), (11, 3), (11, 4), (11, 5),
             (11, 6)]


def q2_of(n, ell, mu):
    Bc = 2 * ell + n - 1
    A = (ell + n) + (ell - 1) * mu * mu
    return 1 - Fraction(Bc * Bc) * mu * mu / (A * A)


def factor_polys(ctx):
    return [({k: fmpq(v.numerator, v.denominator) for k, v in f.items()}, name)
            for f, name in zip(ctx.FACTORS, ("A", "B", "mu+1"))]


def check_box(ctx, box):
    """Returns (ok, info)."""
    ma = Fraction(box["mu"][0])
    mb = Fraction(box["mu"][1])
    Den, Nt, E = build_N(ctx, box)
    # Den > 0 factorwise on [ma, mb]
    for (fp, nm), e in zip(factor_polys(ctx), E):
        if e == 0:
            continue
        ok, info = verify_1d(fp, fmpq(ma.numerator, ma.denominator),
                             fmpq(mb.numerator, mb.denominator))
        if not ok:
            return False, {"reason": f"Den factor {nm} not positive", "info": info}
    N2 = {}
    for yexp, poly in Nt.items():
        for j, c in poly.items():
            if c:
                N2[(yexp, j)] = fmpq(c.numerator, c.denominator)
    ok, info = verify_2d(N2, fmpq(0), fmpq(1),
                         fmpq(ma.numerator, ma.denominator), fmpq(mb.numerator, mb.denominator))
    info = dict(info)
    info["mu"] = box["mu"]
    return ok, info


def check_band(D, ell):
    n = D - 2
    with open(f"{RECREC}/{D}-{ell}.json") as fh:
        d = json.load(fh)
    boxes = d["boxes"]
    ctx = Ctx(ell, n)
    out = {"band": f"{D}-{ell}", "n_boxes": len(boxes), "boxes": []}
    # coverage: contiguity + endpoints
    ma0 = Fraction(boxes[0]["mu"][0])
    mbN = Fraction(boxes[-1]["mu"][1])
    contiguous = all(Fraction(boxes[i]["mu"][1]) == Fraction(boxes[i + 1]["mu"][0])
                     for i in range(len(boxes) - 1))
    cov_hi = q2_of(n, ell, ma0) >= Q99**2
    qs = Q_SPLIT.get((D, ell))
    if qs is None:
        cov_lo = (mbN == 1)
    else:
        cov_lo = q2_of(n, ell, mbN) <= qs**2
    out["coverage"] = {"contiguous": contiguous, "q2(mu_a)>=0.99^2": bool(cov_hi),
                       "low_end_ok": bool(cov_lo),
                       "q2_mu_a": str(q2_of(n, ell, ma0)), "q2_mu_b": str(q2_of(n, ell, mbN))}
    ok_all = contiguous and cov_hi and cov_lo
    for i, box in enumerate(boxes):
        ok, info = check_box(ctx, box)
        out["boxes"].append({"i": i, "ok": bool(ok), "info": info})
        ok_all = ok_all and ok
        print(f"  {D}-{ell} box {i} [{box['mu'][0]},{box['mu'][1]}] {box['variable']}"
              f" deg {box['degree']}: {'POSITIVE' if ok else 'REJECT ' + str(info)[:100]}",
              flush=True)
    out["ok"] = bool(ok_all)
    return out


def main(bands=None):
    bands = bands or ALL_BANDS
    results = {}
    for D, ell in bands:
        r = check_band(D, ell)
        results[f"{D}-{ell}"] = r
        cov = r["coverage"]
        print(f"BAND {D}-{ell}: {'VERIFIED' if r['ok'] else 'FAILED'} "
              f"({r['n_boxes']} boxes; coverage {cov})", flush=True)
    with open(os.path.join(HERE, "verify_all_results.json"), "w") as fh:
        json.dump(results, fh)
    bad = [k for k, v in results.items() if not v["ok"]]
    print("HD-S:", "ALL BANDS VERIFIED" if not bad else f"FAILED: {bad}")
    return 0 if not bad else 1


if __name__ == "__main__":
    bands = None
    if len(sys.argv) > 1:
        bands = [tuple(map(int, b.split("-"))) for b in sys.argv[1:]]
    raise SystemExit(main(bands))
