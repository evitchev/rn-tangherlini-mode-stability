"""HD-S PREREG addendum 1, check X2 (results/hd/s/PREREG_ADDENDUM_1.md): every stored certificate's polynomial against a
direct evaluation of N.

    python -m hd.scheck --out DIR --band D,L [--control NAME] [--root REPO]

For each verified box of the band's sealed record (results/hd/s/runs/record/<D>-<L>/result.json, its SHA-256 checked
against SEALED.sha256), at NPTS seeded random rational points (z, mu) in [0, 1] x box, exactly:
  LHS  the certificate's N L s^(2e), rebuilt from the stored P-hat by hd.scert.Exact (the verified pipeline), divided
       by L(mu) s(z)^(2e);
  RHS  N computed directly: U_-, H_- of ki.potentials at (m, delta(mu), x), x = x_H(mu)(1 - z)^(n-1),
       f = 1 - x + q^2 x^2/4 with q^2 = 1 - w(mu)^2 (not hd.scert's factored f), f_z by the chain rule, and
       P = P-hat/s^e with P_z by the quotient rule.
LHS = RHS at every point of every box, or REJECT.
--control: td-direct  the RHS uses U_- + 16 n m^2: X2 must REJECT (the check is not vacuous).
"""
import argparse
import hashlib
import json
import os
import random
import sys
import time
from fractions import Fraction

import sympy as sp

from hd.elementary import param_n
from hd.scert import Exact, z
from ki.potentials import H_minus, U_minus, d, m, x
from onset.onset import mu
from qnm1c.common import dump_json, provenance

NPTS = 8
DEN = 2 ** 30


def Fr(c):
    return Fraction(str(c))


def peval(poly, zv, muv):
    """Exact value of a Poly in (z, mu) at Fractions."""
    tot = Fraction(0)
    for (i, j), c in poly.terms():
        tot += Fr(c) * zv ** i * muv ** j
    return tot


def direct_N(n, ell, terms, e, db, zv, muv, UH):
    """N from the definition, in Fractions; terms: {(i, j): Fraction} of P-hat."""
    p = param_n(n, ell)
    sub = {mu: sp.Rational(muv.numerator, muv.denominator)}
    w, dl, xH = (Fr(p[k].subs(sub)) for k in ("w", "delta", "xH"))
    mm = p["m"]
    q2 = 1 - w * w
    X = xH * (1 - zv) ** (n - 1)
    Xz = -(n - 1) * xH * (1 - zv) ** (n - 2)
    f = 1 - X + q2 * X * X / 4
    fz = -Xz + q2 * X * Xz / 2
    Ue, He = UH
    sb = {m: mm, d: sp.Rational(dl.numerator, dl.denominator), x: sp.Rational(X.numerator, X.denominator)}
    U, H = Fr(Ue.subs(sb)), Fr(He.subs(sb))
    Ph = sum(c * zv ** i * muv ** j for (i, j), c in terms.items())
    Phz = sum(c * i * zv ** (i - 1) * muv ** j for (i, j), c in terms.items() if i > 0)
    if e == 0:
        P, Pz = Ph, Phz
    else:
        s = zv + db
        P, Pz = Ph / s ** e, (Phz * s - e * Ph) / s ** (e + 1)
    return U - 64 * H * H * ((1 - zv) * fz * P + f * (-P + (1 - zv) * Pz + P * P))


def sealed_ok(root, rel):
    with open(os.path.join(root, rel), "rb") as fh:
        h = hashlib.sha256(fh.read()).hexdigest()
    with open(os.path.join(root, "SEALED.sha256")) as fh:
        return any(line.split()[:2] == [h, rel] for line in fh if not line.startswith("#")), h


def check_band(n, ell, rec, control, UHexact=None, UHdirect=None):
    """Returns (ok, details). UHexact/UHdirect: synthetic (U, H) for the development tests."""
    E = Exact(n, ell, "none", UHexact)
    UH = UHdirect or (U_minus(n) + (16 * n * m ** 2 if control == "td-direct" else 0), H_minus(n))
    out, ok = [], True
    for k, b in enumerate(r for r in rec["boxes"] if r["verified"]):
        a0, a1 = Fraction(b["mu"][0]), Fraction(b["mu"][1])
        terms = {tuple(int(t) for t in key.strip("()").split(",")): Fraction(v) for key, v in b["P"].items()}
        Phat = sp.Poly(sum(sp.Rational(c.numerator, c.denominator) * z ** i * mu ** j for (i, j), c in terms.items()),
                       z, mu)
        e = 0 if b["variable"] == "z" else b["degree"]
        db = None if e == 0 else Fraction(b["delta_b"])
        s = None if e == 0 else sp.Poly(z + sp.Rational(db.numerator, db.denominator), z, mu)
        NL, L = E.NL(Phat, s, e), E.L
        rng = random.Random(1000003 * n + 1009 * ell + k)
        agree = 0
        for _ in range(NPTS):
            zv = Fraction(rng.randrange(DEN + 1), DEN)
            muv = a0 + (a1 - a0) * Fraction(rng.randrange(DEN + 1), DEN)
            lhs = peval(NL, zv, muv) / (peval(L, zv, muv) * (1 if e == 0 else (zv + db) ** (2 * e)))
            rhs = direct_N(n, ell, terms, e, db, zv, muv, UH)
            agree += lhs == rhs
        out.append({"mu": b["mu"], "variable": b["variable"], "degree": b["degree"], "agree": agree, "of": NPTS})
        ok = ok and agree == NPTS
    return ok, out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--band", required=True, help="D,l")
    ap.add_argument("--control", choices=("none", "td-direct"), default="none")
    ap.add_argument("--root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    a = ap.parse_args(argv)
    D, ell = (int(t) for t in a.band.split(","))
    t0 = time.time()
    rel = f"results/hd/s/runs/record/{D}-{ell}/result.json"
    record = {"claim": "results/hd/s/PREREG_ADDENDUM_1.md, X2", "band": f"D={D} l={ell}", "control": a.control,
              "provenance": provenance()}
    try:
        seal, h = sealed_ok(a.root, rel)
        record["record_sha256"] = h
        with open(os.path.join(a.root, rel)) as fh:
            rec = json.load(fh)
        ok, out = check_band(D - 2, ell, rec, a.control)
        record["boxes"] = out
        record["checks"] = {"SEAL": seal, "X2": ok}
        failed = [k for k, v in record["checks"].items() if not v]
        verdict = "VERIFIED" if not failed else "REJECT: " + ", ".join(failed)
    except Exception as exc:  # noqa: BLE001  (fail-closed)
        verdict = f"REJECT: exception {type(exc).__name__}: {exc}"
    record["verdict"] = verdict
    record["timing"] = {"t_total_s": round(time.time() - t0, 2)}
    dump_json(record, f"{a.out}/result.json")
    n_box = len(record.get("boxes", []))
    n_ok = sum(1 for r in record.get("boxes", []) if r["agree"] == r["of"])
    print(f"D={D} l={ell} {a.control}: {n_ok}/{n_box} boxes agree at all {NPTS} points")
    print(verdict[:400])
    return 0 if verdict == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
