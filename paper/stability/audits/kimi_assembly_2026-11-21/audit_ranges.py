"""Exact range-end checks for the A1/HD composition audit.

Run on host-1/host-2 under nice -n 19.  Every comparison is a Fraction
comparison, not a floating comparison.
"""
import json
import os
from fractions import Fraction

ROOT = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(ROOT, "records")
OUT = []


def load(rel):
    with open(os.path.join(R, rel)) as f:
        return json.load(f)


def q2(n, ell, mu):
    mu = Fraction(mu)
    B = 2 * ell + n - 1
    A = (ell + n) + (ell - 1) * mu ** 2
    return 1 - (B * mu / A) ** 2


def check(label, left, relation, right, source):
    if relation == "==" and left == right:
        ok = True
    else:
        left, right = Fraction(left), Fraction(right)
        ok = {"<": left < right, "<=": left <= right,
              "==": left == right, ">=": left >= right,
              ">": left > right}[relation]
    row = {"check": label, "left": str(left), "relation": relation,
           "right": str(right), "ok": ok, "source": source}
    OUT.append(row)
    print(("PASS" if ok else "FAIL"), label, left, relation, right, "|", source, flush=True)
    return ok


def main():
    # ---- D = 6, ell = 2: O2, T3, A2-S ----
    onset = load("results/onset/runs/record/main/result.json")
    qlo, qhi = map(Fraction, onset["q_star_squared_interval"])
    t3lo, t3hi = Fraction(21576, 22801), Fraction(31416, 32041)
    check("D6: T3 lower < O2's q_* interval lower end", t3lo, "<", qlo,
          "onset result.json q_star_squared_interval; p3/PREREG.md:42")
    check("D6: T3 lower < O2's q_* interval upper end", t3lo, "<", qhi,
          "onset result.json q_star_squared_interval")
    check("D6: A2-S lower < T3 upper", Fraction(2961, 3025), "<", t3hi,
          "a2/s/PREREG.md:10; p3/PREREG.md:42")
    check("D6: A2-S q(1/8)^2 <= (99/100)^2", Fraction(2961, 3025), "<=", Fraction(9801, 10000),
          "a2/s/PREREG.md:10,56")
    check("D6: T3 lower is q(1/5)^2", t3lo, "==", q2(4, 2, Fraction(1, 5)),
          "p3 result.json last mu-box (q decreases with mu)")
    check("D6: T3 upper is q(3/25)^2", t3hi, "==", q2(4, 2, Fraction(3, 25)),
          "p3 result.json first mu-box (q decreases with mu)")
    check("D6: T3 has eight certified mu-boxes", len(load("results/p3/runs/record/T3/result.json")["result"]["boxes_mu"]), "==", 8,
          "p3/RESULT.md:18")
    rule2 = load("results/p3/rule2/record/G1/result.json")
    check("D6: rule-2 G1 is VERIFIED", rule2["verdict"], "==", "VERIFIED",
          "p3/rule2/record/G1/result.json")

    # ---- D = 6, ell = 3..10 and ell >= 11 ----
    p1 = load("results/a1/runs/record/main/result.json")
    ae = load("results/a2/elementary/runs/record/none/result.json")
    for row, other in zip(p1["part1"], ae["parts"]):
        ell = row["ell"]
        assert other["ell"] == ell
        check(f"D6 l={ell}: P1 and A2-E use the same mu_lo", row["mu_lo"], "==", other["mu_lo"],
              "a1 result.json part1.mu_lo; a2/elementary result.json parts.mu_lo")
        check(f"D6 l={ell}: P1 and A2-E have the same q(mu_lo)^2", row["q_at_mu_lo_squared"], "==",
              other["q_at_mu_lo_squared"], "a1/a2 result.json q_at_mu_lo_squared")
        check(f"D6 l={ell}: q(mu_lo)^2 >= (99/100)^2", row["q_at_mu_lo_squared"], ">=", Fraction(9801, 10000),
              "a1/PREREG.md:40-42; a2/elementary/PREREG.md:13,26")
    check("D6: Lemma U's bound is positive", Fraction(959747, 17496), ">", 0,
          "a1/RESULT.md:33-41")

    # ---- HD-E E1, E2, E3 ----
    hd = load("results/hd/elementary/runs/record/main/result.json")
    assert hd["L_EL"] == {"5": 4, "6": 5, "7": 6, "8": 6, "9": 7}
    l0_expected = {7: 10, 8: 10, 9: 11, 10: 13, 11: 14}
    for row in hd["E1"]:
        D, ell = row["D"], row["ell"]
        check(f"D{D} l={ell}: E1 q(mu_lo)^2 >= (99/100)^2", row["q_at_mu_lo_squared"], ">=", Fraction(9801, 10000),
              "hd/elementary/PREREG.md:15-17,45-46")
        check(f"D{D} l={ell}: E1 ell is in the elementary partition", ell, ">=", hd["L_EL"][str(D - 2)],
              "hd/elementary/PREREG.md:15-17")
        check(f"D{D} l={ell}: E1 ell is at most E3's l0", ell, "<=", l0_expected[D],
              "hd/elementary/RESULT.md:14-20 and E3.l0")
    qsplit = {
        (7, 2): Fraction(948, 1000), (7, 3): Fraction(977, 1000),
        (8, 3): Fraction(944, 1000), (8, 4): Fraction(983, 1000),
        (9, 3): Fraction(921, 1000), (9, 4): Fraction(952, 1000),
        (9, 5): Fraction(987, 1000), (10, 3): Fraction(490, 1000),
        (10, 4): Fraction(920, 1000), (10, 5): Fraction(961, 1000),
        (11, 4): Fraction(897, 1000), (11, 5): Fraction(929, 1000),
        (11, 6): Fraction(968, 1000),
    }
    for row in hd["E2"]:
        D, ell = row["D"], row["ell"]
        expected = qsplit[(D, ell)]
        check(f"D{D} l={ell}: E2 q_hi is registered q_split", row["q_hi"], "==", expected,
              "hd/elementary/PREREG.md:21-27")
        check(f"D{D} l={ell}: E2 q(mu_lo)^2 >= q_split^2", row["q_at_mu_lo_squared"], ">=", expected ** 2,
              "hd/elementary/RESULT.md:45 and PREREG.md:45-46")
    for row in hd["E3"]:
        D = row["n"] + 2
        check(f"D{D}: E3's l0 is registered", row["l0"], "==", l0_expected[D],
              "hd/elementary/RESULT.md:14-20 and E3.l0")
        check(f"D{D}: E3's uniform bound is positive", row["bound"], ">", 0,
              "hd/elementary/RESULT_ADDENDUM_1.md:23-29")

    # ---- HD-S's 18 bands and their E2 meetings ----
    band_ells = {7: [2, 3], 8: [2, 3, 4], 9: [2, 3, 4, 5],
                 10: [2, 3, 4, 5], 11: [2, 3, 4, 5, 6]}
    for D, ells in band_ells.items():
        for ell in ells:
            band = load(f"results/hd/s/runs/record/{D}-{ell}/result.json")
            cov = band["coverage"]
            qlo = qsplit.get((D, ell), Fraction(0))
            check(f"D{D} l={ell}: HD-S q(mu_b)^2 <= E2 q_split^2", cov["q(mu_b)^2"], "<=", qlo ** 2,
                  "hd/s result.json coverage and hd/elementary E2 q_hi")
            check(f"D{D} l={ell}: HD-S q(mu_a)^2 >= (99/100)^2", cov["q(mu_a)^2"], ">=", Fraction(9801, 10000),
                  "hd/s/PREREG.md:32-37 and result.json coverage")
            check(f"D{D} l={ell}: HD-S boxes are contiguous", cov["contiguous"], "==", True,
                  "hd/s result.json coverage.contiguous")
            check(f"D{D} l={ell}: HD-S coverage is VERIFIED", band["verdict"], "==", "VERIFIED",
                  "hd/s result.json verdict")
            if qlo == 0:
                last = band["boxes"][-1]
                check(f"D{D} l={ell}: the from-0+ box ends at mu=1 and verifies", last["mu"][1], "==", 1,
                      "hd/s result.json last box and PREREG.md:77")
                check(f"D{D} l={ell}: the from-0+ box verifies", last["verified"], "==", True,
                      "hd/s result.json last box verified")
            if (D, ell) == (10, 3):
                check("D10 l=3: HD-S starts strictly below q_split=0.490", cov["q(mu_b)^2"], "<", Fraction(49, 100) ** 2,
                      "hd/s result.json coverage.q(mu_b)^2; hd/s/RESULT.md:50-51")

    # The two extremal onward thresholds quoted in the frozen draft.
    check("HD-X-S q(1/8)^2 <= (99/100)^2", Fraction(2961, 3025), "<=", Fraction(9801, 10000),
          "frozen draft:378")
    check("HD-X-2's largest q(MU1)^2 <= (99/100)^2", Fraction(46562824, 47513449), "<=", Fraction(9801, 10000),
          "frozen draft:379-380")

    result = {"host": os.uname().nodename, "checks": OUT,
              "all_ok": all(r["ok"] for r in OUT)}
    with open(os.path.join(ROOT, "range_results.json"), "w") as f:
        json.dump(result, f, indent=1)
    print("ALL_OK", result["all_ok"], "checks", len(OUT), flush=True)


if __name__ == "__main__":
    main()
