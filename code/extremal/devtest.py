"""Development tests of extremal.zero_mode, run before registration (results/extremal/PREREG.md section 5).

Synthetic inputs only: S5's U and H are never evaluated, and the registered candidate is never run.  Two synthetic
candidates, each with the potential built from it (W := the identity's left side), so that Z-id holds by construction:
    A  g = -nu - (n-1) alpha Y/(1-Y),                  h = 1 + Y   (no pole: the partner is regular)
    B  g = A's + n (n-1) Y/(1+Y),                      h = 1 + Y   (a pole whose double-pole term does not cancel)
Every check, control and drill path, the n-symbolic path, the JSON writer and compare_runs are exercised.

    python -m extremal.devtest
"""
import json
import os
import subprocess
import sys
import tempfile
import time

import sympy as sp

from extremal import zero_mode as zm
from ki.potentials import d, m, x
from kimaster.master import NSYM

RESULTS = []


def expect(name, got, want):
    ok = got == want
    RESULTS.append(ok)
    print(f"{'ok  ' if ok else 'FAIL'} {name}: {got!r}" + ("" if ok else f" (expected {want!r})"))


def cand_syn(kind):
    def cand(n, control):
        nn = zm.nn_of(n)
        nu = zm.ELL + nn / 2 - 1 + (1 if control == "nc-nu" else 0)
        alpha = (zm.ELL + (1 if control == "nc-exp" else 0)) / (nn - 1)
        h = 1 + zm.Y
        g = -nu - (nn - 1) * alpha * zm.Y / (1 - zm.Y)
        if kind == "B":
            g = g + nn * (nn - 1) * zm.Y / h
        return g, nu, alpha, h
    return cand


def potential_syn(kind):
    def pot(n, control, UH):
        nn = zm.nn_of(n)
        g = cand_syn(kind)(n, "none")[0]
        W = sp.cancel(sp.together(zm.lhs(n, g, "none")))
        H = (zm.ELL + nn) * (1 + zm.Y)
        if control == "td-U":
            mm = zm.extremal_md(nn, zm.ELL)[0]
            W = sp.cancel(W + mm ** 2 / H ** 2)
        return W, H
    return pot


def UH_syn(n, sector):
    """Synthetic U and H.  Like S5's master(), it accepts only an int or "N" for n (addendum 1: the run at a188aba passed
    the string "4" to master() and was VOID)."""
    if not (n == "N" or isinstance(n, int)):
        raise TypeError(f"UH called with n = {n!r} of type {type(n).__name__}")
    return (64 * m ** 2 + x * (1 + m * d), m + x) if sector == "minus" else (64 + x, 1 + d * x)


def verdict_of(checks):
    failed = [k for k in zm.ORDER if not checks[k][0]]
    return "VERIFIED" if not failed else "REJECT: " + ", ".join(failed)


def main():
    t0 = time.time()
    real_pot, real_master = zm.potential_W, zm.master

    def refuse(*a, **k):
        raise AssertionError("S5's master() called in a development test")
    zm.master = refuse
    want = {
        "A": {"none": "VERIFIED", "nc-nu": "REJECT: Z-inf, Z-id, P-reg, P-asym",
              "nc-exp": "REJECT: Z-thr, Z-id, P-reg, P-asym", "td-U": "REJECT: Z-inf, Z-thr, Z-id, P-reg, P-asym",
              "td-zid": "REJECT: Z-id, P-reg, P-asym", "td-preg": "REJECT: P-asym"},
        "B": {"none": "REJECT: P-reg", "td-preg": "REJECT: P-reg, P-asym"},
    }
    try:
        for kind, cases in want.items():
            zm.potential_W = potential_syn(kind)
            for n in (4, 9, "N"):
                for control, v in cases.items():
                    checks, facts = zm.run_case(n, control, UH_syn, cand_syn(kind))
                    expect(f"{kind} n={n} {control}", verdict_of(checks), v)
                    if control == "none" and kind == "A":
                        expect(f"{kind} n={n} Ut polynomial in Y", facts.get("Ut_polynomial_in_Y"), True)
                        expect(f"{kind} n={n} comparisons ran", sorted(facts["comparisons"]),
                               ["Ut == W_minus(l+1)", "Ut == W_minus(l-1)", "Ut == W_plus(l)"])
        # The q1, H and Z-pos gates on the synthetic H: break each once.
        zm.potential_W = potential_syn("A")
        checks, _ = zm.run_case(4, "none", UH_syn,
                                lambda n, c: (cand_syn("A")(n, c)[0], cand_syn("A")(n, c)[1], cand_syn("A")(n, c)[2],
                                              -1 + zm.Y))
        expect("A n=4, h = -1 + Y: H and Z-pos fail", verdict_of(checks).split(": ")[1].split(", ")[:2], ["H", "Z-pos"])
        # Addendum 1: the real potential path, with the synthetic UH, which accepts only an int or "N" for n (the
        # defect of the run at a188aba).  main() must convert --n to an int before the potential is built.
        zm.potential_W = real_pot
        with tempfile.TemporaryDirectory() as tmp:
            zm.main(["--out", tmp, "--n", "4"], UH=UH_syn, cand=cand_syn("A"))
            rec = json.load(open(os.path.join(tmp, "result.json")))
            expect("addendum 1: main --n 4 through the real potential path ends without an exception",
                   rec["verdict"].startswith("REJECT: exception"), False)
            expect("addendum 1: ... and runs every check", sorted(rec["checks"]), sorted(zm.ORDER))
        try:
            zm.run_case("4", "none", UH_syn, cand_syn("A"))
            got = "no exception"
        except TypeError:
            got = "TypeError"
        expect("addendum 1: a string n, as at a188aba, is refused by the typed UH", got, "TypeError")
        zm.potential_W = potential_syn("A")
        # The throat classification (formula only; no potential involved).
        cl = zm.classify(5)
        expect("classify n=5 l=2 principal (2l = n - 1)", cl["l=2"]["throat_principal"], True)
        expect("classify n=5 l=3 not principal", cl["l=3"]["throat_principal"], False)
        cl = zm.classify(6)
        expect("classify n=6 l=2 principal (2l < n - 1)", cl["l=2"]["throat_principal"], True)
        expect("classify n=4 l=2 not principal", zm.classify(4)["l=2"]["throat_principal"], False)
        expect("classify n=9 bands", sorted(k for k, v in zm.classify(9).items() if v["throat_principal"]),
               ["l=2", "l=3", "l=4"])
        # The JSON writer and compare_runs, on two synthetic records.
        with tempfile.TemporaryDirectory() as tmp:
            outs = []
            for i in range(2):
                out = os.path.join(tmp, f"r{i}")
                rc = zm.main(["--out", out, "--n", "4", "--control", "nc-nu"], UH=UH_syn, cand=cand_syn("A"))
                expect(f"main exit code, run {i}", rc, 1)
                rec = json.load(open(os.path.join(out, "result.json")))
                expect(f"record verdict, run {i}", rec["verdict"], want["A"]["nc-nu"])
                expect(f"record keys, run {i}", sorted(rec),
                       ["archive_sha256", "checks", "claim", "control", "facts", "n", "provenance", "timing", "verdict"])
                outs.append(os.path.join(out, "result.json"))
            here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cmp = subprocess.run([sys.executable, os.path.join(here, "compare_runs.py"), *outs], capture_output=True,
                                 text=True)
            expect("compare_runs on two synthetic records", cmp.returncode, 0)
            rc = zm.main(["--out", os.path.join(tmp, "bad"), "--n", "12"], UH=UH_syn, cand=cand_syn("A"))
            expect("n outside 2..9 rejects", rc, 1)
    finally:
        zm.potential_W, zm.master = real_pot, real_master
    n_ok = sum(RESULTS)
    print(f"{n_ok}/{len(RESULTS)} as expected in {time.time() - t0:.1f} s")
    return 0 if all(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
