# PREREG — my audit of bh-modes A2-E and A2-S (BHM-096, BHM-100)

*Auditor: Kimi. 2026-10-25.*

Brief: `results/a2/briefs/BRIEF_kimi_2026-10-24.md`, SHA-256
`6a818337dbfccc19f31b775a930dbe7fa84f01af8f8274987346e3935531c86f` (verified against
`SEALED.sha256`).

## Anti-anchoring (allow-list regime)

Until my own checks are on disk, I read only: the brief; the files in its first table
(TARGET.md, TARGET_A2.md, TARGET_A2_ADDENDUM_1.md, results/onset/PREREG.md,
results/a1/PREREG.md, results/a2/elementary/PREREG.md, results/a2/s/PREREG.md,
the pilot record's `design` field only, results/p3/METHOD.md,
results/p3/METHOD_ADDENDUM_1.md, RULES.md); and my own earlier workspaces. Everything else is
barred.

## What I will produce before opening anything barred

1. A2-E: my own exact proofs for ell = 3..10 on [0,1] x [0, mu_lo(ell)] (my mu_lo under the
   registered rule, exact coverage q(mu_lo)^2 >= (99/100)^2): strict positivity for ell >= 4;
   for ell = 3, U_- >= 0 with the only zero at (t, mu) = (1, 0), by an exact argument that
   handles the corner (local factorisation / blow-up of the corner, plus my verifier off it).
2. A2-S: my own N built from my transcription and the registered design
   (P = a(1+eps)/(z+eps) + p_0, a = -2/5, eps = 7mu/(3(6+7mu+mu^2)), p_0 from the pilot
   record's `design` field via float.fromhex), and my own exact proof that N > 0 on
   (0, 1) x [0, 1/8], including an exact treatment of the corner (z, mu) = (0, 0) (where the
   polynomial normalisation of N vanishes), and an exact proof that my regions cover the
   rectangle.
3. Pencil verdicts: (a) the reduction for the singular design; (b) the tortoise map at q = 1
   (METHOD_ADDENDUM_1 section 1); (c) the composition of Theorem A2, with exact range
   comparisons.
4. Controls: (a) A2-E at ell = 2 must reject; (b) a strict bound for ell = 3 must fail at the
   touching point with value exactly 0; (c) a = -7/10 must reject; (d) a planted change making
   N's corner limit exactly 0 with the rest positive must be refused by a strict check;
   (e) a planted bound state in the throat at q = 1 must reject, with Q[b] < 0 certified by
   rigorous integration over the whole support of b with the quadratic form's weights;
   (f) a verifier tamper caught by KATs (KAT1-8, including the coefficient-level substitution
   checks).
5. The reproductions: `kit/a2/run_elementary.sh` at `e422d74` and `kit/a2/run_s.sh` at
   `25c796e`, on host-1 or host-2, exit codes and log hashes.

## Hosts

Every run beyond a sub-minute spot check goes to host-1 or host-2 under `nice -n 19` with the
pinned venv; a copy of every run's outputs stays on the node in `[kimi-folder]/`; the host of
each run is recorded.

## Verdict rule

Each claim passes only on my own exact computation. A failure is reported with the ell (or
region) and an exact point and value. A certified trial function with Q < 0 for any
ell >= 2, q in [99/100, 1] would be reported at once.
