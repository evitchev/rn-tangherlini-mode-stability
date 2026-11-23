"""check_transcription.py -- transcription checks for V_S- of S5 (ib-blind seat, phase 1).

Every check can fail. Each is also run against deliberate corruptions (tampers
T1-T4 of U_-) to show which parts of the formula it actually tests.
Nothing here decides the spectral question; C8 only evaluates the potential
at the horizon (sign change) and at extremality (inverse-square coefficient),
both stated as background in the brief.

Run: python3 -I check_transcription.py   (adds its own directory to sys.path)
"""
import os
import sys
import json
import time
import platform
import socket

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp  # noqa: E402
import ki_s5 as ki  # noqa: E402

n, m, d, x, y, K, z = ki.n, ki.m, ki.d, ki.x, ki.y, ki.K, ki.z
r, M, l, q, mu = sp.symbols('r M l q mu_T', positive=True)

RESULTS = {}


def is_zero(e):
    """Exact test: the numerator of the combined rational expression expands to 0."""
    num, _ = sp.fraction(sp.together(e))
    return sp.expand(num) == 0


def record(name, ok, info=''):
    RESULTS[name] = bool(ok)
    print(f'[{"PASS" if ok else "FAIL"}] {name} {info}', flush=True)


# ---------------------------------------------------------------------------
def C1(tamper=None):
    """Q = 0 (delta = 0) limit vs Paper I (3.2), (3.6), (3.7): general n, m, x, y, K.
    V_S-(delta=0) = f U_-/(64 r^2 H_-^2) must equal f Q_I/(16 r^2 H_I^2)."""
    U0 = ki.U_minus(d=0, tamper=tamper)
    H0 = ki.H_minus(d=0)
    ok_H = is_zero(H0 - ki.H_I())
    ok_U = is_zero(U0 - 4 * ki.Q_I())
    return ok_H and ok_U


def C2(tamper=None):
    """n = 2, K = 1, lambda = 0, Q = 0: V_S- vs the Zerilli potential
    V_Z = (1-2M/r) [2L^2(L+1) r^3 + 6 L^2 M r^2 + 18 L M^2 r + 18 M^3] / (r^3 (L r + 3M)^2),
    L = (l-1)(l+2)/2 = m/2."""
    L = m / 2
    xx = 2 * M / r
    f = 1 - xx
    V = ki.V_S('-', r, n=2, m=m, d=0, x=xx, y=0, K=1, f=f, tamper=tamper)
    VZ = f * (2 * L**2 * (L + 1) * r**3 + 6 * L**2 * M * r**2 + 18 * L * M**2 * r + 18 * M**3) / (
        r**3 * (L * r + 3 * M)**2)
    return is_zero(V - VZ)


def C3(tamper=None):
    """n = 2, K = 1, lambda = 0, Q != 0: V_S- and V_S+ vs Chandrasekhar's polar
    Reissner-Nordstrom potentials V_i^(+) = q_j dF_j/dr_* + q_j^2 F_j^2 + kappa F_j,
    F_j = Delta/(r^3 (mu^2 r + q_j)), kappa = mu^2 (mu^2 + 2), mu^2 = (l-1)(l+2) = m,
    q_{1,2} = 3M +- sqrt(9M^2 + 4 Q^2 mu^2)  (from memory of MTBH ch. 5; S5 itself
    states V_S+ = V_1^(+), V_S- = V_2^(+) for n = 2).
    With (5.65) at n = 2, Q^2 = 9 M^2 delta(1 + m delta): q1 = 6M(1 + m delta), q2 = -6 M m delta."""
    Q2 = 9 * M**2 * d * (1 + m * d)
    xx = 2 * M / r
    f = 1 - xx + Q2 / r**2
    Delta = r**2 * f
    q1 = 6 * M * (1 + m * d)
    q2 = -6 * M * m * d
    # sanity of the roots: q1 + q2 = 6M, q1 q2 = -4 Q^2 m
    ok_roots = is_zero(q1 + q2 - 6 * M) and is_zero(q1 * q2 + 4 * Q2 * m)
    kappa = m * (m + 2)

    def Vc(qj):
        F = Delta / (r**3 * (m * r + qj))
        return qj * f * sp.diff(F, r) + qj**2 * F**2 + kappa * F

    Vm = ki.V_S('-', r, n=2, m=m, d=d, x=xx, y=0, K=1, f=f, tamper=tamper)
    Vp = ki.V_S('+', r, n=2, m=m, d=d, x=xx, y=0, K=1, f=f)
    ok_m = is_zero(Vm - Vc(q1))
    ok_p = is_zero(Vp - Vc(q2))
    return ok_roots and ok_m and ok_p


def C4(tamper=None):
    """Involution mu_S5 -> -mu_S5, i.e. delta -> delta' = -(1 + m delta)/m, which fixes
    Q^2 = (n+1)^2 M^2 delta(1 + m delta) (5.65) and exchanges the two roots of (5.58).
    The +/- formulas were typeset separately in S5; consistency requires
    H_-(delta') = m H_+(delta) and U_-(delta') = m^2 U_+(delta), so V_S-(delta') = V_S+(delta).
    General n, m, x, y, K."""
    dp = -(1 + m * d) / m
    ok_Q = is_zero(dp * (1 + m * dp) - d * (1 + m * d))
    ok_H = is_zero(ki.H_minus(d=dp) - m * ki.H_plus())
    ok_U = is_zero(ki.U_minus(d=dp, tamper=tamper) - m**2 * ki.U_plus())
    return ok_Q and ok_H and ok_U


def C5():
    """(5.66) H = H_+ H_- with (5.38) H = m + n(n+1)x/2 - n^2 z and z = Q^2/r^(2n-2)
    = (n+1)^2 delta(1 + m delta) x^2/4 by (5.65) and (5.40)."""
    zz = (n + 1)**2 * d * (1 + m * d) * x**2 / 4
    return is_zero(ki.H_plus() * ki.H_minus() - ki.H_S5(z=zz))


def C6(tamper=None):
    """x -> 0 (r -> infinity at lambda = 0, K = 1): r^2 V_S- -> U_-(0)/(64 H_-(0)^2) must be the
    free (n+2)-dimensional centrifugal value ((2l + n - 1)^2 - 1)/4 = k^2 + n(n-2)/4,
    with m = (l-1)(l+n); for every delta. n = 5, l = 2: 63/4."""
    mm = (l - 1) * (l + n)
    lim = ki.U_minus(m=mm, x=0, y=0, K=1, tamper=tamper) / (64 * ki.H_minus(m=mm, x=0)**2)
    target = ((2 * l + n - 1)**2 - 1) / 4
    ok = is_zero(lim - target)
    lim52 = sp.simplify(lim.subs({n: 5, l: 2}))
    return ok and (lim52 == sp.Rational(63, 4)), lim52


# ---------------------------------------------------------------------------
def setting_n5_l2():
    """Brief / TARGET_HD sec. 1 setting at n = 5, l = 2, in the rational parameter mu_T."""
    nn, ll = 5, 2
    mm = (ll - 1) * (ll + nn)                      # 7
    A = (ll + nn) + (ll - 1) * mu**2               # 7 + mu^2
    B = 2 * ll + nn - 1                            # 8
    w = B * mu / A                                 # sqrt(1 - q^2)
    s = B * ((ll + nn) - (ll - 1) * mu**2) / ((nn + 1) * A)   # 1 + 2 m delta
    q2 = 1 - w**2
    dl = (s - 1) / (2 * mm)
    xH = 2 / (1 + w)
    return dict(n=nn, l=ll, m=mm, A=A, B=B, w=w, s=s, q2=q2, delta=dl, xH=xH)


def C7():
    """TARGET_HD sec. 1 items, checked against S5 and by algebra."""
    out = {}
    # (a) m = (l-1)(l+n) = k^2 - n with k^2 = l(l+n-1) (S5 (2.3), (5.39), K = 1)
    out['a_m'] = is_zero((l - 1) * (l + n) - (l * (l + n - 1) - n))
    # (b) z = Q^2/r^(2n-2) = q^2 x^2/4 with q = |Q|/M, x = 2M/r^(n-1): f = 1 - x + q^2 x^2/4
    rr, MM, qq, nn_ = sp.symbols('rr MM qq nn_', positive=True)
    xx = 2 * MM / rr**(nn_ - 1)
    zz = (qq * MM)**2 / rr**(2 * nn_ - 2)
    out['b_z'] = sp.simplify(zz - qq**2 * xx**2 / 4) == 0
    # (c) roots of f = 1 - x + q^2 x^2/4 are x = 2/(1 +- w), w = sqrt(1-q^2); outer horizon = smaller x
    w = sp.symbols('w', positive=True)
    fq = 1 - x + (1 - w**2) * x**2 / 4
    out['c_roots'] = is_zero(fq.subs(x, 2 / (1 + w))) and is_zero(fq.subs(x, 2 / (1 - w)))
    # (d) (5.58)+(5.60): (1 + 2 m delta)^2 = 1 + 4 m q^2/(n+1)^2, consistent with (5.65)
    out['d_delta'] = is_zero((1 + 2 * m * d)**2 - (1 + 4 * m * d * (1 + m * d)))
    # (e) rational parametrisation, general n, l
    mm = (l - 1) * (l + n)
    A = (l + n) + (l - 1) * mu**2
    B = 2 * l + n - 1
    wT = B * mu / A
    sT = B * ((l + n) - (l - 1) * mu**2) / ((n + 1) * A)
    out['e_B2'] = is_zero(B**2 - ((n + 1)**2 + 4 * mm))
    out['e_s2'] = is_zero(sT**2 - (1 + 4 * mm * (1 - wT**2) / (n + 1)**2))
    out['e_ends'] = (sp.simplify(wT.subs(mu, 1)) == 1) and (sp.simplify(wT.subs(mu, 0)) == 0)
    # (f) n = 5, l = 2: w increasing on [0,1]; s >= 1 on [0,1] (so delta >= 0 and mu_S5 > 0)
    S = setting_n5_l2()
    dw = sp.factor(sp.diff(S['w'], mu))          # 8(7 - mu^2)/(7 + mu^2)^2
    s_minus_1 = sp.factor(S['s'] - 1)            # (7 - 7 mu^2)... /(6(7+mu^2))
    out['f_dw'] = str(dw)
    out['f_s_minus_1'] = str(s_minus_1)
    num_dw = sp.fraction(sp.together(dw))[0]
    num_s1 = sp.fraction(sp.together(s_minus_1))[0]
    ok_f = (sp.Poly(sp.expand(num_dw), mu).count_roots(0, 1) == 0 and num_dw.subs(mu, sp.Rational(1, 2)) > 0
            and sp.Poly(sp.expand(num_s1), mu).count_roots(0, sp.Rational(999999, 1000000)) == 0
            and num_s1.subs(mu, sp.Rational(1, 2)) > 0)
    out['f_monotone_and_delta_nonneg'] = bool(ok_f)
    ok = all(v for k, v in out.items() if isinstance(v, bool))
    return ok, out


def C8(tamper=None, verbose=True):
    """n = 5, l = 2 background statements of the brief (transcription agreement only):
    (a) the horizon value U_-(x_H) changes sign at q ~ 0.9497;
    (b) at q = 1 the inverse-square coefficient of V in r_* is exactly -1/4."""
    S = setting_n5_l2()
    mm, nn = S['m'], S['n']
    UH = ki.U_minus(n=nn, m=mm, d=S['delta'], x=S['xH'], y=0, K=1, tamper=tamper)
    num, den = sp.fraction(sp.together(UH))
    P = sp.Poly(sp.expand(num), mu)
    roots = [rt for rt in P.real_roots() if 0 < rt < 1]
    qs = [sp.sqrt(1 - S['w'].subs(mu, rt)**2) for rt in roots]
    qnum = [sp.N(qq, 15) for qq in qs]
    if verbose:
        print('   C8a: roots mu_T in (0,1) of numerator of U_-(x_H):', [sp.N(rt, 15) for rt in roots])
        print('   C8a: corresponding q:', qnum)
        print('   C8a: sign of den on (0,1) at mu=1/2:', sp.sign(den.subs(mu, sp.Rational(1, 2))))
    ok_a = (len(qnum) == 1) and abs(float(qnum[0]) - 0.9497) < 0.0001   # brief: 'q ~ 0.9497' (rounded or truncated)
    # (b) extremal: q = 1 <=> mu_T = 0; x_H = 2, delta = 1/42; units r_H = 1 => 2M = x_H = 2
    d0 = S['delta'].subs(mu, 0)
    xH0 = S['xH'].subs(mu, 0)
    WH = ki.U_minus(n=nn, m=mm, d=d0, x=xH0, y=0, K=1, tamper=tamper) / (64 * ki.H_minus(n=nn, m=mm, d=d0, x=xH0)**2)
    rr = sp.symbols('rr', positive=True)
    f_r = 1 - xH0 / rr**(nn - 1) + (xH0 / rr**(nn - 1))**2 / 4     # q = 1
    a = sp.simplify(sp.diff(f_r, rr, 2).subs(rr, 1) / 2)
    f1 = sp.simplify(sp.diff(f_r, rr).subs(rr, 1))
    kappa = sp.simplify(WH / a)
    if verbose:
        print(f'   C8b: delta(q=1) = {d0}, x_H = {xH0}, f(1) = {sp.simplify(f_r.subs(rr, 1))}, '
              f"f'(1) = {f1}, a = f''(1)/2 = {a}, W_H = (V/f)_H = {WH}, kappa = W_H/a = {kappa}")
    ok_b = (kappa == sp.Rational(-1, 4))
    return ok_a and ok_b, dict(q_sign_change=[str(v) for v in qnum], kappa=str(kappa))


def C9():
    """METHOD.md Lemma 2 identity (checked, since I will use it in phase 2), generic f, W, P:
    with z = 1 - 1/rho, beta = (1-z) P(z), S = -f beta, ' = d/dr_* = f d/drho:
      V + S' - S^2 = (f/rho^2) [rho^2 W - (1-z) f_z P - f(-P + (1-z) P_z + P^2)],  V = f W.
    Also the endpoint values at n = 5, l = 2: N(1) = 64 m^2 (m + 35/4 + P(1) - P(1)^2) and
    the admissible window -7/2 < P(1) < 9/2."""
    rho = sp.symbols('rho', positive=True)
    p0, p1_, F0, F1, W0 = sp.symbols('p0 p1_ F0 F1 W0')   # P(z), P'(z), f(rho), f'(rho), W(rho)
    zz = 1 - 1 / rho
    beta = p0 / rho                                        # (1-z) P
    dbeta = p1_ / rho**3 - p0 / rho**2                     # d/drho [P(z(rho))/rho], dz/drho = 1/rho^2
    S = -F0 * beta
    dS = -F1 * beta - F0 * dbeta
    lhs = F0 * W0 + F0 * dS - S**2                         # V + S' - S^2 with ' = f d/drho
    rhs = (F0 / rho**2) * (rho**2 * W0 - (1 - zz) * (rho**2 * F1) * p0
                           - F0 * (-p0 + (1 - zz) * p1_ + p0**2))
    ok_sym = is_zero(lhs - rhs)
    # concrete instance with sympy's own differentiation (no hand chain rule)
    Pc = lambda t: 3 - 2 * t + 5 * t**3
    Fc = 1 - 2 / rho**4 + sp.Rational(1, 3) / rho**8
    Wc = (7 + 1 / rho**4) / rho**2
    betac = (1 - zz) * Pc(zz)
    Sc = -Fc * betac
    lhs_c = Fc * Wc + Fc * sp.diff(Sc, rho) - Sc**2
    t = sp.symbols('t')
    Fz_c = sp.diff(Fc.subs(rho, 1 / (1 - t)), t).subs(t, zz)
    Pz_c = sp.diff(Pc(t), t).subs(t, zz)
    rhs_c = (Fc / rho**2) * (rho**2 * Wc - (1 - zz) * Fz_c * Pc(zz) - Fc * (-Pc(zz) + (1 - zz) * Pz_c + Pc(zz)**2))
    ok_con = is_zero(lhs_c - rhs_c)
    ok_id = ok_sym and ok_con
    print('   C9: Lemma 2 identity symbolic:', ok_sym, '; concrete instance:', ok_con)
    # endpoint at z = 1 (x = 0, f = 1, (1-z) f_z -> 0) for n = 5, l = 2, any delta
    p1 = sp.symbols('p1')
    mm = 7
    N1 = ki.U_minus(n=5, m=mm, d=d, x=0, y=0, K=1) - 64 * ki.H_minus(n=5, m=mm, d=d, x=0)**2 * (-p1 + p1**2)
    target = 64 * mm**2 * (mm + sp.Rational(35, 4) + p1 - p1**2)
    ok_N1 = is_zero(N1 - target)
    roots = sp.solve(sp.Eq(target, 0), p1)
    print('   C9: N(1) =', sp.factor(N1), '; roots in P(1):', roots)
    return ok_id and ok_N1 and sorted(roots) == [sp.Rational(-7, 2), sp.Rational(9, 2)]


def explicit_n5_l2():
    """Print the n = 5, l = 2, y = 0, K = 1 forms used downstream."""
    mm = 7
    Hm = sp.expand(ki.H_minus(n=5, m=mm, d=d, x=x))
    Um = sp.Poly(sp.expand(ki.U_minus(n=5, m=mm, d=d, x=x, y=0, K=1)), x)
    print('   H_- (n=5,l=2) =', Hm)
    for (k,), c in sorted(Um.terms(), reverse=True):
        print(f'   U_- coefficient of x^{k}: {sp.factor(c)}   [= {sp.expand(c)}]')
    S = setting_n5_l2()
    print('   delta(mu_T) =', sp.factor(S['delta']), '; 1 + m delta =', sp.factor(1 + mm * S['delta']))
    print('   q^2(mu_T) =', sp.factor(S['q2']), '; x_H(mu_T) =', sp.factor(S['xH']))
    # spot values (exact) at q = 0 (mu_T = 1) and q = 1 (mu_T = 0)
    for mv in (1, 0):
        print(f'   mu_T = {mv}: q^2 = {S["q2"].subs(mu, mv)}, delta = {S["delta"].subs(mu, mv)}, '
              f'x_H = {S["xH"].subs(mu, mv)}')
    return Hm, Um


def main():
    t0 = time.time()
    print('host', socket.gethostname(), '| python', platform.python_version(), '| sympy', sp.__version__)
    print('time_utc', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    print('== transcription checks (no tamper) ==')
    record('C1 Q=0 limit vs Paper I (general n,m,x,y,K)', C1())
    record('C2 n=2 Q=0 vs Zerilli', C2())
    record('C3 n=2 charged vs Chandrasekhar V_2^(+), V_1^(+)', C3())
    record('C4 involution U_-(delta\') = m^2 U_+(delta), H_-(delta\') = m H_+(delta)', C4())
    record('C5 (5.66) H_+ H_- = H of (5.38) with z from (5.65)', C5())
    ok6, lim52 = C6()
    record('C6 x->0: r^2 V -> ((2l+n-1)^2-1)/4; n=5,l=2 ->', ok6, str(lim52))
    ok7, out7 = C7()
    record('C7 TARGET_HD sec.1 setting items', ok7, json.dumps(out7))
    ok8, out8 = C8()
    record('C8 brief background (q~0.9497 sign change; kappa=-1/4 at q=1)', ok8, json.dumps(out8))
    record('C9 METHOD.md Lemma 2 identity + N(1) window', C9())
    print('== explicit n=5, l=2 forms ==')
    explicit_n5_l2()
    print('== negative drills: tampered U_- must be caught ==')
    drills = {}
    for T in ('T1_x3_sign', 'T2_x4_power', 'T3_const', 'T4_x2_delta_sq'):
        row = {}
        row['C1'] = C1(T)
        row['C2'] = C2(T)
        row['C3'] = C3(T)
        row['C4'] = C4(T)
        row['C6'] = C6(T)[0]
        row['C8'] = C8(T, verbose=False)[0]
        caught = [k for k, v in row.items() if not v]
        drills[T] = dict(results=row, caught_by=caught)
        print(f'   {T}: ' + ', '.join(f'{k}={"pass" if v else "FAIL"}' for k, v in row.items())
              + f'  -> caught by {caught}')
    all_caught = all(len(v['caught_by']) > 0 for v in drills.values())
    record('D  every tamper caught by at least one check', all_caught)
    print('== summary ==')
    print(json.dumps(dict(results=RESULTS, drills=drills), indent=1, default=str))
    print('elapsed_s', round(time.time() - t0, 1))
    print('ALL_PASS' if all(RESULTS.values()) else 'SOME_FAIL')


if __name__ == '__main__':
    main()
