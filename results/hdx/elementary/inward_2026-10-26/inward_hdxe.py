"""Inward (floor) decimals of HD-X-E's certified lower bounds, from its record (BHM-127): 4 significant figures, exact."""
import json
import sys
from fractions import Fraction


def floor_sig(x, sig=4):
    assert x > 0
    e = 0
    while Fraction(10) ** (e + 1) <= x:
        e += 1
    while Fraction(10) ** e > x:
        e -= 1
    k = sig - 1 - e
    n = (x * Fraction(10) ** k).numerator // (x * Fraction(10) ** k).denominator
    v = Fraction(n, 10 ** k) if k >= 0 else Fraction(n * 10 ** (-k))
    assert v <= x
    m, ex = n, e
    return f"{str(m)[0]}.{str(m)[1:]}e{ex}" if len(str(m)) > 1 else f"{m}e{ex}"


rec = json.load(open(sys.argv[1]))
print("| D | l | path | mu_lo | certified lower bound (inward, 4 s.f.) |")
for p in rec["parts"]:
    b = p["bound"]
    if p["path"] == "split":
        txt = f"K >= {floor_sig(Fraction(b['min_bernstein_K']))}, G >= {floor_sig(Fraction(b['min_bernstein_G']))} (min Bernstein)"
    else:
        txt = f"U_- >= {floor_sig(Fraction(b['U_lower_bound']))}"
    print(f"| {p['D']} | {p['ell']} | {p['path']} | {p['mu_lo']} | {txt} |")
strict = [Fraction(p["bound"]["U_lower_bound"]) for p in rec["parts"] if p["path"] != "split"]
print("min strict:", floor_sig(min(strict)), " max strict:", floor_sig(max(strict)), " parts:", len(rec["parts"]))
