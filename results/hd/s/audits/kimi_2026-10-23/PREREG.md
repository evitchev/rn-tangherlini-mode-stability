# PREREG — my audit of bh-modes HD-S (BHM-078)

*Auditor: Kimi. 2026-10-23.*

Brief: `results/hd/s/briefs/BRIEF_kimi_2026-10-23.md`, SHA-256
`e5e9c7df35402576e80c2ac45ec63a36faa3535d3a48352c795a0c827cba416d` (verified against
`SEALED.sha256`; artifact and code hashes in the brief verified where listed).

## Anti-anchoring

Before opening `results/hd/s/RESULT.md`, `results/hd/STAGE_REPORT.md`, any `run.log` or
`planning.jsonl` of the runs, `REGISTRY.md` rows >= BHM-078, the lead's commit messages,
`outbox/`, `notes/`, `lean/`, `results/*/audits/`, `[deliveries]/`, or `[session-R-folder]/`, I
will have on disk:

1. my own N per stored certificate box, built from my own general-n KI (5.62b)/(5.63b)
   transcription and the parametrisation of `TARGET_HD.md` section 1:
   - z-design: N = U_- - 64 H_-^2 [(1-z) f_z P + f(-P + (1-z) P_z + P^2)], x = x_H (1-z)^{n-1},
     f = (1 - (1-z)^{n-1})(1 - k (1-z)^{n-1}), k = (1-w)/(1+w) = x_H - 1;
   - zeta-design: P = Phat/(z + delta_b)^d, verified through N~ = N (z+delta_b)^{2d};
2. my own exact positivity verdict for every box of every one of the 18 bands (my fixed
   Bernstein verifier, KAT1-8), plus the exact coverage checks (contiguity,
   q(mu_a)^2 >= (99/100)^2, q(mu_b)^2 <= q_split^2 or mu_b = 1);
3. pencil verdicts on the two extensions of Proposition 3 ((a) general n; (b) the zeta
   design);
4. controls: (a) a planted bound state (bump) must make my check of the same P reject;
   (b) one stored certificate with one coefficient changed must reject; (c) a verifier tamper
   must be caught by the KATs;
5. the reproduction of `kit/hd/run_s.sh` at `0aa2673` on host-1 or host-2.

I read only the `boxes[]` fields (`mu`, `variable`, `degree`, `delta_b`, `P`) of the
certificate JSONs - never a verdict field.

## Verdict rule

Each band passes only if every box verifies by my own exact route and coverage is exact.
A failure is reported with the band, box and an exact counterexample point.
