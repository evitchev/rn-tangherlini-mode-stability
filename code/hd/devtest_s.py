"""Development tests of hd.scert, run before registration (results/hd/s/PREREG.md section 8).  Synthetic inputs only:
S5's U_- and H_- are not evaluated for any band, and no gate, control or band is run.

    python -m hd.devtest_s
"""
import time
from fractions import Fraction

import sympy as sp

from hd.scert import Exact, design_box, inward, partition, verify_box, w_exact
from ki.potentials import d, m, x
from onset.bernstein import prove_sign
from qnm1c.common import CertificateError

USYN = 64 * m ** 3 + 400 * x ** 2 + x ** 4
HSYN = m + 15 * x
FSYN = (lambda mm, dd, xx: 64 * mm ** 3 + 400 * xx ** 2 + xx ** 4, lambda mm, dd, xx: mm + 15 * xx)


def main():
    n, ell = 5, 4
    print("partition (n, l) = (5, 4), q in [0, 99/100]:", len(partition(n, ell, Fraction(99, 100), Fraction(0))), "boxes;",
          "first", partition(n, ell, Fraction(99, 100), Fraction(0))[0])
    print("inward decimals of [sqrt(1/4), sqrt(98/100)]:", inward(Fraction(1, 4), Fraction(98, 100)))
    print("w at mu = 1:", w_exact(n, ell, Fraction(1)))
    t0 = time.time()
    E = Exact(n, ell, "none", UH=(USYN, HSYN))
    print(f"synthetic exact parts: {time.time() - t0:.1f} s; degrees Un {E.Un.degree(sp.Symbol('z'))}, "
          f"HU {E.HU.degree(sp.Symbol('z'))}")
    box = (Fraction(1, 2), Fraction(11, 20))
    for var, deg in (("z", 16), ("zeta", 16)):
        t0 = time.time()
        Phat, s, e, db, plan = design_box(n, ell, box, var, deg, Fraction(1, 50), funcs=FSYN)
        t1 = time.time()
        stats = {}
        try:
            info = verify_box(E, Phat, s, e, box, prove_sign, stats, f"synthetic {var}")
            verdict = f"VERIFIED {info}"
        except CertificateError as exc:
            verdict = f"REJECT {exc}"[:200]
        print(f"synthetic box {box}, {var} {deg}: design {t1 - t0:.1f} s, verify {time.time() - t1:.1f} s, "
              f"delta_b {db}, Bernstein {stats}: {verdict}")
        print("   planning (first node):", {k: plan[0][k] for k in ("mu", "min_psi1", "sigma_design", "sigma_fit")})
        bump = sp.Poly(sp.Rational(-1000) * sp.Symbol("z") * (1 - sp.Symbol("z")), *Phat.gens)
        try:
            verify_box(E, Phat - bump * (1 if e == 0 else s ** e), s, e, box, prove_sign, {}, "tampered")
            print("   tampered certificate: VERIFIED (unexpected)")
        except CertificateError as exc:
            print("   tampered certificate (P + 1000 z(1 - z)): REJECT", str(exc)[:160])


if __name__ == "__main__":
    main()
