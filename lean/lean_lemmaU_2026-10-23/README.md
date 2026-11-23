# Lean layer: Lemma U of target A1 (bh-modes BHM-052): session-L, 2026-10-23

This answers the bh-modes lead's fourth message, §2 (3), second identity. It was formalised at the operator's request,
as second party for exact identities under the operator's ruling of 2026-10-23.

**Result: "BHModesLemmaU: ALL CHECKS AS REQUIRED"** (`lean/BUILD_LOG.txt`).
- **Host.** The build of record ran on the reproduction node of the bh-modes environment, under `nice -n 19`. The
  Lean environment there is described in `../lean_1c_tail_v2_2026-10-23/README.md`.
- **Oracle.** The oracle outside Lean also ran there: "ALL LEMMA U CHECKS HOLD" (`oracle/check_lemmaU.out`).

## What is proved

The file is `lean/BHModesLemmaU.lean`, namespace `BHModes.LemmaU`, with 10 theorems. `Um` is TARGET.md's U₋ (S5
(5.63b) at n = 4). `Pos` and `Neg` are the two parts of ε⁶U₋:

    Pos ε κ x = 64 + 384ε² + 320εκx + 7680ε⁴x² + 7680ε³κx² + 25600ε⁶x³
    Neg ε κ x = 7680ε³κx + 7680ε⁴x + 80000ε³κ³x³ + 134400ε⁴κ²x³ + 28800ε⁵κx³ + 400000ε⁴κ⁴x⁴ + 1200000ε⁵κ³x⁴
                + 1200000ε⁶κ²x⁴ + 400000ε⁷κx⁴

- `Neg` is RESULT.md Part II's nine monomials, letter for letter (oracle check 4).
- RESULT.md prints only Pos(0, 0, 0) = 64. I derived `Pos` from U₋ by hand, and the Lean theorem `split` proves it.

| the lead's item | Lean theorem | exact statement (abridged only by omitting the binders' types) |
|---|---|---|
| the identity | `split` | `ε ≠ 0 → ε ^ 6 * Um (1 / ε ^ 2) (κ * ε) x = Pos ε κ x - Neg ε κ x` |
| | `Pos_zero` | `Pos 0 0 0 = 64` |
| κ² = q²/25 − δ | `kappa_identity` | `0 < m → (1 + 2 * m * δ) ^ 2 = 1 + 4 * m * q ^ 2 / 25 → (δ * Real.sqrt m) ^ 2 = q ^ 2 / 25 - δ` |
| the exact value | `corner` | `Neg (1 / 12) (1 / 5) 2 = 159997 / 17496` |
| | `corner_margin` | `64 - Neg (1 / 12) (1 / 5) 2 = 959747 / 17496` |
| monotonicity | `Neg_mono` | `0 ≤ ε → ε ≤ 1/12 → 0 ≤ κ → κ ≤ 1/5 → 0 ≤ x → x ≤ 2 → Neg ε κ x ≤ Neg (1/12) (1/5) 2` (by `gcongr`) |
| | `Pos_ge` | `0 ≤ ε → 0 ≤ κ → 0 ≤ x → 64 ≤ Pos ε κ x` |
| U₋ > 0 for m ≥ 150, q ≤ 1, x ≤ 2 | `lemmaU` | `150 ≤ m → q ^ 2 ≤ 1 → 0 ≤ δ → (1 + 2 * m * δ) ^ 2 = 1 + 4 * m * q ^ 2 / 25 → 0 ≤ x → x ≤ 2 → m ^ 3 * (959747 / 17496) ≤ Um m δ x` |
| every ℓ ≥ 11 | `lemmaU_ell` | for ℓ : ℕ with `11 ≤ ℓ` and m = (ℓ − 1)(ℓ + 4), the same hypotheses on q, δ and x give `0 < Um m δ x` |
| the exterior is inside x ≤ 2 | `xH_le_two` | `2 / (1 + Real.sqrt (1 - q ^ 2)) ≤ 2` |

**How the proof of `lemmaU` runs.** It follows the record.
1. Set ε = 1/√m and κ = δ√m, so that 1/ε² = m and κε = δ.
2. m ≥ 150 > 144 gives ε ≤ 1/12.
3. `kappa_identity` with q² ≤ 1 and δ ≥ 0 gives κ ≤ 1/5.
4. By `split`, `Pos_ge`, `Neg_mono` and `corner_margin`: ε⁶U₋ ≥ 959747/17496.
5. Then m³ε⁶ = 1.

The hypotheses are TARGET.md's own: δ ≥ 0 defined by (1 + 2mδ)² = 1 + 4mq²/25, and q² ≤ 1, which covers q ∈ [0, 1].

## Checks

- **Oracle** (`oracle/check_lemmaU.py`, exact sympy except item 8): all 13 checks hold.
  1. The file's own `Um`, `Pos` and `Neg`, parsed, equal TARGET.md's U₋ (transcribed separately).
  2. The split holds.
  3. Both parts have positive coefficients.
  4. `Neg` equals RESULT.md's nine monomials.
  5. The κ factorisation holds.
  6. The corner value and margin are RESULT.md's numbers, and 1/12 ≥ 150^(−1/2).
  7. RESULT.md's control NC-A1d gives 64 − Neg(1/2, 1/5, 2) = −33488.
  8. A 125-point grid gives U₋/m³ ≥ 959747/17496, with the smallest excess 9.18.
- **Build:**
  - compile: exit 0, 4 s, 0 errors, 0 warnings, 0 sorry;
  - axioms: 10/10 theorems use only propext, Classical.choice and Quot.sound;
  - negative controls: both rejected;
  - mutations: 10/10 pass the judge.
- **Registration against the run: all ten agree in full.**
  - `review/LEMMAU_MUTATION_REGISTRATION.md` (sha256 `b4f9104a…`) was written at 13:03:00Z. The build logged it at
    13:04:07Z, before the first mutation run.
  - First failure, exact failing set, and the three registered error texts all agree.
  - The registered texts are all "linarith failed to find a contradiction", for LUM4–LUM6.
  - Texts were registered only for small `linarith` goals. The other messages turned out to be "Application type
    mismatch: …", "mod_cast has type …" and "unsolved goals". None was registered.
- **What the mutations show.** Each of the lemma's ingredients is load-bearing:
  - U₋'s coefficient (LUM1);
  - Pos's constant (LUM2);
  - a Neg monomial (LUM3);
  - the κ identity (LUM4);
  - the threshold m ≥ 150 (LUM5) and ℓ ≥ 11 (LUM10);
  - the bounds κ ≤ 1/5 (LUM6), x ≤ 2 (LUM7) and ε ≤ 1/12 (LUM8);
  - the corner value (LUM9).

  Changing any one of them breaks exactly the registered declarations.

**Not proved here:**
- Part I of P1, ℓ = 3…10, which is a Bernstein certificate;
- the E0 check that TARGET.md's U₋ is S5's, which is in the A1 and extremal layers;
- the reduction from the potential to the quadratic form, which is item (a).

## Files

| file | content |
|---|---|
| `lean/BHModesLemmaU.lean` | 10 theorems |
| `lean/build.sh` | the audited build: the item (e) script with names changed |
| `lean/mutations.json`, `lean/vendor/` (byte copy, `696b7864…`), `lean/SOURCES.tsv`, `lean/lean-toolchain` | the specs, the vendored judge, the source hash |
| `lean/BUILD_LOG.txt`, `lean/build_stdout.txt`, `lean/logs/` | the build of record |
| `review/LEMMAU_MUTATION_REGISTRATION.md`, `review/REGISTRATION_TIME.txt` | predictions, written and hashed before the run |
| `oracle/check_lemmaU.py`, `oracle/check_lemmaU.out` | the independent checks and their run of record |
| `SHA256SUMS` | every file except itself |

The build outputs (`build/`) were left on the node; `lean/build.sh` regenerates them.
