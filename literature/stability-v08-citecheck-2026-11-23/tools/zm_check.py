"""K43/K63: S33's Psi_2 (eq. 4.14) at D = 4 against v0.8's u_0, and S33's V_2 (eq. 4.18) against Kodama-Ishibashi's
V_S- = f U_- / (64 r^2 H_-^2) (S5 eqs. 5.61, 5.62b, 5.63b at y = 0, K = 1, n = 2, q = 1), all transcribed by hand from
the rendered pages. Usage: python3 -B -I zm_check.py"""
import sympy as sp
r, M, l = sp.symbols("r M ell", positive=True)
n = 2
f = (1 - M / r) ** 2                                   # extremal RN, S33 eq. (4.16); S5 (2.19) with Q = M, n = 2
Psi2 = r ** (1 - l) * (1 - M / r) ** (-l) / ((l - 1) * r + 2 * M)          # S33 (4.14), constant dropped
V2 = (r - M) ** 2 / (r ** 6 * ((l - 1) * r + 2 * M) ** 2) * (
    -2 * (l ** 3 - 3 * l + 2) * M * r ** 3 + 8 * (l - 2) * M ** 3 * r - 12 * (l - 1) * M ** 2 * r ** 2
    - (l - 1) ** 2 * l * (l + 1) * r ** 4 + 8 * M ** 4)                          # S33 (4.18)
zm = -f * sp.diff(f * sp.diff(Psi2, r), r) + V2 * Psi2                    # S33 (4.19)
print("S33 (4.19) residual of Psi_2:", sp.simplify(zm / Psi2))
# Kodama-Ishibashi at n = 2, K = 1, y = 0, q = 1: m = (l-1)(l+2), (1+2 m d)^2 = 1 + 4m/9
m = (l - 1) * (l + 2)
d = sp.Rational(1, 2) * (sp.sqrt(1 + sp.Rational(4, 9) * m) - 1) / m
d = sp.simplify(d.subs(sp.sqrt(1 + sp.Rational(4, 9) * m), (2 * l + 1) / sp.Integer(3)))
x = 2 * M / r
H = m + sp.Rational(n * (n + 1), 2) * (1 + m * d) * x
U = (-n ** 3 * (3 * n - 2) * (n + 1) ** 4 * d * (1 + m * d) ** 3 * x ** 4
     - 4 * n ** 2 * (n + 1) ** 2 * (1 + m * d) ** 2 * ((n + 1) * (3 * n - 2) * m * d - n ** 2) * x ** 3
     + 4 * (n + 1) * (1 + m * d) * (m * (n - 2) * (n - 4) * (n + 1) * (m + n ** 2) * d + 4 * n * (2 * n ** 2 - 3 * n + 4) * m
                                     + n ** 2 * (n - 2) * (n - 4) * (n + 1)) * x ** 2
     - 16 * m * ((n + 1) * m * (3 * n ** 2 * (n - 2) - 4 * m) * d + 3 * n * (n - 4) * m + 3 * n ** 2 * (n + 1) * (n - 2)) * x
     + 64 * m ** 3 + 16 * n * (n + 2) * m ** 2)
VS = f * U / (64 * r ** 2 * H ** 2)
print("V_2 (S33) - V_S- (S5):", sp.simplify(V2 - VS))
# v0.8 Theorem 2 at n = 2 with rho = r / r_H, r_H = M at q = 1
rho = r / M
Y = 1 / rho
u0 = rho ** (-(l + sp.Rational(n, 2) - 1)) * (1 - Y) ** (-l / (n - 1)) / ((l - 1) + n * Y)
print("u_0 / Psi_2 (should not depend on r):", sp.simplify(u0 / Psi2))
print("Psi_2 * r^l as r -> oo:", sp.limit(Psi2 * r ** l, r, sp.oo))
# Which potential does Psi_2 solve?
print("KI residual of Psi_2 (-f (f Psi')' + V_S- Psi):", sp.simplify((-f * sp.diff(f * sp.diff(Psi2, r), r) + VS * Psi2) / Psi2))
br = lambda V: sp.factor(sp.expand(sp.simplify(V * r ** 6 * ((l - 1) * r + 2 * M) ** 2 / (r - M) ** 2)))
print("S33 V_2 bracket:", sp.expand(br(V2)))
print("S5  V_S- bracket:", sp.expand(br(VS)))
# The potential that Psi_2 actually solves, in S33's form
Vtrue = sp.simplify(f * sp.diff(f * sp.diff(Psi2, r), r) / Psi2)
print("bracket of the potential Psi_2 solves:", sp.expand(br(Vtrue)))
