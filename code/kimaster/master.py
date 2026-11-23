"""U and H of the scalar-type master equations at an integer n or at n = N symbolic, shared by [another line of this project] and
[another line of this project].  For an integer n they are ki.potentials' (S5 (5.62)-(5.63) at K = 1, y = 0); for n = N, U is
ki.potentials' U at the symbol N and H is rebuilt here, because ki.potentials forms n(n+1)/2 with sp.Rational, which
needs an integer.  gate_general checks the two against each other at n = 2..9.
"""
import sympy as sp

from ki.potentials import H_minus, H_plus, U_minus, U_plus, d, m, x

NSYM = sp.Symbol("N")
SECTORS = ("minus", "plus")


def H_symbolic(nn, sector):
    """S5 (5.62b) for sector "minus", (5.62a) for "plus", with n symbolic."""
    c = nn * (nn + 1) / 2
    return m + c * (1 + m * d) * x if sector == "minus" else 1 - c * d * x


def master(n, sector):
    """(U, H) of V_S- (sector "minus") or V_S+ ("plus"); n an integer, or "N"."""
    if n == "N":
        return (U_minus(NSYM) if sector == "minus" else U_plus(NSYM)), H_symbolic(NSYM, sector)
    return (U_minus(n), H_minus(n)) if sector == "minus" else (U_plus(n), H_plus(n))


def gate_general(sector, UH=master):
    """The n = N forms specialise to the integer-n forms at n = 2..9.  Returns (ok, detail)."""
    U, H = UH("N", sector)
    bad = [k for k in range(2, 10)
           if sp.expand(U.subs(NSYM, k) - UH(k, sector)[0]) != 0 or sp.expand(H.subs(NSYM, k) - UH(k, sector)[1]) != 0]
    return not bad, (f"n = N forms differ from the integer-n forms at n = {bad}" if bad
                     else "n = N forms equal the integer-n forms at n = 2..9")
