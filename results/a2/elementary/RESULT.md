# A2-E RESULT: VERIFIED — U₋ ≥ 0 for ℓ = 3…10 up to extremality (BHM-097)

*2026-10-24, the bh-modes lead. Registration: `PREREG.md` (BHM-096), sealed before the run. The record ran on host-1 and
the reproduction on host-2, from a `git archive` of `e422d74` (archive SHA-256 `6971234840077323…`) with
`kit/a2/run_elementary.sh`. UTC start 03:35:50; 5.3 s.*
- *Both kits print KIT PASS.*
- *All six records are identical after masking, and all six `run.log`s are byte-identical.*

## The result

> **A2-E (certified).** For D = 6, every ℓ ∈ {3, …, 10} and every q ∈ [q(μ_lo(ℓ)), 1], U₋ ≥ 0 on the closed exterior.
> For ℓ = 4…10 it is strict. For ℓ = 3 the only zero is at the extremal horizon. So V_S− ≥ 0 and A_{ℓ,q} ≥ 0.

Every μ_lo(ℓ) has q(μ_lo)² ≥ (99/100)², so these boxes meet A1's P1 boxes [μ_lo, 1].

| ℓ | μ_lo | q(μ_lo)² (exact) | Certified bound on [0, 1] × [0, μ_lo] |
|---|---|---|---|
| 3 | 11/100 | 134331349/137053849 | F = μK + sG, with min Bernstein K = 12192768 and G = 275106444444/390625; F(1, 0) = 0 |
| 4 | 103/1000 | 63226555957929/64510244957929 | U₋ ≥ 917504000000000000/1592858715949 (> 5.7·10⁵) |
| 5 | 49/500 | 312772999176/319113139801 | U₋ ≥ 320000000000000/133237847 (> 2.4·10⁶) |
| 6 | 47/500 | 27471514409/28023764409 | U₋ ≥ 1120000000000000000/171359687181 (> 6.5·10⁶) |
| 7 | 91/1000 | 29925587924649/30523890174649 | U₋ ≥ 110398464000000000000/7496798004383 (> 1.4·10⁷) |
| 8 | 89/1000 | 142474321369809/145333802369809 | U₋ ≥ 2007040000000000000/67087243509 (> 2.9·10⁷) |
| 9 | 87/1000 | 2613126399136/2665281539761 | U₋ ≥ 7733440000000000000/137427108821 (> 5.6·10⁷) |
| 10 | 43/500 | 12122233672881/12366763922881 | U₋ ≥ 4346496000000000000/43802996767 (> 9.9·10⁷) |

- **The bounds.** The exact rationals are the certified ones. The decimals are truncated, so they are inward.
- **For ℓ = 3,** the exact splitting checks all hold: F(1, μ) is divisible by μ, F(1 − s, μ) − F(1, μ) by s, the
  identity F(1 − s, μ) = μK + sG holds, and F(1, 0) = 0.

**Gates:** KAT, E0, H, the parametrisation, and w increasing all pass.

## Controls (all as registered)

| Control | Verdict | Where |
|---|---|---|
| nc-ell2 | REJECT: E l=2 | exact counterexample F = −691200 at (t, μ) = (1, 0) |
| nc-strict | REJECT: E l=3 | F = 0 at the corner (1, 0) |
| nc-bump | REJECT: E l=4 | F = −71054336 at (1/2, 0) |
| td-coeff | REJECT: E0, E l=3 | E0, and the tampered U₋ no longer vanishes at ℓ = 3's corner, so the splitting fails |
| td-verifier | REJECT: KAT | the known-answer tests |

## Status

- **A2-E:** *certified* (exact). Independent re-run by a second party pending (RULES.md A4).
- **For Theorem A2,** ℓ ≥ 3 is now covered: A2-E for 3…10, and Lemma U for ℓ ≥ 11 (q ≤ 1, BHM-052). **ℓ = 2 remains:**
  A2-S, registered next.

## Hashes (SHA-256, first 16 hex)

- Code at `e422d74`: `code/a2/elementary.py` and `kit/a2/run_elementary.sh` as in BHM-096.
- Record `runs/record/none/result.json` `ad59836dff7d3362`, `run.log` `f8db875b4ba6a236`.
- Reproduction `runs/repro-host-2/none/result.json` `b1dcb37fcfa98a85`, `run.log` `f8db875b4ba6a236`.
- The controls' records are under `runs/record/<control>/` and `runs/repro-host-2/<control>/`; all are listed in
  `SEALED.sha256`.
