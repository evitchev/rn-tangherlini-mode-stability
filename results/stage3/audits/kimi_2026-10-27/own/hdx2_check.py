"""HD-X-2 per-band check (Kimi): Z0 identity, the three exact divisions, positivity
on the four charts, and the coverage argument.
"""
import os
import sys
from fractions import Fraction

from flint import fmpq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rfg import Ctx
from hdx2 import build_NL, BANDS_2, MU1
from verify import verify_1d, verify_2d

HERE = os.path.dirname(os.path.abspath(__file__))


def to_flat(Nc):
    out = {}
    for i, poly in Nc.items():
        for j, c in poly.items():
            if c:
                out[(i, j)] = fmpq(c.numerator, c.denominator)
    return out


def eval_at_mu0(Nc):
    """NL(z, 0): the mu^0 part, as a Fraction z-poly."""
    out = {}
    for i, poly in Nc.items():
        c0 = poly.get(0, Fraction(0))
        if c0:
            out[i] = c0
    return out


def div_mu(Nc, e=1):
    """Divide by mu^e exactly (every mu-poly must be divisible)."""
    out = {}
    for i, poly in Nc.items():
        np_ = {}
        for j, c in poly.items():
            if j < e:
                if c != 0:
                    return None
            else:
                np_[j - e] = c
        out[i] = np_
    return out


def div_z(Nc, e=2):
    out = {}
    for i, poly in Nc.items():
        if i < e:
            if any(c for c in poly.values()):
                return None
        else:
            out[i - e] = poly
    return out


def sub_T(Nc):
    """z -> mu*zeta: z^i mu^j -> zeta^i mu^(i+j)."""
    out = {}
    for i, poly in Nc.items():
        for j, c in poly.items():
            out[(i, i + j)] = out.get((i, i + j), Fraction(0)) + c
    return {k: v for k, v in out.items() if v}


def sub_C(Nc):
    """mu -> z*sigma: z^i mu^j -> z^(i+j) sigma^j."""
    out = {}
    for i, poly in Nc.items():
        for j, c in poly.items():
            out[(i + j, j)] = out.get((i + j, j), Fraction(0)) + c
    return {k: v for k, v in out.items() if v}


def flat_div_mu(D, e=1):
    out = {}
    for (i, j), c in D.items():
        if j < e:
            if c:
                return None
        else:
            out[(i, j - e)] = c
    return out


def flat_div_zsigma(D):
    """Divide by z^2 sigma: keys (z, sigma)."""
    out = {}
    for (i, j), c in D.items():
        if i < 2 or j < 1:
            if c:
                return None
        else:
            out[(i - 2, j - 1)] = c
    return out


def check_band(D, ell):
    n = D - 2
    ctx = Ctx(ell, n)
    Den, Nc, E = build_NL(ctx)
    MU = MU1[(D, ell)]
    res = {"band": f"{D}-{ell}", "deg": (max(Nc), max(max(p) for p in Nc.values()))}

    # gate: q(MU1)^2 <= (99/100)^2
    Bc = 2 * ell + n - 1
    A1 = (ell + n) + (ell - 1) * MU * MU
    q2 = 1 - Fraction(Bc * Bc) * MU * MU / (A1 * A1)
    res["q(MU1)^2"] = str(q2)
    res["cover_99"] = bool(q2 <= Fraction(99, 100) ** 2)

    # Z0: NL(z, 0) == 0
    z0 = eval_at_mu0(Nc)
    res["Z0"] = not z0

    # Den > 0 on [0, MU1] factorwise
    for fp, nm, e in zip((ctx.A, ctx.B, ctx.C), ("A", "B", "mu+1"), E):
        if e:
            fp_f = {k: fmpq(v.numerator, v.denominator) for k, v in fp.items()}
            ok, _ = verify_1d(fp_f, fmpq(0), fmpq(MU.numerator, MU.denominator))
            assert ok, f"Den factor {nm}"
    res["Den>0"] = True

    # S and R > 0 (they matter only off the corner): S = eps_n + eps_d z,
    # eps_d = 1 + w > 0 everywhere (1 + w, w >= 0); R = sum (1-z)^j > 0 on [0,1]:
    # R(j) has positive Bernstein coefficients as a polynomial in (1-z)?  R in z:
    # R = sum_j (1-z)^j: at z in [0,1] each term in (0,1]; R(0) = k > 0, R(1) = 1.
    # verify R > 0 with my verifier:
    k = n - 1
    Rz = {}
    for j in range(k):
        # (1-z)^j in z
        from math import comb
        for a in range(j + 1):
            Rz[a] = Rz.get(a, Fraction(0)) + Fraction((-1) ** a * comb(j, a))
    Rz_f = {k2: fmpq(v.numerator, v.denominator) for k2, v in Rz.items()}
    okR, _ = verify_1d(Rz_f, fmpq(0), fmpq(1))
    res["R>0"] = okR

    # divisions
    M = div_mu(Nc, 1)
    NT = flat_div_mu(sub_T(Nc), 2)
    KC = flat_div_zsigma(sub_C(Nc))
    res["DIV-O"] = M is not None
    res["DIV-T"] = NT is not None
    res["DIV-C"] = KC is not None

    # positivity
    tof = lambda D: {k: fmpq(v.numerator, v.denominator) for k, v in D.items() if v}
    okO, iO = verify_2d(to_flat(M), fmpq(1, 4), fmpq(1), fmpq(0), fmpq(MU.numerator, MU.denominator))
    okOp, iOp = verify_2d(to_flat(M), fmpq(0), fmpq(1, 4), fmpq(1, 32), fmpq(MU.numerator, MU.denominator))
    okT, iT = verify_2d(tof(NT), fmpq(0), fmpq(8), fmpq(0), fmpq(1, 32))
    okC, iC = verify_2d(tof(KC), fmpq(0), fmpq(1, 4), fmpq(0), fmpq(1, 8))
    res["POS"] = {"O": okO, "O'": okOp, "T": okT, "C": okC}
    res["ok"] = all([res["cover_99"], res["Z0"], res["Den>0"], res["R>0"], res["DIV-O"],
                     res["DIV-T"], res["DIV-C"], okO, okOp, okT, okC])
    return res


def main():
    results = {}
    for D, ell in BANDS_2:
        r = check_band(D, ell)
        results[f"{D}-{ell}"] = r
        print(f"{D}-{ell}: {'VERIFIED' if r['ok'] else 'FAILED'}  deg={r['deg']} "
              f"q(MU1)^2={float(Fraction(r['q(MU1)^2'])):.6f} POS={r['POS']}", flush=True)
    import json
    with open(os.path.join(HERE, "hdx2_results.json"), "w") as fh:
        json.dump(results, fh, indent=1, default=str)
    bad = [k for k, v in results.items() if not v["ok"]]
    print("HD-X-2:", "ALL BANDS VERIFIED" if not bad else f"FAILED: {bad}")
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
