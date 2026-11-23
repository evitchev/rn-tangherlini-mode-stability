"""Development tests run before registration (results/hd/elementary/PREREG.md section 6).  Synthetic inputs only:
nothing of S5's U_- is evaluated for n = 5..9, and no gate or control is run.

    python -m hd.devtest ROOT
"""
import importlib.util
import os
import sys

import sympy as sp

from hd.elementary import KIMI_BUILD, lemma_U, part1
from ki.potentials import m, x
from onset.bernstein import prove_sign


def main(root):
    u1 = 64 * m**3 + x**2
    r = part1(prove_sign, 5, 4, sp.Rational(99, 100), u1)
    print("part1 code path, synthetic U = 64m^3 + x^2, n = 5, l = 4:",
          {k: r[k] for k in ("mu_lo", "covers", "F_degrees", "bernstein_leaves")})
    u2 = 64 * m**3 - 7680 * m * x
    ok, rec = lemma_U(9, u2)
    print("lemma_U code path, synthetic U = 64m^3 - 7680mx, n = 9:", ok, rec["l0"], rec["bound"], rec["checks"])
    spec = importlib.util.spec_from_file_location("kimi_build", os.path.join(root, KIMI_BUILD))
    kb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kb)
    print("Kimi's build.py loads; it defines ki_Usymbol:", callable(kb.ki_Usymbol))


if __name__ == "__main__":
    main(sys.argv[1])
