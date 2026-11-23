# Z Lean layer, item (d) (BHM-126): registered predictions for mutations ZD1 to ZD15 (session-L, 2026-10-26, before any mutation run)

I wrote this file before running any mutation of `lean/BHModesZd.lean`. `lean/build.sh` records this file's sha256 in
`BUILD_LOG.txt` before the first mutation run. The record binds once that hash reaches the bh-modes lead.

**Predicted against:**
- `lean/BHModesZd.lean`, sha256 `638590d6…` (`lean/SOURCES.tsv`), 773 lines, 46 theorems.
  - Lines 36–174 are lean_z_2026-10-26's lines 25–163, byte for byte (9 theorems).
  - Lines 180–239 are p3 v5's lines 86–145, byte for byte: Lemma 1 and its Corollary.
  - From line 241 on is the new section (d), with 35 theorems.
- `lean/mutations.json`, sha256 `2580b556…`: fifteen specs, all new, all on section (d).
- `lean/build.sh`, sha256 `44f905ee…`. It is lean_z's `build.sh` with the file name, the registration's name and the
  title changed, and nothing else. The namespace stays `BHModes.Z`.
- The vendored judge `lean/vendor/mutation.py` (`696b7864…`), the same byte copy as before.

**What is and is not blind.**
- **All fifteen specs are new.** No mutated copy has been compiled. Each was applied once as text, with the judge's
  own `apply`, to check that its old string occurs once and that it changes one line. None of those copies was compiled.
- **The unmutated file was compiled four times on the editing node:**
  1. The first draft gave ten errors, all in section (d): a `field_simp` that left ρρ⁻¹ terms; a `simp only` that made no
     progress; two hypotheses where r* had been unfolded in one place but not in the other; a `field_simp` that lacked
     c ≠ 0; the set argument of `Monotone.monotoneOn`; `eq_div_iff` used where `div_eq_iff` was needed (twice);
     `.sub` and `.add`, which give pointwise function forms, where `const_sub` and `const_add` keep lambdas; and a
     `Function.comp` left before `ring`.
  2. The second was clean.
  3. The third was clean. It turned the doc comments of `riccati_plus` and `riccati_minus` into `--` line comments.
     A heartbeat timeout is placed at a declaration's first character, and the judge credits that line to the nearest
     declaration keyword above it (lean_z, ZM4/5/10). These are the two largest identities.
  4. The fourth was the final file, after the header's line numbers were filled in. It was clean, in 6 s.
- **Heartbeats** were counted with `-DElab.async=false`, before the third compile and on the final file. Both runs
  were clean. The largest count is 21,589 (`tort_surjOn`); `riccati_plus` and `riccati_minus` take 7,181 and 7,283.
  The limit is 200,000.
- **The oracle (`oracle/check_zd.py`) ran once on the editing node, on the final file, before this registration:
  34/34.** Its section 7 checks that each mutated target is false. It says nothing about how Lean fails.

**What Lean does with a failed theorem.**
- A failed proof is kept with sorry, and later uses of it still elaborate. So a theorem that uses another only as a
  statement keeps compiling while that statement is unchanged, even when it has become false.
- A theorem fails if it unfolds a changed definition, rewrites with a changed statement and then meets a mismatch,
  or passes a term whose type no longer fits.
- Errors appear in file order across declarations. "First failure" below is the declaration of the first error.

**The dependencies these predictions use** (section (d) only; each theorem uses the others as statements):
- `tort_strictMonoOn`, `tort_ge`, `tort_le`, `tortoise_q1` and `Rt_hasDerivAt` use `tort_hasDerivAt`'s derivative
  value. `tort_surjOn` uses only its continuity.
- `fr_le_sq` passes `one_sub_Yr_le`'s statement where its own conclusion is expected. `tort_surjOn` rewrites with
  `tort_le`'s bound after setting c = (n − 1)².
- `w_log_deriv`, `zero_mode` and `A_nonneg` compose with `Rt_hasDerivAt`.
- `V_eq` uses `riccati_plus` and `z_id`; `Vt_eq` uses `riccati_minus` and `partner`, rewriting with their left sides.
- `zero_mode` and `A_nonneg` rewrite with `V_eq`. Neither unfolds `Vr`.
- `w_log_deriv` composes `log_u0_hasDerivAt` with R. `S_eq` and `zero_mode` use `w_log_deriv` as a statement.
- `wr_hasDerivAt` closes its derivative by `convert … using 1` against `dwr`, which uses `dg`.
- `riccati_plus` and `riccati_minus` unfold `wr`, `dwr`, `dg` and `fr`.
- `Vr_S5` and `V_eq` unfold `Vr`. `Vr_continuousAt` builds `Vr`'s continuity term with `ρ ^ 2`.

| id | mutation | first failure | failing set (exactly) | judge-checked error text | why |
|---|---|---|---|---|---|
| ZD1 | `tortoise_q1`: BijOn from (2, ∞) | `tortoise_q1` | {`tortoise_q1`} | (not checked) | False: r*(2) = 0 and r* increases, so −1 has no preimage in (2, ∞). `tort_bijOn` no longer fits. |
| ZD2 | `tortoise_q1`: StrictAntiOn | `tortoise_q1` | {`tortoise_q1`} | (not checked) | False. `tort_strictMonoOn` no longer fits. |
| ZD3 | `tort_hasDerivAt`: 2/f | `tort_hasDerivAt` | {`tort_hasDerivAt`, `tort_strictMonoOn`, `tort_ge`, `tort_le`, `tortoise_q1`, `Rt_hasDerivAt`} | (not checked) | False: dr*/dρ = 1/f. Each listed theorem uses the derivative value: `one_div_pos`, the stated derivatives of `hd`, the third component, and `f' ≠ 0`. `tort_surjOn` uses only continuity. |
| ZD4 | `Rt_hasDerivAt`: 1/f(R) | `Rt_hasDerivAt` | {`Rt_hasDerivAt`, `w_log_deriv`, `zero_mode`, `A_nonneg`} | (not checked) | False: dR/dr* = f(R). The three composites then carry 1/f(R) where f(R) closes the algebra. `S_eq` uses `w_log_deriv` as stated. |
| ZD5 | `riccati_plus` without f in w′ | `riccati_plus` | {`riccati_plus`, `V_eq`} | (not checked) | False. `V_eq`'s `linear_combination` then lacks f. `zero_mode` and `A_nonneg` use `V_eq` as stated. |
| ZD6 | `riccati_minus` with g² − g | `riccati_minus` | {`riccati_minus`, `Vt_eq`} | (not checked) | False. `Vt_eq`'s `rw [partner …]` no longer finds (c)'s left side. |
| ZD7 | `V_eq` with w² − w′ | `V_eq` | {`V_eq`, `zero_mode`, `A_nonneg`} | (not checked) | False (V − Ṽ = 2fw_ρ ≠ 0). Both later theorems rewrite with it and then meet the wrong sign. |
| ZD8 | `log_u0_hasDerivAt` with gρ | `log_u0_hasDerivAt` | {`log_u0_hasDerivAt`, `w_log_deriv`} | (not checked) | False. `apply hL'.congr_of_eventuallyEq` meets g/ρ. `w_log_deriv`'s `ring` meets g R f ≠ f g/R. |
| ZD9 | `u0` with ℓ/(n + 1) | `log_u0_hasDerivAt` | {`log_u0_hasDerivAt`} | (not checked) | False: log u₀ is no longer the function whose derivative is g/ρ, and the last `ring` fails. `u0_pos` is generic in the exponent. |
| ZD10 | `zero_mode` with Ṽ U | `zero_mode` | {`zero_mode`} | (not checked) | False: V ≠ Ṽ and U > 0. |
| ZD11 | `A_nonneg` with V − 1 | `A_nonneg` | {`A_nonneg`} | (not checked) | False: V → 0 as r* → ∞, so a wide bump far out makes the form negative (oracle 7, at n = 4, ℓ = 2). `form_nonneg_of_sdef`'s conclusion no longer fits. |
| ZD12 | `Vr` = f W/ρ³ | `Vr_S5` | {`Vr_S5`, `V_eq`, `Vr_continuousAt`} | (not checked) | `Vr_S5` is false. `V_eq`'s `rw [div_eq_iff (… 2 …)]` finds no ρ². `Vr_continuousAt`'s term has ρ². `zero_mode` and `A_nonneg` use `V_eq` and `Vr_continuousAt` as stated. |
| ZD13 | `tort_le` with (n − 1) for (n − 1)² | `tort_le` | {`tort_le`, `tort_surjOn`} | (not checked) | False at n = 3 near ρ = 1 (oracle 7). `tort_surjOn`'s `rw [e]` no longer finds `/ c`. |
| ZD14 | `one_sub_Yr_le` with n − 2 | `one_sub_Yr_le` | {`one_sub_Yr_le`, `fr_le_sq`} | (not checked) | False at n = 2. `fr_le_sq` passes it where (n − 1)(ρ − 1) is expected. |
| ZD15 | `dg` with +ℓ/(1 − Y)² | `wr_hasDerivAt` | {`wr_hasDerivAt`, `riccati_plus`, `riccati_minus`} | (not checked) | `wr_hasDerivAt` is false, and `convert` leaves its derivative goal open. Both riccati theorems unfold `dg` against `deriv_g`'s formula. `V_eq` and `Vt_eq` use them as stated. |

Every spec is predicted to pass the judge: Lean exits non-zero; no parse error and no unknown name; no error before
the mutated line; the spec's declaration among the failing ones. No error text is registered.

**What the mutations show:**
- **ZD1–ZD3:** the tortoise map is increasing, a bijection from (1, ∞), and dr*/dρ = 1/f.
- **ZD4:** dR/dr* = f(R).
- **ZD5–ZD7 and ZD12:** the chain-rule step needs w′ = f dw/dρ, (c)'s bracket is pinned, V = w² + w′ with its sign,
  and V = fW/ρ².
- **ZD8, ZD9 and ZD15:** d(log u₀)/dρ = g/ρ, u₀'s throat exponent ℓ/(n − 1), and ∂_Y g in dw/dρ.
- **ZD10 and ZD11:** the zero mode solves the equation with V, not Ṽ, and A_{ℓ,1} ≥ 0 does not extend to A_{ℓ,1} − 1.
- **ZD13 and ZD14:** the throat bound (n − 1)², and Bernoulli's factor n − 1.
