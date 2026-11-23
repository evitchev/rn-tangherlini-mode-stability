"""Lemma U, Kimi's own derivation.

P(eps, kap, x) := eps^6 U_-(x; m = eps^-2, delta = kap eps), built symbolically from
my KI (5.63b) transcription at n = 4.  Split P = Pos - Neg with nonnegative
coefficients; check Pos(0,0,0) = 64 and 64 - Neg(1/12, 1/5, 2) > 0 exactly.
"""
from fractions import Fraction

import sympy as sp

eps, kap, x = sp.symbols("eps kap x")
m = eps**-2
d = kap * eps

U = (-400000 * d * (1 + m*d)**3 * x**4
     - 1600 * (1 + m*d)**2 * (50*m*d - 16) * x**3
     + 7680 * m * (1 + m*d) * x**2
     - 16*m * (5*m*(96 - 4*m)*d + 480) * x
     + 64*m**3 + 384*m**2)

P = sp.expand(eps**6 * U)
poly = sp.Poly(P, eps, kap, x)
terms = poly.terms()

pos = {}
neg = {}
for (i, j, k), c in terms:
    c = sp.Rational(c)
    key = (i, j, k)
    if c >= 0:
        pos[key] = c
    else:
        neg[key] = -c   # store the POSITIVE coefficient of the subtracted monomial

def evald(dic, e0, k0, x0):
    return sum(c * e0**i * k0**j * x0**k for (i, j, k), c in dic.items())

print("P(eps,kap,x) terms:", len(terms))
print("P has only nonnegative eps powers:", all(i >= 0 for (i, j, k), _c in terms))
print("Pos(0,0,0) =", evald(pos, 0, 0, 0))
Neg_max = evald(neg, sp.Rational(1, 12), sp.Rational(1, 5), sp.Rational(2))
print("Neg(1/12, 1/5, 2) =", Neg_max, "=", float(Neg_max))
bound = 64 - Neg_max
print("64 - Neg(1/12,1/5,2) =", bound, "=", float(bound), " > 0:", bound > 0)

# show Neg explicitly for the audit record
neg_sorted = sorted(neg.items(), key=lambda kv: kv[0])
print("Neg =")
for k, c in neg_sorted:
    print("   ", c, "* eps^%d kap^%d x^%d" % k)

# the split is genuine: Pos - Neg == P
recon = sum(c * eps**i * kap**j * x**k for (i, j, k), c in pos.items()) \
      - sum(c * eps**i * kap**j * x**k for (i, j, k), c in neg.items())
assert sp.expand(recon - P) == 0
print("Pos - Neg == P: True")
print("LEMMA U:", "PASS" if (bound > 0 and evald(pos, 0, 0, 0) == 64) else "FAIL")
