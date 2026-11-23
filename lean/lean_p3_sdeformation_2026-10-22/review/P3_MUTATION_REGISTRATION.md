# p3 Lean layer, item (a): registered predictions for mutations P3M1 to P3M9 (session-L, 2026-10-22, before any run)

I wrote this file before running any mutation of `lean/BHModesP3.lean`. Each spec had been checked only as text: its old
string occurs exactly once. `lean/build.sh` records this file's sha256 in `BUILD_LOG.txt` before the first mutation run.
The record binds once that hash reaches the operator.

**Predicted against:**
- `lean/BHModesP3.lean` (sha256 `9cbce71a…` in `lean/SOURCES.tsv`);
- `lean/mutations.json`;
- the vendored judge `lean/vendor/mutation.py` (`696b7864…`, the same byte copy as in the A1 layer).

**What Lean does with a failed theorem.** A failed proof is kept with sorry, and later uses of it still elaborate. So a
theorem that uses another theorem only as a statement keeps compiling when that statement is unchanged. A theorem that
unfolds a changed definition, or uses a changed statement in a proof step, fails.

| id | mutation | first failure | failing set (exactly) | judge-checked error text | why |
|---|---|---|---|---|---|
| P3M1 | `Nz`: 64H² → 63H² | `ansatz_identity` | {`ansatz_identity`, `N_at_horizon`, `N_eps_shift`, `N_at_infinity_D6`} | "unsolved goals" (at `ansatz_identity`) | Each of the four unfolds `Nz`, and its closing `ring` meets a false identity. `prop3` and `N_at_horizon_D6` use `ansatz_identity` and `N_at_horizon` only as statements. |
| P3M2 | `sdef_identity` stated with V − S′ − S² | `sdef_identity` | {`sdef_identity`, `form_nonneg_of_sdef`} | (not checked; expected "unsolved goals") | The final `rw` leaves the two sides unequal. `form_nonneg_of_sdef` rewrites with the false statement, and `hVt` no longer fits. `sdef_identity_real` is separate. |
| P3M3 | `beta_hasDerivAt` stated with +P | `beta_hasDerivAt` | {`beta_hasDerivAt`, `Srho_hasDerivAt`} | (not checked) | Its own `congr_deriv … ring` fails. `Srho_hasDerivAt` combines the false β′ with the true f′, and its `ring` no longer reaches `dSrho`. |
| P3M4 | `zc_hasDerivAt` stated with (1 − z)³ | `zc_hasDerivAt` | {`zc_hasDerivAt`, `f_hasDerivAt`, `beta_hasDerivAt`} | (not checked) | `field_simp` cannot reach ρ⁻² = ρ⁻³. `f_hasDerivAt` and `beta_hasDerivAt` take the false derivative into a `congr_deriv` or a typed `have`, and both fail. |
| P3M5 | `N_at_infinity_D6` with m + 5 | `N_at_infinity_D6` | {`N_at_infinity_D6`, `N_at_infinity_ell2`} | "unsolved goals" (at `N_at_infinity_D6`) | The `ring` fails. `N_at_infinity_ell2` rewrites with the false value, and its ← direction then needs 11 + P − P² > 0 on (−3, 4), which fails near the ends. |
| P3M6 | `N_at_infinity_ell2` with −4 < P(1) | `N_at_infinity_ell2` | {`N_at_infinity_ell2`} | (not checked; expected "linarith failed …") | In the ← direction, `0 < P 1 + 3` does not follow from −4 < P(1). |
| P3M7 | `F6'`: 3x_H → 2x_H | `F6_hasDerivAt` | {`F6_hasDerivAt`} | "unsolved goals" | Only `F6_hasDerivAt` checks the value of `F6'`. `N_at_infinity_D6` meets `F6'` only multiplied by 1 − 1 = 0. `prop3_D6` uses `F6'` for continuity only. |
| P3M8 | `prop3` assuming 0 ≤ f_z | `prop3` | {`prop3`, `prop3_D6`} | (not checked) | `mul_nonneg` needs 0 ≤ F. `prop3_D6` supplies 0 ≤ F6, which no longer fits the changed hypothesis. |
| P3M9 | `Vrho` with 64ρ³ | `prop3` | {`prop3`, `Vrho_D6`} | (not checked) | In `prop3`, the step `e` no longer matches `ansatz_identity` (ρ³ against ρ²). `Vrho_D6` states ρ² on its right side. |

**How it will be read.**
- Agreement means three things together:
  - the predicted first failure;
  - exactly the predicted failing set;
  - `pass: true` from the judge, which also checks the registered error text where one is given.
- Any difference is reported as it stands, without changing a spec.
