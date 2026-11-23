"""HD-X-1: the band table shared by hdx.pilot and hdx.scert.

D = n + 2.  BANDS are the 11 bands of D = 7..11 that reach q = 1 with 2l > n - 1 (the screen, BHM-014; the scoping
note results/planning/stage3_2026-10-25/hdx/NOTE.md).  GATE = (4, 2) is A2's D = 6, l = 2, which hdx.pilot and
hdx.scert must reproduce.  For a band (n, l):
    c = l(l - n + 1)/(n - 1)^2                         the extremal throat coefficient (BHM-049)
    a_pr = (l - n + 1)/(n - 1), a_ot = -l/(n - 1)     the ends of the residue window, c - a(a + 1) > 0 between them;
                                                       a_pr, the larger, is the throat-principal residue when 2l > n - 1
    a = a_pr + THETA_RES (a_ot - a_pr)                 the design's residue
    beta0 = (n - 1)^2 (c - a(a + 1)) = THETA_RES (1 - THETA_RES) (2l - n + 1)^2, the design's slack at the throat
    eps = B_POLE delta_t/(n - 1) = w/((n - 1)(1 + w)) the pole of the design, at z = -eps (n = 4: A2's delta_t/6)
    MU1, Z1, ZT, SIG1, MUT                             A2-S's chart constants, the same for every band
The controls' parameters:
    a_nc = a_ot - (a_pr - a_ot)/10                     nc-res's residue, outside the window (n = 4: -7/10)
    k_a2 = (2l - n + 1)^2 + 1                          nc-a2: U - k H^2 x^4 makes c' = -1/4 - 1/(4(n - 1)^2) (n = 4: 2)
    k_d0 = 4 beta0                                     d0: U - k H^2 x^4 makes c' = a(a + 1) exactly (n = 4: 16/25)
    WELL                                               the planted well's support [za, zb], inside U_- < 0 at q = 1
"""
from fractions import Fraction

GATE = (4, 2)
BANDS = ((5, 3), (6, 3), (6, 4), (7, 4), (7, 5), (8, 4), (8, 5), (8, 6), (9, 5), (9, 6), (9, 7))
THETA_RES = Fraction(1, 5)
B_POLE = Fraction(1, 2)
MU1, Z1, ZT, SIG1, MUT = Fraction(1, 8), Fraction(1, 4), Fraction(8), Fraction(1, 8), Fraction(1, 32)
# The planted well's support: [z0/5, 4 z0/5] rounded inward to 1/1000, with z0 the only zero of U_- in (0, 1) at q = 1,
# isolated exactly (planning, wells.log of the development notes; U_- < 0 on (0, z0)).  For the gate band this replaces
# nc-bound's [1/20, 1/5], which BHM-106 section 5 found reaches past z0 = 0.0866846...
WELL = {(4, 2): (Fraction(9, 500), Fraction(69, 1000)), (5, 3): (Fraction(3, 250), Fraction(11, 250)),
        (6, 3): (Fraction(9, 500), Fraction(17, 250)), (6, 4): (Fraction(1, 125), Fraction(29, 1000)),
        (7, 4): (Fraction(13, 1000), Fraction(6, 125)), (7, 5): (Fraction(3, 500), Fraction(1, 50)),
        (8, 4): (Fraction(17, 1000), Fraction(67, 1000)), (8, 5): (Fraction(9, 1000), Fraction(7, 200)),
        (8, 6): (Fraction(1, 250), Fraction(3, 200)), (9, 5): (Fraction(3, 250), Fraction(47, 1000)),
        (9, 6): (Fraction(7, 1000), Fraction(13, 500)), (9, 7): (Fraction(1, 250), Fraction(3, 250))}
Z0 = {(4, 2): 0.086684656221, (5, 3): 0.055272109631, (6, 3): 0.085898519672, (6, 4): 0.036906149751,
      (7, 4): 0.060098862938, (7, 5): 0.026162217500, (8, 4): 0.083978310230, (8, 5): 0.043835649205,
      (8, 6): 0.019455305856, (9, 5): 0.059197408697, (9, 6): 0.033301762699, (9, 7): 0.015014745303}


def label(n, ell):
    return f"{n + 2},{ell}"


def residues(n, ell, theta=THETA_RES):
    """(c, a_pr, a_ot, a, beta0), Fractions.  Refuses a critical band (2l <= n - 1), which is HD-X-2's."""
    if not 2 * ell > n - 1:
        raise ValueError(f"D = {n + 2}, l = {ell} has 2l <= n - 1: a critical band (HD-X-2), not HD-X-1")
    c = Fraction(ell * (ell - n + 1), (n - 1) ** 2)
    apr, aot = Fraction(ell - n + 1, n - 1), Fraction(-ell, n - 1)
    a = apr + theta * (aot - apr)
    beta0 = (n - 1) ** 2 * (c - a * (a + 1))
    if beta0 != theta * (1 - theta) * (2 * ell - n + 1) ** 2:
        raise ArithmeticError("beta0 identity")
    return c, apr, aot, a, beta0


def control_params(n, ell):
    """a_nc (nc-res), k_a2 (nc-a2), k_d0 (d0), Fractions."""
    c, apr, aot, a, beta0 = residues(n, ell)
    return {"a_nc": aot - (apr - aot) / 10, "k_a2": Fraction((2 * ell - n + 1) ** 2 + 1), "k_d0": 4 * beta0}
