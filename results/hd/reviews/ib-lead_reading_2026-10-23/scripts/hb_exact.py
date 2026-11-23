from fractions import Fraction as F
import sympy as sp
x, m, d = sp.symbols("x m delta")
U6 = (-400000 * d * (1 + m*d)**3 * x**4 - 1600 * (1 + m*d)**2 * (50 * m * d - 16) * x**3
      + 7680 * m * (1 + m*d) * x**2 - 16 * m * (5 * m * (96 - 4*m) * d + 480) * x + 64 * m**3 + 384 * m**2)
H6 = m + 10 * (1 + m*d) * x
for mu in (F(3, 25), F(1, 100), F(1, 10000)):
    A = 6 + mu * mu; w = 7 * mu / A
    s = 7 * (6 - mu * mu) / (5 * A); dl = (s - 1) / 12
    xH = 2 / (1 + w); dt = 2 * w / (1 + w)
    sub = {m: 6, d: sp.Rational(dl.numerator, dl.denominator), x: sp.Rational(xH.numerator, xH.denominator)}
    W0 = sp.Rational(U6.subs(sub)) / (64 * sp.Rational(H6.subs(sub)) ** 2)
    hb = W0 / (3 * sp.Rational(dt.numerator, dt.denominator))
    print(mu, "W(0) =", W0 if mu == F(3, 25) else sp.N(W0, 15), "| W(0)/f_z(0) =", hb if mu == F(3, 25) else sp.N(hb, 15))
