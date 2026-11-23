"""spotchecks_p3.py -- Fable's p3 pencil audit (bh-modes BHM-022): machine spot checks of the hand verifications.
Nothing from code/p3 or code/onset is imported; the identities are re-derived in sympy / Fractions.  Exit 0 iff all pass."""
import random
from fractions import Fraction as Fr
from math import comb
import sympy as sp

random.seed(20261022)
FAIL = []
z, rho, P0, eps = sp.symbols("z rho P0 epsilon")
f = sp.Function("f")
Pz = sp.Function("P")
W = sp.Function("W")

# (1) Lemma 2, first form and change of variable, with generic f(rho) and P(z): V-tilde = f N / (64 rho^2 H^2) where
#     V = f W, W = U/(64 rho^2 H^2); beta = (1 - z) P(z) = P/rho; S = -f beta; V-tilde = V + f d/drho(S) - S^2.
zr = 1 - 1 / rho                                   # z as a function of rho
beta = Pz(zr) / rho
S = -f(rho) * beta
Vt = f(rho) * W(rho) + f(rho) * sp.diff(S, rho) - S ** 2
# METHOD's claim: rho^2 Vt / f = rho^2 W - [ (1 - z) f_z P + f(-P + (1 - z) P_z + P^2) ]  with f_z = f'(rho) rho^2 (since dz/drho = 1/rho^2)
fz = sp.diff(f(rho), rho) * rho ** 2                                  # f_z = f' / (dz/drho)
Pz_z = sp.diff(Pz(zr), rho) * rho ** 2                                 # P_z = dP/drho / (dz/drho)
claim = rho ** 2 * W(rho) - ((1 - zr) * fz * Pz(zr) + f(rho) * (-Pz(zr) + (1 - zr) * Pz_z + Pz(zr) ** 2))
ok = sp.simplify(rho ** 2 * Vt / f(rho) - claim) == 0
print(f"(1) Lemma 2: rho^2 V-tilde / f = rho^2 W - [(1-z) f_z P + f(-P + (1-z) P_z + P^2)] for generic f(rho), P(z) (symbolic): {ok}")
FAIL += [] if ok else ["L2"]

# (2) the f factorisation and kappa^3: f = 1 - x + q^2 x^2 / 4 = (1 - x/x_H)(1 - x/x_-) with x_H = 2/(1+w), x_- = 2/(1-w), w^2 = 1 - q^2;
#     kappa^3 := x_H / x_- = (1 - w)/(1 + w); x = x_H (1 - z)^3 gives f = (1 - (1-z)^3)(1 - kappa^3 (1-z)^3); f_z(0) = 3 (1 - kappa^3) > 0 for q < 1
w, x = sp.symbols("w x", positive=True)
q2 = 1 - w ** 2
xH, xm = 2 / (1 + w), 2 / (1 - w)
ok = sp.simplify(1 - x + q2 * x ** 2 / 4 - (1 - x / xH) * (1 - x / xm)) == 0
k3 = sp.simplify(xH / xm)
ok2 = sp.simplify(k3 - (1 - w) / (1 + w)) == 0
fzz = (1 - (1 - z) ** 3) * (1 - k3 * (1 - z) ** 3)
ok3 = sp.simplify(fzz.subs(z, 0)) == 0 and sp.simplify(sp.diff(fzz, z).subs(z, 0) - 3 * (1 - k3)) == 0
print(f"(2) f = (1 - x/x_H)(1 - x/x_-): {ok}; kappa^3 = x_H/x_- = (1-w)/(1+w): {ok2}; f(z=0) = 0 and f_z(0) = 3(1 - kappa^3) (> 0 iff w > 0 iff q < 1): {ok3}")
FAIL += [] if (ok and ok2 and ok3) else ["f factorisation"]

# (3) the rational parametrisation of results/onset/PREREG.md section 1 for general l: s^2 = 1 + 4 m q^2 / 25 identically, with
#     A = (l+4) + (l-1) mu^2, w = (2l+3) mu / A, s = (2l+3)((l+4) - (l-1) mu^2)/(5A), m = (l-1)(l+4); monotonicity on [0, 1] at l = 2
l, mu = sp.symbols("l mu")
A = (l + 4) + (l - 1) * mu ** 2
wmu = (2 * l + 3) * mu / A
s = (2 * l + 3) * ((l + 4) - (l - 1) * mu ** 2) / (5 * A)
m = (l - 1) * (l + 4)
ok = sp.simplify(s ** 2 - (1 + 4 * m * (1 - wmu ** 2) / 25)) == 0
w2, s2 = wmu.subs(l, 2), s.subs(l, 2)
ok2 = (w2.subs(mu, 0) == 0 and w2.subs(mu, 1) == 1 and s2.subs(mu, 1) == 1 and s2.subs(mu, 0) == sp.Rational(7, 5)
       and sp.simplify(sp.diff(w2, mu) * (6 + mu ** 2) ** 2 - 7 * (6 - mu ** 2)) == 0 and sp.simplify(sp.diff(s2, mu) * 5 * (6 + mu ** 2) ** 2 + 84 * mu) == 0)
print(f"(3) parametrisation: s^2 = 1 + 4 m q^2/25 identically in (l, mu): {ok}; at l = 2: w(0) = 0, w(1) = 1, s(1) = 1, s(0) = 7/5, w increasing and s decreasing on [0, 1] (so delta >= 0, q decreasing from 1 to 0): {ok2}")
FAIL += [] if (ok and ok2) else ["parametrisation"]

# (4) N(1) and N(0): with U(x) = 64 m^3 + 384 m^2 + O(x) and H(0) = m: N(1) = 64 m^2 (m + 6 - P(1)^2 + P(1)); N(0) = U(x_H) - 64 H(x_H)^2 f_z(0) P(0)
mm, P1, UH, HH, fz0 = sp.symbols("m P1 U_H H_H f_z0")
N1 = (64 * mm ** 3 + 384 * mm ** 2) - 64 * mm ** 2 * (0 + 1 * (-P1 + 0 + P1 ** 2))
ok = sp.simplify(N1 - 64 * mm ** 2 * (mm + 6 - P1 ** 2 + P1)) == 0
ok2 = sp.solve(sp.Eq(6 + 6 - P1 ** 2 + P1, 0), P1) == [-3, 4]
print(f"(4) N(1) = 64 m^2 (m + 6 - P(1)^2 + P(1)) given f(1) = 1, (1-z) f_z -> 0, U(0) = 64 m^3 + 384 m^2, H(0) = m: {ok}; for m = 6 positive iff -3 < P(1) < 4: {ok2}; "
      f"N(0) = U(x_H) - 64 H(x_H)^2 f_z(0) P(0) since f(0) = 0 (immediate)")
FAIL += [] if (ok and ok2) else ["N endpoints"]

# (5) the remark's epsilon identity: N(P_true - eps) = 64 H^2 eps [(1-z) f_z + f (2 P_true - 1 - eps)] when N(P_true) = 0; (1-z) f_z = rho f'
Pt, fsym, fzs, Hs, Us = sp.symbols("P_true f f_z H U")
Ptz = sp.symbols("P_true_z")
def Nof(Pv, Pvz):
    return Us - 64 * Hs ** 2 * ((1 - z) * fzs * Pv + fsym * (-Pv + (1 - z) * Pvz + Pv ** 2))
diff_ = sp.expand(Nof(Pt - eps, Ptz) - Nof(Pt, Ptz))
ok = sp.simplify(diff_ - 64 * Hs ** 2 * eps * ((1 - z) * fzs + fsym * (2 * Pt - 1 - eps))) == 0
print(f"(5) remark: N(P_true - eps) - N(P_true) = 64 H^2 eps [(1-z) f_z + f(2 P_true - 1 - eps)] (symbolic), and rho f' = (1-z) f_z: {ok}")
FAIL += [] if ok else ["eps identity"]

# (6) N_times_L's algebra: with U = Un/Ud, H = Hn/Hd, f = fn/fd (Ud, Hd, fd free of z), N * (Ud Hd^2 fd) = Un Hd^2 fd - 64 Hn^2 Ud [(1-z) fn_z P + fn(-P + (1-z) P_z + P^2)],
#     and with N' = N - 64 H^2 E:  N' L = N L - 64 Hn^2 Ud fd E
Un, Ud, Hn, Hd, fd, E = sp.symbols("Un Ud Hn Hd fd E")
fn = sp.Function("fn")(z)
Pp = sp.Function("Pp")(z)
Nfull = Un / Ud - 64 * (Hn / Hd) ** 2 * ((1 - z) * sp.diff(fn / fd, z) * Pp + (fn / fd) * (-Pp + (1 - z) * sp.diff(Pp, z) + Pp ** 2))
L = Ud * Hd ** 2 * fd
code = Un * Hd ** 2 * fd - 64 * Hn ** 2 * Ud * ((1 - z) * sp.diff(fn, z) * Pp + fn * (-Pp + (1 - z) * sp.diff(Pp, z) + Pp ** 2))
ok = sp.simplify(Nfull * L - code) == 0
ok2 = sp.simplify((Nfull - 64 * (Hn / Hd) ** 2 * E) * L - (code - 64 * Hn ** 2 * Ud * fd * E)) == 0
print(f"(6) N_times_L: N L = Un Hd^2 fd - 64 Hn^2 Ud br: {ok}; with extra E: N' L = ... - 64 Hn^2 Ud (br + E fd): {ok2}")
FAIL += [] if (ok and ok2) else ["N_times_L"]

# (7) the Bernstein conversion formula b_k = sum_{i<=k} C(k,i)/C(d,i) a_i (power basis on [0,1] -> Bernstein), the affine map, and the
#     tensor-product version, re-implemented in Fractions and tested against direct evaluation at random points (p = sum b_k B_{k,d})
def to_bern(a, d):
    return [sum(Fr(comb(k, i), comb(d, i)) * a[i] for i in range(k + 1)) for k in range(d + 1)]
def bern_basis(k, d, u):
    return comb(d, k) * u ** k * (1 - u) ** (d - k)
def affine(coeffs, a, h):
    # coefficients of p(a + h u): expand with sympy exactly
    uu = sp.symbols("uu")
    pol = sp.Poly(sum(sp.Rational(c.numerator, c.denominator) * (sp.Rational(a.numerator, a.denominator) + sp.Rational(h.numerator, h.denominator) * uu) ** i for i, c in enumerate(coeffs)), uu)
    cs = [Fr(int(c.p), int(c.q)) for c in reversed(pol.all_coeffs())]
    return cs + [Fr(0)] * (len(coeffs) - len(cs))
ok = True
for trial in range(20):
    d = random.randint(1, 7)
    a = [Fr(random.randint(-9, 9), random.randint(1, 9)) for _ in range(d + 1)]
    t0 = Fr(random.randint(-5, 5), random.randint(1, 7)); t1 = t0 + Fr(random.randint(1, 9), random.randint(1, 7))
    b = to_bern(affine(a, t0, t1 - t0), d)
    for _ in range(5):
        u = Fr(random.randint(0, 1000), 1000)
        t = t0 + (t1 - t0) * u
        direct = sum(ai * t ** i for i, ai in enumerate(a))
        viab = sum(bk * bern_basis(k, d, u) for k, bk in enumerate(b))
        if direct != viab:
            ok = False
    # enclosure property on the box [t0, t1]: min b <= p(t) <= max b at the sample points
    for _ in range(5):
        u = Fr(random.randint(0, 1000), 1000)
        t = t0 + (t1 - t0) * u
        v = sum(ai * t ** i for i, ai in enumerate(a))
        if not (min(b) <= v <= max(b)):
            ok = False
    # corners equal the end coefficients
    if b[0] != sum(ai * t0 ** i for i, ai in enumerate(a)) or b[d] != sum(ai * t1 ** i for i, ai in enumerate(a)):
        ok = False
# tensor product in two variables
ok2 = True
for trial in range(10):
    dt, dm = random.randint(1, 4), random.randint(1, 3)
    terms = {(i, j): Fr(random.randint(-9, 9), random.randint(1, 5)) for i in range(dt + 1) for j in range(dm + 1)}
    t0, t1, m0, m1 = Fr(0), Fr(1, 2), Fr(1, 3), Fr(2, 3)
    cols = [to_bern(affine([terms[(i, j)] for i in range(dt + 1)], t0, t1 - t0), dt) for j in range(dm + 1)]
    bb = [to_bern(affine([cols[j][k] for j in range(dm + 1)], m0, m1 - m0), dm) for k in range(dt + 1)]
    for _ in range(5):
        u, v = Fr(random.randint(0, 100), 100), Fr(random.randint(0, 100), 100)
        t, mv = t0 + (t1 - t0) * u, m0 + (m1 - m0) * v
        direct = sum(c * t ** i * mv ** j for (i, j), c in terms.items())
        viab = sum(bb[k][jj] * bern_basis(k, dt, u) * bern_basis(jj, dm, v) for k in range(dt + 1) for jj in range(dm + 1))
        if direct != viab or not (min(min(r) for r in bb) <= direct <= max(max(r) for r in bb)):
            ok2 = False
print(f"(7) Bernstein conversion b_k = sum C(k,i)/C(d,i) a_i after the affine map (1-D, 20 random polynomials; reconstruction, enclosure, corners): {ok}; tensor-product 2-D version (10 random): {ok2}")
FAIL += [] if (ok and ok2) else ["Bernstein"]
print(f"==== p3 spot checks {'PASS' if not FAIL else 'FAIL'}: {FAIL}")
raise SystemExit(0 if not FAIL else 1)
