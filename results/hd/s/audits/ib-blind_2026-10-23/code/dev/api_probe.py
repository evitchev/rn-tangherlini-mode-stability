import time, flint, mpmath as mp
from flint import fmpq, fmpz, fmpq_poly, fmpq_mat, acb, arb, ctx
p = fmpq_poly([1, -3, 2]); q = fmpq_poly([0, 1, 1])
print('compose p(q):', p(q), '| p(1/3):', p(fmpq(1, 3)), '| deriv:', p.derivative(), '| coeffs:', p.coeffs(), '| deg', p.degree())
print('p**3', p**3, '| p*fmpq(1,2)', p * fmpq(1, 2))
M = fmpq_mat(2, 3, [1, 2, 3, fmpq(1, 2), 0, -1]); N = fmpq_mat(3, 2, [1, 0, 0, 1, 1, 1])
print('M*N', M * N, '| M.T', M.transpose(), '| entry', M[1, 0], type(M[1, 0]), M.nrows(), M.ncols())
print('fmpq cmp', fmpq(1, 3) > 0, fmpq(-1, 3) < 0, fmpq(1,3).p, fmpq(1,3).q)
ctx.prec = 128
f = lambda t, analytic: (t*t + 1).inv() if True else None
v = acb.integral(lambda t, a: 1/(1 + t*t), 0, 1)
print('int 1/(1+t^2) on [0,1] =', v, ' pi/4=', arb.pi()/4)
print('acb ops: sqrt', acb(2).sqrt(), ' mid/rad', v.real.mid(), v.real.rad())
# mpmath odefun timing at q = 0.9 (out of band, X1)
mp.mp.dps = 30
t0 = time.time()
F = mp.odefun(lambda x, y: [y[1], -y[0]], 0, [mp.mpf(0), mp.mpf(1)])
print('odefun sin(5) err', F(5)[0] - mp.sin(5), 'time', time.time() - t0)
