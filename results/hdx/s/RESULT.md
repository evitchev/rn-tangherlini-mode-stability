# RESULT — HD-X-S: the singular S-certificates for the 11 non-critical bands

*Item BHM-132. 2026-10-26, the bh-modes lead. Registration: `PREREG.md` (BHM-131), on HD-X-PILOT's sealed designs
(BHM-130). Sealed.*

## Verdict: VERIFIED as registered, KIT PASS

- **The record:** host-1 at `bf23bfc`, from its `git archive` (SHA-256 `99e8a5e2066aaae0…`), 18:26:59–18:29:02 UTC. All
  198 band jobs (11 bands × 18) end as their rules require (`code/hdx/verdicts.py`).
- **The gate band** D = 6 ℓ = 2 is VERIFIED and IDENTICAL to A2-S's record (BHM-101), including every chart's least
  Bernstein coefficient.
- **The reproduction:** host-2, with `BHM_REF`. KIT PASS, and all 199 jobs are IDENTICAL after masking.

| D, ℓ | design degree | NL degree (z, μ) | `none` | its 17 controls |
|---|---|---|---|---|
| 7, 3 | 12 | (42, 12) | VERIFIED | as registered |
| 8, 3 | 16 | (54, 12) | VERIFIED | as registered |
| 8, 4 | 12 | (46, 12) | VERIFIED | as registered |
| 9, 4 | 12 | (50, 12) | VERIFIED | as registered |
| 9, 5 | 12 | (50, 12) | VERIFIED | as registered |
| 10, 4 | 20 | (70, 12) | VERIFIED | as registered |
| 10, 5 | 12 | (54, 12) | VERIFIED | as registered |
| 10, 6 | 12 | (54, 12) | VERIFIED | as registered |
| 11, 5 | 16 | (66, 12) | VERIFIED | as registered |
| 11, 6 | 12 | (58, 12) | VERIFIED | as registered |
| 11, 7 | 12 | (58, 12) | VERIFIED | as registered |

- **Every gate holds in every band:** KAT, E0n, H, PARAM, DESIGN, G-RES, COVER, L, S, DIV-T and DIV-C.
- **All four charts are positive in every band.** The exact least Bernstein coefficients are in each record's
  `min_bernstein`.
- **nc-well's (a)** is certified in every band (Q[b] < 0 in Arb), and its (b) is refused on the support, inside
  U₋ < 0.

## What is certified

> **HD-X-S (certified).** For each of the 11 bands of D = 7–11 with 2ℓ > n − 1, and every q ∈ [q(1/8), 1] with
> q(1/8)² ≤ (99/100)², A_{ℓ,q} ≥ 0 on C₀^∞(ℝ). The reduction is Proposition 3 for P that is C¹ on (0, 1) (*machine-checked*,
> every n); the tortoise map at q = 1 at general n is proved (pencil; audited 0×).

**With Theorem HD, HD-X-E (BHM-128) and Lemma U(n)**, this gives **Theorem HD-X outside the critical set 𝒦**: for
D = 7–11, every ℓ ≥ 2 with (D, ℓ) ∉ 𝒦, and every q ∈ (0, 1], A_{ℓ,q} ≥ 0.

What remains is 𝒦, the 9 bands with 2ℓ ≤ n − 1, on q ∈ (99/100, 1). That is HD-X-2. Their endpoint q = 1 is
already settled by Z (BHM-126).

A second party is pending (RULES.md A4): Kimi, by a brief, at HD-X's stage report.

## Records

- `runs/record/` and `runs/record-gate/` (host-1); `runs/repro-host-2/` and `runs/repro-host-2-gate/`. One directory
  per job, each with `result.json`, `run.log` and `verdict.txt`, and for the reproduction `compare.txt`.
- The kit logs and hosts are in `logs/`.
- The SHA-256 of every record and log are in `SEALED.sha256` under BHM-132.
