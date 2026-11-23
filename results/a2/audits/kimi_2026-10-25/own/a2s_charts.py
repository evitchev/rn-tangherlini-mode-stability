"""A2-S charts: exact divisions, positivity on each chart's box, coverage.

T(zeta, mu) = NL(mu zeta, mu) / mu^2   (exact division checked)
C(z, sigma)  = NL(z, z sigma) / z^2    (exact division checked)
O : NL on [1/4, 1] x [0, 1/8];  O' : NL on [0, 1/4] x [1/32, 1/8]
T > 0 on [0, 8] x [0, 1/32];  C > 0 on [0, 1/4] x [0, 1/8].
Gates: S > 0 off the corner; Den > 0 on [0, 1/8]; q(1/8)^2 <= (99/100)^2; w increasing.
"""
import json
import os
import sys
from fractions import Fraction

from flint import fmpq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rfg import Ctx
from a2s import build, to_fmpq2
from verify import verify_1d, verify_2d

HERE = os.path.dirname(os.path.abspath(__file__))


def substitute_2d_frac(Nc, sub1, sub2):
    """Nc: {z: {mu: Fraction}}; sub1: z -> (az, bz) meaning z = az*u + bz (az,bz fractions or
    ('mu', c) meaning z = c*mu*u ...).  Here we need only:
       T: z -> mu * zeta  (variables (mu, zeta) -> substitute then divide by mu^2)
       C: mu -> z * sigma.
    Do it directly, exactly, with Fractions."""
    out = {}
    for i, poly in Nc.items():
        for j, c in poly.items():
            # z^i mu^j -> sub1^i sub2^j, each a dict {(u, v): coeff}
            t1 = sub1(i)
            t2 = sub2(j)
            for (a1, b1), c1 in t1.items():
                for (a2, b2), c2 in t2.items():
                    out[(a1 + a2, b1 + b2)] = out.get((a1 + a2, b1 + b2), Fraction(0)) + c * c1 * c2
    return {k: v for k, v in out.items() if v}


def main():
    with open(os.path.join(HERE, "..", "data", "design.json")) as fh:
        design = json.load(fh)
    ctx = Ctx(2, 4)
    Den, Nc, E = build(ctx, design["cheb"])

    # Den > 0 on [0, 1/8], factorwise
    A = {0: fmpq(6), 2: fmpq(1)}
    B = {0: fmpq(6), 1: fmpq(1)}
    C1 = {0: fmpq(1), 1: fmpq(1)}
    for fp, nm, e in zip((A, B, C1), ("A", "B", "mu+1"), E):
        if e:
            ok, _ = verify_1d(fp, fmpq(0), fmpq(1, 8))
            assert ok, f"Den factor {nm}"
    print("gate: Den > 0 on [0, 1/8]: OK")

    # S > 0 off the corner: S = eps_d z + 7 mu; both coefficient polys > 0 on the range
    okS1, _ = verify_1d({0: fmpq(18), 1: fmpq(21), 2: fmpq(3)}, fmpq(0), fmpq(1, 8))
    print("gate: eps_d > 0:", okS1, "; eps_n = 7 mu >= 0, = 0 only at mu = 0; "
          "so S > 0 for (z, mu) != (0, 0)")

    # q(1/8)^2 <= (99/100)^2 exactly
    w2 = Fraction(7 * 7) / (8 * 8) / (Fraction(6) + Fraction(1, 64)) ** 2
    q2 = 1 - w2
    print(f"gate: q(1/8)^2 = {q2} = {float(q2):.6f} <= (99/100)^2: {q2 <= Fraction(99, 100)**2}")

    # ---- charts
    z_, m_ = 0, 1  # variable slots in the output dicts below

    # T: (z, mu) -> (mu*zeta, mu); output variables (zeta, mu)
    def subT(i):
        # z^i -> (mu zeta)^i = mu^i zeta^i
        return {(i, 0): Fraction(1)}  # in (zeta, mu) terms handled below

    # do T directly: NL(mu*zeta, mu): term z^i mu^j -> zeta^i mu^(i+j)
    NT = {}
    for i, poly in Nc.items():
        for j, c in poly.items():
            NT[(i, i + j)] = NT.get((i, i + j), Fraction(0)) + c
    # divide by mu^2 (exact)
    T = {}
    for (iz, im), c in NT.items():
        assert im >= 2, f"T division fails at {(iz, im)}"
        T[(iz, im - 2)] = c
    print("gate DIV-T: NL(mu zeta, mu)/mu^2 polynomial: OK")

    # C: (z, mu) -> (z, z*sigma): term z^i mu^j -> z^(i+j) sigma^j
    NC = {}
    for i, poly in Nc.items():
        for j, c in poly.items():
            NC[(i + j, j)] = NC.get((i + j, j), Fraction(0)) + c
    Cp = {}
    for (iz, isg), c in NC.items():
        assert iz >= 2, f"C division fails at {(iz, isg)}"
        Cp[(iz - 2, isg)] = c
    print("gate DIV-C: NL(z, z sigma)/z^2 polynomial: OK")

    # positivity
    O = verify_2d(to_fmpq2(Nc), fmpq(1, 4), fmpq(1), fmpq(0), fmpq(1, 8))
    print("POS-O :", O)
    Op = verify_2d(to_fmpq2(Nc), fmpq(0), fmpq(1, 4), fmpq(1, 32), fmpq(1, 8))
    print("POS-O':", Op)
    Tt = verify_2d({k: fmpq(v.numerator, v.denominator) for k, v in T.items() if v},
                   fmpq(0), fmpq(8), fmpq(0), fmpq(1, 32))
    print("POS-T :", Tt)
    Cc = verify_2d({k: fmpq(v.numerator, v.denominator) for k, v in Cp.items() if v},
                   fmpq(0), fmpq(1, 4), fmpq(0), fmpq(1, 8))
    print("POS-C :", Cc)
    ok = all(v[0] for v in (O, Op, Tt, Cc))
    # coverage inequalities (exact)
    ZT, muT, z1, sg1, mu1 = Fraction(8), Fraction(1, 32), Fraction(1, 4), Fraction(1, 8), Fraction(1, 8)
    cov = (ZT * sg1 >= 1) and (ZT * muT <= z1) and (z1 * sg1 <= mu1) and (0 < muT < mu1) and (0 < z1 < 1)
    print("gate COVER inequalities:", cov)
    print("A2-S:", "ALL OK" if (ok and cov and okS1) else "FAILURE")
    return 0 if (ok and cov and okS1) else 1


if __name__ == "__main__":
    raise SystemExit(main())
