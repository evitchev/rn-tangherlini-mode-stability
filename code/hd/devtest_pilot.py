"""Development tests of hd.pilot, run before registration (results/hd/pilot/PREREG.md section 7).  Synthetic inputs
only: S5's U_- is not evaluated for any band, nor for T1 or G1, and no gate or control is run.

    python -m hd.devtest_pilot
"""
import math
import time
from fractions import Fraction

from hd.pilot import (DEGREES, GRID, Fit, Setting, cheb_coeffs, exact_eval, mu_of_q, nodes, qualify, riccati,
                      sample, slack, tabulate)


class Stub:
    def __init__(self, dt):
        self.dt = dt


def fit_error(g, gz, var, dg, dt):
    vmax, nd = nodes(Stub(dt), var, dg)
    F = Fit(Stub(dt), var, cheb_coeffs([g(zk) for _, zk in nd]), vmax)
    err = errz = 0.0
    for k in range(1, 400):
        z = k / 400
        p, pz = F(z)
        err, errz = max(err, abs(p - g(z))), max(errz, abs(pz - gz(z)))
    return err, errz


def main():
    print("Chebyshev fit of exp(z), degree 16, in z: max errors (P, P_z) =",
          fit_error(math.exp, math.exp, "z", 16, 0.5))
    g, gz = (lambda z: 1 / (z + 0.01)), (lambda z: -1 / (z + 0.01) ** 2)
    for var in ("z", "zeta"):
        print(f"1/(z + 0.01), dt = 0.04, in {var}: degree 16, 32 max errors =",
              [f"{e:.2e}" for dg in (16, 32) for e in fit_error(g, gz, var, dg, 0.04)])
    co = [Fraction(1, 3), Fraction(-2), Fraction(5, 7)]
    ev = exact_eval(co)
    print("exact_eval of 1/3 - 2z + 5z^2/7 at z = 0.25:", ev(0.25), "expected", (1 / 3 - 0.5 + 5 / 112, -2 + 5 / 14))
    for n, ell in ((5, 2), (9, 6)):
        for q in (0.0, 0.9, 0.99):
            mu = mu_of_q(n, ell, q)
            A, B = (ell + n) + (ell - 1) * mu * mu, 2 * ell + n - 1
            print(f"mu_of_q n={n} l={ell} q={q}: mu = {mu:.12g}, w(mu)^2 + q^2 - 1 = {(B * mu / A) ** 2 + q * q - 1:.2e}")
    syn = (lambda m, d, x: 64 * m ** 3 + 400 * x ** 2, lambda m, d, x: m + 15 * x)
    S = Setting(5, 4, 0.5, funcs=syn)
    t0 = time.time()
    rec = sample(S)
    print(f"sample() on a synthetic U = 64 m^3 + 400 x^2, H = m + 15 x (n = 5, l = 4, mu = 1/2), {time.time() - t0:.1f} s:")
    print("  ", {k: rec[k] for k in ("q", "delta_t", "P_true(0)", "P_true(1)", "min_psi1")})
    for eps in ("1/50", "1/200"):
        r = rec[f"eps {eps}"]
        print(f"   eps {eps}: sigma_design {r['sigma_design']:.4g};",
              ", ".join(f"{v} {dg}: {r[f'{v} {dg}']:.4g}" for v in ("z", "zeta") for dg in (DEGREES[0], 28, DEGREES[-1])))
    print("   qualify([rec]):", qualify([rec]))
    Sw = Setting(5, 4, 0.5, well=1e9, funcs=syn)
    print("synthetic setting with a well of depth 1e9: ", sample(Sw).get("breakdown", "no breakdown"))
    tab = tabulate(S)
    sol = riccati(S, list(GRID))
    print("slack() of the zero-energy P_true itself (B = 0 up to integration error): sigma =",
          slack(tab, lambda z: (sol[z][0], float("nan")))[0], "(None expected: P_z not supplied)")


if __name__ == "__main__":
    main()
