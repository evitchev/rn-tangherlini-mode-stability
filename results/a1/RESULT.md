# RESULT — A1 for ℓ ≥ 3 (P1), and Theorem A1 (BHM-052)

*Registered as BHM-047 (`PREREG.md`) with addendum 1 (BHM-051, code only). The run of record was
on host-1 and the reproduction on host-2, both from a `git archive` of `3625bf0`, in
`[venv]` under `nice -n 19`. They are identical after masking (`code/compare_runs.py`),
the main `run.log`s are byte-identical, and `kit/a1/run.sh` gives KIT PASS on both nodes. The main
run takes 5 s. The failed attempt at `e60de7f` (a defect in writing the record) is BHM-050.*

## The claim

**P1: VERIFIED as registered.** For every ℓ ≥ 3, every q ∈ [0, 99/100] and every x ∈ [0, x_H(q)],
U₋ > 0. So V_{ℓ,q} > 0 on the exterior and A_{ℓ,q} ≥ 0.

**Part I, ℓ = 3…10** (exact Bernstein in (t, μ); U₋ = F/Den in lowest terms, F of degree (4, 4)).
Every F was proved positive on its whole box at the first Bernstein node, with no subdivision.

| ℓ | m | μ_lo | q(μ_lo) | Den(μ) | certified lower bound of U₋ on the region |
|---|---|---|---|---|---|
| 3 | 14 | 11/100 | 0.990018 | (μ + 1)³(2μ + 7) | 15271808607/781250 ≈ 1.95·10⁴ |
| 4 | 24 | 103/1000 | 0.990000 | (μ + 1)³(3μ + 8) | ≈ 1.28·10⁵ |
| 5 | 36 | 49/500 | 0.990016 | (μ + 1)³(4μ + 9) | ≈ 4.08·10⁵ |
| 6 | 50 | 47/500 | 0.990098 | (μ + 1)³(μ + 2) | 399839270089/390625 ≈ 1.02·10⁶ |
| 7 | 66 | 91/1000 | 0.990151 | (μ + 1)³(6μ + 11) | ≈ 2.21·10⁶ |
| 8 | 84 | 89/1000 | 0.990113 | (μ + 1)³(7μ + 12) | ≈ 4.36·10⁶ |
| 9 | 104 | 87/1000 | 0.990167 | (μ + 1)³(8μ + 13) | ≈ 7.97·10⁶ |
| 10 | 126 | 43/500 | 0.990064 | (μ + 1)³(9μ + 14) | ≈ 1.38·10⁷ |

- **Coverage.** q(μ_lo)² ≥ (99/100)² holds exactly for every ℓ, so each box covers
  q ∈ [0, 99/100]. The exact values of q(μ_lo)² and of each bound are in `runs/record/main/result.json`.
- **The bound.** The least accepted Bernstein coefficient of F, divided by the largest Bernstein
  coefficient of Den on [μ_lo, 1].

**Part II, Lemma U (ℓ ≥ 11, q ∈ [0, 1], x ∈ [0, 2]).**
- ε⁶U₋(x; ε⁻², κε) = Pos − Neg, with Pos(0, 0, 0) = 64.
- Neg has nine monomials:
  7680ε³κx + 7680ε⁴x + 80000ε³κ³x³ + 134400ε⁴κ²x³ + 28800ε⁵κx³ + 400000ε⁴κ⁴x⁴ + 1200000ε⁵κ³x⁴ +
  1200000ε⁶κ²x⁴ + 400000ε⁷κx⁴.
- At the corner (ε̄, κ, x) = (1/12, 1/5, 2), Neg = 159997/17496 ≈ 9.145.
- So **U₋ ≥ m³ · 959747/17496 ≈ 54.86 m³ > 0**.
- The six exact checks pass: polynomiality, the split, Pos(0) = 64, the κ identity, ε̄ ≥ m₀^{−1/2},
  and the sign of the bound.

## Gates, controls and drills (all as registered)

| Name | Registered | Observed |
|---|---|---|
| KAT1–KAT5, E0, H | hold | hold, in every run except the drill aimed at them |
| NC-A1a, ℓ = 2 on q ≤ 99/100 | REJECT at the corner (1, μ_lo(2)) | REJECT: F = −26545422643219/97656250 at (t, μ) = (1, 121/1000) |
| NC-A1b, a planted bump | REJECT at t = 1/2 | REJECT: F = −37682004040209/390625 at (1/2, 11/100) |
| NC-A1c, coverage for q = 98/100 | REJECT, coverage | REJECT: [31/200, 1] reaches only q² = 2121288169/2207778169 < (99/100)² |
| NC-A1d, ℓ₀ = 1 | REJECT, bound < 0 | REJECT: 64 − Neg(1/2, 1/5, 2) = −33488 |
| TD-A1a, 7680 → 7681 | REJECT at E0 | REJECT: E0 difference −δm²x² − mx² |
| TD-A1b, x⁴ terms dropped from Neg | REJECT, P ≠ Pos − Neg | REJECT: the split fails (the tampered bound would read 56.26) |
| TD-A1c, verifier threshold −1 | REJECT at the KATs | REJECT: KAT2 and KAT3 accepted by the tampered verifier |

## Theorem A1 (assembled as registered, `PREREG.md` §2)

For every integer ℓ ≥ 2 and every q ∈ (0, 99/100], A_{ℓ,q} ≥ 0, so the Kodama–Ishibashi master
equation for Φ₋ (D = 6) has no mode e^{κt}φ with κ > 0:
- ℓ = 2 and q ≤ q_*: V ≥ 0 (BHM-017, O2);
- ℓ = 2 and q ∈ [0.97277, 0.99020] ⊇ (q_*, 99/100]: T3 (BHM-023), through
  `results/p3/METHOD.md` Proposition 3;
- ℓ ≥ 3: P1 (this item).

## Status

- **P1 and Lemma U:** *certified* (exact). The pencil steps (a)–(d) of `PREREG.md` §3 are proved
  (pencil; audited 0×). An independent re-run is pending: a sealed Kimi brief, with its runs of
  record on host-1/005.
- **Theorem A1:** *certified*. It rests on the three items above and on the S-deformation reduction
  (proved, pencil; audited 2×; Lean, BHM-030).
  - BHM-017 has its second party (Kimi, BHM-037; Lean, BHM-030), and so does BHM-023 (Kimi, BHM-036
    and BHM-040). Session-L's second check of T3 is running (BHM-044, BHM-046).
  - Its physical reading rests on S5's reduction to master equations and on S5's results for the
    other sectors, both *cited* (`TARGET.md` §2).
- **Lemma U's range q ≤ 1** settles ℓ ≥ 11 of A2's R4 (`TARGET_A2.md` §4).

## Hashes (SHA-256, first 16 hex)

- Code at `3625bf0`:
  - `code/a1/p1.py` `7e5fac94a3a51087`
  - `kit/a1/run.sh` `dfe445eab152b242`
  - `code/onset/bernstein.py` `a0b1ec5c952055ed`
  - `code/onset/onset.py` `9b346258ad0375d1`
  - `code/ki/potentials.py` `7d686b40ad326544`
  - `code/qnm1c/common.py` `29c30345dec7b2fe`
- The record:
  - `runs/record/main/result.json` `58b9850b6cd76077`
  - `runs/record/main/run.log` `4c086d6acd9d9e3b`
  - `runs/record/kit.log` `32854b74bf18c69d`
- The reproduction: `runs/repro-host-2/main/result.json` `728a93bcc92c3cfa`.
