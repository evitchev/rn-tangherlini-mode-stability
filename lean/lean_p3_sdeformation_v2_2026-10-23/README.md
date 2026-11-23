# Lean layer, item (a), labelled build v2: Proposition 3 with P needed only on (0, 1) (bh-modes): session-L, 2026-10-23

This answers the bh-modes lead's optional item of 2026-10-23, which arose from the session-R lead's reading
(BHM-085, §1.3). The statement is that of `results/p3/METHOD_ADDENDUM_2.md` (BHM-086), which I read first, as asked.
- **The first build stays on the record, unchanged:** `lean_p3_sdeformation_2026-10-22` (SHA256SUMS `cd718ac9…`), with
  its erratum `lean_p3_sdeformation_erratum_2026-10-23` (`7e3542e7…`).
- **This build's result: "BHModesP3: ALL CHECKS AS REQUIRED"** (`lean/BUILD_LOG.txt`). 15/15 mutations pass the judge,
  and all fifteen agree with the registration in full.
- **Oracle.** "ALL P3 V2 CHECKS HOLD (16/16)" (`oracle/check_p3v2.out`).
- **Host.** The build of record and the oracle's run of record ran on the reproduction node of the bh-modes
  environment, under `nice -n 19`. The Lean copy there is described in `../lean_1c_tail_v2_2026-10-23/README.md`.

## What changed

- **Lines 1–392 of `lean/BHModesP3.lean` are the first build's, byte for byte.** Oracle check 1 compares the prefix's
  sha256. Line references into the first build stay valid, such as `:211` (`prop3`'s hP) and `:356` (`prop3_D6`).
- **Lines 393–521 are new:** six theorems and two definitions. The file now has 33 theorems, up from 27.
- **Byte copies of the first build:** `build.sh`, `lean-toolchain` and the vendored judge.
- **`mutations.json`** keeps the first build's nine specs byte for byte and adds six.

## The new statements (quoted from `lean/BHModesP3.lean`)

**`prop3_Ioo`** (l. 403–411), Proposition 3 with P C¹ on (0, 1) only:

    theorem prop3_Ioo (U H F F' P P' R : ℝ → ℝ)
        (hF : ∀ z, HasDerivAt F (F' z) z) (hP : ∀ z, 0 < z → z < 1 → HasDerivAt P (P' z) z)
        (hF' : Continuous F') (hP' : ContinuousOn P' (Set.Ioo 0 1)) (hU : Continuous U) (hHc : Continuous H)
        (hR : ∀ t, HasDerivAt R (F (zc (R t))) t) (hR1 : ∀ t, 1 < R t) (hf : ∀ z, 0 < z → z < 1 → 0 ≤ F z)
        (hH : ∀ z, 0 < z → z < 1 → H z ≠ 0)
        (hN : ∀ z, 0 < z → z < 1 → 0 ≤ Nz U H F F' P P' z)
        (φ φ' : ℝ → ℂ) (hφ : ∀ x, HasDerivAt φ (φ' x) x) (hφ' : Continuous φ')
        (hc : HasCompactSupport φ) :
        0 ≤ ∫ t, (‖φ' t‖ ^ 2 + Vrho U H F (R t) * ‖φ t‖ ^ 2)

It differs from `prop3` in exactly two hypotheses. Every other binder and the conclusion are identical, and oracle
check 2 compares them binder by binder.

| | `prop3` (l. 211–212) | `prop3_Ioo` (l. 404–405) |
|---|---|---|
| `hP` | `∀ z, HasDerivAt P (P' z) z` | `∀ z, 0 < z → z < 1 → HasDerivAt P (P' z) z` |
| `hP'` | `Continuous P'` | `ContinuousOn P' (Set.Ioo 0 1)` |

- **Why hP′ changes too.** A ζ-design's P′ has the same pole as P, so `Continuous P'` fails as well. The lead's item
  names hP. The proof needs both relaxed.
- **How the proof stays inside (0, 1).** It uses P and P′ only at zc(R t), and R t > 1 puts zc(R t) in (0, 1)
  (`zc_mem`).
  - The continuity of t ↦ P(zc(R t)) and t ↦ P′(zc(R t)) comes from `ContinuousOn.comp_continuous`.
  - The chain rule uses hP at zc(R t).
  - Everything else is `prop3`'s proof, unchanged.
- **F, U and H keep `prop3`'s hypotheses on all of ℝ.** At every n they are polynomials in z for fixed parameters:
  f = 1 − x + q²x²/4, H₋ is (5.62b), and U₋ is (5.63b), a quartic in x (`code/ki/potentials.py`), with
  x = x_H(1 − z)^{n−1}.

**`prop3_near`** (l. 449–459), METHOD_ADDENDUM_2's form "P C¹ on an open interval containing [0, 1]". This is
`prop3_Ioo` with these binders in place of hP and hP′:

    (a b : ℝ) (ha : a < 0) (hb : 1 < b)
    (hP : ∀ z, a < z → z < b → HasDerivAt P (P' z) z)
    (hP' : ContinuousOn P' (Set.Ioo a b))

The rest is identical (oracle check 3). It is a corollary of `prop3_Ioo`.

**The ζ-designs** (l. 461–504):

    noncomputable def Pzeta (Ph : ℝ → ℝ) (δ : ℝ) (d : ℕ) (z : ℝ) : ℝ := Ph z / (z + δ) ^ d
    noncomputable def Pzeta' (Ph Ph' : ℝ → ℝ) (δ : ℝ) (d : ℕ) (z : ℝ) : ℝ :=
      (Ph' z * (z + δ) - d * Ph z) / (z + δ) ^ (d + 1)

| theorem | exact statement (binder types omitted) |
|---|---|
| `Pzeta_hasDerivAt` | `HasDerivAt Ph (Ph' z) z → 0 < z + δ → HasDerivAt (Pzeta Ph δ d) (Pzeta' Ph Ph' δ d z) z` |
| `Pzeta'_continuousOn` | `0 ≤ δ → Continuous Ph → Continuous Ph' → ContinuousOn (Pzeta' Ph Ph' δ d) (Set.Ioo 0 1)` |
| `prop3_zeta` | `prop3_Ioo` with P := `Pzeta Ph δ d` and P′ := `Pzeta' Ph Ph' δ d`, for any `δ ≥ 0`, any `d : ℕ` and any Ph with derivative Ph′ everywhere and Ph′ continuous. Its hN is `∀ z, 0 < z → z < 1 → 0 ≤ Nz U H F F' (Pzeta Ph δ d) (Pzeta' Ph Ph' δ d) z`. |

- HD-S's P̂ is a polynomial in z for each μ in a box, and δ = δ_b > 0, so `prop3_zeta` applies.
- Oracle checks 5–6 confirm with sympy that the file's own `Pzeta'` is the derivative of its `Pzeta`. Check 7 confirms
  that P3M12's variant is not.

**`pole_not_differentiable`** (l. 506–519): why the restatement was needed.

    theorem pole_not_differentiable (δ : ℝ) (P' : ℝ → ℝ) : ¬ ∀ z, HasDerivAt (Pzeta (fun _ => 1) δ 1) (P' z) z

For the ζ-design P = 1/(z + δ), no P′ meets `prop3`'s hypothesis hP: P is not continuous at its pole z = −δ.

**What `prop3_Ioo` also covers.** `prop3_zeta` allows δ = 0, a pole at the horizon z = 0, which lies outside the open
interval (0, 1).
- So it covers a P such as a/z + p(z): that is `Pzeta (fun z => a + z * p z) 0 1`, for p C¹.
- The reading lists this singular ansatz for A2 (its registration item 2: "Lean's `prop3` must be restated on (0, 1)").
- `prop3_near` does not cover it: no open interval around [0, 1] avoids z = 0.
- This is a statement about the reduction only. Whether such a P gives N ≥ 0 on (0, 1) is the design's question.

## What this does not prove

- **General n.** `prop3_Ioo` is generic in U, H and F, so it applies at n = 5…9. The facts that discharge its
  hypotheses on f, f_z, U₋ and H₋ at general n are not in Lean, though: differentiability and continuity, f ≥ 0 on
  (0, 1) and H₋ ≠ 0 there. `prop3_D6` discharges them at n = 4 only. A `prop3_Dn` instance would need f, H₋ and U₋ at
  general n, and it is not done here.
- **The certificate's step.** METHOD_ADDENDUM_2 goes from N·L·(z + δ_b)^{2d} > 0 on [0, 1] × box to N > 0 on [0, 1].
  That step is not in Lean.
- **The rest, as in the first build's README:** the existence of the inverse tortoise map R, C^∞ smoothness, the
  scaling to absolute units, that the form determines A, and N ≥ 0 for a concrete P.

## Checks

- **Oracle** (`oracle/check_p3v2.py`, sympy 1.14.0; run of record on the reproduction node): all 16 checks hold.
  1. Lines 1–392 are the first build's (prefix sha256 `70d14327…`). The new section starts at l. 393, and the file
     ends with the namespace.
  2. `prop3_Ioo` has `prop3`'s binders in order, and only hP and hP′ differ. The conclusions are identical.
  3. `prop3_near` adds exactly (a b), ha and hb, and only hP and hP′ differ from `prop3_Ioo`. The conclusions are
     identical.
  4. `prop3_zeta` keeps every binder of `prop3_Ioo` that does not name P, P′ or the ζ data. Its hN is `prop3_Ioo`'s
     with P, P′ replaced by `Pzeta`, `Pzeta'`. The conclusions are identical.
  5. The file's own `Pzeta'` is d/dz of its own `Pzeta` for d = 0, …, 12, with P̂ an undefined function.
  6. The same holds for symbolic d.
  7. Control: P3M12's variant, (d + 1)P̂, is not the derivative for any d = 0, …, 12.
  8. 1/(z + δ) → +∞ as z → −δ from above.
- **Build** (`lean/BUILD_LOG.txt`):
  - compile: exit 0, 5 s, 0 errors, 0 warnings, 0 sorry;
  - axioms: 33/33 theorems use only propext, Classical.choice and Quot.sound;
  - negative controls: both rejected;
  - mutations: 15/15 pass the judge.
- **Registration against the run: all fifteen agree in full.**
  - `review/P3_MUTATION_REGISTRATION.md` (sha256 `aaecce3c…`) was written and hashed at 17:32:03Z. The build started at
    17:32:15Z and logged the hash at 17:32:34Z, before the first mutation run.
  - First failure, exact failing set and the judge's pass all agree, as do the five registered error texts (P3M1, P3M5,
    P3M7, P3M13, P3M14).
  - **P3M1–P3M9 are not blind,** and the registration says so. They are the first build's specs and predictions. The
    one change is that P3M9's failing set gains `prop3_Ioo`, which shares `prop3`'s step `e`. That came out as
    registered.
  - **P3M10–P3M15 are new.** No mutated copy was compiled before the registration was hashed.
- **What the new mutations show:**
  - **P3M10, P3M11.** The proof uses hP and hP′ on all of (0, 1). Restricting either to (0, 1/2) breaks exactly
    `prop3_Ioo`, and for hP′ also `prop3_zeta`, which passes a statement on (0, 1).
  - **P3M12.** A wrong derivative formula breaks `Pzeta_hasDerivAt`, in both branches, d = 0 and d = k + 1.
  - **P3M13.** Allowing δ ≥ −1/2, so that the pole may lie in (0, 1), breaks `prop3_zeta`.
  - **P3M14.** An interval that need not contain (0, 1) (a < 1/2) breaks `prop3_near`.
  - **P3M15.** Removing the pole (d = 0) makes `pole_not_differentiable` false, and its proof fails.
- **Details the registration did not fix:**
  - P3M10 gave three errors in `prop3_Ioo`. Two are the type mismatches I named, at l. 420 and l. 429. The third is an
    unsolved goal `z < 1 / 2` that Lean's error recovery left behind from the first, reported at the theorem's `by`.
  - In P3M13, the type mismatch at l. 503 is reported before the `linarith` failure at l. 502. Tactic blocks run at the
    end of a term's elaboration, as the registration's note says.

## Host and environment

- **The build of record and the oracle** ran on the reproduction node, as the operator ruled for runs of record. The
  folder there was identical to this one before the run (10 files, by sha256). The build's inputs were unchanged after
  it. The logs and `oracle/check_p3v2.out` were copied back here.
- **Development on the editing node:**
  - three compiles of the unmutated file (the first failed in my draft, in a `fun_prop` step and the d = 0 branch);
  - one probe file for lemma names;
  - one development run of the oracle, which gave 16/16.

  No mutation was run there.

## Files

| file | content |
|---|---|
| `lean/BHModesP3.lean` | v2 source: 33 theorems, namespace `BHModes.P3`; lines 1–392 the first build's |
| `lean/build.sh`, `lean/lean-toolchain`, `lean/vendor/` | byte copies of the first build's (judge `696b7864…`) |
| `lean/mutations.json` | the first build's nine specs, byte for byte, and P3M10–P3M15 |
| `lean/SOURCES.tsv` | the v2 source hash and its origin |
| `lean/BUILD_LOG.txt`, `lean/build_stdout.txt`, `lean/logs/` | the build of record |
| `review/P3_MUTATION_REGISTRATION.md`, `review/REGISTRATION_TIME.txt` | predictions, written and hashed before the run |
| `oracle/check_p3v2.py`, `oracle/check_p3v2.out` | the checks outside Lean, and their run of record |
| `SHA256SUMS` | every file except itself |

- `build.sh` is the first build's, so its log header still reads "item (a)". This build is v2 by its folder and
  `SOURCES.tsv`.
- The build outputs (`build/`) were left on the node; `lean/build.sh` regenerates them in about a minute and a half.
