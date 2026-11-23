"""HD-X-E, Kimi's own route: for n = 5..9, ell in [n-1, l0(n)], q in [q(mu_lo), 1]:
F > 0 on [0,1] x [0, mu_lo] for ell >= n; the exact splitting at ell = n-1.
mu_lo: largest k/10000 with w(k/10000)^2 <= 1 - (99/100)^2 (HD-E's grid), exact coverage.
Also EXT, symbolic in (ell, n): H_-(x_H) = (l+n)(l+n-1) and U_-(x_H) = 64 l (l-n+1) H_-(x_H)^2
at q = 1.
"""
import json
import os
import sys
from fractions import Fraction

import sympy as sp
from flint import fmpq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "[kimi-folder]/bhm-hd-elementary-audit-2026-10-23/own")
from rfg import Ctx
from verify import verify_1d, verify_2d
from hd import build_F   # my HD-E builder (general n, from my KI transcription)

HERE = os.path.dirname(os.path.abspath(__file__))
L0 = {5: 10, 6: 10, 7: 11, 8: 13, 9: 14}   # my own Lemma-U thresholds (HD-E audit)
Q99 = Fraction(99, 100)


def mu_lo_of(ctx, grid=10000):
    ell, n = ctx.ell, ctx.n
    Bc = 2 * ell + n - 1
    lim = 1 - Q99**2

    def w2(k):
        mk = Fraction(k, grid)
        A = (ell + n) + (ell - 1) * mk * mk
        return Fraction(Bc * Bc) * mk * mk / (A * A)
    lo, hi = 0, grid
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if w2(mid) <= lim:
            lo = mid
        else:
            hi = mid
    return Fraction(lo, grid)


def to_fmpq2(F):
    out = {}
    for t, poly in F.items():
        for j, c in poly.items():
            if c:
                out[(t, j)] = fmpq(c.numerator, c.denominator)
    return out


def ext_gate():
    """EXT, symbolic in (ell, n): at q = 1, H_-(x_H) = (l+n)(l+n-1) and
    U_-(x_H) = 64 l (l-n+1) H_-(x_H)^2."""
    ell, n = sp.symbols("ell n")
    m = (ell - 1) * (ell + n)
    delta = 1 / ((n + 1) * (ell + n))
    mm, dd = sp.symbols("m d")
    Ux, Hx = ki_Usymbol_at(sp.Symbol("n_"), mm, dd)
    return None


def ki_Usymbol_at(nsym, mm, dd):
    """ki_Usymbol at symbolic n: my transcription's ki_full is integer-n; do the general-n
    evaluation with sympy here."""
    sys.path.insert(0, "[kimi-folder]/bhm-p3-audit-2026-10-22/own")
    from build import ki_Usymbol  # integer-n only
    raise NotImplementedError


def ext_gate_symbolic():
    """EXT by direct symbolic evaluation at symbolic n (the KI formula is polynomial in n)."""
    sys.path.insert(0, "[kimi-folder]/bhm-p3-audit-2026-10-22/own")
    import importlib
    import build as KB
    # my build.py's ki_Usymbol takes integer n; for symbolic n, re-enter (5.62b)/(5.63b)
    # with n symbolic (the formula is polynomial in n at K = 1, y = 0):
    n, m, d, x = sp.symbols("n m d x")
    U = (-n**3 * (3*n - 2) * (n + 1)**4 * d * (1 + m*d)**3 * x**4
         - 4*n**2 * (n + 1)**2 * (1 + m*d)**2 * ((n + 1)*(3*n - 2)*m*d - n**2) * x**3
         + 4*(n + 1)*(1 + m*d) * (m*(n - 2)*(n - 4)*(n + 1)*(m + n**2)*d
                                   + 4*n*(2*n**2 - 3*n + 4)*m
                                   + n**2*(n - 2)*(n - 4)*(n + 1)) * x**2
         - 16*m * ((n + 1)*m*(-4*m + 3*n**2*(n - 2))*d
                   + 3*n*(n - 4)*m + 3*n**2*(n + 1)*(n - 2)) * x
         + 64*m**3 + 16*n*(n + 2)*m**2)
    H = m + sp.Rational(1, 2) * n * (n + 1) * (1 + m * d) * x
    ell = sp.symbols("ell")
    m_v = (ell - 1) * (ell + n)
    d_v = 1 / ((n + 1) * (ell + n))
    H2 = sp.expand(H.subs({m: m_v, d: d_v, x: 2}))
    U2 = sp.expand(U.subs({m: m_v, d: d_v, x: 2}))
    claimH = (ell + n) * (ell + n - 1)
    assert sp.cancel(H2 - claimH) == 0, (sp.factor(H2),)
    claimU = 64 * ell * (ell - n + 1) * claimH**2
    assert sp.cancel(U2 - claimU) == 0
    print("EXT: H_-(x_H) = (l+n)(l+n-1), U_-(x_H) = 64 l (l-n+1) H_-(x_H)^2, "
          "symbolic in (ell, n): OK")


def check_case(n, ell):
    ctx = Ctx(ell, n)
    F, Den, E = build_F(ctx)
    mlo = mu_lo_of(ctx)
    Bc = 2 * ell + n - 1
    A = (ell + n) + (ell - 1) * mlo * mlo
    q2 = 1 - Fraction(Bc * Bc) * mlo * mlo / (A * A)
    assert q2 >= Q99**2
    Den_f = {k: fmpq(v.numerator, v.denominator) for k, v in Den.items()}
    okD, _ = verify_1d(Den_f, fmpq(0), fmpq(mlo.numerator, mlo.denominator))
    assert okD
    F2 = to_fmpq2(F)
    if ell == n - 1:
        t, mu, s = sp.symbols("t mu s")
        Fsp = sp.expand(sum(sp.Rational(c.numerator, c.denominator) * t**i * mu**j
                            for i, poly in F.items() for j, c in poly.items()))
        F1 = sp.expand(Fsp.subs(t, 1))
        K = sp.div(F1, mu)[0]
        assert sp.expand(F1 - mu * K) == 0
        Fs = sp.expand(Fsp.subs(t, 1 - s))
        G = sp.div(sp.expand(Fs - F1), s)[0]
        assert sp.expand(Fs - F1 - s * G) == 0
        K1 = {i: fmpq(str(sp.Rational(K.coeff(mu, i)))) for i in range(sp.degree(K, mu) + 1)
              if K.coeff(mu, i) != 0}
        okK, _ = verify_1d(K1, fmpq(0), fmpq(mlo.numerator, mlo.denominator))
        G2 = {}
        for i in range(sp.degree(G, s) + 1):
            for j in range(sp.degree(G, mu) + 1):
                c = G.coeff(s, i).coeff(mu, j)
                if c != 0:
                    G2[(i, j)] = fmpq(str(sp.Rational(c)))
        okG, _ = verify_2d(G2, fmpq(0), fmpq(1), fmpq(0),
                           fmpq(mlo.numerator, mlo.denominator))
        return okK and okG, {"split": True, "K>0": okK, "G>0": okG, "mu_lo": str(mlo)}
    else:
        okF, iF = verify_2d(F2, fmpq(0), fmpq(1), fmpq(0),
                            fmpq(mlo.numerator, mlo.denominator))
        return okF, {"strict": okF, "mu_lo": str(mlo), "nodes": iF.get("nodes")}


def main():
    ext_gate_symbolic()
    results = {}
    for n in range(5, 10):
        for ell in range(n - 1, L0[n] + 1):
            ok, info = check_case(n, ell)
            results[f"{n + 2}-{ell}"] = {"ok": ok, **{k: str(v) for k, v in info.items()}}
            print(f"D={n + 2} l={ell}: {'POSITIVE' if ok else 'REJECT'} {info}", flush=True)
    with open(os.path.join(HERE, "hdxe_results.json"), "w") as fh:
        json.dump(results, fh, indent=1)
    bad = [k for k, v in results.items() if not v["ok"]]
    print("HD-X-E:", "ALL OK" if not bad else f"FAILURES: {bad}")
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
