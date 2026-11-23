"""Development tests of hdx.elementary, run before registration (results/hdx/elementary/PREREG.md section 5).

    python -m hdx.devtest_elementary

Synthetic inputs for every path at n = 5 and n = 9: U = 64 m^3 (2 - x)(1 + x), which vanishes at the extremal horizon
x = 2 like a touching case but is otherwise unrelated, U + 64 m^3, and U - 200 m^3 (negative at x = 1).  S5's U_- is
evaluated only at n = 4, where A2-E's record (BHM-097) and A2's gate U_-(x_H) = 64 l (l - 3)(l + 3)^2 (l + 4)^2 are
known answers, and inside E0n, the transcription gate (BHM-063).  MEET uses the parametrisation only, on the claim's
(D, l).  No elementary check of the claim's (D, l) runs on S5's U_- here.
"""
import json
import os
import subprocess
import sys
import tempfile

from a1.p1 import kats, tampered_prove_sign
from hdx import elementary as E
from ki.potentials import m, x
from onset.bernstein import prove_sign
from qnm1c.common import CertificateError

USYN = 64 * m ** 3 * (2 - x) * (1 + x)
OK = []
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")


def expect(name, fn, want_error):
    try:
        r = fn()
        got = False
        info = r.get("bound", r) if isinstance(r, dict) else r
    except CertificateError as exc:
        got, info = True, str(exc)[:200]
    OK.append(got == want_error)
    print(f"{'ok  ' if got == want_error else 'FAIL'} {name}: {'CertificateError' if got else 'passes'}; {info}",
          flush=True)


def check(name, cond, info=""):
    OK.append(bool(cond))
    print(f"{'ok  ' if cond else 'FAIL'} {name}: {info}", flush=True)


def synthetic_main(control, U, tmp, k):
    """hdx.elementary.main with U_of replaced by a synthetic U; returns (exit code, record)."""
    saved = E.U_of
    E.U_of = lambda n, c: U
    try:
        out = f"{tmp}/{control}-{k}"
        os.makedirs(out)
        code = E.main(["--out", out, "--control", control, "--root", ROOT])
        return code, json.load(open(f"{out}/result.json")), f"{out}/result.json"
    finally:
        E.U_of = saved


def main():
    for n in (5, 9):
        g = E.GRID[n]
        expect(f"n={n} l={n - 1} splitting on the synthetic U",
               lambda: E.part(prove_sign, n, n - 1, USYN, g, E.QMAX, "split"), False)
        expect(f"n={n} l={n - 1} strict bound on the synthetic U (nc-strict path)",
               lambda: E.part(prove_sign, n, n - 1, USYN, g, E.QMAX, "strict"), True)
        expect(f"n={n} l={n} strict bound on U + 64 m^3",
               lambda: E.part(prove_sign, n, n, USYN + 64 * m ** 3, g, E.QMAX, "strict"), False)
        expect(f"n={n} l={n} with the planted bump (nc-bump path)",
               lambda: E.part(prove_sign, n, n, USYN + 64 * m ** 3, g, E.QMAX, "bump"), True)
        expect(f"n={n} l={n + 1} on a U negative at x = 1 (nc-band path)",
               lambda: E.part(prove_sign, n, n + 1, USYN - 200 * m ** 3, g, E.QMAX, "strict"), True)
        expect(f"n={n} l={n} splitting on U + 64 m^3 (F(1, 0) != 0: the division by mu must fail)",
               lambda: E.part(prove_sign, n, n, USYN + 64 * m ** 3, g, E.QMAX, "split"), True)
    ok, _ = kats(tampered_prove_sign)
    check("the tampered verifier fails the KATs", not ok)
    ok, _ = kats(prove_sign)
    check("the verifier passes the KATs", ok)
    ok, det = E.gate_EXT("none", ns=[4])
    check("EXT at n = 4 (A2's known answer)", ok, det)
    saved = E.U_of
    E.U_of = lambda n, c: USYN
    ok, det = E.gate_EXT("none", ns=[4, 5, 9])
    E.U_of = saved
    check("EXT fails on the synthetic U", not ok, det[:160])
    ok, det = E.gate_EXT("td-coeff", ns=[4])
    check("EXT fails at n = 4 under td-coeff", not ok, det[:160])
    ok, det, table = E.gate_MEET(ROOT, E.QMAX)
    check("MEET with the 99/100 rule: every mu_lo equals HD-E's", ok and all(v["equal"] for v in table.values()), det)
    print(json.dumps({k: v["mu_lo"] for k, v in table.items()}), flush=True)
    ok2, det2, table2 = E.gate_MEET(ROOT, E.Q_TAMPER)
    check("MEET fails with the 995/1000 rule (td-mulo), at every (D, l)",
          not ok2 and not any(v["meets"] for v in table2.values()), det2[:200])
    ok, det, mine = E.gate_A2E4(prove_sign, ROOT, "none")
    check("A2E4: n = 4 reproduces A2-E's record field by field", ok, det)
    ok, det, _ = E.gate_A2E4(prove_sign, ROOT, "td-coeff")
    check("A2E4 fails under td-coeff", not ok, det[:200])
    with tempfile.TemporaryDirectory() as tmp:
        outs = []
        for k in range(2):
            code, rec, path = synthetic_main("none", USYN + 64 * m ** 3, tmp, k)
            outs.append(path)
            check(f"synthetic main run {k}: verdict starts REJECT: EXT, A2E4 (synthetic U)",
                  rec["verdict"].startswith("REJECT: EXT, A2E4") and code == 1, rec["verdict"][:160])
            check(f"synthetic main run {k}: 33 parts, the 5 touching ones fail their splitting",
                  len(rec["parts"]) == 33 and sorted(p["ell"] - p["n"] for p in rec["parts"] if "failure" in p)
                  == [-1] * 5, str([p.get("failure", "")[:60] for p in rec["parts"] if "failure" in p][:2]))
        cmp = subprocess.run([sys.executable, "compare_runs.py"] + outs, capture_output=True, text=True)
        last = cmp.stdout.strip().splitlines()[-1]
        check("compare_runs on the two synthetic records", last == "IDENTICAL after masking", last)
        for control, U, want in [("nc-band", USYN - 200 * m ** 3, "E D=7 l=3, E D=11 l=7"),
                                 ("nc-strict", USYN, "E D=7 l=4, E D=11 l=8"),
                                 ("nc-bump", USYN + 64 * m ** 3, "E D=7 l=5, E D=11 l=9")]:
            code, rec, _ = synthetic_main(control, U, tmp, 0)
            check(f"{control} on a synthetic U: its two parts fail", rec["verdict"].endswith(want) and code == 1,
                  rec["verdict"][:200])
        code, rec, _ = synthetic_main("td-verifier", USYN + 64 * m ** 3, tmp, 0)
        check("td-verifier: KAT fails", rec["verdict"].startswith("REJECT: KAT") and code == 1, rec["verdict"][:120])
        code, rec, _ = synthetic_main("td-mulo", USYN + 64 * m ** 3, tmp, 0)
        check("td-mulo: MEET fails", "MEET" in rec["verdict"] and code == 1, rec["verdict"][:120])
        code, rec, _ = synthetic_main("td-coeff", USYN + 64 * m ** 3, tmp, 0)
        check("td-coeff: E0n fails (its tamper is applied inside hd.elementary's U_of)",
              rec["verdict"].startswith("REJECT: E0n") and code == 1, rec["verdict"][:120])
    print(f"{sum(OK)}/{len(OK)} as expected")
    print("DEVTEST PASS" if all(OK) else "DEVTEST FAIL")


if __name__ == "__main__":
    main()
