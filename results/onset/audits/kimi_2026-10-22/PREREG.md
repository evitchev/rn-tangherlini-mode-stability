# PREREG — my audit of the bh-modes exact onset (BHM-017)

*Auditor: Kimi. 2026-10-22.*

Brief: `results/onset/briefs/BRIEF_kimi_2026-10-22.md`, SHA-256
`318e709c00a91cb807dc4ef4652d73cba5101264ead256c2c0ba293f27ee81df` (verified against
`SEALED.sha256`).

## Anti-anchoring

Before opening `results/onset/RESULT.md`, anything under `results/onset/runs/`,
`REGISTRY.md` rows >= BHM-017, the lead's commit messages after `180824b`, `lean/`, or
`outbox/`, I will have on disk:

1. my own derivation of U_-(x; q) at ell = 2 from KI (5.63b) (already audited in my p3 audit:
   `bhm-p3-audit-2026-10-22/own/build.py`), specialised to the mu-parametrisation
   w = 7mu/(6+mu^2), 1+2m*delta = 7(6-mu^2)/(5(6+mu^2));
2. my own g(mu) := numerator of U_-(x_H; q(mu)) (rf arithmetic), its factorisation, the root
   count on [0,1] (my own Sturm), simplicity, sign checks g(0) < 0 < g(1);
3. my own minimal-polynomial computation for q_*^2 (resultant) and its irreducibility;
4. my own isolating intervals for mu_*, q_*^2, q_* and the comparison with the registered
   prediction q_* in [0.9730564367, 0.9730564368];
5. my own O2 proof: F(t, mu) >= 0 on [0,1] x [mu_*, 1] with equality only at (1, mu_*), via
   my own exact Bernstein verifier on the three regions of the corner argument (F > 0 on
   [0, 1-tau] x [mu_lo, 1]; F > 0 on [1-tau, 1] x [mu_c, 1]; F_t < 0 on [1-tau, 1] x
   [mu_lo, mu_c]), mu_lo < mu_* < mu_hi < mu_c rational;
6. O3 (sign of g), O4 (the KI (6.24) bracket), O5 (setting identities);
7. controls: a perturbed U_- coefficient (must fail my transcription check) and a moved onset
   (claimed root interval shifted by 1e-6: my Sturm count in the shifted interval must be 0);
8. the reproduction run of `kit/onset/run.sh` at `180824b`, exit code and log hash.

## Pre-committed verdict rule

Each of O1-O5 passes only on my own exact/rigorous computation. Overall PASS requires all of
O1-O5 plus a green reproduction of the kit's certificate content (the kit's verdict semantics
aside, its computed isolating intervals and positivity must agree with mine).
