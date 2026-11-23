"""Controls for the a1 audit (Kimi).

(a) ell = 2 on q <= 99/100 must REJECT (BHM-017 O3: U_-(x_H) < 0 above q_*).
(b) ell = 3 with a planted negative region: U_- - 10^7*64 t^3 (1-t)^3 must REJECT
    (expect a counterexample near t = 1/2).
(c) verifier tamper: the KAT suite of verify.py, incl. the tampered-verifier drill.
"""
import os
import sys
from fractions import Fraction

from flint import fmpq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rfg import Ctx
from part1 import build_F, mu_lo_of, to_fmpq2
from verify import verify_2d, kat

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "runs")


def eval_F_at(F, t0, mu0):
    """Exact value of F(t0, mu0) (Fractions)."""
    v = Fraction(0)
    for t, poly in F.items():
        for j, c in poly.items():
            v += c * t0**t * mu0**j
    return v


def main():
    # (a) ell = 2
    ctx2 = Ctx(2)
    F2, Den2, E2 = build_F(ctx2)
    mlo2 = mu_lo_of(ctx2)
    # exact corner value F(1, mu_lo) — the predicted counterexample
    corner = eval_F_at(F2, Fraction(1), mlo2)
    print(f"control (a): ell=2, mu_lo={mlo2}, F(1, mu_lo) = {corner} < 0: {corner < 0}")
    okF, info = verify_2d(to_fmpq2(F2), fmpq(0), fmpq(1),
                          fmpq(mlo2.numerator, mlo2.denominator), fmpq(1))
    print("control (a): verifier verdict:", "REJECT (correct)" if not okF else "PASS (BAD)",
          str(info)[:160])
    ok_a = (corner < 0) and not okF

    # (b) planted negative region at ell = 3
    ctx3 = Ctx(3)
    F3, Den3, E3 = build_F(ctx3)
    mlo3 = mu_lo_of(ctx3)
    # subtract 10^7 * 64 * t^3 (1-t)^3 * Den (so that U_- loses 10^7*64 t^3(1-t)^3)
    from math import comb
    Fb = {t: dict(poly) for t, poly in F3.items()}
    for k in range(4):
        t_pow = 3 + k
        c = Fraction((-1) ** k * comb(3, k)) * Fraction(10**7 * 64)
        cur = Fb.setdefault(t_pow, {})
        for j, dv in Den3.items():
            cur[j] = cur.get(j, Fraction(0)) - c * dv
    Fb = {t: {j: v for j, v in poly.items() if v} for t, poly in Fb.items()}
    Fb = {t: poly for t, poly in Fb.items() if poly}
    mid = eval_F_at(Fb, Fraction(1, 2), mlo3)
    print(f"control (b): ell=3 with planted bump, F(1/2, mu_lo) = {float(mid):.4f} (<0: {mid < 0})")
    okB, infoB = verify_2d(to_fmpq2(Fb), fmpq(0), fmpq(1),
                           fmpq(mlo3.numerator, mlo3.denominator), fmpq(1))
    print("control (b): verifier verdict:", "REJECT (correct)" if not okB else "PASS (BAD)",
          str(infoB)[:160])
    ok_b = not okB

    # (c) verifier tamper (KAT suite incl. tampered-verifier drill)
    ok_c = kat()

    print("CONTROLS:", "ALL OK" if (ok_a and ok_b and ok_c) else "FAILURE")
    return 0 if (ok_a and ok_b and ok_c) else 1


if __name__ == "__main__":
    raise SystemExit(main())
