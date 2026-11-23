"""HD-E controls (Kimi):
(a) horizon band past its onset: D = 7, l = 2, q <= 951/1000 (onset ~ 0.9497) -> REJECT,
    counterexample expected at the horizon corner t = 1;
(b) interior band past its onset: D = 10, l = 3, q <= 99/200 (onset ~ 0.4913) -> REJECT,
    counterexample expected at an interior point 0 < t < 1;
(c) planted negative region: D = 7, l = 4 with U_- - 10^7 * 64 t^3 (1-t)^3 * Den -> REJECT;
(d) verifier tamper -> caught by the KAT suite.
"""
import os
import sys
from fractions import Fraction

from flint import fmpq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rfg import Ctx
from hd import build_F, mu_lo_of, to_fmpq2, param_checks
from verify import verify_1d, verify_2d, kat


def eval_F_at(F, t0, mu0):
    v = Fraction(0)
    for t, poly in F.items():
        for j, c in poly.items():
            v += c * t0**t * mu0**j
    return v


def run_case(n, ell, q_hi):
    ctx = Ctx(ell, n)
    param_checks(ctx)
    F, Den, E = build_F(ctx)
    mlo = mu_lo_of(ctx, q_hi)
    Den_f = {k: fmpq(v.numerator, v.denominator) for k, v in Den.items()}
    okD, _ = verify_1d(Den_f, fmpq(mlo.numerator, mlo.denominator), fmpq(1))
    okF, iF = verify_2d(to_fmpq2(F), fmpq(0), fmpq(1),
                        fmpq(mlo.numerator, mlo.denominator), fmpq(1))
    corner = eval_F_at(F, Fraction(1), mlo)
    centre = eval_F_at(F, Fraction(1, 2), mlo)
    return okF, iF, corner, centre, mlo


def main():
    # (a) horizon band past onset
    okF, iF, corner, centre, mlo = run_case(5, 2, Fraction(951, 1000))
    print(f"(a) D=7 l=2 q<=951/1000: F(1,mu_lo={mlo}) = {corner}  (<0: {corner < 0}); "
          f"verdict: {'REJECT (correct)' if not okF else 'PASS (BAD)'}; info={iF}")
    ok_a = (corner < 0) and not okF

    # (b) interior band past onset
    okF, iF, corner, centre, mlo = run_case(8, 3, Fraction(99, 200))
    print(f"(b) D=10 l=3 q<=99/200: verdict {'REJECT (correct)' if not okF else 'PASS (BAD)'}; "
          f"info={iF}; corner F(1,mu_lo)={corner}; F(1/2,mu_lo)={float(centre):.3f}")
    wit = iF.get("z")
    ok_b = (not okF) and wit is not None and fmpq(wit) not in (fmpq(0), fmpq(1))

    # (c) planted negative region: D=7, l=4, U_- minus a bump
    ctx = Ctx(4, 5)
    F, Den, E = build_F(ctx)
    mlo = mu_lo_of(ctx, Fraction(99, 100))
    from math import comb
    Fb = {t: dict(poly) for t, poly in F.items()}
    for k in range(4):
        t_pow = 3 + k
        c = Fraction((-1) ** k * comb(3, k)) * Fraction(10**7 * 64)
        cur = Fb.setdefault(t_pow, {})
        for j, dv in Den.items():
            cur[j] = cur.get(j, Fraction(0)) - c * dv
    Fb = {t: {j: v for j, v in poly.items() if v} for t, poly in Fb.items() if poly}
    mid = eval_F_at(Fb, Fraction(1, 2), mlo)
    okB, iB = verify_2d(to_fmpq2(Fb), fmpq(0), fmpq(1),
                        fmpq(mlo.numerator, mlo.denominator), fmpq(1))
    print(f"(c) planted bump D=7 l=4: F(1/2,mu_lo)={float(mid):.2f}; "
          f"verdict {'REJECT (correct)' if not okB else 'PASS (BAD)'}; info={iB}")
    ok_c = not okB

    # (d) verifier tamper: KAT suite
    ok_d = kat()

    print("CONTROLS:", "ALL OK" if (ok_a and ok_b and ok_c and ok_d) else "FAILURE")
    return 0 if (ok_a and ok_b and ok_c and ok_d) else 1


if __name__ == "__main__":
    raise SystemExit(main())
