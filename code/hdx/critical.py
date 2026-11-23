"""Stage 3, HD-X-2 (results/hdx/critical/PREREG.md): S-certificates through extremality on HD-X's critical set, the 9
bands with 2l <= n - 1 of D = 7..11 (TARGET_HD_ADDENDUM_2.md section 2), by route (iii) of
results/planning/stage3_2026-10-25/critical/NOTE.md: Z's exact q = 1 zero mode (BHM-126), with its pole moved off the
horizon and a constant first-order term.

    python -m hdx.critical --out DIR --band D,L [--control NAME] [--root REPO]

Units r_H = 1, z = 1 - 1/rho, D = n + 2, k = n - 1, y = (1 - z)^k; mu is HD-E's charge parameter (hd.elementary.param_n),
with q = 1 at mu = 0.  The design is fixed by rule (no fit):
    P(z, mu) = -nu - l y / ((z + eps) R(z)) - (1 - z) H_z / H + c mu,
    nu = l + n/2 - 1,  R = (1 - y)/z,  H = H_-(x_H y) with param_n's (m, delta),  eps = ehat w/(1 + w),
    ehat = (1/k + 2/(k - l))/2, the midpoint of the throat window (1/k, 2/(k - l)),  c = 1/4.
At mu = 0, P = (1 - z)(log u0)_z for Z's zero mode u0 = rho^-nu (1 - y)^(-l/k) / ((l - 1) + n y), so N(z, 0) = 0.
With S = eps_d z + eps_n (eps = eps_n/eps_d), D = S R Hn and Pi = P D (polynomials in z, mu),
    NL := N S^2 R^2 L = Un Hd^2 fd S^2 R^2 - 64 Ud [(1 - z) fzn Pi D + fn (-Pi D + (1 - z)(Pi_z D - Pi D_z) + Pi^2)],
with U = Un/Ud, H = Hn/Hd, f = fn/fd, f_z = fzn/fd and L = Ud Hd^2 fd as in hd.scert.exact_parts.  NL vanishes on
mu = 0, so [0, 1] x [0, MU1] is covered by four charts, each after an exact division:
    O   (z, mu) in [Z1, 1] x [0, MU1]                 M = NL/mu > 0
    O'  (z, mu) in [0, Z1] x [MUT, MU1]               M > 0
    T   z = mu zeta, (zeta, mu) in [0, ZT] x [0, MUT]      T = NL(mu zeta, mu)/mu^2 > 0
    C   mu = z sigma, (z, sigma) in [0, Z1] x [0, SIG1]    K = NL(z, z sigma)/(z^2 sigma) > 0
With ZT SIG1 >= 1, ZT MUT <= Z1 and Z1 SIG1 <= MU1 (COVER), every (z, mu) in (0, 1) x (0, MU1] lies in a chart, where
NL > 0; with S, R and L > 0 there, N > 0.  P is C^infinity on [0, 1] for mu > 0 (its poles are at z = -eps, at the zeros
of R, which satisfy |1 - z| = 1 with z != 0, and at those of H, which is > 0 there), so A_{l,q} >= 0 by Proposition 3
for P C^1 on (0, 1) (Lean prop3_Dn, BHM-091), for every q in [q(MU1), 1).  q = 1 itself is Z (BHM-126).
Gates, in the order of the record: KAT; E0n (S5's transcription, hd.elementary); PARAM (the identities of param_n,
x_H(0) = 2, delta(0) = 1/((l + n)(n + 1)), q(MU1)^2 <= (99/100)^2, w increasing on [0, 1]); H (every coefficient of H in
(x, delta, m) > 0, and delta > 0 on [0, MU1]); S (eps_n(0) = 0, eps_n/mu > 0 and eps_d > 0 on [0, MU1]); R (> 0 on
[0, 1]); L (> 0 on [0, MU1]); COVER; Z0 (NL(z, 0) = 0 identically); DIV-O, DIV-T, DIV-C; THROAT (T(zeta, 0) equals
64 k^2 H(2)^2 L(0) R(0)^2 eps_d(0)^2 w'(0)^2 beta(zeta/w'(0)), beta(s) = 2 a^2 (ehat - 1/k) s + a ehat ((a + 1) ehat
- 2/k), a = -l/k); CORNER (K(0, sigma) = sigma T(1/sigma, 0)); FIRST (M(z, 0) = O(z) and K(0, 0) = C0 eps_d(0)^2 R(0)^2
L(0), C0 = 128 H(2)^2 l^2 w'(0) (ehat - 1/k)); INF (NL(1, mu) = 64 m^2 ((2 nu + 1) c mu - c^2 mu^2) S(1, mu)^2 L(mu), and
c > 0, 2 nu + 1 > c MU1); XN (NL/(S^2 R^2 L) equals N computed directly from U, H, the unfactored f and P's definition, at
XN_POINTS seeded rational points and three fixed ones, exactly); POS-O, POS-O', POS-T, POS-C (exact Bernstein bisection,
onset.bernstein.prove_sign).
Fail-closed (RULES.md A2): VERIFIED and exit 0 only if every check holds; otherwise REJECT: <reasons>, exit 1.
--control (each with its registered verdict, PREREG section 4; run by the kit on D = 7 l = 2 and D = 11 l = 4):
    nc-ehat-low   ehat = 1/k - 1/20, below the window: K(0, 0) < 0, so POS-C fails
    d0-corner     ehat = 1/k, the window's lower edge: K(0, 0) = 0 exactly, so the strict POS-C fails
    nc-ehat-high  ehat = 2/(k - l) + 1/8, above the window: T(0, 0) < 0, so POS-T fails
    d0-throat     ehat = 2/(k - l), the upper edge: T(0, 0) = 0 exactly, so the strict POS-T fails
    nc-Q0         c = 0: N(1, mu) = 0, so INF and POS-O fail
    nc-Qneg       c = -1/4: N(1, mu) < 0 for mu > 0, so INF and POS-O fail
    td-nu         the design's constant -nu shifted by -1/100: NL(z, 0) != 0, so Z0, DIV-O and DIV-C fail
    d6            NL - K6 mu^2 (z - mu)(3 mu - z)(1 - z), K6 = 2 T(2, MU_C)/(MU_C^2 (1 - 2 MU_C)): a planted throat
                  defect that vanishes at mu = 0 and at z = 1, with T(2, MU_C) < 0; every identity holds, POS-T fails
    nc-bound      a planted bound state at mu = MU_C: W - K b, b = ((z - za)(zb - z))^2 with [za, zb] inside the
                  horizon's U_- < 0 region (checked exactly), K = ceil(2 I1/I2); (a) Q[b] < 0 certified in Arb, and
                  (b) NL of the planted potential at MU_C is refused on [za, zb]
    td-coeff      U_minus(n) + 16 n m^2 (hd.elementary's tamper): E0n fails
    td-verifier   the verifier's acceptance threshold lowered from 0 to -1: the KATs fail
    td-cover      SIG1 = 1/16: ZT SIG1 < 1, so COVER fails
    td-div        the T chart divided by mu^3 and the C chart by z^3 sigma: DIV-T and DIV-C fail
  PREREG_ADDENDUM_1.md: a control for each gate that had none (the session-R lead's reading, BHM-151, 2a):
    td-param      the PARAM gate on param_n(n, l, "td-param") (B = 2l + n, hd.elementary's tamper); everything else on
                  the true parametrisation: PARAM fails
    td-H          the H gate on H_- - n(n + 1) x, only the gate's input (as HD-X-S's td-H): H fails
    td-R          the R gate on -R: R fails
    td-L          the L gate on -L: L fails
    td-S          eps_n -> -eps_n in the design itself (as HD-X-S's td-S): the pole moves to z = +eps, inside the
                  exterior; S fails, with PARAM (eps's identity), THROAT, FIRST and XN (the direct N keeps +eps)
    td-XN         mu^2 z^2 (1 - z) added to NL after it is built and before XN: XN fails.  The term vanishes to second
                  order at mu = 0 and at z = 1 and is divisible by z^2 sigma in the C chart, so Z0, the divisions, THROAT,
                  CORNER, FIRST and INF are unchanged; it adds mu z^2 (1 - z) to M, mu^2 zeta^2 (1 - mu zeta) to T and
                  sigma z^2 (1 - z) to K, each with non-negative Bernstein coefficients on its box, so the POS charts
                  still pass
"""
import argparse
import datetime
import math
import os
import random
import sys
import time

import sympy as sp
from flint import acb, ctx, fmpq

from a1.p1 import MAX_DEPTH, kats, plain, positive_mu, tampered_prove_sign
from hd.elementary import U_of, gate_E0n, param_n
from hd.scert import exact_parts, z
from ki.potentials import H_minus, d, m, x
from onset.bernstein import Poly2, Q, prove_sign
from onset.onset import mu
from qnm1c.common import CertificateError, dump_json, provenance

CONTROLS = ("none", "nc-ehat-low", "d0-corner", "nc-ehat-high", "d0-throat", "nc-Q0", "nc-Qneg", "td-nu", "d6",
            "nc-bound", "td-coeff", "td-verifier", "td-cover", "td-div",
            # PREREG_ADDENDUM_1.md: a control for each gate that had none (BHM-151, 2a)
            "td-param", "td-H", "td-R", "td-L", "td-S", "td-XN")
XN_TERM = "mu**2 * z**2 * (1 - z)"                           # td-XN's perturbation of NL
RAT = sp.Rational
QMAX = RAT(99, 100)
# The critical set (TARGET_HD_ADDENDUM_2.md section 2), (n, l) with 2l <= n - 1, and each band's MU1: q(MU1) <= 99/100
# exactly (gate PARAM), so the range [q(MU1), 1] meets Theorem HD's q <= 99/100.
MU1 = {(5, 2): RAT(1, 8), (6, 2): RAT(13, 100), (7, 2): RAT(13, 100), (7, 3): RAT(3, 25), (8, 2): RAT(13, 100),
       (8, 3): RAT(3, 25), (9, 2): RAT(13, 100), (9, 3): RAT(1, 8), (9, 4): RAT(3, 25)}
C_Q = RAT(1, 4)
Z1, ZT, SIG1, MUT = RAT(1, 4), RAT(8), RAT(1, 8), RAT(1, 32)
SIG1_TAMPER = RAT(1, 16)                                    # td-cover
MU_C = MUT / 2                                              # nc-bound's and d6's charge point
XN_POINTS = 24
ORDER = ("KAT", "E0n", "PARAM", "H", "S", "R", "L", "COVER", "Z0", "DIV-O", "DIV-T", "DIV-C", "THROAT", "CORNER",
         "FIRST", "INF", "XN", "POS-O", "POS-O'", "POS-T", "POS-C")
zeta, sig = sp.symbols("zeta sigma")


def parse_band(text):
    """'D,L' -> (n, l) as ints, for a band of the critical set."""
    parts = [int(v) for v in str(text).split(",")]
    if len(parts) != 2:
        raise CertificateError(f"--band {text!r}: expected D,L")
    n, ell = parts[0] - 2, parts[1]
    if (n, ell) not in MU1 or not 2 * ell <= n - 1:
        raise CertificateError(f"--band {text!r}: (D, l) = ({n + 2}, {ell}) is not in HD-X's critical set")
    return n, ell


def potentials(n, ell, control, UH=None):
    """(U, H) as polynomials in (x, m, delta): S5's U_- with hd.elementary's td-coeff tamper and H_-, or, in the
    development tests, a synthetic UH(n, ell, control)."""
    if UH is not None:
        return UH(n, ell, control)
    return U_of(n, control), H_minus(n)


def design(n, ell, control):
    """The registered constants of the band's design, with the controls' changes."""
    k = n - 1
    lo, hi = RAT(1, k), RAT(2, k - ell)
    ehat = {"nc-ehat-low": lo - RAT(1, 20), "d0-corner": lo, "nc-ehat-high": hi + RAT(1, 8),
            "d0-throat": hi}.get(control, (lo + hi) / 2)
    c = {"nc-Q0": RAT(0), "nc-Qneg": RAT(-1, 4)}.get(control, C_Q)
    nu = RAT(2 * ell + n - 2, 2)
    return {"k": k, "window": (lo, hi), "ehat": ehat, "c": c, "nu": nu, "a": -RAT(ell, k), "dhat": RAT(1, k),
            "nu_design": nu + (RAT(1, 100) if control == "td-nu" else 0)}


def P2(e):
    return sp.Poly(e, z, mu)


def build(n, ell, U, H, dz, flip=False):
    """The exact pieces of the design: param_n's p, eps = en/ed, Un, Ud, Hn, Hd, fn, fzn, fd, R, S, L, NL (Polys).
    flip (td-S): eps_n -> -eps_n, which moves the pole to z = +eps, inside the exterior."""
    p = param_n(n, ell)
    k = n - 1
    en, ed = sp.fraction(sp.cancel(dz["ehat"] * p["w"] / (1 + p["w"])))
    if sp.Poly(ed, mu).eval(RAT(1, 2)) < 0:
        en, ed = -en, -ed
    if flip:
        en = -en
    pp = exact_parts(n, ell, "none", UH=(U, H))
    (Un, Ud), (Hn, Hd), (fn, fzn, fd) = pp["U"], pp["H"], pp["f"]
    y = P2((1 - z) ** k)
    Rz = P2(sp.cancel((1 - (1 - z) ** k) / z))
    S = P2(ed * z + en)
    Dp = S * Rz * Hn
    Pi = (P2(-dz["nu_design"]) * Dp - P2(ell * ed) * y * Hn - P2(1 - z) * Hn.diff(z) * S * Rz
          + P2(dz["c"] * mu) * Dp)
    one_z = P2(1 - z)
    NL = (Un * Hd ** 2 * fd * S ** 2 * Rz ** 2
          - 64 * Ud * (one_z * fzn * Pi * Dp + fn * (-Pi * Dp + one_z * (Pi.diff(z) * Dp - Pi * Dp.diff(z)) + Pi ** 2)))
    return {"p": p, "en": sp.expand(en), "ed": sp.expand(ed), "Un": Un, "Ud": Ud, "Hn": Hn, "Hd": Hd, "fn": fn,
            "fzn": fzn, "fd": fd, "R": Rz, "S": S, "L": Ud * Hd ** 2 * fd, "NL": NL}


def charts(NL, kt=2, kc=2):
    """M = NL/mu; T = NL(mu zeta, mu)/mu^kt in (zeta, mu); K = NL(z, z sigma)/(z^kc sigma) in (z, sigma); each a dict
    {(i, j): c}, or None if its division is not exact."""
    terms = dict(NL.terms())
    divO = all(j >= 1 for (_, j) in terms)
    Tt, Kt = {}, {}
    for (i, j), c in terms.items():
        Tt[(i, i + j)] = Tt.get((i, i + j), 0) + c
        Kt[(i + j, j)] = Kt.get((i + j, j), 0) + c
    Tt = {key: c for key, c in Tt.items() if c != 0}
    Kt = {key: c for key, c in Kt.items() if c != 0}
    divT = all(b >= kt for (_, b) in Tt)
    divC = all(a >= kc and b >= 1 for (a, b) in Kt)
    return {"M": {(i, j - 1): c for (i, j), c in terms.items()} if divO else None,
            "T": {(a, b - kt): c for (a, b), c in Tt.items()} if divT else None,
            "K": {(a - kc, b - 1): c for (a, b), c in Kt.items()} if divC else None,
            "DIV-O": divO, "DIV-T": divT, "DIV-C": divC}


def edge(terms, slot, var):
    """The univariate polynomial in var of the terms whose other exponent is 0 (slot 0: keep i where j = 0)."""
    if terms is None:
        return None
    return sp.Poly(sum((c * var ** (i if slot == 0 else j) for (i, j), c in terms.items()
                        if (j if slot == 0 else i) == 0), sp.Integer(0)), var)


def throat_data(b, n, ell, H):
    """H(2) = H at the q = 1 horizon, L(0), R(0), eps_d(0) and w'(0)."""
    p = b["p"]
    H2 = sp.Rational(sp.cancel(sp.together(H.subs({m: p["m"], d: p["delta"].subs(mu, 0), x: 2}))))
    return {"H2": H2, "L0": sp.Rational(b["L"].as_expr().subs({mu: 0, z: 0})),
            "R0": sp.Rational(b["R"].as_expr().subs(z, 0)), "ed0": sp.Rational(sp.Poly(b["ed"], mu).eval(0)),
            "wp0": sp.Rational(sp.diff(p["w"], mu).subs(mu, 0))}


def gate_throat(ch, dz, td):
    T0 = edge(ch["T"], 0, zeta)
    if T0 is None:
        return False, "not run: the T chart's division failed", None
    k, a, eh, dh = dz["k"], dz["a"], dz["ehat"], dz["dhat"]
    s_ = zeta / td["wp0"]
    beta = 2 * a ** 2 * (eh - dh) * s_ + a * eh * ((a + 1) * eh - 2 * dh)
    want = sp.expand(64 * k ** 2 * td["H2"] ** 2 * td["L0"] * td["R0"] ** 2 * td["ed0"] ** 2 * td["wp0"] ** 2 * beta)
    diff_ = sp.expand(T0.as_expr() - want)
    return diff_ == 0, f"T(zeta, 0) = {T0.as_expr()}; minus the pencil limit: {diff_}", T0


def gate_corner(ch, T0):
    K0 = edge(ch["K"], 1, sig)
    if K0 is None or T0 is None:
        return False, "not run: a chart's division failed", K0
    if T0.degree() > 1:
        return False, f"T(zeta, 0) has degree {T0.degree()} > 1", K0
    t0, t1 = T0.as_expr().subs(zeta, 0), sp.diff(T0.as_expr(), zeta)
    diff_ = sp.expand(K0.as_expr() - (t1 + t0 * sig))
    return diff_ == 0, f"K(0, sigma) = {K0.as_expr()}; minus sigma T(1/sigma, 0): {diff_}", K0


def gate_first(ch, dz, td, ell, K0):
    M0 = edge(ch["M"], 0, z)
    if M0 is None or K0 is None:
        return False, "not run: a chart's division failed", None
    C0 = 128 * td["H2"] ** 2 * ell ** 2 * td["wp0"] * (dz["ehat"] - dz["dhat"])
    want = C0 * td["ed0"] ** 2 * td["R0"] ** 2 * td["L0"]
    m00 = M0.as_expr().subs(z, 0)
    m01 = sp.diff(M0.as_expr(), z).subs(z, 0)
    k00 = K0.as_expr().subs(sig, 0)
    ok = m00 == 0 and m01 == k00 and sp.expand(k00 - want) == 0
    return ok, f"M(0, 0) = {m00}; M_z(0, 0) = {m01}; K(0, 0) = {k00}; C0 eps_d(0)^2 R(0)^2 L(0) = {want} (C0 = {C0})", C0


def gate_inf(b, dz, mu1):
    p = b["p"]
    R1 = b["R"].as_expr().subs(z, 1)
    NL1 = sp.expand(b["NL"].as_expr().subs(z, 1))
    S1 = (b["S"].as_expr()).subs(z, 1)
    nu, c = dz["nu"], dz["c"]
    want = sp.expand(64 * p["m"] ** 2 * ((2 * nu + 1) * c * mu - c ** 2 * mu ** 2) * S1 ** 2 * R1 ** 2 * b["L"].as_expr())
    ident = sp.expand(NL1 - want) == 0
    pos = c > 0 and 2 * nu + 1 - c * mu1 > 0
    return ident and pos and R1 == 1, (f"NL(1, mu) = 64 m^2 ((2 nu + 1) c mu - c^2 mu^2) S(1, mu)^2 L(mu): {ident}; "
                                       f"R(1) = {R1}; c = {c} > 0 and 2 nu + 1 - c MU1 > 0: {pos}")


def direct_N(n, ell, U, H, dz, p):
    """N from its definition: U, H at param_n's (m, delta), f = 1 - x + q^2 x^2/4 unfactored, P as defined, P_z by
    sympy's diff (the independent route of XN)."""
    k = n - 1
    xx = p["xH"] * (1 - z) ** k
    Ue = U.subs({m: p["m"], d: p["delta"]}).subs(x, xx)
    He = H.subs({m: p["m"], d: p["delta"]}).subs(x, xx)
    fe = 1 - xx + p["q2"] * xx ** 2 / 4
    yy = (1 - z) ** k
    eps = dz["ehat"] * p["w"] / (1 + p["w"])
    P = -dz["nu_design"] - ell * yy / ((z + eps) * ((1 - yy) / z)) - (1 - z) * sp.diff(He, z) / He + dz["c"] * mu
    return Ue - 64 * He ** 2 * ((1 - z) * sp.diff(fe, z) * P + fe * (-P + (1 - z) * sp.diff(P, z) + P ** 2))


def gate_xn(n, ell, U, H, dz, b, mu1):
    Nd = direct_N(n, ell, U, H, dz, b["p"])
    rng = random.Random(1000 * n + ell)
    pts = [(RAT(rng.randint(1, 9999), 10000), mu1 * RAT(rng.randint(1, 9999), 10000)) for _ in range(XN_POINTS)]
    pts += [(RAT(1, 4), RAT(1, 32)), (RAT(1, 1000), RAT(1, 1000)), (RAT(999, 1000), mu1)]
    bad = []
    for zv, mv in pts:
        pt = {z: zv, mu: mv}
        lhs = b["NL"].eval(pt) / (b["S"].eval(pt) ** 2 * b["R"].eval(pt) ** 2 * b["L"].eval(pt))
        rhs = sp.cancel(sp.together(Nd.subs(pt)))
        if not rhs.is_Rational or sp.cancel(lhs - rhs) != 0:
            bad.append([str(zv), str(mv)])
    return not bad, f"{len(pts)} points, seed {1000 * n + ell}; mismatches at {bad[:5]}"


def positive_z(verify, poly_z, a, b_, stats, minrec, label):
    """Exact: the univariate polynomial in z is > 0 on [a, b_]."""
    p2 = Poly2({(i, 0): Q(c) for (i,), c in sp.Poly(poly_z, z).terms()})
    verify(p2, (Q(a), Q(b_), fmpq(0), fmpq(0)), 1, 30, stats, label, minrec)


def gate(checks, label, fn):
    """Run fn() -> (ok, detail); a CertificateError is a failed gate."""
    try:
        checks[label] = fn()
    except CertificateError as exc:
        checks[label] = (False, str(exc)[:400])


def nc_bound(verify, b, dz, stats, minrec):
    """The planted bound state at mu = MU_C: (a) nc_bound_a, then (b) the certificate on the planted potential."""
    certified, info, plant = nc_bound_a(verify, b, stats, minrec)
    refused, msg = nc_bound_b(verify, b, plant, stats)
    info["refusal"] = msg
    return certified, refused, info


def nc_bound_a(verify, b, stats, minrec):
    """(a): the support [za, zb] inside the band's U_- < 0 region near the horizon at mu = MU_C (BHM-106 section 5),
    checked exactly; K = ceil(2 I1/I2) from a midpoint rule; and Q[b] = int f (1 - z)^2 b_z^2 + (W - K b) b^2 dz < 0
    certified in Arb.  Returns (certified, info, the planted data for (b))."""
    mc = MU_C
    sub = {mu: mc}
    Ud_c = sp.Rational(b["Ud"].as_expr().subs(sub))
    Un_c = sp.Poly(sp.expand(b["Un"].as_expr().subs(sub)), z)
    sgn = 1 if Ud_c > 0 else -1
    u0 = sgn * Un_c.eval(0)
    info = {"mu_c": str(mc), "U(z = 0)": str(u0 / abs(Ud_c))}
    if not u0 < 0:
        raise CertificateError(f"nc-bound: U_- >= 0 at the horizon at mu = {mc}")
    roots = Un_c.intervals(inf=0, sup=1, eps=RAT(1, 10 ** 6))
    if not roots:
        raise CertificateError("nc-bound: no root of U_- in (0, 1) at mu = MU_C")
    zl = min(RAT(iv[0][0]) for iv in roots)
    if zl == 0:
        zl = min(iv[0][1] for iv in roots) / 2
    za = RAT(math.ceil(zl / 5 * 10000), 10000)
    zb = RAT(math.floor(4 * zl / 5 * 10000), 10000)
    if not 0 < za < zb:
        raise CertificateError(f"nc-bound: empty support from z_U >= {zl}")
    positive_z(verify, -sgn * Un_c.as_expr(), za, zb, stats, minrec, "nc-bound U_- < 0 on the support")
    bexpr = (z - za) ** 2 * (zb - z) ** 2
    fq = b["fn"].as_expr().subs(sub) / b["fd"].as_expr().subs(sub)
    Wq = (b["Un"].as_expr().subs(sub) * b["Hd"].as_expr().subs(sub) ** 2
          / (64 * b["Ud"].as_expr().subs(sub) * b["Hn"].as_expr().subs(sub) ** 2))
    kin = fq * (1 - z) ** 2 * sp.diff(bexpr, z) ** 2
    nodes = [za + (zb - za) * (RAT(2 * j + 1, 800)) for j in range(400)]
    I1f = sum(float((kin + Wq * bexpr ** 2).subs(z, t)) for t in nodes) * float(zb - za) / 400
    I2f = sum(float((bexpr ** 3).subs(z, t)) for t in nodes) * float(zb - za) / 400
    K = sp.Integer(math.ceil(2 * I1f / I2f)) if I1f > 0 else sp.Integer(1)
    info.update({"support": [str(za), str(zb)], "z_U lower bound": str(zl), "K": str(K), "I1_float": I1f})
    ctx.prec = 128
    polys = {"kn": sp.Poly(sp.expand(b["fn"].as_expr().subs(sub) * (1 - z) ** 2 * sp.diff(bexpr, z) ** 2), z),
             "Un": Un_c, "Hn": sp.Poly(sp.expand(b["Hn"].as_expr().subs(sub)), z), "b2": sp.Poly(sp.expand(bexpr ** 2), z),
             "Kb3": sp.Poly(sp.expand(K * bexpr ** 3), z)}
    cf = {key: [acb(Q(c)) for c in pl.all_coeffs()[::-1]] for key, pl in polys.items()}
    fd_c = acb(Q(sp.Rational(b["fd"].as_expr().subs(sub))))
    Hd2 = acb(Q(sp.Rational(b["Hd"].as_expr().subs(sub)))) ** 2
    Ud_a = acb(Q(Ud_c))

    def horner(cs, t):
        acc = acb(0)
        for c in reversed(cs):
            acc = acc * t + c
        return acc

    def integrand(t, analytic):
        Hv = horner(cf["Hn"], t)
        return (horner(cf["kn"], t) / fd_c + horner(cf["Un"], t) * Hd2 / (64 * Ud_a * Hv * Hv) * horner(cf["b2"], t)
                - horner(cf["Kb3"], t))

    Qv = acb.integral(integrand, acb(Q(za)), acb(Q(zb)))
    certified = bool(Qv.real < 0)
    info["Q_b"] = Qv.real.str(10)
    return certified, info, {"K": K, "za": za, "zb": zb, "bexpr": bexpr, "Ud_c": Ud_c}


def nc_bound_b(verify, b, plant, stats):
    """(b): NL of the planted potential W - K b at mu = MU_C, i.e. NL - 64 Hn^2 Ud fd K b S^2 R^2, on [za, zb]: a
    certificate must refuse it.  Returns (refused, message)."""
    sub = {mu: MU_C}
    planted = sp.Poly(sp.expand(b["NL"].as_expr().subs(sub) - 64 * b["Hn"].as_expr().subs(sub) ** 2 * plant["Ud_c"]
                                * b["fd"].as_expr().subs(sub) * plant["K"] * plant["bexpr"]
                                * b["S"].as_expr().subs(sub) ** 2 * b["R"].as_expr() ** 2), z)
    try:
        positive_z(verify, planted.as_expr(), plant["za"], plant["zb"], stats, {}, "nc-bound on the planted potential")
        return False, ""
    except CertificateError as exc:
        return True, str(exc)[:300]


def gates(n, ell, control, root, UH, verify, stats, minrec):
    """Every check but the four POS charts and nc-bound, in the record's order: KAT ... XN.  Returns the checks, the
    record, the timings, the exact pieces b, the charts ch, MU1 and SIG1.  run() calls it, so the development tests can
    run the real potential path through it without running a POS chart."""
    checks, timing = {}, {}
    mu1 = MU1[(n, ell)]
    dz = design(n, ell, control)
    rec = {"band": {"D": n + 2, "l": ell, "n": n, "k": dz["k"]},
           "design": {"nu": str(dz["nu"]), "nu_design": str(dz["nu_design"]), "ehat": str(dz["ehat"]),
                      "window": [str(v) for v in dz["window"]], "c": str(dz["c"]), "a": str(dz["a"])},
           "charts": {"MU1": str(mu1), "Z1": str(Z1), "ZT": str(ZT), "SIG1": str(SIG1_TAMPER if control == "td-cover"
                                                                                   else SIG1), "MUT": str(MUT)},
           "max_depth": MAX_DEPTH}
    ok, res = kats(verify)
    checks["KAT"] = (ok, str(res))
    checks["E0n"] = gate_E0n(root, control)
    U, H = potentials(n, ell, control, UH)
    t0 = time.time()
    b = build(n, ell, U, H, dz, flip=control == "td-S")
    timing["build_s"] = round(time.time() - t0, 2)
    if control == "td-XN":                 # addendum 1: one term of NL perturbed, after the build and before XN
        b["NL"] = b["NL"] + P2(sp.sympify(XN_TERM, locals={"mu": mu, "z": z}))
        rec["td-XN"] = {"term added to NL": XN_TERM}
    p = b["p"]
    rec["eps"] = {"num": str(b["en"]), "den": str(b["ed"])}

    def g_param():
        pg = param_n(n, ell, "td-param") if control == "td-param" else p    # addendum 1: only the gate's input
        ids = [sp.cancel(pg["s"] ** 2 - (1 + 4 * pg["m"] * pg["q2"] / (n + 1) ** 2)) == 0,
               sp.cancel(pg["q2"].subs(mu, 0) - 1) == 0, sp.cancel(pg["xH"].subs(mu, 0) - 2) == 0,
               sp.cancel(pg["delta"].subs(mu, 0) - RAT(1, (ell + n) * (n + 1))) == 0,
               sp.cancel(b["en"] / b["ed"] - dz["ehat"] * pg["w"] / (1 + pg["w"])) == 0]
        q2 = sp.cancel(pg["q2"].subs(mu, mu1))
        rec["q(MU1)^2"] = str(q2)
        rec["q(MU1)_approx"] = float(sp.sqrt(q2).evalf(20))
        wn, wd = sp.fraction(sp.cancel(sp.diff(pg["w"], mu)))
        sw = 1 if sp.Poly(wn, mu).eval(RAT(1, 2)) > 0 else -1
        sd = 1 if sp.Poly(wd, mu).eval(RAT(1, 2)) > 0 else -1
        positive_mu(verify, sw * wn, 0, 1, stats, minrec, "w' numerator")
        positive_mu(verify, sd * wd, 0, 1, stats, minrec, "w' denominator")
        ok_ = all(ids) and q2 <= QMAX ** 2 and sw * sd > 0
        return ok_, (f"identities (s^2, q(0) = 1, x_H(0) = 2, delta(0), eps): {ids}; q(MU1)^2 = {q2} <= (99/100)^2: "
                     f"{q2 <= QMAX ** 2}; w increasing on [0, 1]: {sw * sd > 0}")

    def g_H():
        Hg = H - n * (n + 1) * x if control == "td-H" else H          # addendum 1: only the gate's input
        coef = all(c > 0 for _, c in sp.Poly(Hg, x, d, m).terms())
        dn, dd = sp.fraction(sp.cancel(p["delta"]))
        sn = 1 if sp.Poly(dn, mu).eval(0) > 0 else -1
        sdd = 1 if sp.Poly(dd, mu).eval(0) > 0 else -1
        positive_mu(verify, sn * dn, 0, mu1, stats, minrec, "delta numerator")
        positive_mu(verify, sdd * dd, 0, mu1, stats, minrec, "delta denominator")
        return coef and sn * sdd > 0, f"every coefficient of H in (x, delta, m) > 0: {coef}; delta > 0 on [0, MU1]"

    def g_S():
        en0 = sp.Poly(b["en"], mu).eval(0) == 0
        positive_mu(verify, sp.cancel(b["en"] / mu), 0, mu1, stats, minrec, "eps_n/mu")
        positive_mu(verify, b["ed"], 0, mu1, stats, minrec, "eps_d")
        return en0, f"eps_n = {b['en']}, eps_n(0) = 0: {en0}; eps_n/mu > 0 and eps_d = {b['ed']} > 0 on [0, MU1]"

    def g_R():
        positive_z(verify, (-1 if control == "td-R" else 1) * b["R"].as_expr(), 0, 1, stats, minrec, "R")
        return True, f"R = {b['R'].as_expr()} > 0 on [0, 1]"

    def g_L():
        positive_mu(verify, (-1 if control == "td-L" else 1) * b["L"].as_expr(), 0, mu1, stats, minrec, "L")
        return True, "L = Ud Hd^2 fd > 0 on [0, MU1]"

    gate(checks, "PARAM", g_param)
    gate(checks, "H", g_H)
    gate(checks, "S", g_S)
    gate(checks, "R", g_R)
    gate(checks, "L", g_L)
    sig1 = SIG1_TAMPER if control == "td-cover" else SIG1
    cov = [ZT * sig1 >= 1, ZT * MUT <= Z1, Z1 * sig1 <= mu1, 0 < MUT < mu1, 0 < Z1 < 1]
    checks["COVER"] = (all(cov), f"ZT SIG1 >= 1, ZT MUT <= Z1, Z1 SIG1 <= MU1, 0 < MUT < MU1, 0 < Z1 < 1: {cov}")
    t0 = time.time()
    gate(checks, "XN_pending", lambda: gate_xn(n, ell, U, H, dz, b, mu1))
    timing["XN_s"] = round(time.time() - t0, 2)
    xn = checks.pop("XN_pending")
    if control == "d6":
        base = charts(b["NL"])
        T2 = sum((c * 2 ** i * MU_C ** j for (i, j), c in base["T"].items()), sp.Integer(0)) if base["T"] else None
        if T2 is None or not T2 > 0:
            raise CertificateError(f"d6: T(2, MU_C) = {T2} is not > 0 on the base design")
        K6 = 2 * T2 / (MU_C ** 2 * (1 - 2 * MU_C))
        rec["d6"] = {"K6": str(K6), "T(2, MU_C) base": str(T2), "defect": "K6 mu^2 (z - mu)(3 mu - z)(1 - z)"}
        b["NL"] = b["NL"] - P2(K6 * mu ** 2 * (z - mu) * (3 * mu - z) * (1 - z))
    NL = b["NL"]
    checks["Z0"] = (sp.expand(NL.as_expr().subs(mu, 0)) == 0, "NL(z, 0) = 0 identically")
    kt = kc = 3 if control == "td-div" else 2
    ch = charts(NL, kt, kc)
    checks["DIV-O"] = (ch["DIV-O"], "NL divisible by mu")
    checks["DIV-T"] = (ch["DIV-T"], f"NL(mu zeta, mu) divisible by mu^{kt}")
    checks["DIV-C"] = (ch["DIV-C"], f"NL(z, z sigma) divisible by z^{kc} sigma")
    td = throat_data(b, n, ell, H)
    rec["throat_data"] = {key: str(v) for key, v in td.items()}
    ok, det, T0 = gate_throat(ch, dz, td)
    checks["THROAT"] = (ok, det[:600])
    ok, det, K0 = gate_corner(ch, T0)
    checks["CORNER"] = (ok, det[:600])
    ok, det, C0 = gate_first(ch, dz, td, ell, K0)
    checks["FIRST"] = (ok, det[:600])
    rec["C0"] = str(C0)
    gate(checks, "INF", lambda: gate_inf(b, dz, mu1))
    checks["XN"] = xn
    rec["degrees"] = {"NL": [NL.degree(z), NL.degree(mu)],
                      "M": None if ch["M"] is None else [max(i for i, _ in ch["M"]), max(j for _, j in ch["M"])],
                      "T": None if ch["T"] is None else [max(i for i, _ in ch["T"]), max(j for _, j in ch["T"])],
                      "K": None if ch["K"] is None else [max(i for i, _ in ch["K"]), max(j for _, j in ch["K"])]}
    return checks, rec, timing, b, ch, mu1, sig1, dz


def run(n, ell, control, root, UH=None):
    verify = tampered_prove_sign if control == "td-verifier" else prove_sign
    stats, minrec = {}, {}
    checks, rec, timing, b, ch, mu1, sig1, dz = gates(n, ell, control, root, UH, verify, stats, minrec)
    for label, terms, box in (("POS-O", ch["M"], (Q(Z1), fmpq(1), fmpq(0), Q(mu1))),
                              ("POS-O'", ch["M"], (fmpq(0), Q(Z1), Q(MUT), Q(mu1))),
                              ("POS-T", ch["T"], (fmpq(0), Q(ZT), fmpq(0), Q(MUT))),
                              ("POS-C", ch["K"], (fmpq(0), Q(Z1), fmpq(0), Q(sig1)))):
        t1 = time.time()
        if terms is None:
            checks[label] = (False, "not run: the chart's division failed")
            continue
        try:
            verify(Poly2({key: Q(c) for key, c in terms.items()}), box, 1, MAX_DEPTH, stats, label, minrec)
            checks[label] = (True, f"> 0 on {[str(v) for v in box]}; least Bernstein coefficient {minrec[label]}")
        except CertificateError as exc:
            checks[label] = (False, str(exc)[:400])
        timing[label] = round(time.time() - t1, 2)
    if control == "nc-bound":
        t1 = time.time()
        try:
            certified, refused, info = nc_bound(verify, b, dz, stats, minrec)
            rec["nc-bound"] = info
            checks["nc-bound (a)"] = (certified, f"Q[b] certified < 0 on the planted potential: {certified}; {info}")
            checks["nc-bound (b)"] = (not refused, f"the certificate on the planted potential: refused {refused}")
        except CertificateError as exc:
            checks["nc-bound (a)"] = (False, str(exc)[:400])
            checks["nc-bound (b)"] = (True, "not run")
        timing["nc-bound"] = round(time.time() - t1, 2)
    rec["bernstein_leaves"] = stats
    rec["min_bernstein"] = {key: str(v) for key, v in minrec.items()}
    return checks, rec, timing


def main(argv=None, UH=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--band", required=True)
    ap.add_argument("--control", choices=CONTROLS, default="none")
    ap.add_argument("--root", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    a = ap.parse_args(argv)
    t0, start = time.time(), datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    record = {"claim": "results/hdx/critical/PREREG.md (HD-X-2: the critical bands, q in [q(MU1), 1))",
              "band_arg": a.band, "control": a.control, "provenance": provenance(),
              "archive_sha256": os.environ.get("BHM_ARCHIVE", "unknown")}
    timing = {}
    try:
        n, ell = parse_band(a.band)
        checks, rec, timing = run(n, ell, a.control, a.root, UH)
        record.update(rec)
        record["checks"] = {k: {"ok": bool(ok), "detail": det} for k, (ok, det) in checks.items()}
        failed = [k for k, (ok, _) in checks.items() if not ok]
        verdict = "VERIFIED" if not failed else "REJECT: " + ", ".join(failed)
    except Exception as exc:  # noqa: BLE001  (fail-closed)
        verdict = f"REJECT: exception {type(exc).__name__}: {exc}"
    record["verdict"] = verdict
    record["timing"] = {**timing, "utc_start": start, "t_total_s": round(time.time() - t0, 2)}
    try:
        os.makedirs(a.out, exist_ok=True)
        dump_json(plain(record), f"{a.out}/result.json")
    except Exception as exc:  # noqa: BLE001  (fail-closed: an unwritten record is a REJECT)
        verdict = record["verdict"] = f"REJECT: record not written: {type(exc).__name__}: {exc}"
    for k, v in record.get("checks", {}).items():
        print(f"{k}: {'PASS' if v['ok'] else 'FAIL'}  {v['detail'][:300]}")
    print(verdict)
    return 0 if verdict == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
