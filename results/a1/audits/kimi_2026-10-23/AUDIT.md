# AUDIT — bh-modes A1 for ℓ ≥ 3 (BHM-052, P1 and Lemma U)

*Auditor: Kimi (second auditor for machine results), 2026-10-23.
Brief: `results/a1/briefs/BRIEF_kimi_2026-10-23.md`, SHA-256
`fae7c88aec67ae2895f2f33342ce12e7bf45c790a1dc8079c26af2fd8162f72e` (verified against
`SEALED.sha256`; the brief's five artifact hashes and five code hashes all verified).
Workspace: `[kimi-folder]/bhm-a1-audit-2026-10-23/`. The bh-modes tree was never
modified. Runs of record: my own suite on **host-1**, the kit reproduction on **host-2**, both
under `nice -n 19` with the pinned venv (`[venv]`: python-flint 0.9.0 / FLINT 3.6.0 /
sympy 1.14.0). Development spot checks ran on host-0; the artifacts built on both hosts are
byte-identical.*

**Anti-anchoring.** Every own check below was complete and on disk before I opened
`results/a1/RESULT.md`, `STAGE_REPORT.md`, `results/a1/runs/`, the attempt directory, or the
registry rows.

## Task 1 — transcription

Reused my own KI (5.62b)/(5.63b) transcription from the p3 audit (BHM-036), where it was
checked against the rendered PDF page 25 and proved symbolically identical to TARGET.md §1 at
n = 4 for all (m, δ). The same transcription underlies everything below.

## Task 2 — own positivity proof, ℓ = 3 … 10: PASS

My own machinery, new for general ℓ (`own/rfg.py`): exact QQ(μ) arithmetic with the per-ℓ
denominator factors A = (ℓ−1)μ² + (ℓ+4), B = (ℓ−1)μ + (ℓ+4), μ+1 (design validated in the p3
and onset audits, where its output was cross-checked coefficient-by-coefficient against an
independent sympy route).

Per ℓ = 3, …, 10 (`own/part1.py`, log `own/part1.host-1.log`, host host-1):

- the parametrisation identities hold exactly (s² = 1 + 4mq²/25, q(1) = 0, q(0) = 1,
  δ(1) = 0 — sympy symbolic checks);
- w increases on [0,1] (my Bernstein verifier on the numerator of w′);
- μ_lo = k/1000 with k largest such that w(k/1000)² ≤ 1 − (99/100)², and the coverage check
  q(μ_lo)² ≥ (99/100)² is exact rational arithmetic (μ_lo = 11/100, 103/1000, 49/500, 47/500,
  91/1000, 89/1000, 87/1000, 43/500 for ℓ = 3..10);
- Den = B·(μ+1)³ > 0 on [μ_lo, 1] (verified);
- **F > 0 on [0,1] × [μ_lo, 1], closed, proved by my own exact Bernstein verifier — one box,
  no subdivision, for every ℓ.**

So U₋ > 0 on the whole physical region for each ℓ = 3..10, covering q ∈ [0, 99/100] (in fact
slightly more, up to q(μ_lo) ≈ 0.99005).

## Task 3 — Lemma U re-derived; pencil verdicts

My own symbolic build (`own/lemmaU.py`): P(ε, κ, x) = ε⁶U₋(x; ε⁻², κε) is a polynomial with
15 terms, no negative ε-powers; split P = Pos − Neg with Pos, Neg nonnegative-coefficient;
Pos(0,0,0) = 64; **Neg(1/12, 1/5, 2) = 159997/17496**, so 64 − Neg = **959747/17496 ≈ 54.86
> 0** (exact). Hence U₋ = m³P ≥ m³·959747/17496 > 0 for ℓ ≥ 11, all q ∈ [0,1], x ∈ [0,2].

Pencil verdicts for `results/a1/PREREG.md` §3:

- **(a) SOUND.** (5.58) ÷ 4m gives mδ² + δ = q²/25 (re-derived), so κ² = q²/25 − δ ≤ 1/25
  and 0 ≤ κ ≤ 1/5 for q ≤ 1. (I also verified κ ≤ 1/5 directly from κ = (√(1+4m/25)−1)/(2√m).)
- **(b) SOUND.** x_H = 2/(1 + √(1−q²)) ≤ 2.
- **(c) SOUND.** m = (ℓ−1)(ℓ+4) increases in ℓ; m(11) = 150; ε ≤ 1/√150 ≤ 1/12, and the
  code's check m₀ε̄² = 150/144 ≥ 1 is exactly that.
- **(d) SOUND.** Nonnegative-coefficient polynomials are monotone in each variable on the
  positive orthant; Pos ≥ 64 and Neg ≤ Neg(1/12, 1/5, 2); U₋ = m³P since ε⁶ = m⁻³.

No gaps. (d)'s bound is far from tight — the margin 54.86 against 64 is comfortable — which is
fine for a certificate.

## Task 4 — controls: all REJECT as required

- **(a) ℓ = 2** on the same machinery: my verifier REJECTS with the exact counterexample
  F(1, 121/1000) = −26545422643219/97656250 < 0 — the corner (t, μ) = (1, μ_lo(2)), exactly
  the predicted mechanism (and the same corner the lead's attempt-e60de7f found).
- **(b) planted negative region** (ℓ = 3, U₋ − 10⁷·64·t³(1−t)³): REJECT, counterexample at
  t = 1/2 (F(1/2, μ_lo) ≈ −9.6·10⁷ exactly computed).
- **(c) verifier tamper:** my KAT suite (`own/verify.py::kat`) — the tampered verifier
  (acceptance margin −2) is caught by KAT1; strictness at zeros (KAT3) works.

## Task 5 — reproduction

`kit/a1/run.sh` at `3625bf0`, on **host-2** (`runs/kit-run-host-2/`): exit 0, **KIT PASS** —
main VERIFIED; all seven registered controls and drills REJECT (nc-ell2, nc-bump,
nc-coverage, nc-uniform, td-coeff, td-split, td-verifier). Log and record hashes in
`SHA256SUMS`.

## Reconciliation

(Completed after all own checks.) My reproduction's main `result.json` is identical to the run
of record in every substantive field (timings/provenance masked). The record's Part II data
match my own derivation term-for-term (same nine Neg monomials, Neg(1/12,1/5,2) =
159997/17496, 64 − Neg = 54.8552…); the registered NC-A1a corner counterexample (1, 121/1000)
is exactly the one my control (a) produced independently.

## Findings

None against P1, Lemma U, or the method. The e60de7f record-writing defect (BHM-050) is a
plumbing failure, honestly recorded by the lead in the addendum; the fixed code reproduces.

## Overall verdict

**P1 and Lemma U stand: certified, independently verified.** With BHM-017 (ℓ = 2, q ≤ q_*),
BHM-023's T3 (ℓ = 2, q ∈ [0.97277, 0.99020]) and `results/p3/METHOD.md` Proposition 3
(pencil-audited SOUND in my BHM-036 review), Theorem A1 (D = 6, ℓ ≥ 2, q ≤ 99/100) has all its
inputs second-party checked.

Pointer for the operator: audit workspace `[kimi-folder]/bhm-a1-audit-2026-10-23/` with
AUDIT.md, audit_record.json, SHA256SUMS.
