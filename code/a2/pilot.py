"""Stage A2, A2-PILOT (results/a2/pilot/PREREG.md): the untrusted design pilot for l = 2 near extremality.

    python -m a2.pilot --out DIR [--root REPO]

Floats only; nothing here is part of a certificate.  D = 6 (n = 4), l = 2, hd.pilot's Setting (units r_H = 1,
z = 1 - 1/rho, the charge through mu, q = 1 at mu = 0).  The design (TARGET_A2_ADDENDUM_1.md section 3):

    P(z, mu) = a (1 + eps)/(z + eps) + p0(z),   a = -2/5,   eps = delta_t/6 = w/(3(1 + w)),

with p0 the degree-g Chebyshev-Lobatto interpolant on [0, 1] of the regular part P_beta - a/z of the principal
solution, P_beta ~ a/z, of the q = 1 Riccati equation for the lowered potential W - beta0, beta0 = 9 (c - a (a + 1)),
c = W(0)/9 at q = 1 (c = -2/9, E3, so beta0 = 4/25).  Its slack is sigma = min B/B(1) on a grid that resolves the
throat, B = N/(64 H_-^2) = W - [(1 - z) f_z P + f (-P + (1 - z) P_z + P^2)].  The design qualifies at degree g if
sigma >= THETA and B(1) > 0 at every sample; the pilot reports the least such g in DEGREES.
Gates and controls (VALID only if all are as registered):
    PG-T3  T3's recorded certificate (BHM-023; N > 0 proved exactly on its first box) at mu = 1/8: sigma > 0 here
    NC-H   the design with a replaced by -7/10, outside the window (-2/3, -1/3): sigma < 0 at mu = 0
    NC-B   a planted bound state at q = 1, W - K b on [3/10, 3/5], K = 2 I1/I2: the design gives sigma < 0, and the
           design rebuilt on the planted potential qualifies at no degree
Information: the Sturm cross-check, psi_1 > 0 at every sample (the regular solution for q < 1, the principal one at
q = 1); a breakdown is a node (K2, numerical).
"""
import argparse
import datetime
import json
import math
import os
import sys
import time
from fractions import Fraction

from hd.pilot import GRID, Setting, bound_K, cheb_deriv, clenshaw, mu_of_q, riccati
from p3.scert import cheb_coeffs
from qnm1c.common import dump_json, provenance

N_DIM, ELL = 4, 2
A_RES = Fraction(-2, 5)
B_POLE = Fraction(1, 2)                 # eps = B_POLE delta_t/3
MU1 = Fraction(1, 8)
DEGREES = (12, 16, 20, 24, 32)          # the cap is the last
THETA = 1e-4
RUNGS = (1e-2, 1e-3, 1e-4, 1e-6)        # 1 - q; and q = 1 (mu = 0)
NCHEB, NGEO = 9, 12
TAU0, H_TAU = -27.6, 0.002
BREAKDOWN = 1e12
A_NCH = Fraction(-7, 10)
T3_RECORD = "results/p3/runs/record/T3/result.json"
ZMIN = 1e-6                             # p0's value at z = 0 is taken at z = ZMIN


class Breakdown(ArithmeticError):
    """The Riccati integration left the finite range: the solution has a zero (a node)."""


def grid(S):
    """GRID with the endpoints, plus points that resolve the throat (scale delta_t) and the extremal horizon."""
    pts = set(GRID)
    sc = S.dt / 3 if S.dt > 0 else 1e-3
    pts |= {sc * 10 ** (j / 40) for j in range(-200, 121)}
    pts |= {10 ** (-j / 20) for j in range(1, 241)}
    pts = {z for z in pts if 0 <= z <= 1}
    if S.mu == 0:
        pts.discard(0.0)
    return sorted(pts)


def integrate(S, zs, P0, extra=0.0):
    """{z: (P, log psi)} on the sorted zs in (0, 1): RK4 in tau = log(z/(1 - z)) from TAU0, P(z(TAU0)) = P0, for the
    Riccati (1 - z) P_z = P - P^2 + [W - extra - (1 - z) f_z P]/f, with d log psi/d tau = z P."""
    def rhs(tau, Y):
        zz = 1 / (1 + math.exp(-tau))
        P = Y[0]
        return (zz * (P - P * P + (S.W(zz) - extra - (1 - zz) * S.fz(zz) * P) / S.f(zz)), zz * P)

    out, tau, Y = {}, TAU0, (P0, 0.0)
    for zk in zs:
        tk = math.log(zk / (1 - zk))
        if tk < tau:
            raise ValueError(f"node {zk} below the start of the integration")
        while tau < tk:
            h = min(H_TAU, tk - tau)
            k1 = rhs(tau, Y)
            k2 = rhs(tau + h / 2, tuple(a + h / 2 * b for a, b in zip(Y, k1)))
            k3 = rhs(tau + h / 2, tuple(a + h / 2 * b for a, b in zip(Y, k2)))
            k4 = rhs(tau + h, tuple(a + h * b for a, b in zip(Y, k3)))
            Y = tuple(a + h / 6 * (b1 + 2 * b2 + 2 * b3 + b4) for a, b1, b2, b3, b4 in zip(Y, k1, k2, k3, k4))
            tau += h
            if not (math.isfinite(Y[0]) and abs(Y[0]) < BREAKDOWN and math.isfinite(Y[1])):
                raise Breakdown(f"P = {Y[0]!r} at z = {1 / (1 + math.exp(-tau)):.6g}")
        out[zk] = Y
    return out


def p0_fit(S1, a, beta0, g):
    """Chebyshev coefficients of the degree-g interpolant of P_beta - a/z on [0, 1]."""
    nodes = [(1 - math.cos(math.pi * k / g)) / 2 for k in range(g + 1)]
    inner = sorted({max(z, ZMIN) for z in nodes if z < 1})
    z0 = 1 / (1 + math.exp(-TAU0))
    sol = integrate(S1, inner, a / z0, extra=beta0)
    Pinf = (1 + math.sqrt(1 + 4 * (S1.W(1.0) - beta0))) / 2
    vals = [(Pinf - a) if z >= 1 else sol[max(z, ZMIN)][0] - a / max(z, ZMIN) for z in nodes]
    return cheb_coeffs(vals)


class Design:
    """P(z) and P_z(z) at the charge of S: a (1 + eps)/(z + eps) + p0(z)."""

    def __init__(self, S, a, c):
        self.a, self.c, self.dc = float(a), c, cheb_deriv(c)
        self.eps = float(B_POLE) * S.dt / 3

    def __call__(self, z):
        e, a = self.eps, self.a
        u = 2 * z - 1
        return (a * (1 + e) / (z + e) + clenshaw(self.c, u), -a * (1 + e) / (z + e) ** 2 + 2 * clenshaw(self.dc, u))


def sigma(S, P_of):
    """sigma = min B/B(1) on grid(S), the z of the minimum and B(1); sigma None if B(1) <= 0 or a value is not finite."""
    zs = grid(S)
    Bs = []
    for z in zs:
        P, Pz = P_of(z)
        Bs.append(S.W(z) - ((1 - z) * S.fz(z) * P + S.f(z) * (-P + (1 - z) * Pz + P * P)))
    P1 = P_of(1.0)[0]
    B1 = S.W(1.0) + P1 - P1 * P1
    if not all(math.isfinite(b) for b in Bs) or B1 <= 0:
        return None, None, B1
    i = min(range(len(Bs)), key=Bs.__getitem__)
    return Bs[i] / B1, zs[i], B1


def samples_mu():
    mus = {0.0, float(MU1)} | {mu_of_q(N_DIM, ELL, 1 - r) for r in RUNGS}
    mus |= {float(MU1) * (1 - math.cos(math.pi * j / (NCHEB - 1))) / 2 for j in range(NCHEB)}
    mus |= {float(MU1) * 2.0 ** (-k) for k in range(NGEO + 1)}
    return sorted(mus)


def sturm(S):
    """min psi_1 on the grid: the regular solution (psi_1(r_H) = 1) for q < 1, the principal one at q = 1."""
    nu = (ELL - N_DIM + 1) / (N_DIM - 1)
    try:
        if S.mu == 0:
            z0 = 1 / (1 + math.exp(-TAU0))
            sol = integrate(S, [z for z in grid(S) if z0 < z < 1], nu / z0)
            lg = min(v[1] for v in sol.values())
            return {"min_log_psi": lg, "breakdown": None}
        sol = riccati(S, list(GRID))
        return {"min_psi1": math.exp(min(sol[z][1] for z in GRID[:-1])), "breakdown": None}
    except ArithmeticError as exc:
        return {"breakdown": f"{type(exc).__name__}: {exc}"}


def t3_design(root):
    with open(os.path.join(root, T3_RECORD)) as fh:
        box = json.load(fh)["result"]["boxes_mu"][0]
    lo, hi = (Fraction(t) for t in box["mu"])
    if not lo <= MU1 <= hi:
        raise ValueError(f"mu = {MU1} is not in T3's first box [{lo}, {hi}]")
    co = {tuple(int(t) for t in k.strip("()").split(",")): Fraction(v) for k, v in box["P"].items()}
    cz = {}
    for (i, j), v in co.items():
        cz[i] = cz.get(i, Fraction(0)) + v * MU1 ** j
    cs = [cz.get(i, Fraction(0)) for i in range(max(cz) + 1)]
    dcs = [i * c for i, c in enumerate(cs)][1:]

    def ev(z):
        zf, p, dp = Fraction(z), Fraction(0), Fraction(0)
        for c in reversed(cs):
            p = p * zf + c
        for c in reversed(dcs):
            dp = dp * zf + c
        return float(p), float(dp)
    return ev, [str(lo), str(hi)]


def run(root, log, funcs=None):
    rec = {"params": {"a": str(A_RES), "b_pole": str(B_POLE), "mu1": str(MU1), "degrees": list(DEGREES),
                      "theta": THETA, "rungs_1_minus_q": list(RUNGS), "ncheb": NCHEB, "ngeo": NGEO, "tau0": TAU0,
                      "h_tau": H_TAU, "zmin": ZMIN}}
    S1 = Setting(N_DIM, ELL, 0.0, funcs=funcs)
    c = S1.W(0.0) / 9
    beta0 = 9 * (c - float(A_RES) * (float(A_RES) + 1))
    rec["c"], rec["beta0"] = c, beta0
    log(f"c = W(0)/9 at q = 1: {c!r}; beta0 = {beta0!r} (4/25 = {4 / 25!r})")
    mus = samples_mu()
    rec["samples_mu"] = mus
    fits, out = {}, []
    for g in DEGREES:
        try:
            fits[g] = p0_fit(S1, float(A_RES), beta0, g)
        except ArithmeticError as exc:
            fits[g] = None
            log(f"degree {g}: the lowered solution broke down: {exc}")
    for mv in mus:
        S = Setting(N_DIM, ELL, mv, funcs=funcs)
        r = {"mu": mv, "q": S.q, "delta_t": S.dt, "sturm": sturm(S)}
        for g in DEGREES:
            if fits[g] is None:
                r[f"g {g}"] = None
                continue
            sg, zm, B1 = sigma(S, Design(S, A_RES, fits[g]))
            r[f"g {g}"] = {"sigma": sg, "z_min": zm, "B1": B1}
        out.append(r)
        log(f"mu = {mv:.6g} (q = {S.q:.10f}): " + "  ".join(
            f"g{g}: {'-' if r[f'g {g}'] is None or r[f'g {g}']['sigma'] is None else format(r[f'g {g}']['sigma'], '.3g')}"
            for g in DEGREES) + f"; sturm {r['sturm']}")
    rec["samples"] = out
    least = None
    for g in DEGREES:
        if all(s[f"g {g}"] is not None and s[f"g {g}"]["sigma"] is not None and s[f"g {g}"]["sigma"] >= THETA
               and s[f"g {g}"]["B1"] > 0 for s in out):
            least = g
            break
    rec["least_degree"] = least
    rec["design"] = None if least is None else {"a": str(A_RES), "b_pole": str(B_POLE), "degree": least,
                                                "beta0": beta0, "cheb": [float.hex(v) for v in fits[least]]}
    gd = least if least is not None else DEGREES[-1]
    gates = {}
    if funcs is None:
        ev, box = t3_design(root)
        S = Setting(N_DIM, ELL, float(MU1))
        sg, zm, B1 = sigma(S, ev)
        gates["PG-T3"] = {"box": box, "sigma": sg, "z_min": zm, "ok": sg is not None and sg > 0}
    if fits[gd] is not None:
        sg, zm, B1 = sigma(S1, Design(S1, A_NCH, fits[gd]))
        gates["NC-H"] = {"a": str(A_NCH), "degree": gd, "sigma": sg, "z_min": zm, "B1": B1,
                         "ok": sg is not None and sg < 0}
        K, I1 = bound_K(S1)
        Sw = Setting(N_DIM, ELL, 0.0, well=K, funcs=funcs)
        sg, zm, B1 = sigma(Sw, Design(Sw, A_RES, fits[gd]))
        rebuilt = {}
        for g in DEGREES:
            try:
                sgw, _, _ = sigma(Sw, Design(Sw, A_RES, p0_fit(Sw, float(A_RES), beta0, g)))
            except ArithmeticError as exc:
                sgw = f"breakdown: {exc}"
            rebuilt[str(g)] = sgw
        none = all(not isinstance(v, float) or v < THETA for v in rebuilt.values())
        gates["NC-B"] = {"K": K, "I1": I1, "design sigma": sg, "z_min": zm, "rebuilt": rebuilt,
                         "ok": I1 > 0 and sg is not None and sg < 0 and none}
    rec["gates"] = gates
    for k, v in gates.items():
        log(f"{k}: ok = {v['ok']}; {json.dumps({kk: vv for kk, vv in v.items() if kk != 'ok'}, sort_keys=True)}")
    return rec


def main(argv=None, funcs=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    a = ap.parse_args(argv)
    t0, start = time.time(), datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    os.makedirs(a.out, exist_ok=True)
    lines = []

    def log(s):
        print(s, flush=True)
        lines.append(s)
    record = {"claim": "results/a2/pilot/PREREG.md (untrusted design pilot)", "provenance": provenance(),
              "archive_sha256": os.environ.get("BHM_ARCHIVE", "unknown")}
    try:
        record.update(run(a.root, log, funcs))
        g = record["gates"]
        need = ("NC-H", "NC-B") if funcs is not None else ("PG-T3", "NC-H", "NC-B")
        valid = all(k in g and g[k]["ok"] for k in need)
        verdict = ("VALID" if valid else "VOID") + (f": qualifies at degree {record['least_degree']}"
                                                   if record["least_degree"] is not None else ": qualifies nowhere (K3)")
    except Exception as exc:  # noqa: BLE001
        verdict = f"VOID: exception {type(exc).__name__}: {exc}"
    record["verdict"] = verdict
    record["timing"] = {"utc_start": start, "t_total_s": round(time.time() - t0, 1)}
    dump_json(record, os.path.join(a.out, "result.json"))
    print(verdict)
    return 0 if verdict.startswith("VALID") else 1


if __name__ == "__main__":
    sys.exit(main())
