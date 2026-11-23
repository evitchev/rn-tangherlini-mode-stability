"""Run my Bernstein verifier on every built certificate (Kimi's audit, task 3).

Single-mu: N(z) on [0, 1].   Box: Ntilde(Y, mu) on [0, 1] x [mua, mub] (Y = 1-z),
with Den(mu) > 0 on the box proved factorwise (each factor verified on the box).
Prints one line per certificate; exit 0 only if all verify.
"""
import json
import os
import sys

from flint import fmpq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify import verify_1d, verify_2d

HERE = os.path.dirname(os.path.abspath(__file__))
BUILT = os.path.join(HERE, "built")

FACTOR_POLYS = {0: {0: fmpq(6), 2: fmpq(1)},     # mu^2 + 6
                1: {0: fmpq(1), 1: fmpq(1)},     # mu + 1
                2: {0: fmpq(6), 1: fmpq(1)}}     # mu + 6


def load(name):
    with open(os.path.join(BUILT, name + ".json")) as fh:
        return json.load(fh)


def fmpq_map_1d(m):
    return {int(k): fmpq(v) for k, v in m.items()}


def fmpq_map_2d(m):
    out = {}
    for key, v in m.items():
        i, j = eval(key)
        out[(i, j)] = fmpq(v)
    return out


def main():
    results = {}
    for name in ["T1_rule1", "T1_rule2", "G1_rule2"]:
        d = load(name)
        p = fmpq_map_1d(d["N"])
        ok, info = verify_1d(p, fmpq(0), fmpq(1))
        results[name] = (ok, info)
        print(f"{name}: {'POSITIVE' if ok else 'REJECT'}  {info}", flush=True)
    for name, nboxes in [("T2_rule1", 1), ("T3_rule1", 8), ("T2_rule2", 1)]:
        for k in range(nboxes):
            d = load(f"{name}_box{k}")
            mua, mub = (fmpq(d["mu_box"][0]), fmpq(d["mu_box"][1]))
            # Den > 0 on the box, factorwise
            den_ok = True
            for fi, e in enumerate(d["Den_exps"]):
                if e == 0:
                    continue
                fok, finfo = verify_1d(FACTOR_POLYS[fi], mua, mub)
                if not fok:
                    den_ok = False
                    print(f"{name}_box{k}: DENOMINATOR FACTOR {fi} NOT POSITIVE {finfo}",
                          flush=True)
            N2 = fmpq_map_2d(d["Ntilde"])
            ok, info = verify_2d(N2, fmpq(0), fmpq(1), mua, mub)
            ok = ok and den_ok
            results[f"{name}_box{k}"] = (ok, info)
            print(f"{name}_box{k} mu in [{d['mu_box'][0]},{d['mu_box'][1]}]: "
                  f"{'POSITIVE' if ok else 'REJECT'}  Den_exps={d['Den_exps']} {info}",
                  flush=True)
    allok = all(ok for ok, _ in results.values())
    print("ALL CERTIFICATES:", "POSITIVE" if allok else "SOME REJECTED")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
