"""Stage A2, A2-S addendum 1 (results/a2/s/PREREG_ADDENDUM_1.md): X0, inward decimals of the certified range ends, and
X1, the main run's consistency with the sealed record of BHM-101.

    python -m a2.scheck --out DIR --main MAIN_RESULT.json [--root REPO]

X0  (exact integer square roots; no float enters a decimal)
    - A2-S's lower end q(1/8) = sqrt(1 - w(1/8)^2): rounded up at 5 decimals (inward for a lower end);
    - T3's range [q(mu_hi), q(mu_lo)] from its sealed record's boxes: the lower end rounded up and the upper end rounded
      down at 5 decimals, and the upper end truncated at 8 decimals (for BHM-060's digits);
    - q(mu_lo(l)) for l = 3..10 from A2-E's sealed record: rounded up (A2-E's lower end) and down (P1's upper end) at 7.
X1  the main record of this run equals BHM-101's sealed record after removing timing, provenance and archive_sha256.
Every record read is checked against SEALED.sha256 first.  VERIFIED only if X0's values are the registered ones and X1
holds; otherwise REJECT: <reasons>.
"""
import argparse
import datetime
import hashlib
import json
import os
import sys
import time
from fractions import Fraction
from math import isqrt

import sympy as sp

from a2.scert import MU1, sealed_hash
from hd.elementary import param_n
from onset.onset import mu
from qnm1c.common import CertificateError, dump_json, provenance

T3_RECORD = "results/p3/runs/record/T3/result.json"
E_RECORD = "results/a2/elementary/runs/record/none/result.json"
S_RECORD = "results/a2/s/runs/record/none/result.json"
# The registered values (PREREG_ADDENDUM_1.md, X0), as the session-R lead's reading computed them (BHM-103)
WANT = {"A2-S lower end": "0.98937", "T3": ["0.97277", "0.99019"], "T3 upper end, 8 decimals truncated": "0.99019883"}


def decimal(q2, digits, up):
    """sqrt(q2) at `digits` decimals, rounded up (up=True) or down, exactly."""
    q2 = Fraction(q2)
    num, den = q2.numerator * 10 ** (2 * digits), q2.denominator
    r = isqrt(num // den)
    if up and r * r * den != num:
        r += 1
    return f"{r // 10 ** digits}.{r % 10 ** digits:0{digits}d}"


def sealed_json(root, path):
    with open(os.path.join(root, path), "rb") as fh:
        raw = fh.read()
    if hashlib.sha256(raw).hexdigest() != sealed_hash(root, path):
        raise CertificateError(f"SEAL: {path} is not the sealed file")
    return json.loads(raw)


def q2_at(muv):
    muv = Fraction(muv)
    return Fraction(str(sp.cancel(param_n(4, 2)["q2"].subs(mu, sp.Rational(muv.numerator, muv.denominator)))))


def strip(rec):
    return {k: v for k, v in rec.items() if k not in ("timing", "provenance", "archive_sha256")}


def run(root, main_path):
    checks, rec = {}, {}
    q2s = q2_at(Fraction(str(MU1)))
    s_low = decimal(q2s, 5, True)
    t3 = sealed_json(root, T3_RECORD)["result"]["boxes_mu"]
    mlo, mhi = Fraction(t3[0]["mu"][0]), Fraction(t3[-1]["mu"][1])
    t3q = [q2_at(mhi), q2_at(mlo)]
    t3d = [decimal(t3q[0], 5, True), decimal(t3q[1], 5, False)]
    t3_8 = decimal(t3q[1], 8, False)
    erec = sealed_json(root, E_RECORD)
    ed = {f"l={p['ell']}": {"q(mu_lo)^2": p["q_at_mu_lo_squared"],
                             "A2-E lower end (up, 7)": decimal(Fraction(p["q_at_mu_lo_squared"]), 7, True),
                             "P1 upper end (down, 7)": decimal(Fraction(p["q_at_mu_lo_squared"]), 7, False)}
          for p in erec["parts"]}
    rec["X0"] = {"A2-S": {"q(1/8)^2": str(q2s), "lower end (up, 5)": s_low},
                 "T3": {"mu range": [str(mlo), str(mhi)], "q^2 range": [str(t3q[0]), str(t3q[1])],
                        "inward (5)": t3d, "upper end truncated (8)": t3_8},
                 "A2-E and P1": ed}
    got = {"A2-S lower end": s_low, "T3": t3d, "T3 upper end, 8 decimals truncated": t3_8}
    checks["X0"] = (got == WANT, f"computed {got}; registered {WANT}")
    srec = sealed_json(root, S_RECORD)
    with open(main_path) as fh:
        mrec = json.load(fh)
    same = strip(mrec) == strip(srec)
    diff = sorted(k for k in set(strip(mrec)) | set(strip(srec)) if strip(mrec).get(k) != strip(srec).get(k))
    checks["X1"] = (same, f"this run's main record equals BHM-101's after removing timing, provenance, archive_sha256: "
                          f"{same}; differing keys {diff}")
    return checks, rec


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--main", required=True)
    ap.add_argument("--root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    a = ap.parse_args(argv)
    t0, start = time.time(), datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    record = {"claim": "results/a2/s/PREREG_ADDENDUM_1.md, X0 and X1", "provenance": provenance(),
              "archive_sha256": os.environ.get("BHM_ARCHIVE", "unknown")}
    try:
        checks, rec = run(a.root, a.main)
        record.update(rec)
        record["checks"] = {k: {"ok": bool(ok), "detail": det} for k, (ok, det) in checks.items()}
        failed = [k for k, (ok, _) in checks.items() if not ok]
        verdict = "VERIFIED" if not failed else "REJECT: " + ", ".join(failed)
    except Exception as exc:  # noqa: BLE001  (fail-closed)
        verdict = f"REJECT: exception {type(exc).__name__}: {exc}"
    record["verdict"] = verdict
    record["timing"] = {"utc_start": start, "t_total_s": round(time.time() - t0, 1)}
    os.makedirs(a.out, exist_ok=True)
    dump_json(record, os.path.join(a.out, "result.json"))
    for k, v in record.get("checks", {}).items():
        print(f"{k}: {'PASS' if v['ok'] else 'FAIL'}  {v['detail'][:400]}")
    print(verdict)
    return 0 if verdict == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
