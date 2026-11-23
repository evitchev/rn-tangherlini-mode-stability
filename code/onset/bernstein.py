"""Exact Bernstein enclosures (python-flint fmpq) for polynomial positivity certificates.

A polynomial is given in the power basis as a dict {(i, j): coefficient} in two variables
(t, mu), or as a list of coefficients in one variable.  On a box, the Bernstein coefficients
of the polynomial bound it from both sides; if they are all > 0 the polynomial is > 0 on the
box (the Bernstein enclosure property).  Everything is exact rational arithmetic, so a
positive verdict is a proof, and the coefficients can be re-checked by any exact system.
"""
from fractions import Fraction
from math import comb

from flint import fmpq, fmpq_poly

from qnm1c.common import CertificateError


def Q(v):
    """Exact conversion of an int, Fraction, sympy Rational or decimal string to fmpq.
    A float is refused: its decimal string is not its binary value (Fable's audit, BHM-042)."""
    if isinstance(v, float):
        raise TypeError(f"Q: float {v!r} refused; pass an exact rational")
    fr = Fraction(str(v)) if not isinstance(v, Fraction) else v
    return fmpq(fr.numerator, fr.denominator)


def _pad(coeffs, d):
    c = list(coeffs)
    return c + [fmpq(0)] * (d + 1 - len(c))


def _affine(coeffs, a, h, d):
    """Coefficients (in u) of p(a + h u), padded to degree d."""
    if not any(coeffs):
        return [fmpq(0)] * (d + 1)
    return _pad(fmpq_poly(list(coeffs))(fmpq_poly([a, h])).coeffs(), d)


def _to_bernstein(a, d):
    """Power basis on [0, 1] -> Bernstein coefficients of degree d."""
    return [sum((fmpq(comb(k, i), comb(d, i)) * a[i] for i in range(k + 1)), fmpq(0))
            for k in range(d + 1)]


class Poly2:
    """Polynomial in (t, mu) with exact rational coefficients."""

    def __init__(self, terms):
        self.terms = {k: fmpq(v) for k, v in terms.items() if v != 0}
        self.dt = max((i for i, _ in self.terms), default=0)
        self.dm = max((j for _, j in self.terms), default=0)

    def bernstein(self, t0, t1, m0, m1):
        """Bernstein coefficients on [t0, t1] x [m0, m1] (exact)."""
        dt, dm = self.dt, self.dm
        cols = []                                    # for each mu-power j, the t-polynomial
        for j in range(dm + 1):
            col = [self.terms.get((i, j), fmpq(0)) for i in range(dt + 1)]
            cols.append(_to_bernstein(_affine(col, t0, t1 - t0, dt), dt))
        out = []
        for k in range(dt + 1):                      # for each t-Bernstein index, the mu-polynomial
            row = [cols[j][k] for j in range(dm + 1)]
            out.append(_to_bernstein(_affine(row, m0, m1 - m0, dm), dm))
        return out

    def value(self, t, mu):
        return sum((c * fmpq(t) ** i * fmpq(mu) ** j for (i, j), c in self.terms.items()), fmpq(0))


def prove_sign(p, box, sign, max_depth, stats, label, minrec=None):
    """Prove sign * p > 0 on the closed box by adaptive bisection; raise CertificateError if
    a leaf at max_depth is still undecided or a corner value has the wrong sign.  If a dict
    minrec is given, minrec[label] is the least Bernstein coefficient of sign * p over the
    accepted leaves: a certified lower bound of sign * p on the box."""
    stack = [(box, 0)]
    while stack:
        (t0, t1, m0, m1), depth = stack.pop()
        b = p.bernstein(t0, t1, m0, m1)
        lo = min(sign * c for row in b for c in row)
        stats[label] = stats.get(label, 0) + 1
        if lo > 0:
            if minrec is not None:
                minrec[label] = lo if label not in minrec else min(minrec[label], lo)
            continue
        for (tt, mm) in ((t0, m0), (t0, m1), (t1, m0), (t1, m1)):
            if sign * p.value(tt, mm) <= 0:
                raise CertificateError(f"{label}: sign*p = {sign * p.value(tt, mm)} <= 0 at "
                                       f"(t, mu) = ({tt}, {mm})  (a counterexample)")
        if depth >= max_depth:
            raise CertificateError(f"{label}: undecided at depth {depth} on box {(t0, t1, m0, m1)}")
        # bisect the side whose Bernstein coefficients vary more (never a variable p lacks)
        if p.dm == 0 or (p.dt > 0 and (t1 - t0) * p.dt >= (m1 - m0) * p.dm):
            tm = (t0 + t1) / 2
            stack += [((t0, tm, m0, m1), depth + 1), ((tm, t1, m0, m1), depth + 1)]
        else:
            mm_ = (m0 + m1) / 2
            stack += [((t0, t1, m0, mm_), depth + 1), ((t0, t1, mm_, m1), depth + 1)]
    return True
