# PREREG — my audit of bh-modes A1 for ell >= 3 (BHM-052, P1)

*Auditor: Kimi. 2026-10-23.*

Brief: `results/a1/briefs/BRIEF_kimi_2026-10-23.md`, SHA-256
`fae7c88aec67ae2895f2f33342ce12e7bf45c790a1dc8079c26af2fd8162f72e` (verified against
`SEALED.sha256`; the five artifact hashes in the brief also verified).

## Anti-anchoring

Before opening `results/a1/RESULT.md`, `STAGE_REPORT.md`, `results/a1/runs/`,
`results/a1/attempt-e60de7f/`, `REGISTRY.md` rows >= BHM-049, the lead's commit messages,
`outbox/`, `lean/`, `results/*/audits/`, or `[deliveries]/`, I will have on disk:

1. my own per-ell exact build of F_ell(t, mu) and Den_ell(mu) (my own QQ(mu) arithmetic with
   per-ell factors A = (ell-1)mu^2 + (ell+4), B = (ell-1)mu + (ell+4), mu+1), from my own KI
   (5.62b)/(5.63b) transcription (p3 audit, BHM-036);
2. my own positivity proofs: for ell = 3..10, Den > 0 on [mu_lo, 1] and F > 0 on
   [0, 1] x [mu_lo, 1] (my own Bernstein verifier, KAT-tested), with mu_lo = k/1000 the largest
   k with w(k/1000)^2 <= 1 - (99/100)^2 and an exact coverage check q(mu_lo)^2 >= (99/100)^2;
   the parametrisation identities and w increasing checked exactly per ell;
3. my own derivation of Lemma U: P(eps, kap, x) = eps^6 U_-(x; eps^-2, kap eps) built
   symbolically, split Pos - Neg with nonnegative coefficients, Pos(0,0,0) = 64,
   64 - Neg(1/12, 1/5, 2) > 0 in exact rationals; pencil verdicts for steps (a)-(d);
4. my controls: (a) ell = 2 on q <= 99/100 must REJECT (counterexample expected at
   (t, mu) = (1, mu_lo(2))); (b) ell = 3 with U_- - 10^7*64 t^3 (1-t)^3 must REJECT;
   (c) a tampered verifier must be caught by the KATs;
5. the reproduction of `kit/a1/run.sh` at `3625bf0` on host-1 or host-2, exit code and log
   hashes, host recorded.

## Hosts

Runs of record (own proofs, controls, reproduction) go to host-1 or host-2 under `nice -n 19`
with `[venv]` there; development spot checks may run on host-0. The host of every
run is recorded in the JSON record.

## Pre-committed verdict rule

P1 passes only if every ell = 3..10 verifies by my own exact route AND Lemma U re-derives
with 64 - Neg(1/12, 1/5, 2) > 0 exactly. A failure is reported with an exact counterexample
point. Overall PASS additionally requires the reproduction to be green.
