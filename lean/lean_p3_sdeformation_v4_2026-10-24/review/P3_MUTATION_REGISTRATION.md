# p3 Lean layer, labelled build v4: registered predictions for mutations P3M1 to P3M37 (session-L, 2026-10-24, before any mutation run)

I wrote this file before running any mutation of the v4 `lean/BHModesP3.lean`. Each spec was checked only as text:
its old string occurs exactly once in the v4 file. `lean/build.sh` (a byte copy of the first build's) records this
file's sha256 in `BUILD_LOG.txt` before the first mutation run. The record binds once that hash reaches the bh-modes
lead.

**Predicted against:**
- `lean/BHModesP3.lean`, sha256 `bcbff2b0…` (`lean/SOURCES.tsv`).
  - Lines 1–681 are the v3 build's, byte for byte.
  - Lines 682–900 are new: the bh-modes lead's message 7, §3, items (a) and (b).
  - (a) G-RES: the definitions `mEll`, `dEll`, `Pres` and `Pres'`, and the theorems `mEll_dEll_S5`, `D6_extremal`,
    `Pres_hasDerivAt`, `H2_ell`, `U2_ell`, `g_res` and `g_res_tendsto`.
  - (b) the D = 4 Darboux identities: the definitions `f4`, `VKI4`, `VRW4` and `W4`, and the theorems `W4_deriv`,
    `darboux_KI`, `darboux_RW`, `H_zero_iff` and `RW_regular_at_r0`.
- `lean/mutations.json`, sha256 `f2e68aee…`. Its first twenty-four specs are v3's, byte for byte. P3M25 to P3M37 are
  new.
- The vendored judge `lean/vendor/mutation.py` (`696b7864…`), the same byte copy as before.

**What is and is not blind.**
- **P3M1 to P3M24 are not blind.** They ran in v3, and all twenty-four came out as registered. Their predictions carry
  over, except where a new theorem joins a failing set (marked "new member" below).
- **P3M25 to P3M37 are new.** No mutated copy has been compiled.
  - The unmutated v4 file was compiled on the editing node. Two development versions of the new section failed
    before the final one compiled clean. None of them was a mutated copy.
    - The first had four faults. `field_simp` left the factor mr + 6M in its normal form, so the proofs now name it
      with `set`. `fun_prop`'s side condition at r₀ needed a different discharger. One lemma had a hypothesis it did
      not use (a linter warning). A closing `ring` came after `field_simp` had already closed the goal.
    - The second had one: a `field_simp` step needed a closing `ring`.
  - One probe file checked lemma names and two tactic calls. A copy of the final file with `#count_heartbeats` before
    each new theorem measured at most 30,000 heartbeats (`g_res`); the limit is 200,000.
  - The oracle's section 5 ran before this registration, on the editing node. It checks in sympy that each new mutated
    statement is false. It says nothing about how Lean fails.

**What Lean does with a failed theorem.**
- A failed proof is kept with sorry, and later uses of it still elaborate. So a theorem that uses another theorem only
  as a statement keeps compiling when that statement is unchanged.
- A theorem fails if it unfolds a changed definition, uses a changed statement in a proof step, or passes its own
  hypothesis where a changed one is expected.
- A `have` whose proof fails is kept with sorry inside its theorem, so the rest of that proof still elaborates.
- Tactic blocks inside a term run at the end of its elaboration. Within one declaration, errors appear in that
  order, and across declarations, in file order.

| id | mutation | first failure | failing set (exactly) | judge-checked error text | why |
|---|---|---|---|---|---|
| P3M1 | `Nz`: 64H² → 63H² | `ansatz_identity` | {`ansatz_identity`, `N_at_horizon`, `N_eps_shift`, `N_at_infinity_D6`, `N_at_infinity_Dn`, `g_res`} | "unsolved goals" (at `ansatz_identity`) | New member: `g_res`, whose first case unfolds `Nz`, so its closing `ring` meets 63H² against the polynomial's 64H². `g_res_tendsto` uses `g_res` only as a statement. |
| P3M2 | `sdef_identity` with V − S′ − S² | `sdef_identity` | {`sdef_identity`, `form_nonneg_of_sdef`} | (not checked) | As in v3. |
| P3M3 | `beta_hasDerivAt` with +P | `beta_hasDerivAt` | {`beta_hasDerivAt`, `Srho_hasDerivAt`} | (not checked) | As in v3. |
| P3M4 | `zc_hasDerivAt` with (1 − z)³ | `zc_hasDerivAt` | {`zc_hasDerivAt`, `f_hasDerivAt`, `beta_hasDerivAt`} | (not checked) | As in v3. |
| P3M5 | `N_at_infinity_D6` with m + 5 | `N_at_infinity_D6` | {`N_at_infinity_D6`, `N_at_infinity_ell2`} | "unsolved goals" (at `N_at_infinity_D6`) | As in v3. |
| P3M6 | `N_at_infinity_ell2` with −4 < P(1) | `N_at_infinity_ell2` | {`N_at_infinity_ell2`} | (not checked) | As in v3. |
| P3M7 | `F6'`: 3x_H → 2x_H | `F6_hasDerivAt` | {`F6_hasDerivAt`, `Dn_four`, `D6_extremal`} | "unsolved goals" (at `F6_hasDerivAt`) | New member: `D6_extremal`, which unfolds `F6'`; its third part now asks 4(1 − z)²(…) = 6(1 − z)²(…). `g_res` uses `D6_extremal` only as a statement. |
| P3M8 | `prop3` assuming 0 ≤ f_z | `prop3` | {`prop3`, `prop3_D6`} | (not checked) | As in v3. |
| P3M9 | `Vrho` with 64ρ³ | `prop3` | {`prop3`, `Vrho_D6`, `prop3_Ioo`, `Vrho_Dn`} | (not checked) | As in v3. Nothing in v4 uses `Vrho`. |
| P3M10 | `prop3_Ioo` with hP only on (0, 1/2) | `prop3_Ioo` | {`prop3_Ioo`, `prop3_Dn`} | (not checked) | As in v3. |
| P3M11 | `prop3_Ioo` with hP′ only on (0, 1/2) | `prop3_Ioo` | {`prop3_Ioo`, `prop3_zeta`, `prop3_Dn`} | (not checked) | As in v3. |
| P3M12 | `Pzeta'` with (d + 1)P̂ | `Pzeta_hasDerivAt` | {`Pzeta_hasDerivAt`} | (not checked) | As in v3. |
| P3M13 | `prop3_zeta` with −1/2 ≤ δ | `prop3_zeta` | {`prop3_zeta`} | "linarith failed to find a contradiction" (at `prop3_zeta`) | As in v3. |
| P3M14 | `prop3_near` with a < 1/2 | `prop3_near` | {`prop3_near`} | "linarith failed to find a contradiction" (at `prop3_near`) | As in v3. |
| P3M15 | `pole_not_differentiable` at d = 0 | `pole_not_differentiable` | {`pole_not_differentiable`} | (not checked) | As in v3. |
| P3M16 | `UmN`: 16n(n + 2)m²K → 16n(n + 3)m²K | `UmN_four` | {`UmN_four`, `N_at_infinity_Dn`, `darboux_KI`} | (not checked) | New member: `darboux_KI`, which unfolds `UmN` at n = 2; U₋'s term 128m² becomes 160m². |
| P3M17 | `HmN`: n(n + 1) → n(n + 2) | `HmN_four` | {`HmN_four`, `darboux_KI`, `H_zero_iff`} | (not checked) | New members: `darboux_KI` and `H_zero_iff`. Each proves H₋ = (mr + 6M)/r in a local `have` by unfolding `HmN`, and at n = 2 the mutated H₋ is m + 8M/r. `RW_regular_at_r0` uses `H_zero_iff` only as a statement. |
| P3M18 | `Fn'`: (n − 1) → n | `Dn_four` | {`Dn_four`, `Fn_hasDerivAt`} | (not checked) | As in v3. |
| P3M19 | `Fn_pos` from 1 ≤ n | `Fn_pos` | {`Fn_pos`, `prop3_Dn`} | (not checked) | As in v3. |
| P3M20 | `Fn_zero` for q² ≤ 2 | `Fn_zero` | {`Fn_zero`, `N_at_horizon_Dn`} | (not checked) | As in v3. |
| P3M21 | `Hn_pos` for m ≥ 0 | `Hn_pos` | {`Hn_pos`, `prop3_Dn`} | (not checked) | As in v3. |
| P3M22 | `Fn_zc_TARGET` with qM² in place of (qM)² | `Fn_zc_TARGET` | {`Fn_zc_TARGET`} | "unsolved goals" (at `Fn_zc_TARGET`) | As in v3. |
| P3M23 | `N_at_infinity_Dn` with n(n + 1)/4 | `N_at_infinity_Dn` | {`N_at_infinity_Dn`} | (not checked) | As in v3. |
| P3M24 | `prop3_Dn` with hP only on (0, 1/2) | `prop3_Dn` | {`prop3_Dn`} | (not checked) | As in v3. |
| P3M25 | `g_res`: 576H₋(2)² → 575H₋(2)² | `g_res` | {`g_res`, `g_res_tendsto`} | "unsolved goals" (at `g_res`) | p(0) is fixed by N, so the statement is false. In `g_res`, the second case's closing `ring` is a small identity in H₋(2), ℓ and a, and fails. `g_res_tendsto` rewrites with `g_res`'s value, and the pattern 575H₋(2)²(…) is not in its goal. |
| P3M26 | `g_res`: a(a + 1) → a(a − 1) | `g_res` | {`g_res`, `g_res_tendsto`} | (not checked) | False, by 1152H₋(2)²a. It fails as P3M25 does. |
| P3M27 | `dEll`: 1/(5(ℓ + 4)) → 1/(4(ℓ + 4)) | `mEll_dEll_S5` | {`mEll_dEll_S5`, `H2_ell`, `U2_ell`} | (not checked) | Not a root of S5 (5.58): 1 + 2mδ = (ℓ + 1)/2. H₋(2) and U₋(2) change. `H2_ell` and `U2_ell` unfold `dEll`. `g_res` keeps `dEll ℓ` as an atom and uses `U2_ell` only as a statement, so it compiles. |
| P3M28 | `Pres`: a/z → a/z² | `Pres_hasDerivAt` | {`Pres_hasDerivAt`, `g_res`} | "unsolved goals" (at `Pres_hasDerivAt`) | In `Pres_hasDerivAt`, the step that rewrites P as a·z⁻¹ + b₀ + b₁z is left with a·(z²)⁻¹ against a·z⁻¹. In `g_res`, N gains the term −576a²H₋(2)²/z² at leading order, so no polynomial agrees with it, and the first case's `ring` fails. `g_res_tendsto` uses `g_res` only as a statement. |
| P3M29 | `g_res`: f and f_z at q = 1/2 | `g_res` | {`g_res`, `g_res_tendsto`} | (not checked) | f has a simple zero at the horizon, so N has a 1/z pole, proportional to a², and the statement is false. In `g_res`, the rewrite with `D6_extremal`'s F6 1 z finds no F6 1 z. `g_res_tendsto`'s N (q = 1) no longer matches `g_res`'s. |
| P3M30 | `g_res`: hℓ : ℓ + 4 ≠ 0 → ℓ + 5 ≠ 0 | `g_res` | {`g_res`, `g_res_tendsto`} | (not checked) | False at ℓ = −4. There m = 0, and Lean's 1/0 = 0 gives δ = 0, so p(0) = 204800 − 230400a(a + 1), not 716800 − 230400a(a + 1). `g_res` passes hℓ to `U2_ell`, which expects ℓ + 4 ≠ 0, and `g_res_tendsto` passes ℓ + 4 ≠ 0 where ℓ + 5 ≠ 0 is expected. |
| P3M31 | `mEll`: (ℓ − 1)(ℓ + 4) → (ℓ − 1)(ℓ + 5) | `mEll_dEll_S5` | {`mEll_dEll_S5`, `H2_ell`, `U2_ell`} | (not checked) | m ≠ ℓ(ℓ + 3) − 4, and (5.58) fails. The rest is as in P3M27: `g_res` keeps `mEll ℓ` as an atom. |
| P3M32 | `W4`: βF = 6MF → 5MF | `W4_deriv` | {`W4_deriv`, `darboux_KI`, `darboux_RW`} | (not checked) | `W4_deriv`'s quotient rule supplies 6M·F′, not 5M·F′. Both identities unfold `W4` and become false. `RW_regular_at_r0` uses `darboux_RW` only as a statement. |
| P3M33 | `W4`: κ = m(m + 2) → m(m + 1) | `darboux_KI` | {`darboux_KI`, `darboux_RW`} | (not checked) | `W4_deriv` still holds and compiles, because its proof leaves the constant to unification. Both identities unfold `W4` and change by 2𝒲Δ + Δ², with Δ = −m/(12M), which depends on r; they become false. |
| P3M34 | `VRW4`: m + 2 → m + 1 | `darboux_RW` | {`darboux_RW`} | (not checked) | False, by f/r². `RW_regular_at_r0` still proves analyticity of the mutated potential, and uses `darboux_RW` only as a statement. |
| P3M35 | `darboux_KI` with 𝒲² − 𝒲_* | `darboux_KI` | {`darboux_KI`} | (not checked) | It would say that V_S− is Regge–Wheeler's potential, which is false. They differ by 2𝒲_*. |
| P3M36 | `RW_regular_at_r0`: analytic at r = 0 | `RW_regular_at_r0` | {`RW_regular_at_r0`} | (not checked) | False: r⁴·V_RW → 12M² ≠ 0 at r = 0. `fun_prop`'s side condition becomes 0 ≠ 0. |
| P3M37 | `RW_regular_at_r0`: zero of H₋ at −3M/m | `RW_regular_at_r0` | {`RW_regular_at_r0`} | (not checked) | False: H₋ = −m there. `H_zero_iff` applied with hr0, which is about −6M/m, no longer fits the goal. |

**What the new mutations test.**
- **P3M25 and P3M26.** The value N(0) of G-RES: its normalisation 576H₋(2)² and its dependence on the residue a.
- **P3M27 and P3M31.** m and δ are S5's at n = 4 and q = 1, and `H2_ell` and `U2_ell` depend on them.
- **P3M28.** A double pole breaks the polynomial property.
- **P3M29.** Away from extremality (q = 1/2), where f has a simple zero at the horizon, the polynomial property fails.
- **P3M30.** The hypothesis ℓ ≠ −4 is load-bearing in Lean, where 1/0 = 0.
- **P3M32 and P3M33.** β and κ of the superpotential are each load-bearing in both identities.
- **P3M34 and P3M35.** Regge–Wheeler's form, and the sign that separates the two Darboux partners.
- **P3M36 and P3M37.** The point r₀ of the analyticity claim, and that it is the zero of H₋.
- Each mutated statement is false, not merely unproved (oracle section 5).

**How it will be read.**
- Agreement means three things together:
  - the predicted first failure;
  - exactly the predicted failing set;
  - `pass: true` from the judge, which also checks the registered error text where one is given.
- Any difference is reported as it stands, without changing a spec.
