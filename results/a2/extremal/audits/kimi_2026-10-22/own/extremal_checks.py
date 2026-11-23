"""Kimi's own checks of E0-E5 (extremal, D=6, q=1, M=1) as identities in ell.

E0 is already established symbolically in my p3 audit (build.py: KI (5.62b)/(5.63b) at n=4
== TARGET.md identically in (x, m, delta)); the relevant output is re-run here for the record.
"""
import os
import sys

import sympy as sp

sys.path.insert(0, "[kimi-folder]/bhm-p3-audit-2026-10-22/own")
from build import ki_Usymbol, target_UH_D6  # my own transcription, p3 audit

ell = sp.symbols("ell", integer=True, positive=True)
x, r = sp.symbols("x r")
m = (ell - 1) * (ell + 4)


def main():
    # ---- E0 (re-run of my p3 transcription check)
    U4, H4 = ki_Usymbol(4)
    Ut, Ht = target_UH_D6()
    assert sp.expand(U4 - Ut) == 0 and sp.expand(H4 - Ht) == 0
    print("E0: KI (5.62b)/(5.63b) at n=4 == TARGET.md (symbolic in x, m, delta): PASS")

    # ---- E1
    lhs = sp.expand(25 + 4 * m)
    rhs = (2 * ell + 3) ** 2
    assert sp.expand(lhs - rhs) == 0
    delta = 1 / (5 * (ell + 4))
    s = sp.simplify(1 + 2 * m * delta)
    assert sp.simplify(s - (2 * ell + 3) / 5) == 0
    # branch: s > 0 for ell >= 2
    assert sp.simplify(s.subs(ell, 2)) > 0
    # and s^2 = 1 + 4 m q^2/25 at q=1:
    assert sp.simplify(s**2 - (1 + 4 * m / 25)) == 0
    print("E1: 25+4m = (2l+3)^2; 1+2m*delta = (2l+3)/5 > 0; s^2 = 1+4m/25: PASS")

    # ---- U_-, H_- at q = 1 (delta above), as functions of x, ell
    Ux, Hx = ki_Usymbol(4)
    U_q1 = sp.expand(Ux.subs({sp.Symbol("m"): m, sp.Symbol("d"): delta}))
    H_q1 = sp.expand(Hx.subs({sp.Symbol("m"): m, sp.Symbol("d"): delta}))

    # ---- E2
    f = 1 - x + x**2 / 4          # q = 1, x = 2/r^3
    assert sp.expand(f - (1 - x / 2) ** 2) == 0
    fr = f.subs(x, 2 / r**3)
    print("E2: f = (1 - r^-3)^2:", sp.simplify(fr - (1 - r**-3)**2) == 0, "; f(1) =", fr.subs(r, 1))
    ratio = sp.cancel((r - 1) ** 2 / fr).together()
    num, den = sp.fraction(sp.cancel(ratio))
    print("E2: (r-1)^2/f =", sp.factor(num), "/", sp.factor(den),
          " value at r=1:", sp.Rational(num.subs(r, 1)) / den.subs(r, 1))
    assert num.subs(r, 1) * 9 == den.subs(r, 1)
    print("E2: PASS")

    # ---- E3
    U2 = sp.expand(U_q1.subs(x, 2))
    H2 = sp.expand(H_q1.subs(x, 2))
    c = sp.simplify(U2 / (576 * H2**2))
    claim = ell * (ell - 3) / 9
    print("E3: c(ell) =", sp.factor(c), " claimed:", claim,
          " equal:", sp.simplify(c - claim) == 0)
    assert sp.simplify(c - claim) == 0

    # ---- E4
    e4 = sp.simplify(c + sp.Rational(1, 4))
    claim4 = (2 * ell - 3) ** 2 / 36
    assert sp.simplify(e4 - claim4) == 0
    print("E4: c + 1/4 = (2l-3)^2/36: PASS")

    # ---- E5: indicial exponents at r = 1
    # equation psi'' + (f'/f) psi' - (V/f^2) psi = 0; V = f U/(64 r^2 H^2)
    # regular singular: p1 = lim (r-1) f'/f,  q2 = lim (r-1)^2 V/f^2 = c
    fp = sp.diff(fr, r)
    p1 = sp.simplify((r - 1) * fp / fr)
    print("E5: (r-1) f'/f =", sp.factor(p1), " -> at r=1:", p1.subs(r, 1))
    # (r-1)^2 V/f^2 = U(r) r^4 / (64 H(r)^2 (r^2+r+1)^2), since 1/f = r^6/((r-1)^2 (r^2+r+1)^2)
    Ur = U_q1.subs(x, 2 / r**3)
    Hr = H_q1.subs(x, 2 / r**3)
    q2_clean = sp.cancel(Ur * r**4 / (64 * Hr**2 * (r**2 + r + 1) ** 2))
    qn, qd = sp.fraction(q2_clean)
    q2_at_1 = sp.simplify(qn.subs(r, 1) / qd.subs(r, 1))
    print("E5: (r-1)^2 V/f^2 =", "rational function, regular at r=1; value there:",
          sp.factor(q2_at_1), " == c(ell):", sp.simplify(q2_at_1 - c) == 0)
    assert sp.simplify(q2_at_1 - c) == 0
    # indicial equation s(s-1) + p1(1) s - q2(1) = 0
    s = sp.symbols("s")
    ind = sp.expand(s * (s - 1) + 2 * s - c)
    roots = sp.solve(sp.Eq(ind, 0), s)
    print("E5: indicial exponents:", [sp.simplify(t) for t in roots])
    expected = {(ell - 3) / 3, -ell / 3}
    assert {sp.simplify(t) for t in roots} == {sp.simplify(t) for t in expected}
    print("E5: PASS")

    print("E0-E5: ALL PASS (my own CAS, identities in ell)")

    # ---- controls
    # (a) the other (negative) branch of (5.58) at q = 1: 1 + 2m d = -(2l+3)/5
    delta_bad = (-(2 * ell + 3) / 5 - 1) / (2 * m)
    U_bad = sp.expand(Ux.subs({sp.Symbol("m"): m, sp.Symbol("d"): delta_bad}))
    H_bad = sp.expand(Hx.subs({sp.Symbol("m"): m, sp.Symbol("d"): delta_bad}))
    c_bad = sp.simplify(U_bad.subs(x, 2) / (576 * H_bad.subs(x, 2) ** 2))
    print("control (a): negative branch gives c =", sp.factor(c_bad),
          " == l(l-3)/9 ?", sp.simplify(c_bad - claim) == 0, "-> REJECT expected")
    # (b) perturbed U_- coefficient 7680 -> 7681
    m_, d_ = sp.symbols("m d")
    U_pert = (-400000 * d_ * (1 + m_*d_)**3 * x**4
              - 1600 * (1 + m_*d_)**2 * (50*m_*d_ - 16) * x**3
              + 7681 * m_ * (1 + m_*d_) * x**2
              - 16*m_ * (5*m_*(96 - 4*m_)*d_ + 480) * x
              + 64*m_**3 + 384*m_**2)
    Up = sp.expand(U_pert.subs({m_: m, d_: delta}))
    cp = sp.simplify(Up.subs(x, 2) / (576 * H_q1.subs(x, 2) ** 2))
    print("control (b): perturbed U_- gives c == l(l-3)/9 ?", sp.simplify(cp - claim) == 0,
          "-> REJECT expected")
    ok = (sp.simplify(c_bad - claim) != 0) and (sp.simplify(cp - claim) != 0)
    print("CONTROLS:", "ALL OK" if ok else "FAILURE")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
