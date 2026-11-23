"""extremal_kappa.py -- observation only (not a pass/fail check): the inverse-square coefficient
kappa(n, l) = W_H / a of V_S- at q = 1 (extremal), from my S5 transcription, for general n, l.
At q = 1: x_H = 2, 1 + 2 m delta = B/(n+1) with B = 2l + n - 1, so delta = 1/((l+n)(n+1));
f = (1 - rho^-(n-1))^2 ~ (n-1)^2 (rho-1)^2, a = (n-1)^2; W_H = U_-(2)/(64 H_-(2)^2) (r_H = 1)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
import ki_s5 as ki
n, l = sp.symbols('n l', positive=True)
m = (l - 1) * (l + n)
d = 1 / ((l + n) * (n + 1))
assert sp.simplify((1 + 2 * m * d) - (2 * l + n - 1) / (n + 1)) == 0
WH = ki.U_minus(n=n, m=m, d=d, x=2, y=0, K=1) / (64 * ki.H_minus(n=n, m=m, d=d, x=2)**2)
kappa = sp.factor(sp.simplify(WH / (n - 1)**2))
print('kappa(n,l) =', kappa)
print('kappa + 1/4 =', sp.factor(sp.simplify(kappa + sp.Rational(1, 4))))
for nn in range(2, 10):
    print(nn, [sp.simplify(kappa.subs({n: nn, l: ll})) for ll in range(2, 6)])
