"""Development tests of hd.scheck, run before registration (results/hd/s/PREREG_ADDENDUM_1.md section 5).  Synthetic
inputs only: no record is read, and S5's U_- is not evaluated.

    python -m hd.devtest_scheck
"""
from fractions import Fraction

from hd.devtest_s import FSYN, HSYN, USYN
from hd.scert import design_box
from hd.scheck import check_band
from ki.potentials import m


def synthetic_record(n, ell, box, var, deg):
    Phat, s, e, db, _ = design_box(n, ell, box, var, deg, Fraction(1, 50), funcs=FSYN)
    return {"boxes": [{"mu": [str(box[0]), str(box[1])], "variable": var, "degree": deg, "verified": True,
                       "delta_b": None if db is None else str(db),
                       "P": {str(k): str(c) for k, c in Phat.as_dict().items()}}]}


def main():
    n, ell, box = 5, 4, (Fraction(1, 2), Fraction(11, 20))
    for var in ("z", "zeta"):
        rec = synthetic_record(n, ell, box, var, 16)
        ok, out = check_band(n, ell, rec, "none", UHexact=(USYN, HSYN), UHdirect=(USYN, HSYN))
        print(f"synthetic {var} 16: identity holds: {ok}", out)
        ok, out = check_band(n, ell, rec, "none", UHexact=(USYN, HSYN), UHdirect=(USYN + 16 * n * m ** 2, HSYN))
        print(f"synthetic {var} 16, direct route tampered: identity holds: {ok} (False expected)", out)


if __name__ == "__main__":
    main()
