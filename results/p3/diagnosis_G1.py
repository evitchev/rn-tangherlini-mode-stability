"""Post-hoc diagnosis of the failed gate G1 (results/p3/PREREG.md; not registered, numerical).

For the registered design P = P_true - EPS, METHOD.md's remark gives
  rho^2 (V~/f) = EPS [rho f' + f (2 P_true - 1 - EPS)]  (exact for the exact P_true).
If that bracket is negative somewhere, the registered design direction cannot work there, whatever
the fit.  Evaluate it for G1 (D = 10, l = 2, Q = 0) and for T1 (D = 6, l = 2, mu = 1/6).
"""
import math
from fractions import Fraction

import sympy as sp

from p3.scert import EPS, numeric, riccati_values, setting, z

for name, kind, muv in (("G1", "G1", None), ("T1", "D6", Fraction(1, 6))):
    S = setting(kind)
    W, f, fz = numeric(S, muv)
    zs = [k / 400 for k in range(1, 400)]
    P = riccati_values(S, muv, zs)
    worst = None
    for zz, p in zip(zs, P):
        rho = 1 / (1 - zz)
        fprime = fz(zz) * (1 - zz) ** 2
        val = rho * fprime + f(zz) * (2 * p - 1 - float(EPS))
        if worst is None or val < worst[0]:
            worst = (val, zz, p)
    print(f"{name}: min over z of [rho f' + f (2 P_true - 1 - EPS)] = {worst[0]:.4g} at z = {worst[1]:.4g} "
          f"(P_true = {worst[2]:.4g}); P_true range [{min(P):.4g}, {max(P):.4g}]")
