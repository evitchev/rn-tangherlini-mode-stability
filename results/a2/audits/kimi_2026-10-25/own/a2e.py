"""A2-E, Kimi's own route: for ell = 3..10, U_- >= 0 on [0, x_H] x [q(mu_lo), 1],
i.e. F > 0 on [0,1] x [0, mu_lo] for ell = 4..10, and for ell = 3 the exact splitting
F(1-s, mu) = mu K(mu) + s G(s, mu) with K > 0 and G > 0 (the only zero at s = mu = 0,
i.e. x = x_H, q = 1).

Also the exact gate facts: the parametrisation identities, w increasing, coverage,
and U_-(x_H) at q = 1 equal to 64 l (l-3) (l+3)^2 (l+4)^2 identically in ell.
"""
import json
import os
import sys
from fractions import Fraction

import sympy as sp
from flint import fmpq

sys.path.insert(0, "[kimi-folder]/bhm-a1-audit-2026-10-23/own")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rfg import Ctx
from part1 import build_F, mu_lo_of   # my a1 machinery (n = 4 there)
from verify import verify_1d, verify_2d
sys.path.insert(0, "[kimi-folder]/bhm-p3-audit-2026-10-22/own")
from build import ki_Usymbol

HERE = os.path.dirname(os.path.abspath(__file__))
Q99 = Fraction(99, 100)


def to_fmpq2(F):
    out = {}
    for t, poly in F.items():
        for j, c in poly.items():
            if c:
                out[(t, j)] = fmpq(c.numerator, c.denominator)
    return out


def horizon_value_formula():
    """U_-(x_H) at q = 1:  64 l (l-3) (l+3)^2 (l+4)^2 identically in ell (symbolic)."""
    ell = sp.symbols("ell")
    m = (ell - 1) * (ell + 4)
    delta = 1 / (5 * (ell + 4))
    mm, dd = sp.symbols("m d")
    Ux, Hx = ki_Usymbol(4)
    U2 = sp.expand(Ux.subs({mm: m, dd: delta, sp.Symbol("x"): 2}))
    claim = 64 * ell * (ell - 3) * (ell + 3) ** 2 * (ell + 4) ** 2
    assert sp.cancel(U2 - claim) == 0, (sp.cancel(U2 - claim),)
    print("gate: U_-(x_H) at q=1 == 64 l (l-3) (l+3)^2 (l+4)^2  identically in ell: OK")


def check_ell(ell):
    ctx = Ctx(ell, 4)
    F, Den, E = build_F(ctx)
    mlo = mu_lo_of(ctx)  # A1's rule: largest k/1000 with w(k/1000)^2 <= 1 - (99/100)^2
    # coverage: q(mu_lo)^2 >= (99/100)^2 exactly
    A = (ell + 4) + (ell - 1) * mlo * mlo
    q2 = 1 - Fraction((2 * ell + 3) ** 2) * mlo * mlo / (A * A)
    assert q2 >= Q99**2, f"coverage failed at ell={ell}"
    Den_f = {k: fmpq(v.numerator, v.denominator) for k, v in Den.items()}
    okD, _ = verify_1d(Den_f, fmpq(0), fmpq(mlo.numerator, mlo.denominator))
    assert okD
    F2 = to_fmpq2(F)
    if ell == 3:
        # the splitting: F(1-s, mu) = mu K(mu) + s G(s, mu)
        t, mu = sp.symbols("t mu")
        Fsp = sp.expand(sum(sp.Rational(c.numerator, c.denominator) * t**i * mu**j
                            for i, poly in F.items() for j, c in poly.items()))
        F1 = sp.expand(Fsp.subs(t, 1))                    # F(1, mu)
        K = sp.div(F1, mu)[0]
        assert sp.expand(F1 - mu * K) == 0, "mu division not exact"
        s = sp.symbols("s")
        F_s = sp.expand(Fsp.subs(t, 1 - s))               # F(1-s, mu)
        G = sp.div(sp.expand(F_s - F1), s)[0]
        assert sp.expand(F_s - F1 - s * G) == 0, "s division not exact"
        # verify identity: F(1-s, mu) = mu K + s G
        assert sp.expand(F_s - (mu * K + s * G)) == 0
        # positivity: K > 0 on [0, mu_lo], G > 0 on [0,1]x[0,mu_lo]
        K1 = {i: fmpq(str(sp.Rational(K.coeff(mu, i)))) for i in range(sp.degree(K, mu) + 1)
              if K.coeff(mu, i) != 0}
        okK, iK = verify_1d(K1, fmpq(0), fmpq(mlo.numerator, mlo.denominator))
        G2 = {}
        for i in range(sp.degree(G, s) + 1):
            for j in range(sp.degree(G, mu) + 1):
                c = G.coeff(s, i).coeff(mu, j)
                if c != 0:
                    G2[(i, j)] = fmpq(str(sp.Rational(c)))
        okG, iG = verify_2d(G2, fmpq(0), fmpq(1), fmpq(0), fmpq(mlo.numerator, mlo.denominator))
        return okK and okG, {"splitting": "exact", "K>0": okK, "G>0": okG,
                             "mu_lo": str(mlo)}
    else:
        okF, iF = verify_2d(F2, fmpq(0), fmpq(1), fmpq(0), fmpq(mlo.numerator, mlo.denominator))
        return okF, {"strict": okF, "nodes": iF.get("nodes"), "mu_lo": str(mlo)}


def main():
    horizon_value_formula()
    results = {}
    for ell in range(3, 11):
        ok, info = check_ell(ell)
        results[ell] = (ok, info)
        print(f"ell={ell}: {'POSITIVE' if ok else 'REJECT'} {info}", flush=True)
    with open(os.path.join(HERE, "a2e_results.json"), "w") as fh:
        json.dump({str(k): {"ok": v[0], **{kk: str(vv) for kk, vv in v[1].items()}}
                   for k, v in results.items()}, fh, indent=1)
    print("A2-E:", "ALL OK" if all(v[0] for v in results.values()) else "FAILURE")
    return 0 if all(v[0] for v in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
