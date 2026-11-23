# RESULT — HD-X-E: D = 7–11 near extremality, by U₋ ≥ 0

*Item BHM-128. 2026-10-26, the bh-modes lead. Registration: `PREREG.md` (BHM-127). Sealed.*

## Verdict: VERIFIED as registered, KIT PASS

- **The record:** host-1 at `8679d8b`, from its `git archive` (SHA-256 `53e25088d611512a…`), 18:06:53–18:07:23 UTC. The
  main run took 29.5 s.
- **The reproduction:** host-2, with `BHM_REF`. All 7 jobs are IDENTICAL after masking.
- **Every gate holds:** KAT, E0n, PARAM4, H, EXT, A2E4 and MEET.
  - A2E4 means the general-n code at n = 4 reproduces A2-E's sealed record field by field.
  - MEET means every μ_lo equals HD-E's sealed E1 lower end, and the hand-off ℓ₀ = 10, 10, 11, 13, 14 matches.
- **All 33 parts are certified.**

| Control | Verdict |
|---|---|
| nc-band | REJECT: E D=7 l=3, E D=11 l=7, as registered |
| nc-strict | REJECT: E D=7 l=4, E D=11 l=8, as registered |
| nc-bump | REJECT: E D=7 l=5, E D=11 l=9, as registered |
| td-coeff | REJECT: E0n, EXT, A2E4, E D=7 l=4, E D=8 l=5, E D=9 l=6, E D=10 l=7, E D=11 l=8, the predicted full list |
| td-verifier | REJECT: KAT, as registered |
| td-mulo | REJECT: MEET, the predicted full list |

## What is certified

> **HD-X-E (certified).** For D = 7–11, every ℓ from n − 1 to ℓ₀(n), and every q ∈ [q(μ_lo), 1] with
> q(μ_lo) ≥ 99/100, U₋ ≥ 0 on the closed exterior.
> - For ℓ ≥ n the inequality is strict.
> - For ℓ = n − 1 its only zero is at the extremal horizon.
>
> So V_S− ≥ 0 there, and A_{ℓ,q} ≥ 0.

**With Theorem HD** (HD-E's E1, q ∈ [0, q(μ_lo)]) **and Lemma U(n)** (ℓ > ℓ₀, every q ≤ 1): for D = 7–11, every ℓ ≥ n − 1
and every q ∈ (0, 1], A_{ℓ,q} ≥ 0. What is left of Theorem HD-X is the 11 S-bands (HD-X-S) and the critical set 𝒦
(HD-X-2). Their q = 1 endpoint is already settled by Z (BHM-126).

**The certified bounds.** These are inward decimals, floored to 4 significant figures in exact arithmetic on host-1
from the record's rationals (`inward_2026-10-26/`). The exact values are in the record.

| D | ℓ = n − 1 (split: min Bernstein of K, G) | strict ℓ: U₋ ≥ |
|---|---|---|
| 7 | ℓ = 4: K ≥ 2.654·10⁷, G ≥ 3.140·10⁶ | ℓ = 5…10: from 1.866·10⁶ (ℓ = 5) to 1.230·10⁸ (ℓ = 10) |
| 8 | ℓ = 5: K ≥ 3.484·10⁸, G ≥ 5.512·10⁷ | ℓ = 6…10: from 4.827·10⁶ to 1.351·10⁸ |
| 9 | ℓ = 6: K ≥ 1.177·10⁹, G ≥ 2.194·10⁸ | ℓ = 7…11: from 1.072·10⁷ to 2.415·10⁸ |
| 10 | ℓ = 7: K ≥ 1.106·10⁹, G ≥ 2.292·10⁸ | ℓ = 8…13: from 2.132·10⁷ to 6.465·10⁸ |
| 11 | ℓ = 8: K ≥ 8.182·10⁹, G ≥ 1.827·10⁹ | ℓ = 9…14: from 3.904·10⁷ to 1.009·10⁹ |

The per-part table, with every μ_lo, is in `inward_2026-10-26/inward_hdxe.host-1.log`.

**Label:** *certified* (exact). It rests on S5's transcription, checked by gate E0n against Kimi's independent one (as in
HD-E). A second party is pending (RULES.md A4): Kimi, by a brief, at HD-X's stage report.

## Records

- `runs/record/` (host-1) and `runs/repro-host-2/`, one directory per job.
- The kit logs and hosts are in `logs/`.
- The SHA-256 of every record and log are in `SEALED.sha256` under BHM-128.
