"""Lemma U(n) at general n, Kimi's own derivation.

P_n(eps, kap, x) := eps^6 U_-(x; m = eps^-2, delta = kap eps) at general n (my KI (5.63b)
transcription).  Split Pos_n - Neg_n, Pos_n(0) = 64, and the corner bound
64 - Neg_n(eps_bar, 1/(n+1), 2) > 0 in exact rationals, with eps_bar = 1/isqrt(m(l0+1));
l0(n) = least l0 >= max(l_el(n), 10), searched up to 400, at which the bound is > 0.
"""
import sys
from fractions import Fraction

import sympy as sp

sys.path.insert(0, "[kimi-folder]/bhm-p3-audit-2026-10-22/own")
from build import ki_Usymbol

eps, kap, x = sp.symbols("eps kap x")
m_ = eps**-2
d_ = kap * eps

L_EL = {5: 4, 6: 5, 7: 6, 8: 6, 9: 7}   # n -> ell_el


def isqrt(a):
    r = sp.integer_nthroot(a, 2)[0]
    return int(r)


def lemmaU(n):
    Ux, Hx = ki_Usymbol(n)
    U = sp.expand(Ux.subs({sp.Symbol("m"): m_, sp.Symbol("d"): d_}))
    P = sp.expand(eps**6 * U)
    poly = sp.Poly(P, eps, kap, x)
    terms = poly.terms()
    assert all(i >= 0 for (i, j, k), c in terms), "negative eps power: not a polynomial"
    pos, neg = {}, {}
    for key, c in terms:
        c = sp.Rational(c)
        (pos if c >= 0 else neg)[key] = abs(c)
    def evald(dic, e0, k0, x0):
        return sum(c * e0**i * k0**j * x0**k for (i, j, k), c in dic.items())
    assert evald(pos, 0, 0, 0) == 64
    # search l0
    l0 = None
    for cand in range(max(L_EL[n], 10), 401):
        m0 = cand * (cand + 1 + n)   # m(l0+1) = l0 (l0 + 1 + n)
        eb = Fraction(1, isqrt(m0))
        val = evald(neg, sp.Rational(eb.numerator, eb.denominator),
                    sp.Rational(1, n + 1), sp.Rational(2))
        if 64 - val > 0:
            l0 = cand
            break
    bound = None
    if l0 is not None:
        m0 = l0 * (l0 + n + 1)
        eb = Fraction(1, isqrt(m0))
        val = evald(neg, sp.Rational(eb.numerator, eb.denominator),
                    sp.Rational(1, n + 1), sp.Rational(2))
        bound = 64 - val
    return {"n": n, "l0": l0, "eps_bar": str(eb) if l0 else None,
            "Neg_corner": str(val) if l0 else None,
            "bound": str(bound) if l0 else None,
            "bound_float": float(bound) if l0 else None,
            "terms": len(terms)}


def main():
    out = {}
    for n in range(5, 10):
        r = lemmaU(n)
        out[n] = r
        print(f"n={n}: terms={r['terms']} l0={r['l0']} eps_bar={r['eps_bar']} "
              f"Neg_corner={r['Neg_corner']} bound={r['bound']} ({r['bound_float']})",
              flush=True)
    import json, os
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "lemmaU_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    ok = all(r["l0"] is not None and r["bound_float"] > 0 for r in out.values())
    print("LEMMA U(n):", "ALL PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
