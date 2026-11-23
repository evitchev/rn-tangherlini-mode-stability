# AUDIT — bh-modes HD-E, D = 7–11 (BHM-063)

*Auditor: Kimi (second auditor for machine results), 2026-10-23.
Brief: `results/hd/elementary/briefs/BRIEF_kimi_2026-10-23.md`, SHA-256
`999576eb7dfe64713ad0ea2972de84d032b44128904cb04d5cb867bd6494307c` (verified against
`SEALED.sha256`; all artifact and code hashes in the brief verified).
Workspace: `[kimi-folder]/bhm-hd-elementary-audit-2026-10-23/`.
Runs of record: own suite on **host-1** (`nice -n 19`, `[venv]`), kit reproduction on
**host-2**. The bh-modes tree was never modified.*

**Anti-anchoring.** All own checks were complete and on disk before I opened anything under
`results/hd/` beyond the PREREG and the brief.

## Task 1 — transcription

My own general-n transcription of KI (5.62b)/(5.63b) (`own/build.py` from the p3 audit,
BHM-036, the same file the kit's E0n gate uses as oracle), validated against the rendered PDF
page 25 in the p3 audit and proved symbolically identical to TARGET.md §1 at n = 4 there.

## Task 2 — own positivity proofs: PASS

Machinery: my own exact QQ(μ) arithmetic with per-(n,ℓ) denominator factors
A = (ℓ+n) + (ℓ−1)μ², B = (ℓ−1)μ + (ℓ+n), μ+1 (`own/rfg.py`), my own exact Bernstein verifier
(`own/verify.py`, KAT-tested), exact μ_lo = k/10000 with exact coverage. Per job: the
parametrisation identities (s² law, q(1) = 0, q(0) = 1, δ(1) = 0) and w increasing verified.

- **E1 — PASS for every D.** Per (D, ℓ) with ℓ from ℓ_el(D) to my own ℓ₀(n) (see task 3):
  F > 0 on [0,1] × [μ_lo, 1] and Den > 0 — 35 checks, all POSITIVE (one Bernstein box each in
  the host-1 record run; `own/run_all.host-1.log`). Coverage exact: q(μ_lo)² ≥ (99/100)².
- **E2 — PASS for all 13 bands**, each to its q_split, same method. The interior band
  D = 10 ℓ = 3 (q ≤ 49/100) needed 31 boxes; the others 1–9.

## Task 3 — Lemma U(n) re-derived; pencil verdicts

For each n = 5..9, my own symbolic P_n(ε,κ,x) = ε⁶U₋(x; ε⁻², κε) (20 terms, polynomial), the
split Pos_n − Neg_n with nonnegative coefficients, Pos_n(0) = 64, and the corner value:

| n | my ℓ₀ | ε̄ | 64 − Neg_n(ε̄, 1/(n+1), 2) |
|---|---|---|---|
| 5 | 10 | 1/12 | 399917/10368 ≈ 38.57 |
| 6 | 10 | 1/13 | 1481614528/62748517 ≈ 23.61 |
| 7 | 11 | 1/14 | 17257/2401 ≈ 7.19 |
| 8 | 13 | 1/16 | 79325/16384 ≈ 4.84 |
| 9 | 14 | 1/18 | 19870/6561 ≈ 3.03 |

My ℓ₀(n) search followed the PREREG's rule (least ℓ₀ ≥ max(ℓ_el, 10) with a positive bound).
The record's ℓ₀ values are identical to mine.

Pencil verdicts on `results/hd/elementary/PREREG.md` §3 at general n:
- **(a) SOUND.** (5.58) ÷ 4m gives mδ² + δ = q²/(n+1)²; κ² = q²/(n+1)² − δ ≤ 1/(n+1)² for
  q ≤ 1; κ ≥ 0. Re-derived.
- **(b) SOUND.** x_H = 2/(1+√(1−q²)) ≤ 2.
- **(c) SOUND.** m increases in ℓ; ε ≤ 1/√(m(ℓ₀+1)) ≤ 1/isqrt(m(ℓ₀+1)) = ε̄.
- **(d) SOUND.** Monotone nonnegative-coefficient polynomials; Pos ≥ 64, Neg ≤ corner value;
  U₋ = m³P.

## Task 4 — controls: all REJECT as required

- **(a)** D = 7, ℓ = 2, q ≤ 951/1000: REJECT with the exact counterexample
  F(1, 1367/5000) = −4937563735773837/122070312500 < 0 — at the horizon corner t = 1, as
  predicted.
- **(b)** D = 10, ℓ = 3, q ≤ 99/200: REJECT with the exact counterexample
  F(1/2, 1653/2000) = −6078885677633951/62500000000 < 0 — an interior point 0 < t < 1, as
  predicted.
- **(c)** planted bump (D = 7, ℓ = 4, U₋ − 10⁷·64·t³(1−t)³·Den): REJECT, exact counterexample
  at t = 1/2.
- **(d)** verifier tamper: caught by the KAT suite (KAT1–KAT8).

## The verifier defect (full account)

Control (b) initially returned a wrong POSITIVE: my own verifier's box-substitution routines
(`substitute_1d`, `substitute_2d`) used `h**j` where the binomial expansion requires `h**k`
(a wrong power of the box width), so non-unit and subdivided boxes tested a corrupted
polynomial. The control caught it — exactly its job. Fix made in all four of my audit
workspaces; regression KATs added (KAT6/7: coefficient-level identities against hand-computed
expansions; KAT8: a non-unit-box corner rejection) — they fail under the old code, pass under
the new. **Every verifier-dependent result in my earlier audits (p3, onset, a1) was
re-produced with the fixed verifier; no verdict changed** (p3: all six certificate sets
POSITIVE again, G1 now in 5 boxes matching the record's count; onset O2–O5 unchanged; a1 Part I
and controls unchanged). Addenda are in those audits' AUDIT.md files, with new manifests
(p3: SHA256SUMS.v3; onset: v2; a1: v2).

## Task 5 — reproduction

`kit/hd/run_elementary.sh` at `6fe9689` on **host-2**: exit 0, **KIT PASS** — main VERIFIED;
nc-onset-h, nc-onset-i, nc-zero, nc-coverage, nc-uniform, td-coeff, td-param, td-verifier all
REJECT. My main `result.json` is substantively identical to the run of record
(timings/provenance masked).

## Overall verdict

**HD-E stands: E1 (every D), E2 (all 13 bands), E3 (Lemma U(n), every n) — certified,
independently verified.** No fixes requested.

Pointer for the operator: audit workspace `[kimi-folder]/bhm-hd-elementary-audit-2026-10-23/`
(AUDIT.md, audit_record.json, SHA256SUMS).
