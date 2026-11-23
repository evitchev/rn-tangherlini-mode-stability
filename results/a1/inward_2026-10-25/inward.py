"""Inward (floor) decimals of A1's Lemma U bound, from the record of BHM-052.

Reads part2.bound from results/a1/runs/record/main/result.json and floors it to 4 and 5 significant figures in
exact integer arithmetic. A certified lower bound must be quoted rounded down (BHM-084).
"""
import json
import sys
from fractions import Fraction


def floor_sig(x, sig):
    """Largest decimal with `sig` significant figures that is <= x, for x > 0 (exact)."""
    assert x > 0
    e = 0
    while Fraction(10) ** (e + 1) <= x:
        e += 1
    while Fraction(10) ** e > x:
        e -= 1
    scale = Fraction(10) ** (sig - 1 - e)
    n = (x * scale).numerator // (x * scale).denominator
    return n, sig - 1 - e


rec = json.load(open(sys.argv[1]))
b = Fraction(rec["part2"]["bound"])
print("bound:", b)
for sig in (4, 5):
    n, d = floor_sig(b, sig)
    s = str(n)
    dec = s[:len(s) - d] + "." + s[len(s) - d:] if d > 0 else s
    assert Fraction(n, 10 ** d) <= b < Fraction(n + 1, 10 ** d)
    print(f"floor, {sig} significant figures: {dec}")
print("54.86 <= bound:", Fraction(5486, 100) <= b)
