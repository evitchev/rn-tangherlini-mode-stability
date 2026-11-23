"""Stage 2, step 2, HD-PILOT (results/hd/pilot/PREREG.md): the untrusted design pilot that fixes q_max(D).

    python -m hd.pilot --out DIR [--root REPO]

Floats only.  Nothing here is part of a certificate: the pilot chooses q_max(D) by the rule of TARGET_HD.md section 4,
and HD-S's exact verification is the trust base.

For each band of TARGET_HD.md section 3 and each rung q_r in RUNGS above the band's lower end q_lo (q_split of
hd.elementary.BANDS, or 0 for a band from 0+), the pilot takes NSAMP charges, the Chebyshev-Lobatto points in mu on
[mu(q_r), mu(q_lo)].  At each one it
  - integrates (1 - z) P_z = P - P^2 + [W - (1 - z) f_z P]/f, W = U_-/(64 H_-^2), in tau = log(z/(1 - z)) for the
    regular solution P_true = rho psi_1'/psi_1 at the horizon, and log psi_1 (as p3.scert; RK4, step H_TAU);
  - forms rule 2's design (results/p3/PREREG_ADDENDUM_1.md)  P_d = P_true - eps (rho - 1)/(f psi_1^2) - eps z^6;
  - interpolates P_d at the Chebyshev-Lobatto nodes of each degree in DEGREES, in z on [0, 1] and in
    zeta = z/(z + delta_t) on [0, 1/(1 + delta_t)], delta_t = 1 - x_H/x_- = 2w/(1 + w) (the throat width);
  - evaluates the bracket  B = N/(64 H_-^2) = W - [(1 - z) f_z P + f (-P + (1 - z) P_z + P^2)]  on GRID, and the
    scaled slack  sigma = min B / B(1).
A (band, rung) qualifies if, in some variable and at some degree, sigma >= THETA at every sample: first with
eps = EPS[0]; with the fallback EPS[1] only if EPS[0] qualifies nowhere.  q_max(D) is the largest rung at which every
band of D active there qualifies (a rung with no active band qualifies); if none, D is not attempted at this stage.
Gates and controls (all in the same run; VALID only if all are as registered):
    PG1   the recorded rule-2 certificates T1 and G1 (BHM-025; N > 0 proved exactly): sigma > 0 under this evaluator
    PG2   the pilot's own design at T1 and G1 (z, degree 28, eps = 1/50): sigma >= THETA
    NC-H  T1's pilot design plus c (1 - z), which raises P(0) to 1/10 above the horizon bound W(0)/f_z(0) and leaves
          P(1) unchanged (PREREG_ADDENDUM_1.md): sigma < 0
    NC-B  a planted bound state at G1's setting, W - K b on [3/10, 3/5], b = ((z - 3/10)(3/5 - z))^2, K = 2 I1/I2
          (the trial function b then has energy -I1 < 0): no qualifying design at all, and G1's design gives sigma < 0
"""
import argparse
import json
import math
import os
import sys
import time
from fractions import Fraction

import sympy as sp

from hd.elementary import BANDS
from ki.potentials import H_minus, U_minus, d, m, x
from p3.scert import cheb_coeffs
from qnm1c.common import dump_json, provenance

RUNGS = (Fraction(9, 10), Fraction(97, 100), Fraction(99, 100))
ZERO_BANDS = ((6, 2), (7, 2), (8, 2), (9, 2), (9, 3))      # (n, l) from 0+: D = 8..11 l = 2, D = 11 l = 3
EPS = (Fraction(1, 50), Fraction(1, 200))                  # rule 2's eps1 = eps2; the second is the fallback
KPOW = 6
DEGREES = (16, 20, 24, 28, 32, 40, 48)                      # the cap is the last
VARIABLES = ("z", "zeta")
THETA = 1e-4
NSAMP = 9
H_TAU, TAU0 = 0.002, -27.0
BREAKDOWN = 1e12
GRID = sorted({0.0, 1.0} | {1 / (1 + math.exp(-k / 200)) for k in range(-2800, 2801)}
              | {k / 1000 for k in range(1, 1000)})
ZA, ZB = 0.3, 0.6
CERTS = {"T1": ((4, 2, Fraction(1, 6)), "results/p3/rule2/record/T1/result.json"),
         "G1": ((8, 2, Fraction(1)), "results/p3/rule2/record/G1/result.json")}


class Breakdown(ArithmeticError):
    """The Riccati integration left the finite range: psi_1 vanishes (a zero-energy node)."""


# ---------------------------------------------------------------- the setting (floats)
_UH = {}


def uh(n):
    """U_-(n), H_-(n) of ki.potentials as float functions of (m, delta, x)."""
    if n not in _UH:
        _UH[n] = (sp.lambdify((m, d, x), U_minus(n), "math"), sp.lambdify((m, d, x), H_minus(n), "math"))
    return _UH[n]


class Setting:
    """D = n + 2, l and the charge through mu (TARGET_HD.md section 1), units r_H = 1, z = 1 - 1/rho:
    x = x_H (1 - z)^(n-1), f = (1 - (1 - z)^(n-1)) (1 - k (1 - z)^(n-1)) with k = x_H/x_-.  well: a planted K b(z).
    funcs: synthetic (U, H) for the development tests."""

    def __init__(self, n, ell, mu, well=0.0, funcs=None):
        mu = float(mu)
        A = (ell + n) + (ell - 1) * mu * mu
        B = 2 * ell + n - 1
        w = B * mu / A
        s = B * ((ell + n) - (ell - 1) * mu * mu) / ((n + 1) * A)
        self.n, self.ell, self.mu, self.well = n, ell, mu, well
        self.m = (ell - 1) * (ell + n)
        self.delta = (s - 1) / (2 * self.m)
        self.q = math.sqrt(max(0.0, 1 - w * w))
        self.xH = 2 / (1 + w)
        self.k = (1 - w) / (1 + w)
        self.dt = 2 * w / (1 + w)
        self.U, self.H = funcs or uh(n)

    def f(self, z):
        y = (1 - z) ** (self.n - 1)
        return (1 - y) * (1 - self.k * y)

    def fz(self, z):
        y1 = (1 - z) ** (self.n - 2)
        y = y1 * (1 - z)
        return (self.n - 1) * y1 * ((1 - self.k * y) + self.k * (1 - y))

    def W(self, z):
        xx = self.xH * (1 - z) ** (self.n - 1)
        h = self.H(self.m, self.delta, xx)
        v = self.U(self.m, self.delta, xx) / (64 * h * h)
        if self.well and ZA < z < ZB:
            v -= self.well * ((z - ZA) * (ZB - z)) ** 2
        return v


def mu_of_q(n, ell, q):
    """The mu in [0, 1] with w(mu) = B mu/A = sqrt(1 - q^2)."""
    w = math.sqrt(1 - q * q)
    if w >= 1:
        return 1.0
    B = 2 * ell + n - 1
    return (B - math.sqrt(B * B - 4 * (ell - 1) * (ell + n) * w * w)) / (2 * (ell - 1) * w)


# ---------------------------------------------------------------- design (rule 2)
def riccati(S, nodes):
    """{z: (P_true, log psi_1)} at the given z in [0, 1]: the regular solution at the horizon, psi_1(r_H) = 1."""
    P0 = S.W(0.0) / S.fz(0.0)
    Pinf = (1 + math.sqrt(1 + 4 * S.W(1.0))) / 2

    def rhs(tau, Y):
        zz = 1 / (1 + math.exp(-tau))
        P = Y[0]
        return (zz * (P - P * P + (S.W(zz) - (1 - zz) * S.fz(zz) * P) / S.f(zz)), zz * P)

    out, tau, Y = {}, TAU0, (P0, 0.0)
    for zk in sorted(set(nodes)):
        if zk <= 0:
            out[zk] = (P0, 0.0)
            continue
        if zk >= 1:
            out[zk] = (Pinf, math.inf)
            continue
        tk = math.log(zk / (1 - zk))
        while tau < tk:
            hh = min(H_TAU, tk - tau)
            k1 = rhs(tau, Y)
            k2 = rhs(tau + hh / 2, tuple(a + hh / 2 * b for a, b in zip(Y, k1)))
            k3 = rhs(tau + hh / 2, tuple(a + hh / 2 * b for a, b in zip(Y, k2)))
            k4 = rhs(tau + hh, tuple(a + hh * b for a, b in zip(Y, k3)))
            Y = tuple(a + hh / 6 * (b1 + 2 * b2 + 2 * b3 + b4) for a, b1, b2, b3, b4 in zip(Y, k1, k2, k3, k4))
            tau += hh
            if not (math.isfinite(Y[0]) and abs(Y[0]) < BREAKDOWN and math.isfinite(Y[1])):
                raise Breakdown(f"P = {Y[0]!r} at z = {1 / (1 + math.exp(-tau)):.6g}")
        out[zk] = Y
    return out


def design_value(S, zk, P, lg, eps):
    if zk <= 0:
        t1 = 1 / S.fz(0.0)                                   # (rho - 1)/f -> 1/f_z(0) at the horizon
    elif zk >= 1:
        t1 = 0.0
    else:
        t1 = (zk / (1 - zk)) / S.f(zk) * math.exp(-2 * lg)
    return P - eps * t1 - eps * zk ** KPOW


def nodes(S, var, dg):
    """(v_k, z_k): Chebyshev-Lobatto nodes in the variable on [0, vmax], and their z."""
    vmax = 1.0 if var == "z" else 1 / (1 + S.dt)
    out = []
    for k in range(dg + 1):
        v = vmax * (1 - math.cos(math.pi * k / dg)) / 2
        if k == 0:
            zk = 0.0
        elif k == dg:
            zk = 1.0
        else:
            zk = v if var == "z" else S.dt * v / (1 - v)
        out.append((v, zk))
    return vmax, out


def cheb_deriv(c):
    """Chebyshev coefficients of the u-derivative of sum c_j T_j(u)."""
    dg = len(c) - 1
    if dg == 0:
        return [0.0]
    dc = [0.0] * (dg + 1)
    dc[dg - 1] = 2 * dg * c[dg]
    for j in range(dg - 1, 0, -1):
        dc[j - 1] = dc[j + 1] + 2 * j * c[j]
    dc[0] /= 2
    return dc[:dg]


def clenshaw(c, u):
    b1 = b2 = 0.0
    for cj in reversed(c[1:]):
        b1, b2 = 2 * u * b1 - b2 + cj, b1
    return u * b1 - b2 + c[0]


class Fit:
    """P as a Chebyshev series in the variable; P(z) and P_z(z)."""

    def __init__(self, S, var, c, vmax):
        self.var, self.c, self.dc, self.vmax, self.dt = var, c, cheb_deriv(c), vmax, S.dt

    def __call__(self, z):
        if self.var == "z":
            u = 2 * z - 1
            return clenshaw(self.c, u), 2 * clenshaw(self.dc, u)
        u = 2 * (z / (z + self.dt)) / self.vmax - 1
        return clenshaw(self.c, u), clenshaw(self.dc, u) * (2 / self.vmax) * self.dt / (z + self.dt) ** 2


def design_fit(S, sol, var, dg, eps):
    vmax, nd = nodes(S, var, dg)
    vals = [design_value(S, zk, *sol[zk], eps) for _, zk in nd]
    return Fit(S, var, cheb_coeffs(vals), vmax)


# ---------------------------------------------------------------- measurement
def tabulate(S):
    """W, f, f_z on GRID."""
    return [(z, S.W(z), S.f(z), S.fz(z)) for z in GRID]


def slack(tab, P_of):
    """sigma = min B / B(1) on GRID, and the z of the minimum; None if B(1) <= 0 or a value is not finite."""
    Bs = []
    for z, W, f, fz in tab:
        P, Pz = P_of(z)
        Bs.append(W - ((1 - z) * fz * P + f * (-P + (1 - z) * Pz + P * P)))
    B1 = Bs[-1]                                              # GRID[-1] = 1
    if not all(math.isfinite(b) for b in Bs) or B1 <= 0:
        return None, None
    i = min(range(len(Bs)), key=Bs.__getitem__)
    return Bs[i] / B1, tab[i][0]


def design_slack(S, tab, sol, eps):
    """The exact design's sigma, from BHM-024's identity B = eps/psi^2 + eps z^5[...] - rho^2 f eta^2 (no fit)."""
    Pinf = sol[1.0][0]
    Bs = []
    for z, W, f, fz in tab:
        P, lg = sol[z]
        if z <= 0:
            Bs.append(eps)
        elif z >= 1:
            Bs.append(eps * (2 * Pinf - 1) - eps * eps)
        else:
            ip2 = math.exp(-2 * lg)
            eta = eps * z * ip2 / f + eps * z ** KPOW * (1 - z)
            Bs.append(eps * ip2 + eps * z ** (KPOW - 1) * (z * ((1 - z) * fz + f * (2 * P - 1)) + KPOW * f * (1 - z))
                      - f * eta * eta / (1 - z) ** 2)
    return min(Bs) / Bs[-1]


def sample(S):
    """The planning record of one charge: every (eps, variable, degree)."""
    rec = {"mu": S.mu, "q": S.q, "delta_t": S.dt}
    need = list(GRID)
    for var in VARIABLES:
        for dg in DEGREES:
            need += [zk for _, zk in nodes(S, var, dg)[1]]
    try:
        sol = riccati(S, need)
        tab = tabulate(S)
        lmin, zmin = min((sol[z][1], z) for z in GRID[:-1])
        rec.update({"P_true(0)": sol[0.0][0], "P_true(1)": sol[1.0][0], "min_psi1": math.exp(lmin),
                    "z_min_psi1": zmin})
        for eps in EPS:
            e = float(eps)
            r = {"sigma_design": design_slack(S, tab, sol, e)}
            for var in VARIABLES:
                for dg in DEGREES:
                    sg, zm = slack(tab, design_fit(S, sol, var, dg, e))
                    r[f"{var} {dg}"] = sg
                    r[f"{var} {dg} z_min"] = zm
            rec[f"eps {eps}"] = r
    except ArithmeticError as exc:                           # Breakdown, overflow: the sample fails (fail-closed)
        rec = {"mu": S.mu, "q": S.q, "delta_t": S.dt, "breakdown": f"{type(exc).__name__}: {exc}"}
    return rec


def qualify(samples):
    """{eps: {var: least degree with sigma >= THETA at every sample, or None}}, and the design for HD-S."""
    out, design = {}, None
    for eps in EPS:
        out[str(eps)] = {}
        for var in VARIABLES:
            least = None
            for dg in DEGREES:
                sig = [s.get(f"eps {eps}", {}).get(f"{var} {dg}") for s in samples]
                if all(v is not None and v >= THETA for v in sig):
                    least = dg
                    break
            out[str(eps)][var] = least
        cands = [(dg, VARIABLES.index(v), v) for v, dg in out[str(eps)].items() if dg is not None]
        if design is None and cands:
            dg, _, var = min(cands)
            design = {"eps": str(eps), "variable": var, "degree": dg}
    return out, design


# ---------------------------------------------------------------- gates and controls
def cert_poly(root, path):
    with open(os.path.join(root, path)) as fh:
        P = json.load(fh)["result"]["P"]
    co = {}
    for k, v in P.items():
        i, j = (int(t) for t in k.strip("()").split(","))
        if j != 0:
            raise ValueError("a point certificate has no mu-dependence")
        co[i] = Fraction(v)
    return [co.get(i, Fraction(0)) for i in range(max(co) + 1)]


def exact_eval(co):
    """P(z) and P_z(z) of the monomial coefficients, evaluated exactly at the float z, then rounded."""
    dco = [i * c for i, c in enumerate(co)][1:]

    def ev(z):
        zf = Fraction(z)
        p = dp = Fraction(0)
        for c in reversed(co):
            p = p * zf + c
        for c in reversed(dco):
            dp = dp * zf + c
        return float(p), float(dp)
    return ev


def bound_K(S):
    """NC-P1's construction: K = 2 I1/I2 with the trial function b, so that its energy I1 - K I2 = -I1 < 0."""
    nq = 2000
    h = (ZB - ZA) / nq
    I1 = I2 = 0.0
    for i in range(nq):
        z = ZA + (i + 0.5) * h
        b = ((z - ZA) * (ZB - z)) ** 2
        bz = 2 * (z - ZA) * (ZB - z) * (ZA + ZB - 2 * z)
        I1 += (S.f(z) * bz * bz * (1 - z) ** 2 + S.W(z) * b * b) * h
        I2 += b * b * b * h
    return 2 * I1 / I2, I1


def gates(root):
    g = {}
    own = {}
    for name, ((n, ell, mu), path) in CERTS.items():
        S = Setting(n, ell, mu)
        tab = tabulate(S)
        sg, zm = slack(tab, exact_eval(cert_poly(root, path)))
        g[f"PG1 {name}"] = {"sigma": sg, "z_min": zm, "ok": sg is not None and sg > 0}
        sol = riccati(S, list(GRID) + [zk for _, zk in nodes(S, "z", 28)[1]])
        own[name] = (S, tab, design_fit(S, sol, "z", 28, float(EPS[0])))
        sg, zm = slack(tab, own[name][2])
        g[f"PG2 {name}"] = {"sigma": sg, "z_min": zm, "ok": sg is not None and sg >= THETA}
    S, tab, fit = own["T1"]
    shift = S.W(0.0) / S.fz(0.0) - fit(0.0)[0] + 0.1          # addendum 1: + shift (1 - z) keeps P(1)
    sg, zm = slack(tab, lambda z: (fit(z)[0] + shift * (1 - z), fit(z)[1] - shift))
    g["NC-H"] = {"shift": shift, "sigma": sg, "z_min": zm, "ok": sg is not None and sg < 0}
    S0 = own["G1"][0]
    K, I1 = bound_K(S0)
    Sw = Setting(8, 2, 1, well=K)
    rec = sample(Sw)
    q, _ = qualify([rec])
    none = all(v is None for e in q.values() for v in e.values())
    sg, zm = slack(tabulate(Sw), own["G1"][2])
    g["NC-B"] = {"K": K, "I1": I1, "pilot": {k: v for k, v in rec.items() if k in ("breakdown", "min_psi1")},
                 "qualifies": q, "G1 design on the well: sigma": sg, "z_min": zm,
                 "ok": none and I1 > 0 and sg is not None and sg < 0}
    return g


# ---------------------------------------------------------------- the pilot
def bands():
    """(n, l, q_lo, its text, kind) for the 18 bands of TARGET_HD.md section 3."""
    out = [(n, ell, Fraction(qs), qs, "onset") for (n, ell), (_, qs) in BANDS.items()]
    out += [(n, ell, Fraction(0), "0", "from 0+") for (n, ell) in ZERO_BANDS]
    return sorted(out)


def run(root, log):
    t_all = {}
    rec = {"params": {"rungs": [str(r) for r in RUNGS], "eps": [str(e) for e in EPS], "kpow": KPOW,
                      "degrees": list(DEGREES), "theta": THETA, "nsamp": NSAMP, "h_tau": H_TAU, "tau0": TAU0,
                      "grid_points": len(GRID), "variables": list(VARIABLES)}}
    t0 = time.time()
    rec["gates"] = g = gates(root)
    t_all["gates"] = round(time.time() - t0, 1)
    for k, v in g.items():
        log(f"{k}: ok = {v['ok']}, sigma = {v.get('sigma', v.get('G1 design on the well: sigma'))}")
    rec["pairs"] = []
    for n, ell, qlo, qtext, kind in bands():
        for qr in RUNGS:
            if qr <= qlo:
                continue
            t0 = time.time()
            ma, mb = mu_of_q(n, ell, float(qr)), mu_of_q(n, ell, float(qlo))
            mus = [ma + (mb - ma) * (1 - math.cos(math.pi * j / (NSAMP - 1))) / 2 for j in range(NSAMP)]
            samples = [sample(Setting(n, ell, mv)) for mv in mus]
            q, design = qualify(samples)
            rec["pairs"].append({"D": n + 2, "l": ell, "kind": kind, "q_lo": qtext, "rung": str(qr),
                                 "mu_range": [ma, mb], "qualifies": design is not None, "least_degree": q,
                                 "design": design, "samples": samples})
            t_all[f"D={n + 2} l={ell} q<={qr}"] = round(time.time() - t0, 1)
            sz = []
            for v in VARIABLES:
                for dg in (DEGREES[0], DEGREES[-1]):
                    sig = [s.get(f"eps {EPS[0]}", {}).get(f"{v} {dg}") for s in samples]
                    sz.append(min(-math.inf if t is None else t for t in sig))
            log(f"D={n + 2} l={ell} ({kind}, q_lo {qtext}) rung {qr}: qualifies {design is not None}, least degree "
                f"{q}, design {design}; min sigma z16/z48/zeta16/zeta48 = {[f'{v:.3g}' for v in sz]}")
    rec["q_max"] = {}
    for n in range(5, 10):
        ok = [qr for qr in RUNGS
              if all(p["qualifies"] for p in rec["pairs"] if p["D"] == n + 2 and p["rung"] == str(qr))]
        rec["q_max"][f"D={n + 2}"] = str(max(ok)) if ok else "not attempted"
        log(f"q_max(D={n + 2}) = {rec['q_max'][f'D={n + 2}']}")
    valid = all(v["ok"] for v in g.values())
    return rec, valid, t_all


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    a = ap.parse_args(argv)
    t0 = time.time()
    record = {"claim": "results/hd/pilot/PREREG.md (untrusted design pilot; no certificate)",
              "provenance": provenance()}
    try:
        res, valid, t_all = run(a.root, print)
        record["result"] = res
        verdict = "VALID" if valid else "VOID: a gate or control is not as registered"
    except Exception as exc:  # noqa: BLE001  (fail-closed)
        verdict, t_all = f"VOID: exception {type(exc).__name__}: {exc}", {}
    record["verdict"] = verdict
    record["timing"] = {"t_total_s": round(time.time() - t0, 1), **t_all}
    dump_json(record, f"{a.out}/result.json")
    print(verdict[:400])
    return 0 if verdict == "VALID" else 1


if __name__ == "__main__":
    sys.exit(main())
