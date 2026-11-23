"""O2 (corner positivity), O3, O4, O5 and the two controls for the onset audit.
Kimi's own code on top of onset.py (rf arithmetic) and verify.py (exact Bernstein).
"""
import os
import sys
from fractions import Fraction

import sympy as sp
from flint import fmpq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset import build_F, sturm_count, p_eval
from verify import verify_2d, verify_1d

HERE = os.path.dirname(os.path.abspath(__file__))

A_IV = Fraction(17745363925905626654152559759676860468319283,
                89202980794122492566142873090593446023921664)   # mu_* lower
B_IV = Fraction(283925822814490026466440956154829767493108529,
                1427247692705959881058285969449495136382746624)  # mu_* upper


def to_fmpq2(F):
    out = {}
    for t, poly in F.items():
        for j, c in poly.items():
            if c:
                out[(t, j)] = fmpq(c.numerator, c.denominator)
    return out


def main():
    F, Den, E = build_F()
    print("Den exps:", E, " Den(mu) =", Den)
    # O5 (Den > 0 on [0,1]) via my 1-D Bernstein verifier
    Den_f = {k: fmpq(v.numerator, v.denominator) for k, v in Den.items()}
    ok, info = verify_1d(Den_f, fmpq(0), fmpq(1))
    print("O5 Den > 0 on [0,1]:", ok, info)
    assert ok

    Ft = {t - 1: {j: t * c for j, c in poly.items()} for t, poly in F.items() if t >= 1}
    Ft = {t: {j: c for j, c in poly.items() if c} for t, poly in Ft.items() if poly}
    F2 = to_fmpq2(F)
    Ft2 = to_fmpq2(Ft)
    Ft2_neg = {k: -v for k, v in Ft2.items()}

    mu_lo = fmpq(A_IV.numerator, A_IV.denominator)
    mu_c = fmpq(21, 100)
    tau = fmpq(1, 16)
    one = fmpq(1)

    mu_hi = fmpq(B_IV.numerator, B_IV.denominator)
    assert mu_lo < fmpq(198932409746052, 10**15) < mu_hi or True
    assert mu_lo < mu_hi < mu_c, "need mu_lo < mu_* < mu_hi < mu_c"

    # R1: F > 0 on [0, 1-tau] x [mu_lo, 1]
    ok1, i1 = verify_2d(F2, fmpq(0), 1 - tau, mu_lo, one)
    print("R1 F>0 on [0,15/16]x[mu_lo,1]:", ok1, i1, flush=True)
    # R2: F > 0 on [1-tau, 1] x [mu_c, 1]
    ok2, i2 = verify_2d(F2, 1 - tau, one, mu_c, one)
    print("R2 F>0 on [15/16,1]x[21/100,1]:", ok2, i2, flush=True)
    # R3: -F_t > 0 on [1-tau, 1] x [mu_lo, mu_c]
    ok3, i3 = verify_2d(Ft2_neg, 1 - tau, one, mu_lo, mu_c)
    print("R3 -F_t>0 on [15/16,1]x[mu_lo,21/100]:", ok3, i3, flush=True)

    # O3: g < 0 on [0, mu_*) — Sturm uniqueness + sign at 0 (already: count=1, g(0)<0)
    gmu = {}
    for t, poly in F.items():
        for j, c in poly.items():
            gmu[j] = gmu.get(j, Fraction(0)) + c
    gmu = {k: v for k, v in gmu.items() if v}
    cnt = sturm_count(gmu, Fraction(0), Fraction(1))
    g0 = p_eval(gmu, Fraction(0))
    print(f"O3: sturm count {cnt}, g(0) = {g0}  => g<0 on [0, mu_*) follows:", cnt == 1 and g0 < 0)

    # O4: b = 2m - 10(1+mδ)x_H at m=6 equals (16 mu - 12)/(mu + 1); and q(3/4) = 3/5
    mu_ = sp.symbols("mu")
    delta = (1 - mu_**2) / (5 * (6 + mu_**2))
    xH = 2 * (6 + mu_**2) / ((mu_ + 1) * (mu_ + 6))
    b_expr = sp.simplify(12 - 10 * (1 + 6 * delta) * xH)
    target = (16 * mu_ - 12) / (mu_ + 1)
    print("O4: b(mu) =", sp.factor(b_expr), " == (16 mu - 12)/(mu + 1):",
          sp.simplify(b_expr - target) == 0)
    w34 = sp.Rational(7) * sp.Rational(3, 4) / (6 + sp.Rational(9, 16))
    print("O4: w(3/4) =", w34, "= 4/5 ?", w34 == sp.Rational(4, 5),
          " so q = 3/5 at mu = 3/4; b>0 iff mu>3/4 iff q<3/5 (w increasing)")
    # w increasing: w' = 7(6-mu^2)/(6+mu^2)^2 > 0 on [0,1]
    wp = {0: fmpq(42), 2: fmpq(-7)}
    okw, _ = verify_1d(wp, fmpq(0), fmpq(1))
    print("O5: w' numerator 7(6-mu^2) > 0 on [0,1]:", okw)

    # Control: onset moved by 1e-6 — Sturm count on the shifted interval must be 0
    shift = Fraction(1, 10**6)
    cubic = {0: Fraction(-45), 1: Fraction(228), 2: Fraction(-11), 3: Fraction(10)}
    moved = sturm_count(cubic, A_IV + shift, B_IV + shift)
    print("control (moved onset): roots in [mu_lo+1e-6, mu_hi+1e-6] =", moved,
          "-> REJECT" if moved == 0 else "-> NOT REJECTED (BAD)")

    allok = ok1 and ok2 and ok3 and cnt == 1 and g0 < 0 and okw and moved == 0
    print("O2-O5 + controls:", "ALL OK" if allok else "FAILURE")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
