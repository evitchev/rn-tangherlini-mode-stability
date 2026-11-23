#!/usr/bin/env python3
"""Exact endpoints of the D = 7, l = 2 cover (n = 5): q(mu)^2 = 1 - (8 mu/(7 + mu^2))^2, to 15 digits (integer sqrt),
and an inward test of the decimals quoted in our blind seat's VERDICT.md (lines 30-32) and in bh-modes' RESULT.md."""
from fractions import Fraction as F
from math import isqrt

def q2(mu):
    return 1 - (8 * mu / (7 + mu * mu)) ** 2

def dec(fr, digits=15):
    s = 10 ** (2 * digits)
    v = isqrt(fr.numerator * s // fr.denominator)
    return f"{v // 10**digits}.{v % 10**digits:0{digits}d} (floor)"

pts = {"mu=1237/10000 (q top)": F(1237, 10000), "mu=2780/10000 (blind split)": F(2780, 10000), "mu=2817/10000 (q bottom)": F(2817, 10000)}
for k, mu in pts.items():
    print(k, "q^2 =", q2(mu), " q =", dec(q2(mu)))
lo, split, hi = q2(F(2817, 10000)), q2(F(2780, 10000)), q2(F(1237, 10000))
tests = [("blind E2 lower 0.94797859 (lower end: inward iff >= exact)", F("0.94797859"), lo, "lower"),
         ("blind E2 upper 0.99000061", F("0.99000061"), hi, "upper"),
         ("blind E0 lower 0.947979", F("0.947979"), lo, "lower"),
         ("blind E0 upper 0.949342", F("0.949342"), split, "upper"),
         ("blind C lower 0.949342", F("0.949342"), split, "lower"),
         ("blind C upper 0.990001", F("0.990001"), hi, "upper"),
         ("bh-modes S(7,2) lower 0.94798", F("0.94798"), lo, "lower"),
         ("bh-modes S(7,2) upper 0.99000", F("0.99000"), hi, "upper")]
for name, d, ex2, side in tests:
    ok = d * d >= ex2 if side == "lower" else d * d <= ex2
    print(f"{name}: inward {ok}")
