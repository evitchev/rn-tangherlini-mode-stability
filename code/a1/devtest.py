"""Development tests run before registration (results/a1/PREREG.md section 6).  Synthetic inputs only:
nothing of U_- is evaluated and no control is run.

    python -m a1.devtest
"""
import sympy as sp

import cn.identity as cn_identity
from a1.p1 import kats, part1, part2, tampered_prove_sign
from ki.potentials import m, x
from onset.bernstein import prove_sign


def main():
    print("KATs, real verifier:", kats(prove_sign))
    print("KATs, tampered verifier (KAT2 must fail):", kats(tampered_prove_sign))
    u1 = 64 * m**3 + 384 * m**2 + x**2
    ok, rec = part1(prove_sign, 3, u1, sp.Rational(99, 100), False)
    print("Part I code path, synthetic U = 64m^3 + 384m^2 + x^2, l = 3:", ok,
          {k: rec[k] for k in ("mu_lo", "covers_q_max", "F_degrees", "Den_degree", "U_lower_bound_approx")})
    u2 = 64 * m**3 + 384 * m**2 - 7680 * m * x
    ok, rec = part2(u2, 10, False)
    print("Part II code path, synthetic U = 64m^3 + 384m^2 - 7680mx:", ok, rec["Neg"], rec["bound"])
    U, H = cn_identity.potentials("none")
    print("cn.identity imports; symbolic-n H_-:", H)

    # Addendum 1: the record of a run, assembled as main() does, must serialize (synthetic parts).
    import json
    import tempfile

    from a1.p1 import plain
    from qnm1c.common import dump_json
    _, r1 = part1(prove_sign, 3, u1, sp.Rational(99, 100), False)
    _, r2 = part2(u2, 10, False)
    record = {"part1": [r1], "part2": r2, "sympy_true": sp.true, "rational": sp.Rational(1, 3)}
    with tempfile.TemporaryDirectory() as tmp:
        dump_json(plain(record), f"{tmp}/result.json")
        back = json.load(open(f"{tmp}/result.json"))
    print("record of synthetic parts serializes:", back["part2"]["checks"], back["sympy_true"], back["rational"])
    _, r3 = part1(tampered_prove_sign, 3, u1, sp.Rational(99, 100), False)
    print("tampered verifier fills minrec (no KeyError):", "U_lower_bound" in r3)


if __name__ == "__main__":
    main()
