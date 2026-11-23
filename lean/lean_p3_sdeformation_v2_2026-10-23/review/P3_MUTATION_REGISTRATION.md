# p3 Lean layer, labelled build v2: registered predictions for mutations P3M1 to P3M15 (session-L, 2026-10-23, before any mutation run)

I wrote this file before running any mutation of the v2 `lean/BHModesP3.lean`. Each spec was checked only as text:
its old string occurs exactly once in the v2 file. `lean/build.sh` (a byte copy of the first build's) records this
file's sha256 in `BUILD_LOG.txt` before the first mutation run. The record binds once that hash reaches the bh-modes
lead.

**Predicted against:**
- `lean/BHModesP3.lean`, sha256 `1ade9f3e…` (`lean/SOURCES.tsv`). Lines 1–392 are the first build's, byte for byte.
  Lines 393–521 are new: `prop3_Ioo`, `prop3_near`, `Pzeta`, `Pzeta'`, `Pzeta_hasDerivAt`, `Pzeta'_continuousOn`,
  `prop3_zeta` and `pole_not_differentiable`.
- `lean/mutations.json`, sha256 `a462aaaa…`. Its first nine specs are the first build's, byte for byte. P3M10 to P3M15
  are new.
- The vendored judge `lean/vendor/mutation.py` (`696b7864…`), the same byte copy as in the first build.

**What is and is not blind.**
- **P3M1 to P3M9 are not blind.** The first build ran them, and all nine came out as registered. Their predictions
  carry over, with one change: P3M9's failing set gains `prop3_Ioo`, because its proof has the same step `e` as
  `prop3`'s.
- **P3M10 to P3M15 are new.** No mutated copy has been compiled.
  - During development, the unmutated v2 file was compiled three times on the editing node. The first compile failed
    in two places in my draft: a `fun_prop` step, and the d = 0 branch. The second and third were clean.
  - I also compiled one probe file, which checked lemma names.

**What Lean does with a failed theorem.** A failed proof is kept with sorry, and later uses of it still elaborate. So a
theorem that uses another theorem only as a statement keeps compiling when that statement is unchanged. A theorem that
unfolds a changed definition, or uses a changed statement in a proof step, fails. Tactic blocks inside a term are run
at the end of its elaboration, each on its own, so one failing argument does not stop the others from being checked.

| id | mutation | first failure | failing set (exactly) | judge-checked error text | why |
|---|---|---|---|---|---|
| P3M1 | `Nz`: 64H² → 63H² | `ansatz_identity` | {`ansatz_identity`, `N_at_horizon`, `N_eps_shift`, `N_at_infinity_D6`} | "unsolved goals" (at `ansatz_identity`) | As in the first build. `prop3_Ioo` uses `ansatz_identity` only as a statement, and its own `ring` step never unfolds `Nz`. `prop3_zeta` mentions `Nz` only in its statement. |
| P3M2 | `sdef_identity` stated with V − S′ − S² | `sdef_identity` | {`sdef_identity`, `form_nonneg_of_sdef`} | (not checked) | As in the first build. `prop3_Ioo` uses `form_nonneg_of_sdef` only as a statement. |
| P3M3 | `beta_hasDerivAt` stated with +P | `beta_hasDerivAt` | {`beta_hasDerivAt`, `Srho_hasDerivAt`} | (not checked) | As in the first build. `prop3_Ioo` uses `Srho_hasDerivAt` only as a statement. |
| P3M4 | `zc_hasDerivAt` stated with (1 − z)³ | `zc_hasDerivAt` | {`zc_hasDerivAt`, `f_hasDerivAt`, `beta_hasDerivAt`} | (not checked) | As in the first build. |
| P3M5 | `N_at_infinity_D6` with m + 5 | `N_at_infinity_D6` | {`N_at_infinity_D6`, `N_at_infinity_ell2`} | "unsolved goals" (at `N_at_infinity_D6`) | As in the first build. |
| P3M6 | `N_at_infinity_ell2` with −4 < P(1) | `N_at_infinity_ell2` | {`N_at_infinity_ell2`} | (not checked) | As in the first build. |
| P3M7 | `F6'`: 3x_H → 2x_H | `F6_hasDerivAt` | {`F6_hasDerivAt`} | "unsolved goals" | As in the first build. |
| P3M8 | `prop3` assuming 0 ≤ f_z | `prop3` | {`prop3`, `prop3_D6`} | (not checked) | As in the first build. `prop3_Ioo` has its own `hf`, which the old string does not touch. |
| P3M9 | `Vrho` with 64ρ³ | `prop3` | {`prop3`, `Vrho_D6`, `prop3_Ioo`} | (not checked) | In `prop3` and in `prop3_Ioo`, the step `e` no longer matches `ansatz_identity` (ρ³ against ρ²). The continuity step `hV` still holds, by `positivity` with R t ≠ 0. `Vrho_D6` states ρ² on its right side. `prop3_near` and `prop3_zeta` use `prop3_Ioo` only as a statement. |
| P3M10 | `prop3_Ioo` with hP only on (0, 1/2) | `prop3_Ioo` | {`prop3_Ioo`} | (not checked) | The proof uses hP at zc(R t), which ranges over all of (0, 1). It does so twice: for the continuity of t ↦ P(zc(R t)) (`hPz`) and for the chain rule (`hS`). Both become type mismatches, z < 1 against z < 1/2. `prop3_near` and `prop3_zeta` still supply the weaker hypothesis: their `linarith` side goals hold, because they assume P's derivative on larger sets. |
| P3M11 | `prop3_Ioo` with hP′ continuous only on (0, 1/2) | `prop3_Ioo` | {`prop3_Ioo`, `prop3_zeta`} | (not checked) | `hP'z` needs zc(R t) in the set for every t, but `hzm` gives (0, 1): a type mismatch. `prop3_zeta` passes `Pzeta'_continuousOn`, which is stated on (0, 1) and no longer fits. `prop3_near` passes `hP'.mono` with `linarith` side goals (a ≤ 0 and 1/2 ≤ b), which still hold. |
| P3M12 | `Pzeta'` with (d + 1)P̂ in place of dP̂ | `Pzeta_hasDerivAt` | {`Pzeta_hasDerivAt`} | (not checked) | The quotient-rule algebra fails in both branches (d = 0 and d = k + 1). `Pzeta'_continuousOn` needs only continuity, which still holds. `prop3_zeta` uses both theorems only as statements. |
| P3M13 | `prop3_zeta` with −1/2 ≤ δ in place of 0 ≤ δ | `prop3_zeta` | {`prop3_zeta`} | "linarith failed to find a contradiction" (at `prop3_zeta`) | With δ ≥ −1/2, 0 < z + δ no longer follows from 0 < z, so the `linarith` that keeps z away from the pole fails. Passing hδ to `Pzeta'_continuousOn`, which wants 0 ≤ δ, is a second error. |
| P3M14 | `prop3_near` with a < 1/2 in place of a < 0 | `prop3_near` | {`prop3_near`} | "linarith failed to find a contradiction" (at `prop3_near`) | For z ∈ (0, 1), a < z no longer follows, and neither does a ≤ 0 for `Set.Ioo_subset_Ioo`. Both `linarith` side goals fail. |
| P3M15 | `pole_not_differentiable` at d = 0 | `pole_not_differentiable` | {`pole_not_differentiable`} | (not checked) | At d = 0, P = 1 is differentiable, so the statement is false. The proof's `rw [e]` finds no instance of the d = 1 pattern. |

**What the new mutations test.**
- **P3M10 and P3M11.** The proof of `prop3_Ioo` uses hP and hP′ on all of (0, 1), not on a part of it. It uses
  nothing outside (0, 1): Lean checks that from the statement itself.
- **P3M12.** `Pzeta_hasDerivAt` is checked against the derivative formula.
- **P3M13.** The ζ instance needs the pole outside (0, 1).
- **P3M14.** METHOD_ADDENDUM_2's open interval must contain (0, 1).
- **P3M15.** The pole theorem depends on the pole.

**How it will be read.**
- Agreement means three things together:
  - the predicted first failure;
  - exactly the predicted failing set;
  - `pass: true` from the judge, which also checks the registered error text where one is given.
- Any difference is reported as it stands, without changing a spec.
