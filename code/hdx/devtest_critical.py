"""Development tests of hdx.critical, run before registration (results/hdx/critical/PREREG.md section 5).

    python -m hdx.devtest_critical

The synthetic potential: for a band (n, l), H_syn = m + (1 + m delta) x replaces S5's H_- (whose x-coefficient is
n(n + 1)/2), and U_syn(x) is the polynomial for which the band's design is exact at mu = 0, so Z0 holds by construction:
U_syn(2 Y) = 64 H0^2 [(1 - z) f_z P + f (-P + (1 - z) P_z + P^2)] at q = 1, with (1 - z) d/dz = -k Y d/dY.  Like S5's
functions, the synthetic UH accepts only int n and l (BHM-124: the run of Z at a188aba was VOID because a development
test replaced the very function that made the call).
1. main() end to end on the synthetic potential at D = 7 l = 2, D = 9 l = 2 and D = 11 l = 4: VERIFIED; then every
   control at D = 7 l = 2 and D = 11 l = 4, judged by the kit's registered forms (hdx.kitcheck, the kit's own matcher;
   the kit's table is read from kit/hdx/run_critical.sh and must equal SPECS).
2. The record writer and compare_runs on two synthetic records.
3. parse_band and the typed UH: '7,2' gives (5, 2) as ints; non-critical and malformed bands are refused; a str n is refused.
4. The real potential path through gates(), which is run()'s first part, without any POS chart: every critical band
   with control none passes every gate; at D = 7 l = 2 and D = 11 l = 4 each control fails exactly its registered
   non-POS gates; nc-bound's part (a) runs on the real potential at both.  POS-O, POS-O', POS-T, POS-C and nc-bound's
   part (b) never run on S5's potential here.
5. kitcheck on sample verdicts, and the KATs of the verifier and of its tamper.
PREREG_ADDENDUM_1.md adds six controls (td-param, td-H, td-R, td-L, td-S, td-XN), one for each gate that had none
(BHM-151, 2a).  They run in 1 (synthetic, both kit bands) and in 4 (S5's potential, both kit bands, gates() only: no POS
chart, td-S included).  Also: the sealed kit's table equals BHM-143's forms, the addendum's kit has all 20, and td-XN's
term has the stated chart images, each with non-negative Bernstein coefficients on its boxes.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time

import sympy as sp

from a1.p1 import kats, tampered_prove_sign
from hdx import critical as C
from hdx.kitcheck import matches
from ki.potentials import d, m, x
from onset.bernstein import prove_sign

RAT = sp.Rational
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
POS = ("POS-O", "POS-O'", "POS-T", "POS-C")
# The registered verdicts (PREREG section 4), as the kit matches them.
SPECS = {
    "none": "=VERIFIED",
    "nc-ehat-low": "+POS-C|POS-O,POS-O',POS-T",
    "d0-corner": "+POS-C|POS-O,POS-O',POS-T",
    "nc-ehat-high": "+POS-T|POS-O,POS-O',POS-C",
    "d0-throat": "+POS-T|POS-O,POS-O',POS-C",
    "nc-Q0": "+INF,POS-O|POS-O',POS-T,POS-C",
    "nc-Qneg": "+INF,POS-O|POS-O',POS-T,POS-C",
    "td-nu": "+Z0,DIV-O,DIV-C,CORNER,FIRST,INF,POS-O,POS-O',POS-C|POS-T",
    "d6": "+POS-T|POS-O,POS-O',POS-C",
    "nc-bound": "=REJECT: nc-bound (b)",
    "td-coeff": "+E0n,Z0,DIV-O,DIV-C,THROAT,CORNER,FIRST,INF,POS-O,POS-O',POS-C|POS-T",
    "td-verifier": "=REJECT: KAT",
    "td-cover": "=REJECT: COVER",
    "td-div": "+DIV-T,DIV-C,THROAT,CORNER,FIRST,POS-T,POS-C|POS-O,POS-O'",
    # PREREG_ADDENDUM_1.md: a control for each gate that had none (BHM-151, 2a)
    "td-param": "=REJECT: PARAM",
    "td-H": "=REJECT: H",
    "td-R": "=REJECT: R",
    "td-L": "=REJECT: L",
    "td-S": "+PARAM,S,THROAT,FIRST,XN|POS-O,POS-O',POS-T,POS-C",
    "td-XN": "=REJECT: XN",
}
ORIGINAL = ("none", "nc-ehat-low", "d0-corner", "nc-ehat-high", "d0-throat", "nc-Q0", "nc-Qneg", "td-nu", "d6",
            "nc-bound", "td-coeff", "td-verifier", "td-cover", "td-div")     # BHM-143's controls, in its sealed kit
# Each control's failing gates before the POS charts (PREREG section 4), on S5's potential and on the synthetic one.
NONPOS = {"none": [], "nc-ehat-low": [], "d0-corner": [], "nc-ehat-high": [], "d0-throat": [], "nc-Q0": ["INF"],
          "nc-Qneg": ["INF"], "td-nu": ["Z0", "DIV-O", "DIV-C", "CORNER", "FIRST", "INF"], "d6": [], "nc-bound": [],
          "td-coeff": ["E0n", "Z0", "DIV-O", "DIV-C", "THROAT", "CORNER", "FIRST", "INF"], "td-verifier": ["KAT"],
          "td-cover": ["COVER"], "td-div": ["DIV-T", "DIV-C", "THROAT", "CORNER", "FIRST"],
          "td-param": ["PARAM"], "td-H": ["H"], "td-R": ["R"], "td-L": ["L"],
          "td-S": ["PARAM", "S", "THROAT", "FIRST", "XN"], "td-XN": ["XN"]}
OK = []


def check(name, cond, info=""):
    OK.append(bool(cond))
    print(f"{'ok  ' if cond else 'FAIL'} {name}: {info}", flush=True)


def synthetic_UH(h1=1):
    """UH(n, l, control) -> (U_syn, H_syn) in (x, m, delta), for int n and l only."""
    cache = {}

    def UH(n, ell, control):
        if type(n) is not int or type(ell) is not int:
            raise TypeError(f"synthetic UH called with n = {n!r} ({type(n).__name__}), l = {ell!r} ({type(ell).__name__})")
        if control not in C.CONTROLS:
            raise ValueError(f"synthetic UH called with control {control!r}")
        key = (n, ell, control)
        if key not in cache:
            k = n - 1
            nu = RAT(2 * ell + n - 2, 2)
            m0, d0 = (ell - 1) * (ell + n), RAT(1, (ell + n) * (n + 1))
            Y = sp.Symbol("Y")
            g = 2 * h1 * (1 + m0 * d0)
            H0 = m0 + g * Y
            P = -nu - ell * Y / (1 - Y) + k * g * Y / H0
            f = (1 - Y) ** 2
            br = (-k * Y * sp.diff(f, Y)) * P + f * (-P + (-k * Y * sp.diff(P, Y)) + P ** 2)
            U0 = sp.cancel(sp.together(64 * H0 ** 2 * br))
            if sp.fraction(U0)[1].has(Y):
                raise AssertionError("U_syn is not a polynomial in Y")
            Us = sp.expand(U0.subs(Y, x / 2))
            if control == "td-coeff":                    # hd.elementary's tamper, applied as U_of applies it
                Us = Us + 16 * n * m ** 2
            cache[key] = (Us, m + h1 * (1 + m * d) * x)
        return cache[key]
    return UH


def kit_specs(name="run_critical.sh"):
    """A kit's table of registered forms, read from kit/hdx/<name>."""
    text = open(os.path.join(ROOT, "kit", "hdx", name)).read()
    return dict(re.findall(r'\[([A-Za-z0-9-]+)\]="([^"]*)"', text))


def xn_term_checks():
    """td-XN's term: its images in the charts are mu z^2 (1 - z) (M), mu^2 zeta^2 (1 - mu zeta) (T) and
    sigma z^2 (1 - z) (K), and each has non-negative Bernstein coefficients on its chart's box(es)."""
    from flint import fmpq
    from onset.bernstein import Poly2, Q
    from onset.onset import mu
    z = C.z
    term = sp.Poly(sp.sympify(C.XN_TERM, locals={"mu": mu, "z": z}), z, mu)
    ch = C.charts(term)
    zeta, sig = C.zeta, C.sig
    want = {"M": sp.Poly(mu * z ** 2 * (1 - z), z, mu), "T": sp.Poly(mu ** 2 * zeta ** 2 * (1 - mu * zeta), zeta, mu),
            "K": sp.Poly(sig * z ** 2 * (1 - z), z, sig)}
    same = all(ch[key] is not None and dict(want[key].terms()) == {k: v for k, v in ch[key].items() if v != 0}
               for key in want)
    signs = {}
    for mu1 in sorted(set(C.MU1.values())):
        for label, key, box in (("O", "M", (C.Z1, 1, 0, mu1)), ("O'", "M", (0, C.Z1, C.MUT, mu1)),
                                ("T", "T", (0, C.ZT, 0, C.MUT)), ("C", "K", (0, C.Z1, 0, C.SIG1))):
            p2 = Poly2({k: Q(v) for k, v in ch[key].items()})
            bern = p2.bernstein(*(Q(v) if v != 0 else fmpq(0) for v in box))
            signs[f"{label}, MU1 = {mu1}"] = min(c for row in bern for c in row) >= 0
    return same, signs


def failed(checks):
    return [k for k, (ok, _) in checks.items() if not ok]


def in_order(verdict):
    """A REJECT's failed checks appear in the order of C.ORDER, then nc-bound (a), (b)."""
    if not verdict.startswith("REJECT: ") or verdict.startswith("REJECT: exception"):
        return verdict == "VERIFIED"
    order = list(C.ORDER) + ["nc-bound (a)", "nc-bound (b)"]
    names = verdict[len("REJECT: "):].split(", ")
    return all(nm in order for nm in names) and [order.index(nm) for nm in names] == sorted(order.index(nm) for nm in names)


def main():
    t0 = time.time()
    UH = synthetic_UH()
    # 5. kitcheck and the KATs
    check("kitcheck: exact", matches("=VERIFIED", "VERIFIED") and not matches("=VERIFIED", "REJECT: KAT"))
    check("kitcheck: prefix", matches("^REJECT: E0n", "REJECT: E0n, Z0") and not matches("^REJECT: E0n", "REJECT: KAT"))
    check("kitcheck: required and allowed",
          matches("+POS-C|POS-O,POS-T", "REJECT: POS-O, POS-C") and not matches("+POS-C|POS-O", "REJECT: POS-T, POS-C")
          and not matches("+POS-C", "REJECT: POS-T") and not matches("+POS-C", "REJECT: exception KeyError: 'POS-C'")
          and not matches("+POS-C", "VERIFIED"))
    check("kitcheck: required only", matches("+INF,POS-O", "REJECT: INF, POS-O, POS-T"))
    ok, _ = kats(prove_sign)
    check("the verifier passes the KATs", ok)
    ok, _ = kats(tampered_prove_sign)
    check("the tampered verifier fails the KATs", not ok)
    orig = {k: SPECS[k] for k in ORIGINAL}
    check("the sealed kit's registered forms equal BHM-143's (SPECS without addendum 1)", kit_specs() == orig,
          str(sorted(set(kit_specs()) ^ set(orig))))
    check("addendum 1's kit has every registered form", kit_specs("run_critical_a1.sh") == SPECS,
          str(sorted(set(kit_specs("run_critical_a1.sh")) ^ set(SPECS))))
    check("CONTROLS = BHM-143's 14, then addendum 1's 6", tuple(C.CONTROLS[:14]) == ORIGINAL
          and set(C.CONTROLS[14:]) == set(SPECS) - set(ORIGINAL) and len(C.CONTROLS) == 20, str(C.CONTROLS))
    same, signs = xn_term_checks()
    check("td-XN's term: its chart images are mu z^2 (1 - z), mu^2 zeta^2 (1 - mu zeta), sigma z^2 (1 - z)", same)
    check("td-XN's term: non-negative Bernstein coefficients on every chart box, for every MU1", all(signs.values()),
          str(signs))
    # 3. parse_band and the typed UH
    check("parse_band '7,2' -> (5, 2) as ints", C.parse_band("7,2") == (5, 2) and all(type(v) is int for v in C.parse_band("7,2")))
    for bad in ("7,3", "12,2", "7", "x,2", "11,5"):
        try:
            C.parse_band(bad)
            got = "accepted"
        except (C.CertificateError, ValueError):
            got = "refused"
        check(f"parse_band {bad!r} refused", got == "refused", got)
    try:
        UH("5", 2, "none")
        got = "accepted"
    except TypeError:
        got = "TypeError"
    check("the typed synthetic UH refuses a str n", got == "TypeError", got)
    check("the critical set: 9 bands, each with 2l <= n - 1",
          len(C.MU1) == 9 and all(2 * ell <= n - 1 for n, ell in C.MU1), str(sorted(C.MU1)))
    # 1. main() end to end on the synthetic potential
    with tempfile.TemporaryDirectory() as tmp:
        for band in ("7,2", "9,2", "11,4"):
            out = f"{tmp}/none-{band}"
            t1 = time.time()
            code = C.main(["--out", out, "--band", band], UH=UH)
            rec = json.load(open(f"{out}/result.json"))
            check(f"synthetic {band} none: VERIFIED", code == 0 and rec["verdict"] == "VERIFIED",
                  f"{rec['verdict'][:200]} ({time.time() - t1:.1f} s)")
            check(f"synthetic {band} none: the record has every registered check",
                  sorted(rec["checks"]) == sorted(C.ORDER), str(sorted(rec["checks"]))[:200])
        for band in ("7,2", "11,4"):
            for control, spec in SPECS.items():
                if control == "none":
                    continue
                out = f"{tmp}/{control}-{band}"
                t1 = time.time()
                code = C.main(["--out", out, "--band", band, "--control", control], UH=UH)
                rec = json.load(open(f"{out}/result.json"))
                nonpos = [k for k in failed({k: (v["ok"], "") for k, v in rec["checks"].items()})
                          if k not in POS and not k.startswith("nc-bound")]
                check(f"synthetic {band} {control}: {spec}", code == 1 and matches(spec, rec["verdict"]),
                      f"{rec['verdict'][:200]} ({time.time() - t1:.1f} s)")
                # the record's JSON is written with sorted keys, so compare as sets; the verdict keeps the order
                check(f"synthetic {band} {control}: non-POS failures {NONPOS[control]}",
                      sorted(nonpos) == sorted(NONPOS[control]), str(sorted(nonpos)))
                check(f"synthetic {band} {control}: the verdict lists its failures in the registered order",
                      in_order(rec["verdict"]), rec["verdict"][:200])
                if control == "nc-bound":
                    nb = rec.get("nc-bound", {})
                    check(f"synthetic {band} nc-bound: support inside U_- < 0, Q[b] certified < 0",
                          rec["checks"]["nc-bound (a)"]["ok"], f"support {nb.get('support')}, K {nb.get('K')}, "
                          f"Q_b {nb.get('Q_b')}")
                if control == "d6":
                    check(f"synthetic {band} d6: K6 recorded", "K6" in rec.get("d6", {}), str(rec.get("d6"))[:160])
        # 2. the record writer and compare_runs
        outs = []
        for i in range(2):
            out = f"{tmp}/repeat{i}"
            C.main(["--out", out, "--band", "7,2", "--control", "td-cover"], UH=UH)
            outs.append(f"{out}/result.json")
            rec = json.load(open(outs[-1]))
            check(f"record {i}: keys", {"archive_sha256", "band", "band_arg", "charts", "checks", "claim", "control",
                                        "design", "eps", "provenance", "timing", "verdict"} <= set(rec), str(sorted(rec)))
        cmp = subprocess.run([sys.executable, os.path.join(ROOT, "code", "compare_runs.py"), *outs], capture_output=True,
                             text=True)
        last = cmp.stdout.strip().splitlines()[-1]
        check("compare_runs on two synthetic records", last == "IDENTICAL after masking", last)
        code = C.main(["--out", f"{tmp}/bad", "--band", "7,3"], UH=UH)
        rec = json.load(open(f"{tmp}/bad/result.json"))
        check("main with a non-critical band: REJECT, record written", code == 1 and rec["verdict"].startswith("REJECT"),
              rec["verdict"][:120])
    # 4. the real potential path, without any POS chart
    for n, ell in sorted(C.MU1):
        t1 = time.time()
        checks, rec, timing, b, ch, mu1, sig1, dz = C.gates(n, ell, "none", ROOT, None, prove_sign, {}, {})
        check(f"real D={n + 2} l={ell} none: every gate before the POS charts passes", failed(checks) == [],
              f"{failed(checks)}; degrees {rec['degrees']} ({time.time() - t1:.1f} s)")
    for n, ell in ((5, 2), (9, 4)):
        for control in SPECS:
            if control == "none":
                continue
            verify = tampered_prove_sign if control == "td-verifier" else prove_sign
            checks, rec, timing, b, ch, mu1, sig1, dz = C.gates(n, ell, control, ROOT, None, verify, {}, {})
            check(f"real D={n + 2} l={ell} {control}: non-POS failures {NONPOS[control]}",
                  failed(checks) == NONPOS[control], str(failed(checks)))
        checks, rec, timing, b, ch, mu1, sig1, dz = C.gates(n, ell, "nc-bound", ROOT, None, prove_sign, {}, {})
        certified, info, plant = C.nc_bound_a(prove_sign, b, {}, {})
        check(f"real D={n + 2} l={ell} nc-bound (a): support inside U_- < 0, Q[b] certified < 0", certified,
              f"support {info['support']}, K {info['K']}, I1 {info['I1_float']:.4g}, Q_b {info['Q_b']}")
    # Addendum 1, the precondition of the kit's consistency requirement (a), without any POS chart: for each of BHM-144's
    # 35 jobs, gates() on S5's potential gives exactly the record's checks before the POS charts and its fields.
    from a1.p1 import plain
    keys = ("band", "design", "charts", "max_depth", "eps", "q(MU1)^2", "q(MU1)_approx", "throat_data", "C0", "degrees",
            "d6")
    jobs = [(n, ell, "none") for n, ell in sorted(C.MU1)] + [(n, ell, c) for n, ell in ((5, 2), (9, 4))
                                                             for c in ORIGINAL if c != "none"]
    for n, ell, control in jobs:
        path = os.path.join(ROOT, "results", "hdx", "critical", "runs", "record", f"D{n + 2}l{ell}", control, "result.json")
        ref = json.load(open(path))
        verify = tampered_prove_sign if control == "td-verifier" else prove_sign
        checks, rec, timing, b, ch, mu1, sig1, dz = C.gates(n, ell, control, ROOT, None, verify, {}, {})
        mine = plain({"checks": {k: {"ok": bool(ok), "detail": det} for k, (ok, det) in checks.items()},
                      **{k: rec[k] for k in keys if k in rec}})
        bad = [k for k in mine["checks"] if mine["checks"][k] != ref["checks"].get(k)]
        bad += [k for k in keys if (k in rec) != (k in ref) or (k in rec and mine[k] != ref[k])]
        check(f"(a) without POS: D={n + 2} l={ell} {control}: gates() equals BHM-144's record", not bad, str(bad))
    print(f"{sum(OK)}/{len(OK)} as expected in {time.time() - t0:.0f} s")
    print("DEVTEST PASS" if all(OK) else "DEVTEST FAIL")
    return 0 if all(OK) else 1


if __name__ == "__main__":
    sys.exit(main())
