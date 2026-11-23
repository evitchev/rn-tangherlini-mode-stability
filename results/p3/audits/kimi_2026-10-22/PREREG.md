# PREREG — my audit of the bh-modes p3 S-certificates (BHM-023/025)

*Auditor: Kimi. 2026-10-22.*

Brief: `results/p3/briefs/BRIEF_kimi_2026-10-22.md`, SHA-256
`3c828902dcd2d518f9eecd82b45f352446bddc5240c4024f2445d66e40700ee1`
(verified byte-identical to the `SEALED.sha256` line, together with the other three bundle
briefs).

## Anti-anchoring commitment

Before opening any of `results/p3/RESULT.md`, `results/p3/RULE2_RESULT.md`,
`results/p3/diagnosis_G1.*`, any `run.log` under `results/p3/`, any `verdict` field of the JSON
records, `REGISTRY.md` rows >= BHM-023, the lead's commit messages after `782fc56`, or anything
under `lean/` or `outbox/`, I will have on disk:

1. my own transcription of f, U-, H- (D = 6, from `TARGET.md` section 1), checked against
   Kodama-Ishibashi hep-th/0308128 (5.62b), (5.63b), and the same for G1 (n = 8, Q = 0);
2. my own derivation of the identity  V~ = V + dS/dr* - S^2 = f N/(64 rho^2 H-^2)  for
   S = -f(1-z)P (my own CAS; N's formula is stated in the brief itself and in the p3 PREREG,
   which are allowed; `METHOD.md` is read only afterwards, for the pencil audit);
3. my own exact positivity verdicts for T1, T2, T3 (all eight boxes), G1 (rule 2), and rule-2
   T1, T2, built from the stored polynomials only (`result.P`, `result.mu`,
   `result.boxes_mu[k].{mu,P}` — no other fields);
4. my three controls: (a) P(0) raised above the horizon bound, (b) U- coefficient 7680 -> 7681,
   (c) a tamper in my own positivity code — each must REJECT;
5. the reproduction runs of `kit/p3/run.sh` at `782fc56` and `kit/p3/run_rule2.sh` at
   `094591c` in this workspace, with exit codes and log hashes.

## Pre-committed verdict rule

Each certificate passes only if my own exact arithmetic proves N > 0 on the closed domain
(z in [0, 1], and the mu-box where present), endpoints included, with the mu-dependence carried
exactly through delta(mu), x_H(mu), f and every cleared denominator proved positive on the box.
Any failure is reported with an exact counterexample point. The overall verdict is PASS only if
T1, T2, T3 (rule 1) and G1, T1, T2 (rule 2) all pass my own check AND the reproduction runs are
green.

## Method for my positivity proof

Exact rational Bernstein-basis enclosures in z (and tensor-product in (z, mu)) with adaptive
bisection, implemented by me on sympy Rational arithmetic, fail-closed. Independent of
`code/onset/bernstein.py` (which I will not read before my own verifier passes or fails).
