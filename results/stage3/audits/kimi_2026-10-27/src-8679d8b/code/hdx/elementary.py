"""Stage 3, HD-X-1, HD-X-E (results/hdx/elementary/PREREG.md): U_- >= 0 on the closed exterior for D = 7..11, every l
from n - 1 to l0(n), and every q in [q(mu_lo), 1].  Then V_S- >= 0, so A_{l,q} >= 0.

    python -m hdx.elementary --out DIR [--control NAME] [--root REPO]

D = n + 2, n = 5..9.  HD-E's parametrisation (hd.elementary.param_n): mu = 0 is q = 1 and mu = 1 is q = 0.  HD-E's E1
(BHM-063) covers [mu_lo, 1] for l_el(n) <= l <= l0(n), with mu_lo the largest k/10000 such that w(k/10000)^2 <=
1 - (99/100)^2.  HD-X-E covers [0, mu_lo] with the same rule, so the two boxes meet; gate MEET checks each mu_lo against
HD-E's sealed record.  With x = t x_H, U_- = F(t, mu)/Den(mu) in lowest terms.
  l = n..l0(n)  Den > 0 on [0, mu_lo] and F > 0 on [0, 1] x [0, mu_lo], by exact Bernstein bisection.
  l = n - 1     at q = 1, U_-(x_H) = 64 l (l - n + 1) H_-(x_H)^2 with H_-(x_H) = (l + n)(l + n - 1) (gate EXT, symbolic in
                l), so F(1, 0) = 0 and no strict bound holds at that corner.  With s = 1 - t, F(1 - s, mu) = mu K(mu) +
                s G(s, mu), where K = F(1, mu)/mu and G = (F(1 - s, mu) - F(1, mu))/s are exact polynomial divisions
                (remainders 0, checked).  K > 0 on [0, mu_lo] and G > 0 on [0, 1] x [0, mu_lo] give F >= 0, with equality
                only at (t, mu) = (1, 0), the extremal horizon.
  l > l0(n)     Lemma U(n), HD-E's E3, for every q in [0, 1] (BHM-063): not re-checked here.  l0(n) is checked against
                HD-E's record (gate MEET).
  l <= n - 2    U_-(x_H) < 0 at q = 1 (EXT): the S-bands, not covered here.
Gates: KAT (a1.p1); E0n and PARAM4 (hd.elementary); H, every coefficient of H_- positive; EXT; MEET; A2E4, this code at
n = 4 with A1's P1 rule (k/1000) reproduces A2-E's sealed record (BHM-097) for l = 3..10, field by field.
Fail-closed (RULES.md A2): VERIFIED and exit 0 only if every check holds; otherwise REJECT: <reasons>, exit 1.
--control (each must end with its registered verdict):
    nc-band      D = 7 l = 3 and D = 11 l = 7, S-bands, on the strict path: U_-(x_H) = -602112 and -25804800 at q = 1
    nc-strict    D = 7 l = 4 and D = 11 l = 8, touching, with a strict bound on F itself: F(1, 0) = 0
    nc-bump      D = 7 l = 5 and D = 11 l = 9 with F - c 64 t^3 (1 - t)^3 Den, c = 2 |U_-(t = 1/2, mu = 0)| + 1: negative
                 at (t, mu) = (1/2, 0)
    td-coeff     U_minus(n) + 16 n m^2 (hd.elementary's tamper): E0n must fail
    td-verifier  the verifier's acceptance threshold lowered from 0 to -1: the KATs must fail
    td-mulo      the mu_lo rule with 995/1000 in place of 99/100: the boxes stop short of HD-E's, so MEET must fail
"""
import argparse
import datetime
import hashlib
import json
import os
import sys
import time
from fractions import Fraction

import sympy as sp
from flint import fmpq

from a1.p1 import MAX_DEPTH, kats, plain, positive_mu, tampered_prove_sign
from hd.elementary import gate_E0n, gate_PARAM4, param_n
from ki.potentials import H_minus, U_minus, d, m, x
from onset.bernstein import Poly2, Q, prove_sign
from onset.onset import mu, t
from qnm1c.common import CertificateError, dump_json, provenance

CONTROLS = ("none", "nc-band", "nc-strict", "nc-bump", "td-coeff", "td-verifier", "td-mulo")
QMAX = sp.Rational(99, 100)
Q_TAMPER = sp.Rational(995, 1000)                    # td-mulo
NS = range(5, 10)
L0 = {5: 10, 6: 10, 7: 11, 8: 13, 9: 14}             # HD-E's E3 hand-off (BHM-063), checked against its record (MEET)
CLAIM = {n: list(range(n - 1, L0[n] + 1)) for n in NS}
GRID = {4: 1000, 5: 10000, 6: 10000, 7: 10000, 8: 10000, 9: 10000}   # n = 4: A1's P1 (BHM-052); n = 5..9: HD-E (BHM-063)
HD_RECORD = "results/hd/elementary/runs/record/main/result.json"
HD_RECORD_SHA256 = "bb06c9023b0f7ad0b30b18b66221ebfe5095866caa4c426d406725d41da96da5"     # SEALED.sha256 (BHM-063)
A2E_RECORD = "results/a2/elementary/runs/record/none/result.json"
A2E_RECORD_SHA256 = "ad59836dff7d3362ff188ba567d3d5d6c8d0fc6c9f5528c609f9079d176a1fa2"    # SEALED.sha256 (BHM-097)
A2E_KEYS = ("ell", "m", "mu_lo", "q_at_mu_lo_squared", "q_at_mu_lo_approx", "q(0) = 1", "F_degrees", "Den", "bound",
            "bernstein_leaves", "splitting")
JOBS = {"nc-band": [(5, 3, "strict"), (9, 7, "strict")], "nc-strict": [(5, 4, "strict"), (9, 8, "strict")],
        "nc-bump": [(5, 5, "bump"), (9, 9, "bump")]}
s = sp.Symbol("s")
L = sp.Symbol("l", positive=True)


def U_of(n, control):
    return U_minus(n) + (16 * n * m ** 2 if control == "td-coeff" else 0)


def poly2(expr, a, b):
    """A polynomial in (a, b) as a Poly2 in the slots (t, mu)."""
    return Poly2({(i, j): Q(c) for (i, j), c in sp.Poly(expr, a, b).terms()})


def mu_lo_rule(P, grid, q_rule):
    """The largest k/grid with w(k/grid)^2 <= 1 - q_rule^2 (binary search; w increases on [0, 1], checked in part)."""
    def w2(k):
        return sp.Rational(P["w"].subs(mu, sp.Rational(k, grid))) ** 2

    w2max = 1 - q_rule ** 2
    lo, hi = 0, grid                                  # w2(0) = 0 <= w2max
    if w2(hi) <= w2max:
        lo = hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if w2(mid) <= w2max:
            lo = mid
        else:
            hi = mid
    return sp.Rational(lo, grid)


def part(verify, n, ell, U, grid, q_rule, path):
    """U_- >= 0 on [0, x_H] for q in [q(mu_lo), 1], by the path "split" (l = n - 1), "strict" or "bump" (strict, with
    the planted bump of nc-bump).  Returns a record; raises CertificateError on failure."""
    P = param_n(n, ell)
    stats, minrec = {}, {}
    rec = {"n": n, "D": n + 2, "ell": ell, "m": int(P["m"]), "path": path}
    ids = [sp.cancel(P["s"] ** 2 - (1 + 4 * P["m"] * P["q2"] / (n + 1) ** 2)) == 0,
           sp.cancel(P["q2"].subs(mu, 1)) == 0, sp.cancel(P["q2"].subs(mu, 0) - 1) == 0,
           sp.cancel(P["delta"].subs(mu, 1)) == 0]
    wn, wd = sp.fraction(sp.cancel(sp.diff(P["w"], mu)))
    sw = 1 if sp.Poly(wn, mu).eval(sp.Rational(1, 2)) > 0 else -1
    sd = 1 if sp.Poly(wd, mu).eval(sp.Rational(1, 2)) > 0 else -1
    positive_mu(verify, sw * wn, 0, 1, stats, minrec, "w' numerator")
    positive_mu(verify, sd * wd, 0, 1, stats, minrec, "w' denominator")
    if sw * sd < 0 or not all(ids):
        raise CertificateError(f"n={n} l={ell}: parametrisation: identities {ids}, w increasing {sw * sd > 0}")
    lo = mu_lo_rule(P, grid, q_rule)
    q2_lo = 1 - sp.Rational(P["w"].subs(mu, lo)) ** 2
    rec.update({"mu_lo": str(lo), "q_at_mu_lo_squared": str(q2_lo),
                "q_at_mu_lo_approx": float(sp.sqrt(q2_lo).evalf(20)), "q(0) = 1": True,
                "mu_lo_rule": f"largest k/{grid} with w(k/{grid})^2 <= 1 - ({q_rule})^2"})
    if q2_lo < q_rule ** 2:
        raise CertificateError(f"n={n} l={ell}: q(mu_lo)^2 = {q2_lo} < ({q_rule})^2")
    expr = U.subs({m: P["m"], d: P["delta"]}).subs(x, t * P["xH"])
    num, den = sp.fraction(sp.cancel(sp.together(expr)))
    if den.has(t):
        raise CertificateError(f"n={n} l={ell}: denominator depends on t")
    sg = 1 if sp.Poly(den, mu).eval(sp.Rational(1, 2)) > 0 else -1
    F, Den = sp.expand(sg * num), sp.expand(sg * den)
    if sp.cancel(F / Den - expr) != 0:
        raise CertificateError(f"n={n} l={ell}: F/Den differs from U_-")
    rec.update({"F_degrees": [sp.Poly(F, t, mu).degree(t), sp.Poly(F, t, mu).degree(mu)], "Den": str(sp.factor(Den)),
                "U(t=1, mu=0)": str(sp.Rational(F.subs({t: 1, mu: 0})) / sp.Rational(Den.subs(mu, 0)))})
    positive_mu(verify, Den, 0, lo, stats, minrec, "Den")
    if path == "split":
        Fs = sp.expand(F.subs(t, 1 - s))
        F1 = sp.expand(F.subs(t, 1))
        K, rK = sp.div(sp.Poly(F1, mu), sp.Poly(mu, mu))
        G, rG = sp.div(sp.Poly(sp.expand(Fs - F1), s, mu), sp.Poly(s, s, mu))
        identity = sp.expand(Fs - (mu * K.as_expr() + s * G.as_expr())) == 0
        rec["splitting"] = {"F(1, mu) divisible by mu": rK.is_zero, "F(1 - s, mu) - F(1, mu) divisible by s": rG.is_zero,
                            "F(1 - s, mu) = mu K + s G": identity, "F(1, 0)": str(F1.subs(mu, 0))}
        if not (rK.is_zero and rG.is_zero and identity):
            raise CertificateError(f"n={n} l={ell}: the splitting fails: {rec['splitting']}")
        positive_mu(verify, K.as_expr(), 0, lo, stats, minrec, "K")
        verify(poly2(G.as_expr(), s, mu), (fmpq(0), fmpq(1), fmpq(0), Q(lo)), 1, MAX_DEPTH, stats, "G", minrec)
        rec["bound"] = {"min_bernstein_K": str(minrec["K"]), "min_bernstein_G": str(minrec["G"])}
    else:
        if path == "bump":
            c = 2 * abs(sp.Rational(F.subs({t: sp.Rational(1, 2), mu: 0})) / sp.Rational(Den.subs(mu, 0))) + 1
            F = sp.expand(F - c * 64 * t ** 3 * (1 - t) ** 3 * Den)
            rec["bump_c"] = str(c)
        verify(poly2(F, t, mu), (fmpq(0), fmpq(1), fmpq(0), Q(lo)), 1, MAX_DEPTH, stats, "F", minrec)
        den2 = poly2(Den, t, mu)
        den_max = max(c for row in den2.bernstein(fmpq(0), fmpq(1), fmpq(0), Q(lo)) for c in row)
        lower = minrec["F"] / den_max
        rec["bound"] = {"min_bernstein_F": str(minrec["F"]), "max_bernstein_Den": str(den_max),
                        "U_lower_bound": str(lower),
                        "U_lower_bound_approx": float(Fraction(int(lower.p), int(lower.q)))}
    rec["bernstein_leaves"] = stats
    return rec


def gate_EXT(control, ns=range(4, 10)):
    """At q = 1 (mu = 0): param_n gives q^2 = 1, x_H = 2 and delta = 1/((l + n)(n + 1)); and, symbolic in l,
    H_-(x_H) = (l + n)(l + n - 1) and U_-(x_H) = 64 l (l - n + 1) H_-(x_H)^2."""
    res = {}
    for n in ns:
        nn = sp.Integer(n)
        sub = {m: (L - 1) * (L + nn), d: 1 / ((L + nn) * (nn + 1)), x: 2}
        Hx = sp.cancel(H_minus(n).subs(sub))
        Ux = sp.cancel(U_of(n, control).subs(sub))
        h_ok = sp.cancel(Hx - (L + nn) * (L + nn - 1)) == 0
        u_ok = sp.cancel(Ux - 64 * L * (L - nn + 1) * ((L + nn) * (L + nn - 1)) ** 2) == 0
        p_ok = True
        for ell in range(2, (10 if n == 4 else L0[n]) + 1):
            P = param_n(n, ell)
            p_ok = p_ok and sp.cancel(P["q2"].subs(mu, 0) - 1) == 0 and sp.cancel(P["xH"].subs(mu, 0) - 2) == 0 \
                and sp.cancel(P["delta"].subs(mu, 0) - sp.Rational(1, (ell + n) * (n + 1))) == 0
        res[n] = {"H_-(x_H)": h_ok, "U_-(x_H)": u_ok, "param at q = 1": p_ok}
    ok = all(all(v.values()) for v in res.values())
    return ok, f"at q = 1, symbolic in l: {res}"


def gate_MEET(root, q_rule):
    """For each claimed (D, l): HD-E's E1 record covers [mu_lo^HD, 1] for q <= 99/100, and mu_lo^HD <= this code's
    mu_lo, so [0, mu_lo] and [mu_lo^HD, 1] cover [0, 1].  Also l0(n) of HD-E's E3 equals L0 (the hand-off).  The
    parametrisation alone is used; U_- is not."""
    with open(os.path.join(root, HD_RECORD), "rb") as fh:
        raw = fh.read()
    sha_ok = hashlib.sha256(raw).hexdigest() == HD_RECORD_SHA256
    rec = json.loads(raw)
    e1 = {(p["D"], p["ell"]): p for p in rec["E1"]}
    l0 = {r["n"]: r["l0"] for r in rec["E3"]}
    bad, table = [], {}
    for n in NS:
        if l0.get(n) != L0[n]:
            bad.append(f"l0({n}) = {l0.get(n)} in HD-E's record, not {L0[n]}")
        for ell in CLAIM[n]:
            lo = mu_lo_rule(param_n(n, ell), GRID[n], q_rule)
            ref = e1.get((n + 2, ell))
            meets = (ref is not None and ref["q_hi"] == "99/100" and ref["covers"] is True
                     and sp.Rational(ref["mu_lo"]) <= lo)
            table[f"D={n + 2} l={ell}"] = {"mu_lo": str(lo), "HD-E mu_lo": ref["mu_lo"] if ref else None,
                                           "equal": bool(ref is not None and sp.Rational(ref["mu_lo"]) == lo),
                                           "meets": bool(meets)}
            if not meets:
                bad.append(f"D={n + 2} l={ell}: mu_lo = {lo}, HD-E's {ref['mu_lo'] if ref else 'missing'}")
    ok = sha_ok and not bad
    return ok, f"HD-E record SHA-256 matches: {sha_ok}; l0 = {L0}; failures: {bad[:12]}", table


def gate_A2E4(verify, root, control):
    """This code at n = 4, with A1's P1 rule (k/1000), against A2-E's sealed record (BHM-097), l = 3..10."""
    with open(os.path.join(root, A2E_RECORD), "rb") as fh:
        raw = fh.read()
    sha_ok = hashlib.sha256(raw).hexdigest() == A2E_RECORD_SHA256
    ref = {p["ell"]: p for p in json.loads(raw)["parts"]}
    U = U_of(4, control)
    mine, same = [], {}
    for ell in range(3, 11):
        try:
            r = plain(part(verify, 4, ell, U, GRID[4], QMAX, "split" if ell == 3 else "strict"))
        except CertificateError as exc:
            r = {"n": 4, "ell": ell, "failure": str(exc)[:600]}
        same[ell] = ell in ref and all(r.get(k) == ref[ell].get(k) for k in A2E_KEYS)
        mine.append(r)
    ok = sha_ok and set(ref) == set(range(3, 11)) and all(same.values())
    return ok, f"A2-E record SHA-256 matches: {sha_ok}; l = 3..10 identical field by field: {same}", mine


def run(control, root):
    verify = tampered_prove_sign if control == "td-verifier" else prove_sign
    q_rule = Q_TAMPER if control == "td-mulo" else QMAX
    checks, timing = {}, {}
    rec = {"qmax": str(QMAX), "claim": {f"D={n + 2}": CLAIM[n] for n in NS}, "l0": {str(n): L0[n] for n in NS},
           "grid": {str(k): v for k, v in GRID.items()}}
    ok, res = kats(verify)
    checks["KAT"] = (ok, str(res))
    checks["E0n"] = gate_E0n(root, control)
    checks["PARAM4"] = gate_PARAM4()
    hpos = all(all(c > 0 for _, c in sp.Poly(H_minus(n), x, d, m).terms()) for n in range(4, 10))
    checks["H"] = (hpos, "H_- = m + n(n+1)x/2 + n(n+1) m delta x/2, n = 4..9: every coefficient > 0, so H_- >= m > 0")
    t0 = time.time()
    checks["EXT"] = gate_EXT(control)
    timing["EXT"] = round(time.time() - t0, 2)
    t0 = time.time()
    ok, det, rec["A2E4"] = gate_A2E4(verify, root, control)
    checks["A2E4"] = (ok, det)
    timing["A2E4"] = round(time.time() - t0, 2)
    t0 = time.time()
    ok, det, rec["MEET"] = gate_MEET(root, q_rule)
    checks["MEET"] = (ok, det)
    timing["MEET"] = round(time.time() - t0, 2)
    jobs = JOBS.get(control, [(n, ell, "split" if ell == n - 1 else "strict") for n in NS for ell in CLAIM[n]])
    rec["parts"] = []
    for n, ell, path in jobs:
        t0 = time.time()
        key = f"E D={n + 2} l={ell}"
        try:
            r = part(verify, n, ell, U_of(n, control), GRID[n], q_rule, path)
            checks[key] = (True, f"U_- >= 0 on [0, x_H] for q in [q(mu_lo), 1]: {r['bound']}")
        except CertificateError as exc:
            r = {"n": n, "D": n + 2, "ell": ell, "path": path, "failure": str(exc)[:600]}
            checks[key] = (False, str(exc)[:600])
        rec["parts"].append(r)
        timing[key] = round(time.time() - t0, 2)
    return checks, rec, timing


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--control", choices=CONTROLS, default="none")
    ap.add_argument("--root", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    a = ap.parse_args(argv)
    t0, start = time.time(), datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    record = {"claim": "results/hdx/elementary/PREREG.md (HD-X-E: D = 7..11, l = n - 1..l0(n), q in [q(mu_lo), 1])",
              "control": a.control, "provenance": provenance(), "archive_sha256": os.environ.get("BHM_ARCHIVE", "unknown")}
    timing = {}
    try:
        checks, rec, timing = run(a.control, a.root)
        record.update(rec)
        record["checks"] = {k: {"ok": bool(ok), "detail": det} for k, (ok, det) in checks.items()}
        failed = [k for k, (ok, _) in checks.items() if not ok]
        verdict = "VERIFIED" if not failed else "REJECT: " + ", ".join(failed)
    except Exception as exc:  # noqa: BLE001  (fail-closed)
        verdict = f"REJECT: exception {type(exc).__name__}: {exc}"
    record["verdict"] = verdict
    record["timing"] = {**timing, "utc_start": start, "t_total_s": round(time.time() - t0, 2)}
    try:
        dump_json(plain(record), f"{a.out}/result.json")
    except Exception as exc:  # noqa: BLE001  (fail-closed: an unwritten record is a REJECT)
        verdict = record["verdict"] = f"REJECT: record not written: {type(exc).__name__}: {exc}"
    for k, v in record.get("checks", {}).items():
        print(f"{k}: {'PASS' if v['ok'] else 'FAIL'}  {v['detail'][:300]}")
    print(verdict)
    return 0 if verdict == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
