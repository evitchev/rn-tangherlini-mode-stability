"""Kimi's own derivation for the onset audit (BHM-017).

U_-(x; mu) for D = 6, ell = 2 from KI (5.63b) (my transcription, cross-checked in the p3
audit), x = t x_H(mu).  F(t, mu) = numerator after clearing mu-denominators.
g(mu) = F(1, mu)  (horizon value, up to the positive Den).

All exact.  Sturm counts are mine (polynomial remainder sequences over QQ).
"""
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rf import (rf_const, rf_mul, rf_add, rf_sub, rf_scale, p_mul, p_add, p_pow,
                p_eval, p_divmod, common_den, den_poly, clear, FACTORS)

HERE = os.path.dirname(os.path.abspath(__file__))


def D6_blocks():
    one = rf_const(1)
    delta = ({0: Fraction(1, 5), 2: Fraction(-1, 5)}, (1, 0, 0))
    md = rf_scale(delta, 6)
    one_md = rf_add(one, md)
    xH = ({0: Fraction(12), 2: Fraction(2)}, (0, 1, 1))
    q2 = ({0: Fraction(36), 2: Fraction(-37), 4: Fraction(1)}, (2, 0, 0))
    return delta, md, one_md, xH, q2


def U_in_t():
    """U_-(t x_H) as dict {t_exp: rf} for D=6, ell=2."""
    delta, md, one_md, xH, q2 = D6_blocks()
    U0 = rf_const(27648)
    U1 = rf_scale(rf_add(rf_scale(delta, 2160), rf_const(480)), -96)
    U2 = rf_scale(one_md, 46080)
    U3 = rf_scale(rf_mul(rf_mul(one_md, one_md),
                         rf_sub(rf_scale(delta, 300), rf_const(16))), -1600)
    U4 = rf_scale(rf_mul(delta, rf_mul(rf_mul(one_md, one_md), one_md)), -400000)
    Uk = [U0, U1, U2, U3, U4]
    xHk = [rf_const(1)]
    for _ in range(4):
        xHk.append(rf_mul(xHk[-1], xH))
    return {k: rf_mul(Uk[k], xHk[k]) for k in range(5)}


def build_F():
    """F(t, mu): dict {t: {mu_exp: Fraction}} with U_- = F / Den."""
    U = U_in_t()
    E = common_den(U)
    Den = den_poly(E)
    F = clear(U, E)
    return F, Den, E


# ---------- my Sturm over QQ ----------

def p_diff(a):
    return {k - 1: k * v for k, v in a.items() if k >= 1}


def p_rem(a, b):
    """Remainder of a modulo b over QQ."""
    a = dict(a)
    db = max(b)
    lb = b[db]
    while a and max(a) >= db:
        k = max(a) - db
        c = a[max(a)] / lb
        for j, vj in b.items():
            a[k + j] = a.get(k + j, Fraction(0)) - c * vj
            if a[k + j] == 0:
                del a[k + j]
    return a


def sturm_seq(p):
    seq = [p, p_diff(p)]
    while seq[-1]:
        seq.append({k: -v for k, v in p_rem(seq[-2], seq[-1]).items()})
    return seq[:-1]


def sign_variations(seq, t):
    vals = [p_eval(s, t) for s in seq]
    vals = [v for v in vals if v != 0]
    return sum(1 for i in range(len(vals) - 1) if vals[i] * vals[i + 1] < 0)


def sturm_count(p, a, b):
    """Number of distinct real roots in (a, b]... standard: V(a) - V(b), roots at
    endpoints handled by convention: we use [a, b] with exact endpoint checks outside."""
    seq = sturm_seq(p)
    return sign_variations(seq, a) - sign_variations(seq, b)


def isolate(p, a, b, width):
    """Bisect [a,b] (known to contain exactly one root) to the given width."""
    fa = p_eval(p, a)
    assert fa * p_eval(p, b) < 0
    while b - a > width:
        m = (a + b) / 2
        fm = p_eval(p, m)
        if fm == 0:
            return m, m
        if fa * fm < 0:
            b = m
        else:
            a, fa = m, fm
    return a, b
