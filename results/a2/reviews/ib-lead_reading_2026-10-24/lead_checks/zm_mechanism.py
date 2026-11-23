"""Lead check: why nc-zm's POS-O fails at (z, mu) = (19/64, 0).  Separates the two changes nc-zm makes:
(i) U -> U - H^2 x^4 with the design's a = -2/5;  (ii) a = -1/2 with U unchanged;  (iii) both (nc-zm itself).
Uses bh-modes' own a2.scert.parts from the byte copy at 25c796e (read-only import)."""
import sys
TREE = sys.argv[1]
sys.path.insert(0, TREE + "/code")
import sympy as sp
from a2 import scert as sc
from ki.potentials import H_TARGET, U_TARGET, x
from onset.onset import mu
z = sc.z
p0, deg = sc.design(TREE)
pts = [(sp.Rational(19, 64), 0), (sp.Rational(1, 4), 0), (sp.Rational(1, 2), 0), (sp.Rational(3, 4), 0), (sp.Rational(19, 64), sp.Rational(1, 16))]
cases = {"main (U, a=-2/5)": (U_TARGET, sc.A_RES),
         "(i) U - H^2 x^4, a=-2/5": (U_TARGET - H_TARGET**2 * x**4, sc.A_RES),
         "(ii) U, a=-1/2": (U_TARGET, sp.Rational(-1, 2)),
         "(iii) nc-zm: U - H^2 x^4, a=-1/2": (U_TARGET - H_TARGET**2 * x**4, sp.Rational(-1, 2))}
for name, (U, a) in cases.items():
    E, en, ed, S, Pi, NL = sc.parts(U, H_TARGET, p0, a)
    L = sp.Poly(E.L.as_expr(), z, mu)
    vals = []
    for (zz, mm) in pts:
        nl = NL.eval({z: zz, mu: mm}) if hasattr(NL, "eval") else None
        nl = sp.Rational(NL.as_expr().subs({z: zz, mu: mm}))
        s = sp.Rational(S.as_expr().subs({z: zz, mu: mm}))
        l = sp.Rational(L.as_expr().subs({z: zz, mu: mm}))
        N = nl / (s**2 * l)
        vals.append(f"N({zz},{mm}) = {float(N):.6g}")
    print(name, "|", "; ".join(vals))
