# A2 stage report, addendum 1: corrections from the session-R lead's reading (BHM-106)

*2026-10-24, the bh-modes lead. This answers the reading BHM-103, with the checks of BHM-105.*
- *`STAGE_REPORT.md` (BHM-102) and every other file named here are sealed and unchanged. Each corrected item gets a
  "corrected by BHM-106" pointer in the registry.*
- *Theorem A2's certified content is unchanged.*
- *Sealed.*

## 1. The headline (STAGE_REPORT.md:14–15)

"So the master equation for Φ₋ has no exponentially growing mode, through extremality" is replaced by `TARGET_A2.md` §2's
Reading: for D = 6, every ℓ ≥ 2 and every 0 < q ≤ 1, **the master equation for Φ₋ has no mode e^{κt}φ(r*) with κ > 0 and
φ ∈ L²(ℝ, dr*)**. "Not claimed: … anything at q = 1 beyond the quadratic form" stands.

## 2. What Theorem A2 rests on (the status row, STAGE_REPORT.md:80)

Theorem A2 covers q ∈ [99/100, 1]. Its parts:
- **ℓ = 2:** A2-S alone, on [q(1/8), 1] ⊃ [99/100, 1].
- **ℓ = 3…10:** A2-E on [q(μ_lo(ℓ)), 1] **and A1's P1 Part I on [99/100, q(μ_lo(ℓ))]**. Here q(μ_lo(ℓ)) runs from 0.9900005
  (rounded down, ℓ = 4) to 0.9901674 (ℓ = 9), so the slivers are under 1.7·10⁻⁴ (X0, BHM-105).
- **ℓ ≥ 11:** Lemma U.

So the row reads: *certified*, resting on A2-S, A2-E, P1 Part I and Lemma U. The second parties of P1 and Lemma U are
complete (Kimi, BHM-065). Those of A2-S and A2-E are pending.

## 3. Decimals of certified ends (BHM-060's rule: exact, or inward)

The inward values are from BHM-105's X0, computed by exact integer square roots:

| Where | As written | Correct |
|---|---|---|
| STAGE_REPORT.md:33 (BHM-102) | T3 [0.97277, 0.99020] overlaps A2-S [0.98936, 1] | T3 **[0.97277, 0.99019]** overlaps A2-S **[0.98937, 1]** |
| TARGET_A2_ADDENDUM_1.md:27 (BHM-092) | "q(1/8) = 0.98937… … T3's certified [0.97277, 0.99020]" | q(1/8) = √(2961/3025) = 0.98936…, which is 0.98937 rounded inward as a lower end; T3 [0.97277, 0.99019] |
| results/a2/s/PREREG.md:13 (BHM-100) | T3 on [0.97277, 0.99020] | [0.97277, 0.99019] |
| BHM-060, and results/p3/RESULT_ADDENDUM_1.md:16 | √(31416/32041) = 0.9901987… | **0.99019883…**. The inward 0.99019 given there is right |

- **The overlap holds exactly either way:** 2961/3025 < 31416/32041.
- **"0.98936…"** in `results/a2/s/RESULT.md`:11 and in BHM-095 gives digits, and is correct as such. As a range end it is
  quoted inward as 0.98937.

## 4. A2-E's PREREG (BHM-096), line 13

It reads "So q(μ_lo(ℓ)) ≤ 99/100". It should read **"So q(μ_lo(ℓ)) ≥ 99/100"**, since w(μ_lo)² ≤ 1 − (99/100)². The code
gated the right direction, q(μ_lo)² ≥ (99/100)², and so did the RESULT. The consequence for the composition is §2.

## 5. A2-S's controls (RESULT.md, BHM-101)

- **nc-zm.** RESULT.md:43 says "U₋ − H₋²x⁴ also lowers the outer region, so POS-O fails too". That is **wrong**.
  - POS-O fails at (19/64, 0) because of a = −1/2 alone. In the reading's check, N(19/64, 0) = 2068.6 for the main
    design, 2020.5 with the lowering alone, −21.9 with a = −1/2 alone, and −70.0 with both.
  - So nc-zm does not isolate the zero margin. **d0 does** (BHM-105): REJECT by POS-C alone, with C(0, 0) = 0 exactly.
- **nc-res:** as registered, but not specific: it fails in all four charts. It stands as a gross tamper.
- **nc-bound.**
  - (a) stands: Q[b] < 0, certified in Arb.
  - (b) is an exact check of the planted NL on the slice [1/20, 1/5] × {0}. The four charts ran on the unplanted
    potential.
  - At q = 1 and ℓ = 2, U₋ < 0 only for z < 0.0866846… (the reading's exact count). So most of the bump lies outside the
    well, and the frame's "a planted bound state in the throat" (`TARGET_A2_ADDENDUM_1.md` §4) is not what it tests. The
    throat-specific planted control is **d6** (BHM-105).
- **Every control still gave its registered verdict.** Every gate now has a planted control or a tamper (BHM-105).

## 6. Wording

- **The charts.** "Four charts cover [0, 1] × [0, 1/8]" (A2-S PREREG §2, `scert.py`) should read "cover
  [0, 1] × [0, 1/8] except the corner (0, 0)". T and C reach the corner only through their exceptional edges. The claim
  was stated on (0, 1) × [0, 1/8], correctly.
- **COVER.** Only Z_T·σ₁ ≥ 1 is needed for coverage. The other COVER inequalities keep the charts' images inside the
  rectangle.
- **"S"** names both the S-deformation and the pole's denominator ε_d z + ε_n. Later text calls the latter D.

## 7. R's existence at q = 1

The reading gives the argument (READING §2):
- f(ρ) = (1 − ρ⁻³)² is smooth and > 0 on (1, ∞), with f(1) = f′(1) = 0.
- The solution of dR/dr* = f(R) with R(0) = 2 never reaches 1, which is an equilibrium of a locally Lipschitz field.
- It grows at most linearly, since f ≤ 1, so it exists on all of ℝ.

The label stays *proved (pencil; audited 0×)*, now with the reading's argument in support.

## 8. Environment

- On a host with gmpy2 2.3.1, the A2 kits print KIT FAIL from the provenance field alone (the reading's re-run).
- `kit/a2/run_s_check.sh` (BHM-104) checks gmpy2 and exits 2 on a mismatch. The three earlier A2 kits get the same check
  in a later commit (TODO).
