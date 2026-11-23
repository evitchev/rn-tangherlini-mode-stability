"""Stage 3, HD-X-PILOT: the untrusted design pilot of HD-X-1 (D = 7..11 through extremality, the bands with 2l > n - 1).

    python -m hdx.pilot --out DIR [--root REPO] [--band D,L ...]
    python -m hdx.pilot --out DIR --gate-a2 [--legacy-f]          (the gate band (4, 2): A2-PILOT, BHM-095)

Floats only; nothing here is part of a certificate.  For each band (n, l) of hdx.bands (D = n + 2): A2-PILOT's
construction (code/a2/pilot.py) at general n, with hd.pilot's units (r_H = 1, z = 1 - 1/rho, q = 1 at mu = 0):
    P(z, mu) = a (1 + eps)/(z + eps) + p0(z),   eps = B_POLE delta_t/(n - 1) = w/((n - 1)(1 + w)),
with a and beta0 of hdx.bands, and p0 the degree-g Chebyshev-Lobatto interpolant on [0, 1] of the regular part
P_beta - a/z of the principal solution, P_beta ~ a/z, of the q = 1 Riccati equation for the lowered potential
W - beta0, beta0 = (n - 1)^2 (c - a(a + 1)), c = W(0)/(n - 1)^2 at q = 1.  Its slack is sigma = min B/B(1) on a grid that
resolves the throat (scale delta_t/(n - 1)) and the extremal horizon, B = N/(64 H_-^2) = W - [(1 - z) f_z P +
f (-P + (1 - z) P_z + P^2)].  A band qualifies at degree g if sigma >= SIGMA_MIN and B(1) > 0 at every sample; the pilot
records the least such g in DEGREES (the cap is the last).  The samples: q = 1, mu1, the rungs 1 - q in RUNGS, NCHEB
Chebyshev-Lobatto points on [0, mu1] and mu1 2^-k for k = 0..NGEO.
The setting (Acc) computes f and f_z without cancellation near the horizon, 1 - (1 - z)^(n-1) = -expm1((n-1) log1p(-z))
and 1 - k y = (1 - k) + k (1 - y); --legacy-f uses hd.pilot.Setting's f (for the gate only).
Gates and controls, per band (VALID only if all are as registered):
    C-EXACT the float c = W(0)/(n - 1)^2 at q = 1 equals hdx.bands' exact c to 1e-9 (relative)
    PG-HDS  HD-S's recorded certificate (BHM-078) on the band's first box, at that box's lower end mu_a (q(mu_a) >= 99/100):
            sigma > 0 under this evaluator; not run for D = 10 l = 6 and D = 11 l = 7, which HD-S does not have
    NC-H    the design with a replaced by hdx.bands' a_nc, outside the residue window: sigma < 0 at q = 1
    NC-B    a planted bound state at q = 1, W - K b, b = ((z - za)(zb - z))^2 on WELL's support inside U_- < 0,
            K = 2 I1/I2: the design gives sigma < 0, and the design rebuilt on the planted potential qualifies at no degree
--gate-a2 runs the gate band with A2-PILOT's mu1 = 1/8 and A2-PILOT's gates (PG-T3, NC-H at -7/10, NC-B on [3/10, 3/5]) in
the same engine; with --legacy-f its record must equal A2-PILOT's record of record (kit/hdx/run_pilot.sh compares them).
Information: the Sturm cross-check at every sample, psi > 0 (the regular solution for q < 1; at q = 1 the throat-principal
one, started at the residue a_pr = (l - n + 1)/(n - 1)); a breakdown is a node (K2, numerical).
"""
import argparse
import datetime
import json
import math
import os
import sys
import time
from fractions import Fraction

from a2.pilot import t3_design
from hd.pilot import GRID, Setting, cheb_deriv, clenshaw, mu_of_q, riccati
from hd.pilot import bound_K as bound_K_a2
from hdx.bands import BANDS, B_POLE, GATE, MU1, WELL, control_params, label, residues
from p3.scert import cheb_coeffs
from qnm1c.common import dump_json, provenance

DEGREES = (12, 16, 20, 24, 32)          # the cap is the last
SIGMA_MIN = 1e-4
RUNGS = (1e-2, 1e-3, 1e-4, 1e-6)        # 1 - q; and q = 1 (mu = 0)
NCHEB, NGEO = 9, 12
TAU0, H_TAU = -27.6, 0.002
BREAKDOWN = 1e12
ZMIN = 1e-6                             # p0's value at z = 0 is taken at z = ZMIN
HDS_RECORD = "results/hd/s/runs/record/{D}-{l}/result.json"
A2_MU1, A2_A_NCH = Fraction(1, 8), Fraction(-7, 10)


class Breakdown(ArithmeticError):
    """The Riccati integration left the finite range: the solution has a zero (a node)."""


class Legacy(Setting):
    """hd.pilot.Setting's f.  A number as well is hd.pilot's own well on [3/10, 3/5] (A2-PILOT's NC-B); a tuple
    (K, za, zb) is a well K ((z - za)(zb - z))^2 on [za, zb]."""

    def __init__(self, n, ell, mu, well=None, funcs=None):
        super().__init__(n, ell, mu, well=well if isinstance(well, (int, float)) else 0.0, funcs=funcs)
        self.wellK, self.za, self.zb = well if isinstance(well, tuple) else (0.0, 0.0, 0.0)

    def W(self, z):
        v = Setting.W(self, z)
        if self.wellK and self.za < z < self.zb:
            v -= self.wellK * ((z - self.za) * (self.zb - z)) ** 2
        return v


class Acc(Legacy):
    """Legacy with f and f_z free of cancellation near the horizon: 1 - (1 - z)^(n-1) = -expm1((n - 1) log1p(-z)),
    and 1 - k y = (1 - k) + k (1 - y) with 1 - k = 2w/(1 + w) = delta_t."""

    def __init__(self, n, ell, mu, well=None, funcs=None):
        super().__init__(n, ell, mu, well=well, funcs=funcs)
        self.one_k = self.dt

    def oy(self, z):                                           # 1 - (1 - z)^(n - 1)
        if z >= 1:
            return 1.0
        return -math.expm1((self.n - 1) * math.log1p(-z))

    def f(self, z):
        oy = self.oy(z)
        return oy * (self.one_k + self.k * oy)

    def fz(self, z):
        oy = self.oy(z)
        y1 = 0.0 if z >= 1 else math.exp((self.n - 2) * math.log1p(-z))
        return (self.n - 1) * y1 * ((self.one_k + self.k * oy) + self.k * oy)


def grid(S):
    """GRID with the endpoints, plus points that resolve the throat (scale delta_t/(n - 1)) and the extremal horizon."""
    pts = set(GRID)
    sc = S.dt / (S.n - 1) if S.dt > 0 else 1e-3
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
    """P(z) and P_z(z) at the charge of S: a (1 + eps)/(z + eps) + p0(z), eps = B_POLE delta_t/(n - 1)."""

    def __init__(self, S, a, c):
        self.a, self.c, self.dc = float(a), c, cheb_deriv(c)
        self.eps = float(B_POLE) * S.dt / (S.n - 1)

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


def samples_mu(n, ell, mu1):
    mus = {0.0, float(mu1)} | {mu_of_q(n, ell, 1 - r) for r in RUNGS}
    mus |= {float(mu1) * (1 - math.cos(math.pi * j / (NCHEB - 1))) / 2 for j in range(NCHEB)}
    mus |= {float(mu1) * 2.0 ** (-k) for k in range(NGEO + 1)}
    return sorted(mus)


def start_residue(n, ell):
    """The throat-principal residue: the larger end of the window, which is (l - n + 1)/(n - 1) when 2l > n - 1."""
    ends = (Fraction(ell - n + 1, n - 1), Fraction(-ell, n - 1))
    apr = max(ends)
    if 2 * ell > n - 1 and apr != ends[0]:
        raise ArithmeticError("the principal residue is not (l - n + 1)/(n - 1)")
    return apr


def sturm(S, nu):
    """min psi on the grid: the regular solution (psi(r_H) = 1) for q < 1, the throat-principal one at q = 1."""
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


def bound_K(S, za, zb):
    """NC-B's construction on [za, zb]: K = 2 I1/I2 with b = ((z - za)(zb - z))^2, so that I1 - K I2 = -I1 < 0."""
    za, zb = float(za), float(zb)
    nq = 2000
    h = (zb - za) / nq
    I1 = I2 = 0.0
    for i in range(nq):
        z = za + (i + 0.5) * h
        b = ((z - za) * (zb - z)) ** 2
        bz = 2 * (z - za) * (zb - z) * (za + zb - 2 * z)
        I1 += (S.f(z) * bz * bz * (1 - z) ** 2 + S.W(z) * b * b) * h
        I2 += b * b * b * h
    return 2 * I1 / I2, I1


def exact_design_eval(cs, dcs):
    """A polynomial with Fraction coefficients cs (and its derivative's dcs) as a float function z -> (P, P_z)."""
    def ev(z):
        zf, p, dp = Fraction(z), Fraction(0), Fraction(0)
        for c in reversed(cs):
            p = p * zf + c
        for c in reversed(dcs):
            dp = dp * zf + c
        return float(p), float(dp)
    return ev


def hds_design(root, n, ell):
    """HD-S's certificate on the band's first box, at that box's lower end mu_a: (evaluator, record facts), or None."""
    path = os.path.join(root, HDS_RECORD.format(D=n + 2, l=ell))
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        box = json.load(fh)["boxes"][0]
    mua = Fraction(box["mu"][0])
    co = {tuple(int(t) for t in k.strip("()").split(",")): Fraction(v) for k, v in box["P"].items()}
    cz = {}
    for (i, j), v in co.items():
        cz[i] = cz.get(i, Fraction(0)) + v * mua ** j
    ph = [cz.get(i, Fraction(0)) for i in range(max(cz) + 1)]
    dph = [i * c for i, c in enumerate(ph)][1:]
    base = exact_design_eval(ph, dph)
    facts = {"mu": box["mu"], "variable": box["variable"], "degree": box["degree"], "delta_b": box["delta_b"]}
    if box["variable"] == "z":
        return base, mua, facts
    db, e = Fraction(box["delta_b"]), int(box["degree"])

    def ev(z):
        p, dp = base(z)
        s = float(Fraction(z) + db)
        return p / s ** e, dp / s ** e - e * p / s ** (e + 1)
    return ev, mua, facts


def run_band(n, ell, a, mu1, cls, log, funcs=None):
    """The design search for one band: the record fields of A2-PILOT's run (params excepted) and the fits."""
    rec = {}
    S1 = cls(n, ell, 0.0, funcs=funcs)
    c = S1.W(0.0) / (n - 1) ** 2
    beta0 = (n - 1) ** 2 * (c - float(a) * (float(a) + 1))
    rec["c"], rec["beta0"] = c, beta0
    log(f"D = {n + 2}, l = {ell}: c = W(0)/(n - 1)^2 at q = 1: {c!r}; beta0 = {beta0!r}")
    mus = samples_mu(n, ell, mu1)
    rec["samples_mu"] = mus
    fits, out = {}, []
    for g in DEGREES:
        try:
            fits[g] = p0_fit(S1, float(a), beta0, g)
        except ArithmeticError as exc:
            fits[g] = None
            log(f"degree {g}: the lowered solution broke down: {exc}")
    nu = float(start_residue(n, ell))
    for mv in mus:
        S = cls(n, ell, mv, funcs=funcs)
        r = {"mu": mv, "q": S.q, "delta_t": S.dt, "sturm": sturm(S, nu)}
        for g in DEGREES:
            if fits[g] is None:
                r[f"g {g}"] = None
                continue
            sg, zm, B1 = sigma(S, Design(S, a, fits[g]))
            r[f"g {g}"] = {"sigma": sg, "z_min": zm, "B1": B1}
        out.append(r)
        log(f"mu = {mv:.6g} (q = {S.q:.10f}): " + "  ".join(
            f"g{g}: {'-' if r[f'g {g}'] is None or r[f'g {g}']['sigma'] is None else format(r[f'g {g}']['sigma'], '.3g')}"
            for g in DEGREES) + f"; sturm {r['sturm']}")
    rec["samples"] = out
    least = None
    for g in DEGREES:
        if all(s[f"g {g}"] is not None and s[f"g {g}"]["sigma"] is not None and s[f"g {g}"]["sigma"] >= SIGMA_MIN
               and s[f"g {g}"]["B1"] > 0 for s in out):
            least = g
            break
    rec["least_degree"] = least
    return rec, fits, S1, beta0


def nc_h(S1, a_nc, fit, gd):
    sg, zm, B1 = sigma(S1, Design(S1, a_nc, fit))
    return {"a": str(a_nc), "degree": gd, "sigma": sg, "z_min": zm, "B1": B1, "ok": sg is not None and sg < 0}


def nc_b(Sw, a, beta0, fit):
    sg, zm, B1 = sigma(Sw, Design(Sw, a, fit))
    rebuilt = {}
    for g in DEGREES:
        try:
            sgw, _, _ = sigma(Sw, Design(Sw, a, p0_fit(Sw, float(a), beta0, g)))
        except ArithmeticError as exc:
            sgw = f"breakdown: {exc}"
        rebuilt[str(g)] = sgw
    none = all(not isinstance(v, float) or v < SIGMA_MIN for v in rebuilt.values())
    return sg, zm, rebuilt, none


def run_gate_a2(root, cls, log, funcs=None):
    """The gate band (4, 2) with A2-PILOT's constants and gates, in this engine (A2-PILOT's record layout)."""
    n, ell = GATE
    a = residues(n, ell)[3]
    rec = {"params": {"a": str(a), "b_pole": str(B_POLE), "mu1": str(A2_MU1), "degrees": list(DEGREES),
                      "theta": SIGMA_MIN, "rungs_1_minus_q": list(RUNGS), "ncheb": NCHEB, "ngeo": NGEO, "tau0": TAU0,
                      "h_tau": H_TAU, "zmin": ZMIN}}
    band, fits, S1, beta0 = run_band(n, ell, a, A2_MU1, cls, log, funcs)
    rec.update(band)
    least = band["least_degree"]
    rec["design"] = None if least is None else {"a": str(a), "b_pole": str(B_POLE), "degree": least, "beta0": beta0,
                                                "cheb": [float.hex(v) for v in fits[least]]}
    gd = least if least is not None else DEGREES[-1]
    gates = {}
    if funcs is None:
        ev, box = t3_design(root)
        S = cls(n, ell, float(A2_MU1))
        sg, zm, B1 = sigma(S, ev)
        gates["PG-T3"] = {"box": box, "sigma": sg, "z_min": zm, "ok": sg is not None and sg > 0}
    if fits[gd] is not None:
        gates["NC-H"] = nc_h(S1, A2_A_NCH, fits[gd], gd)
        K, I1 = bound_K_a2(S1)
        Sw = cls(n, ell, 0.0, well=K, funcs=funcs)
        sg, zm, rebuilt, none = nc_b(Sw, a, beta0, fits[gd])
        gates["NC-B"] = {"K": K, "I1": I1, "design sigma": sg, "z_min": zm, "rebuilt": rebuilt,
                         "ok": I1 > 0 and sg is not None and sg < 0 and none}
    rec["gates"] = gates
    for k, v in gates.items():
        log(f"{k}: ok = {v['ok']}; {json.dumps({kk: vv for kk, vv in v.items() if kk != 'ok'}, sort_keys=True)}")
    return rec, ("NC-H", "NC-B") if funcs is not None else ("PG-T3", "NC-H", "NC-B")


def run_bands(root, bands, cls, log, funcs=None):
    rec = {"params": {"b_pole": str(B_POLE), "mu1": str(MU1), "degrees": list(DEGREES), "sigma_min": SIGMA_MIN,
                      "rungs_1_minus_q": list(RUNGS), "ncheb": NCHEB, "ngeo": NGEO, "tau0": TAU0, "h_tau": H_TAU,
                      "zmin": ZMIN, "f": cls.__name__}, "bands": {}, "designs": {}}
    need = []
    for n, ell in bands:
        lab = label(n, ell)
        c_ex, apr, aot, a, beta0_ex = residues(n, ell)
        ctl = control_params(n, ell)
        band, fits, S1, beta0 = run_band(n, ell, a, MU1, cls, log, funcs)
        band.update({"a": str(a), "a_pr": str(apr), "a_ot": str(aot), "c_exact": str(c_ex), "beta0_exact": str(beta0_ex)})
        least = band["least_degree"]
        if least is not None:
            rec["designs"][lab] = {"a": str(a), "b_pole": str(B_POLE), "degree": least, "beta0": beta0,
                                   "mu1": str(MU1), "cheb": [float.hex(v) for v in fits[least]]}
        gd = least if least is not None else DEGREES[-1]
        gates = {}
        rel = abs(band["c"] - float(c_ex)) / abs(float(c_ex))
        gates["C-EXACT"] = {"c_float": band["c"], "c_exact": str(c_ex), "relative": rel, "ok": rel < 1e-9}
        if funcs is None:
            hd = hds_design(root, n, ell)
            if hd is not None:
                ev, mua, facts = hd
                S = cls(n, ell, float(mua))
                sg, zm, _ = sigma(S, ev)
                gates["PG-HDS"] = {**facts, "sigma": sg, "z_min": zm, "ok": sg is not None and sg > 0}
        if fits[gd] is not None:
            gates["NC-H"] = nc_h(S1, ctl["a_nc"], fits[gd], gd)
            za, zb = WELL[(n, ell)]
            K, I1 = bound_K(S1, za, zb)
            Sw = cls(n, ell, 0.0, well=(K, float(za), float(zb)), funcs=funcs)
            sg, zm, rebuilt, none = nc_b(Sw, a, beta0, fits[gd])
            gates["NC-B"] = {"support": [str(za), str(zb)], "K": K, "I1": I1, "design sigma": sg, "z_min": zm,
                             "rebuilt": rebuilt, "ok": I1 > 0 and sg is not None and sg < 0 and none}
        band["gates"] = gates
        for k, v in gates.items():
            log(f"D = {n + 2}, l = {ell}, {k}: ok = {v['ok']}; "
                f"{json.dumps({kk: vv for kk, vv in v.items() if kk != 'ok'}, sort_keys=True)[:400]}")
        rec["bands"][lab] = band
        need += [(lab, k) for k in ("C-EXACT", "NC-H", "NC-B") + (("PG-HDS",) if "PG-HDS" in gates else ())]
    return rec, need


def main(argv=None, funcs=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    ap.add_argument("--band", action="append", default=None, help="D,l (repeatable); default: every band of hdx.bands")
    ap.add_argument("--gate-a2", action="store_true")
    ap.add_argument("--legacy-f", action="store_true")
    a = ap.parse_args(argv)
    t0, start = time.time(), datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    os.makedirs(a.out, exist_ok=True)
    cls = Legacy if a.legacy_f else Acc

    def log(s):
        print(s, flush=True)
    claim = ("hdx.pilot --gate-a2: A2-PILOT (results/a2/pilot/PREREG.md) in HD-X's engine" if a.gate_a2
             else "HD-X-PILOT (untrusted design pilot of HD-X-1)")
    record = {"claim": claim, "provenance": provenance(), "archive_sha256": os.environ.get("BHM_ARCHIVE", "unknown")}
    try:
        if a.gate_a2:
            if a.band:
                raise ValueError("--gate-a2 takes no --band")
            rec, need = run_gate_a2(a.root, cls, log, funcs)
            record.update(rec)
            g = record["gates"]
            valid = all(k in g and g[k]["ok"] for k in need)
            least = record["least_degree"]
            verdict = ("VALID" if valid else "VOID") + (f": qualifies at degree {least}" if least is not None
                                                       else ": qualifies nowhere (K3)")
        else:
            bands = BANDS if not a.band else [(int(s.split(",")[0]) - 2, int(s.split(",")[1])) for s in a.band]
            for nb in bands:
                if nb not in BANDS:
                    raise ValueError(f"D = {nb[0] + 2}, l = {nb[1]} is not a band of hdx.bands")
            rec, need = run_bands(a.root, bands, cls, log, funcs)
            record.update(rec)
            bad = [f"{lab} {k}" for lab, k in need if not record["bands"][lab]["gates"].get(k, {}).get("ok")]
            k3 = [lab for lab, b in record["bands"].items() if b["least_degree"] is None]
            degs = ", ".join(f"{lab}: {b['least_degree']}" for lab, b in record["bands"].items())
            verdict = ("VOID: " + "; ".join(bad) if bad else "VALID") + f" (least degrees {degs})" + \
                      (f"; qualifies nowhere (K3): {', '.join(k3)}" if k3 else "")
    except Exception as exc:  # noqa: BLE001
        verdict = f"VOID: exception {type(exc).__name__}: {exc}"
    record["verdict"] = verdict
    record["timing"] = {"utc_start": start, "t_total_s": round(time.time() - t0, 1)}
    dump_json(record, os.path.join(a.out, "result.json"))
    print(verdict)
    return 0 if verdict.startswith("VALID") and "K3" not in verdict else 1


if __name__ == "__main__":
    sys.exit(main())
