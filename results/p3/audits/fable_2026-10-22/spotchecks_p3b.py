"""spotchecks_p3b.py -- p3 audit: item (3b) of spotchecks_p3.py re-run with the corrected test constant.  In run 1 the monotonicity
test of s(mu) at l = 2 used the constant 84 where the derivative gives ds/dmu = -168 mu / (5 (6 + mu^2)^2); the parametrisation
was never in doubt, the test constant was.  Here every quantity is printed."""
import sympy as sp
mu = sp.symbols("mu")
A = 6 + mu ** 2
w2 = 7 * mu / A
s2 = 7 * (6 - mu ** 2) / (5 * A)
dw = sp.simplify(sp.diff(w2, mu))
ds = sp.simplify(sp.diff(s2, mu))
print(f"w(mu) = {w2}: w(0) = {w2.subs(mu, 0)}, w(1) = {w2.subs(mu, 1)}, dw/dmu = {dw} (> 0 on [0, 1): numerator 7(6 - mu^2) > 0)")
print(f"s(mu) = {s2}: s(1) = {s2.subs(mu, 1)}, s(0) = {s2.subs(mu, 0)}, ds/dmu = {ds} (< 0 on (0, 1])")
ok = (w2.subs(mu, 0) == 0 and w2.subs(mu, 1) == 1 and s2.subs(mu, 1) == 1 and s2.subs(mu, 0) == sp.Rational(7, 5)
      and sp.simplify(dw * A ** 2 - 7 * (6 - mu ** 2)) == 0 and sp.simplify(ds * 5 * A ** 2 + 168 * mu) == 0)
q2 = sp.simplify(1 - w2 ** 2)
print(f"q^2(mu) = {sp.factor(q2)}: q(1) = {q2.subs(mu, 1)}, q(0) = {q2.subs(mu, 0)}; delta = (s - 1)/12 = {sp.factor((s2 - 1) / 12)} >= 0 on [0, 1]")
print(f"(3b) at l = 2: w increasing from 0 to 1, s decreasing from 7/5 to 1 (so delta >= 0 and q decreases from 1 to 0): {ok}")
raise SystemExit(0 if ok else 1)
