# p3 Lean layer, labelled build v3: registered predictions for mutations P3M1 to P3M24 (session-L, 2026-10-23, before any mutation run)

I wrote this file before running any mutation of the v3 `lean/BHModesP3.lean`. Each spec was checked only as text:
its old string occurs exactly once in the v3 file. `lean/build.sh` (a byte copy of the first build's) records this
file's sha256 in `BUILD_LOG.txt` before the first mutation run. The record binds once that hash reaches the bh-modes
lead.

**Predicted against:**
- `lean/BHModesP3.lean`, sha256 `3a2dcd68…` (`lean/SOURCES.tsv`).
  - Lines 1–520 are the v2 build's, byte for byte.
  - Lines 521–682 are new: the general-n instance (BHM-090). It consists of the definitions `HmN`, `UmN`, `xn`, `Fn`,
    `Fn'`, `Hn` and `Un`, and the theorems `HmN_four`, `UmN_four`, `Dn_four`, `xn_zc`, `Fn_zc_TARGET`, `Vrho_Dn`,
    `Fn_hasDerivAt`, `Fn_zero`, `Fn_pos`, `Hn_pos`, `prop3_Dn`, `prop3_Dn_zeta`, `N_at_horizon_Dn` and
    `N_at_infinity_Dn`.
- `lean/mutations.json`, sha256 `3b2ea3e3…`. Its first fifteen specs are v2's, byte for byte. P3M16 to P3M24 are new.
- The vendored judge `lean/vendor/mutation.py` (`696b7864…`), the same byte copy as before.

**What is and is not blind.**
- **P3M1 to P3M15 are not blind.** They ran in v2, and all fifteen came out as registered. Their predictions carry
  over, except where a new theorem joins a failing set (marked "new member" below).
- **P3M16 to P3M24 are new.** No mutated copy has been compiled.
  - The unmutated v3 file was compiled twice on the editing node, both times clean. The second compile only
    confirmed the exit code.
  - One probe file checked three lemma names.

**What Lean does with a failed theorem.**
- A failed proof is kept with sorry, and later uses of it still elaborate. So a theorem that uses another theorem only
  as a statement keeps compiling when that statement is unchanged.
- A theorem fails if it unfolds a changed definition, uses a changed statement in a proof step, or passes its own
  hypothesis where a changed one is expected.
- Tactic blocks inside a term run at the end of its elaboration. Within one declaration, errors appear in that
  order, and across declarations, in file order.

| id | mutation | first failure | failing set (exactly) | judge-checked error text | why |
|---|---|---|---|---|---|
| P3M1 | `Nz`: 64H² → 63H² | `ansatz_identity` | {`ansatz_identity`, `N_at_horizon`, `N_eps_shift`, `N_at_infinity_D6`, `N_at_infinity_Dn`} | "unsolved goals" (at `ansatz_identity`) | New member: `N_at_infinity_Dn`, which unfolds `Nz`, so its `ring` meets a false identity. `N_at_horizon_Dn` uses `N_at_horizon` only as a statement, and `prop3_Dn` does not unfold `Nz`. |
| P3M2 | `sdef_identity` with V − S′ − S² | `sdef_identity` | {`sdef_identity`, `form_nonneg_of_sdef`} | (not checked) | As in v2. |
| P3M3 | `beta_hasDerivAt` with +P | `beta_hasDerivAt` | {`beta_hasDerivAt`, `Srho_hasDerivAt`} | (not checked) | As in v2. |
| P3M4 | `zc_hasDerivAt` with (1 − z)³ | `zc_hasDerivAt` | {`zc_hasDerivAt`, `f_hasDerivAt`, `beta_hasDerivAt`} | (not checked) | As in v2. `xn_zc` uses `one_sub_zc`, which is unchanged. |
| P3M5 | `N_at_infinity_D6` with m + 5 | `N_at_infinity_D6` | {`N_at_infinity_D6`, `N_at_infinity_ell2`} | "unsolved goals" (at `N_at_infinity_D6`) | As in v2. |
| P3M6 | `N_at_infinity_ell2` with −4 < P(1) | `N_at_infinity_ell2` | {`N_at_infinity_ell2`} | (not checked) | As in v2. |
| P3M7 | `F6'`: 3x_H → 2x_H | `F6_hasDerivAt` | {`F6_hasDerivAt`, `Dn_four`} | "unsolved goals" (at `F6_hasDerivAt`) | New member: `Dn_four`, whose second part, `Fn' 4 q = F6' q`, unfolds `F6'` and now asks 3 = 2. |
| P3M8 | `prop3` assuming 0 ≤ f_z | `prop3` | {`prop3`, `prop3_D6`} | (not checked) | As in v2. |
| P3M9 | `Vrho` with 64ρ³ | `prop3` | {`prop3`, `Vrho_D6`, `prop3_Ioo`, `Vrho_Dn`} | (not checked) | New member: `Vrho_Dn`, which unfolds `Vrho` and states ρ² on its right side, like `Vrho_D6`. `prop3_Dn` uses `prop3_Ioo` only as a statement. |
| P3M10 | `prop3_Ioo` with hP only on (0, 1/2) | `prop3_Ioo` | {`prop3_Ioo`, `prop3_Dn`} | (not checked) | New member: `prop3_Dn`. It passes `fun z h0 h1 => hP z ⟨h0, h1⟩`, and h1 : z < 1/2 no longer fits the membership z ∈ (0, 1). `prop3_Dn_zeta` uses `prop3_Dn` only as a statement. |
| P3M11 | `prop3_Ioo` with hP′ only on (0, 1/2) | `prop3_Ioo` | {`prop3_Ioo`, `prop3_zeta`, `prop3_Dn`} | (not checked) | New member: `prop3_Dn`, which passes its own hP′ on (0, 1), a type mismatch. |
| P3M12 | `Pzeta'` with (d + 1)P̂ | `Pzeta_hasDerivAt` | {`Pzeta_hasDerivAt`} | (not checked) | As in v2. `prop3_Dn_zeta` uses `Pzeta_hasDerivAt` and `Pzeta'_continuousOn` only as statements. |
| P3M13 | `prop3_zeta` with −1/2 ≤ δ | `prop3_zeta` | {`prop3_zeta`} | "linarith failed to find a contradiction" (at `prop3_zeta`) | As in v2. `prop3_Dn_zeta` does not use `prop3_zeta`, and its own shift is δb. |
| P3M14 | `prop3_near` with a < 1/2 | `prop3_near` | {`prop3_near`} | "linarith failed to find a contradiction" (at `prop3_near`) | As in v2. |
| P3M15 | `pole_not_differentiable` at d = 0 | `pole_not_differentiable` | {`pole_not_differentiable`} | (not checked) | As in v2. |
| P3M16 | `UmN`: 16n(n + 2)m²K → 16n(n + 3)m²K (bh-modes' td-coeff control) | `UmN_four` | {`UmN_four`, `N_at_infinity_Dn`} | (not checked) | Both unfold `UmN` and become false: at n = 4 the constant 448m² is not TARGET.md's 384m², and N(1) gains 16nm². `Dn_four` uses `UmN_four` only as a statement. `prop3_Dn` needs only continuity. |
| P3M17 | `HmN`: n(n + 1) → n(n + 2) | `HmN_four` | {`HmN_four`} | (not checked) | At n = 4, the coefficient is 12 rather than TARGET.md's 10. `Hn_pos` still holds by `positivity`. In `N_at_infinity_Dn`, x = 0 at z = 1 removes the changed term. `Dn_four` uses `HmN_four` only as a statement. |
| P3M18 | `Fn'`: (n − 1) → n | `Dn_four` | {`Dn_four`, `Fn_hasDerivAt`} | (not checked) | `Dn_four` (l. 566) unfolds `Fn'` and compares with `F6'`: 4 against 3. `Fn_hasDerivAt` (l. 590) checks the derivative: n against n − 1. In `N_at_infinity_Dn`, `Fn'` is multiplied by 1 − 1. `prop3_Dn` needs only continuity. |
| P3M19 | `Fn_pos` from 1 ≤ n | `Fn_pos` | {`Fn_pos`, `prop3_Dn`} | (not checked) | False at n = 1, where f ≡ 0. The `omega` for n − 1 ≠ 0 fails. `prop3_Dn` passes hn : 2 ≤ n where 1 ≤ n is now expected, a type mismatch. |
| P3M20 | `Fn_zero` for q² ≤ 2 | `Fn_zero` | {`Fn_zero`, `N_at_horizon_Dn`} | (not checked) | False for q² > 1: there is no horizon, and f(0) = q² − 1. Passing hq to `F6_zero` is a type mismatch. `N_at_horizon_Dn` passes hq : q² ≤ 1 where q² ≤ 2 is expected. |
| P3M21 | `Hn_pos` for m ≥ 0 | `Hn_pos` | {`Hn_pos`, `prop3_Dn`} | (not checked) | False at z = 1, m = 0 and n ≠ 1, where H₋ = 0. `positivity` cannot prove the strict bound. `prop3_Dn` passes hm : 0 < m where 0 ≤ m is expected. |
| P3M22 | `Fn_zc_TARGET` with qM² in place of (qM)² | `Fn_zc_TARGET` | {`Fn_zc_TARGET`} | "unsolved goals" (at `Fn_zc_TARGET`) | A small false identity: the closing `ring` leaves its normal form unsolved. Nothing uses the theorem. |
| P3M23 | `N_at_infinity_Dn` with n(n + 1)/4 | `N_at_infinity_Dn` | {`N_at_infinity_Dn`} | (not checked) | False, by 16nm² (the term from `UmN`'s 16n(n + 2)m²). Nothing uses the theorem. No text is registered, because the unfolded `UmN` is not small. |
| P3M24 | `prop3_Dn` with hP only on (0, 1/2) | `prop3_Dn` | {`prop3_Dn`} | (not checked) | ⟨h0, h1⟩ with h1 : z < 1 no longer proves z ∈ (0, 1/2). `prop3_Dn_zeta` still supplies the weaker hypothesis: its `linarith` needs only 0 < z. |

**What the new mutations test.**
- **P3M16 and P3M17.** The general-n transcription reduces at n = 4 to TARGET.md's U₋ and H₋. P3M16 is bh-modes' own
  td-coeff control, carried into Lean.
- **P3M18.** The derivative f_z is checked, and so is its agreement with `F6'`.
- **P3M19 to P3M21.** Each hypothesis that makes f > 0, f(0) = 0 and H₋ > 0 true is load-bearing: n ≥ 2, q² ≤ 1 and
  m > 0. Each mutated statement is false, not merely unproved.
- **P3M22.** Agreement with TARGET_HD.md's f.
- **P3M23.** The value of N at z = 1 for general n.
- **P3M24.** `prop3_Dn` uses hP on all of (0, 1).

**How it will be read.**
- Agreement means three things together:
  - the predicted first failure;
  - exactly the predicted failing set;
  - `pass: true` from the judge, which also checks the registered error text where one is given.
- Any difference is reported as it stands, without changing a spec.
