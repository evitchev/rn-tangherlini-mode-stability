# Lean layer, item (a), labelled build v3: Proposition 3 at general n (bh-modes): session-L, 2026-10-23

This answers the bh-modes lead's request in the v2 receipt (BHM-090): `prop3_Dn`, the general-n instance, as
`prop3_D6` is at n = 4, with K = 1, Λ = 0 and q² ≤ 1. U₋ is S5 (5.63b) at y = 0 in my transcription from the c_n
build, as the lead specified. The step N·L·s^{2e} > 0 ⇒ N > 0 stays out, as agreed.
- **The earlier builds stay on the record, unchanged:**
  - v2, `lean_p3_sdeformation_v2_2026-10-23` (SHA256SUMS `a6fd891d…`);
  - the first build, `lean_p3_sdeformation_2026-10-22` (`cd718ac9…`), with its erratum.
- **This build's result: "BHModesP3: ALL CHECKS AS REQUIRED"** (`lean/BUILD_LOG.txt`). 24/24 mutations pass the judge,
  and all twenty-four agree with the registration in full.
- **Oracle.** "ALL P3 V3 CHECKS HOLD (20/20)" (`oracle/check_p3v3.out`).
- **Host.** The build of record and the oracle's run of record ran on the reproduction node of the bh-modes
  environment, under `nice -n 19`.

## What changed

- **Lines 1–520 of `lean/BHModesP3.lean` are v2's, byte for byte** (oracle check 1). Every line reference into v2
  stays valid.
- **Lines 521–682 are new:** seven definitions and fourteen theorems. The file now has 47 theorems.
- **Byte copies of the earlier builds:** `build.sh`, `lean-toolchain` and the vendored judge.
- **`mutations.json`** keeps v2's fifteen specs byte for byte and adds nine.

## The data at general n (quoted)

`HmN` and `UmN` are the c_n layer's `Hm` and `Um` (`../lean_cn_2026-10-23/lean/BHModesCn.lean`), renamed, with bodies
byte for byte (oracle check 2). The names `Hm` and `Um` already belong to the n = 4 polynomials in this file.

    noncomputable def HmN (n m δ x : ℝ) : ℝ := m + n * (n + 1) / 2 * (1 + m * δ) * x
    noncomputable def UmN (n K m δ x y : ℝ) : ℝ := …   -- S5 (5.63b) with K and y, l. 533–542
    noncomputable def xn (n : ℕ) (q z : ℝ) : ℝ := xH q * (1 - z) ^ (n - 1)
    noncomputable def Fn (n : ℕ) (q z : ℝ) : ℝ := 1 - xn n q z + q ^ 2 * xn n q z ^ 2 / 4
    noncomputable def Fn' (n : ℕ) (q z : ℝ) : ℝ := (n - 1) * xH q * (1 - z) ^ (n - 2) * (1 - q ^ 2 * xn n q z / 2)
    noncomputable def Hn (n : ℕ) (q m δ z : ℝ) : ℝ := HmN n m δ (xn n q z)
    noncomputable def Un (n : ℕ) (q m δ z : ℝ) : ℝ := UmN n 1 m δ (xn n q z) 0

Here n is a natural number, so (1 − z)^(n−1) is an ordinary power. `xH q` = 2/(1 + √(1 − q²)) is the file's own.

## The new statements

**`prop3_Dn`** (l. 638–644):

    theorem prop3_Dn (n : ℕ) (hn : 2 ≤ n) (q m δ : ℝ) (hq : q ^ 2 ≤ 1) (hm : 0 < m) (hδ : 0 ≤ δ) (P P' R : ℝ → ℝ)
        (hP : ∀ z ∈ Set.Ioo (0 : ℝ) 1, HasDerivAt P (P' z) z) (hP' : ContinuousOn P' (Set.Ioo (0 : ℝ) 1))
        (hR : ∀ t, HasDerivAt R (Fn n q (zc (R t))) t) (hR1 : ∀ t, 1 < R t)
        (hN : ∀ z, 0 < z → z < 1 → 0 ≤ Nz (Un n q m δ) (Hn n q m δ) (Fn n q) (Fn' n q) P P' z)
        (φ φ' : ℝ → ℂ) (hφ : ∀ x, HasDerivAt φ (φ' x) x) (hφ' : Continuous φ')
        (hc : HasCompactSupport φ) :
        0 ≤ ∫ t, (‖φ' t‖ ^ 2 + Vrho (Un n q m δ) (Hn n q m δ) (Fn n q) (R t) * ‖φ t‖ ^ 2)

- **Relation to `prop3_D6`.** Under (U6, H6, F6, F6′) → (Un, Hn, Fn, Fn′) it is `prop3_D6`'s statement, with n and
  hn added and with hP and hP′ needed only on (0, 1), as in `prop3_Ioo` (oracle check 9).
- **Why hP and hP′ use set membership.** They are written as z ∈ (0, 1) rather than `0 < z → z < 1 → …`. This is the
  same hypothesis, but it keeps the text of mutations P3M10 and P3M11 unique in the file.
- **What it discharges itself:**
  - the derivative of f (`Fn_hasDerivAt`);
  - the continuity of f_z, U₋ and H₋;
  - f ≥ 0 on (0, 1) (`Fn_pos`);
  - H₋ ≠ 0 there (`Hn_pos`).
- **What remains a hypothesis:** n ≥ 2, q² ≤ 1, m > 0 and δ ≥ 0; P C¹ on (0, 1); the map R; N ≥ 0 on (0, 1); and φ.
- **δ's link to q is not used.** Since (1 + 2mδ)² = 1 + 4mq²/(n + 1)² is never needed, the theorem holds for every
  δ ≥ 0.

**The other theorems** (exact statements; binder types omitted):

| theorem | statement |
|---|---|
| `prop3_Dn_zeta` | `prop3_Dn` with P := `Pzeta Ph δb d` and P′ := `Pzeta' Ph Ph' δb d`, for δb ≥ 0 and Ph C¹ (HD-S's ζ-bands; δb is the shift δ_b, and δ stays S5's) |
| `Fn_hasDerivAt` | `1 ≤ n → HasDerivAt (Fn n q) (Fn' n q z) z` |
| `Fn_zero` | `q ^ 2 ≤ 1 → Fn n q 0 = 0`, for every n (the horizon) |
| `Fn_pos` | `2 ≤ n → q ^ 2 ≤ 1 → 0 < z → z < 1 → 0 < Fn n q z` |
| `Hn_pos` | `0 < m → 0 ≤ δ → z ≤ 1 → 0 < Hn n q m δ z` |
| `xn_zc` | `xn n q (zc ρ) = xH q / ρ ^ (n - 1)` |
| `Fn_zc_TARGET` | `M * (1 + Real.sqrt (1 - q ^ 2)) = 1 → Fn n q (zc ρ) = 1 - 2 * M / ρ ^ (n - 1) + (q * M) ^ 2 / (ρ ^ (n - 1)) ^ 2`, i.e. TARGET_HD.md's f in units r_H = 1 |
| `Vrho_Dn` | `Vrho (Un n q m δ) (Hn n q m δ) (Fn n q) ρ` is TARGET_HD.md's V = f U₋/(64r²H₋²) at r = ρ, x = x_H/ρ^(n−1) |
| `N_at_horizon_Dn` | `q ^ 2 ≤ 1 →` N(0) = `Un n q m δ 0 - 64 * Hn n q m δ 0 ^ 2 * Fn' n q 0 * P 0` |
| `N_at_infinity_Dn` | `2 ≤ n →` N(1) = `64 * m ^ 2 * (m + n * (n + 2) / 4 - P 1 ^ 2 + P 1)` (at n = 4 this is `N_at_infinity_D6`'s m + 6) |
| `HmN_four` | `HmN 4 m δ x = Hm m δ x` |
| `UmN_four` | `UmN 4 1 m δ x 0 = Um m δ x`: the general-n U₋ at n = 4 is TARGET.md's U₋ |
| `Dn_four` | `Fn 4 q = F6 q ∧ Fn' 4 q = F6' q ∧ Hn 4 q m δ = H6 q m δ ∧ Un 4 q m δ = U6 q m δ` |

So at n = 4, `prop3_Dn` is `prop3_D6` with the weaker hypothesis on P, about the same f, f_z, H₋ and U₋.

## The transcription of S5 (5.63b)

The lead's choice is the c_n build's transcription, and it is used unchanged. Three checks bear on it here:
- **In Lean:** `UmN_four` and `HmN_four` show that at n = 4 it reduces to TARGET.md's U₋ and H₋, which the A1 and
  extremal layers already use.
- **Oracle check 3:** symbolically in n and K, it equals the bh-modes lead's own transcription in
  `code/ki/potentials.py` (`U_minus`, `H_minus`). That is a second hand. Kimi's transcription agreed with the lead's
  (BHM-036).
- **The potential check of 2026-10-22:** the same transcription agreed term by term with 1001.0019's eqs. (9) and (11).

What none of these checks is the reading of S5's printed pages themselves.

## What this does not prove

- **The certificate's step** N·L·s^{2e} > 0 on [0, 1] × box ⇒ N > 0 on [0, 1], as agreed.
- **As in the first build's README:** the existence of the inverse tortoise map R, C^∞ smoothness, the scaling to
  absolute units, that the form determines A, and N ≥ 0 for a concrete P.
- **D ≥ 4 only.** The instance is stated for n ≥ 2. `Fn_pos` is false at n = 1, where f ≡ 0: oracle check 8's control gives the
  counterexample, and mutation P3M19 shows that the proof needs n ≥ 2.

## Checks

- **Oracle** (`oracle/check_p3v3.py`, sympy 1.14.0; run of record on the reproduction node): all 20 checks hold.
  1. Lines 1–520 are v2's (prefix sha256 `eb9af1c1…`). The v3 section starts at l. 521, and the file ends with the
     namespace.
  2. The bodies of `HmN` and `UmN` are the c_n layer's, byte for byte.
  3. The file's own `UmN` (at y = 0) and `HmN` equal the lead's `potentials.py` transcription, symbolically in n and K.
  4. At n = 4 they equal the file's own TARGET.md `Um` and `Hm`, independently of `UmN_four` and `HmN_four`.
  5. `Fn'` is d/dz `Fn` for n = 2, …, 12.
  6. `Fn` at z = 1 − 1/ρ is TARGET_HD's f, with x_H = 2M, for n = 2, …, 12.
  7. METHOD's N at z = 1, built from the parsed definitions, is 64m²(m + n(n + 2)/4 − P² + P) for n = 2, …, 12.
  8. Signs, using exact rational arithmetic on a grid:
     - f(0) = 0;
     - f > 0 (smallest value 0.0025);
     - H₋ > 0 (smallest 0.1);
     - the three controls behind P3M19–P3M21: f = 0 at n = 1, f(0) = 1 at q² = 2, and H₋ = 0 at z = 1, m = 0.
  9. `prop3_Dn`'s binders are `prop3_D6`'s under the renaming, plus n and hn, with hP and hP′ in `prop3_Ioo`'s form.
     The conclusions agree.
- **Build** (`lean/BUILD_LOG.txt`):
  - compile: exit 0, 6 s, 0 errors, 0 warnings, 0 sorry;
  - axioms: 47/47 theorems use only propext, Classical.choice and Quot.sound;
  - negative controls: both rejected;
  - mutations: 24/24 pass the judge.
- **Registration against the run: all twenty-four agree in full.**
  - `review/P3_MUTATION_REGISTRATION.md` (sha256 `ad90732f…`) was written and hashed at 17:50:47Z. The build started at
    17:50:53Z and logged the hash at 17:51:18Z, before the first mutation run.
  - First failure, exact failing set and the judge's pass all agree, as do the six registered error texts (P3M1,
    P3M5, P3M7, P3M13 and P3M14 as in v2, and P3M22's new "unsolved goals").
  - **P3M1–P3M15 are not blind,** and the registration says so. Five of their failing sets gained a new theorem, each
    as predicted:
    - P3M1 gained `N_at_infinity_Dn`;
    - P3M7 gained `Dn_four`;
    - P3M9 gained `Vrho_Dn`;
    - P3M10 and P3M11 gained `prop3_Dn`.
  - **P3M16–P3M24 are new.** No mutated copy was compiled before the registration was hashed.
- **What the new mutations show:**
  - **P3M16 and P3M17.** A wrong coefficient in the general-n U₋ or H₋ breaks the reduction to TARGET.md at n = 4.
    P3M16 is bh-modes' own td-coeff control, 16n(n + 3)m²K. It also breaks N(1).
  - **P3M18.** A wrong f_z breaks `Fn_hasDerivAt` and its agreement with `F6'`.
  - **P3M19–P3M21.** Each hypothesis that makes f > 0, f(0) = 0 and H₋ > 0 true is needed: n ≥ 2, q² ≤ 1 and m > 0.
    Each mutated statement is false. Oracle check 8's controls give the counterexamples.
  - **P3M22 and P3M23.** TARGET_HD's f and the value N(1) are checked.
  - **P3M24.** `prop3_Dn` uses hP on all of (0, 1).
- **Error texts the registration did not fix,** for the record:
  - P3M19: "omega could not prove the goal:";
  - P3M21: "failed to prove strict positivity, but it would be possible to prove nonnegativity if desired";
  - P3M23: "unsolved goals". Its text was left unregistered out of caution about the size of `UmN`, but `ring`'s
    fallback finished normally.

## Host and environment

- **The build of record and the oracle** ran on the reproduction node. The folder there was identical to this one
  before the run (10 files, by sha256). The build's inputs were unchanged after it. The logs and
  `oracle/check_p3v3.out` were copied back here.
- **Development on the editing node:**
  - two compiles of the unmutated file, both clean;
  - one probe file for three lemma names;
  - one development run of the oracle, which gave 20/20.

  No mutation was run there.

## Files

| file | content |
|---|---|
| `lean/BHModesP3.lean` | v3 source: 47 theorems, namespace `BHModes.P3`; lines 1–520 v2's |
| `lean/build.sh`, `lean/lean-toolchain`, `lean/vendor/` | byte copies of the earlier builds' (judge `696b7864…`) |
| `lean/mutations.json` | v2's fifteen specs, byte for byte, and P3M16–P3M24 |
| `lean/SOURCES.tsv` | the v3 source hash and its origin |
| `lean/BUILD_LOG.txt`, `lean/build_stdout.txt`, `lean/logs/` | the build of record |
| `review/P3_MUTATION_REGISTRATION.md`, `review/REGISTRATION_TIME.txt` | predictions, written and hashed before the run |
| `oracle/check_p3v3.py`, `oracle/check_p3v3.out` | the checks outside Lean, and their run of record |
| `SHA256SUMS` | every file except itself |

- `build.sh` is the first build's, so its log header still reads "item (a)". This build is v3 by its folder and
  `SOURCES.tsv`.
- The build outputs (`build/`) were left on the node; `lean/build.sh` regenerates them in under three minutes.
