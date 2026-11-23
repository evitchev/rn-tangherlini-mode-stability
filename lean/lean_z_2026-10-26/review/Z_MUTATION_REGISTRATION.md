# Z Lean layer (BHM-126): registered predictions for mutations ZM1 to ZM17 (session-L, 2026-10-26, before any mutation run)

I wrote this file before running any mutation of `lean/BHModesZ.lean`. `lean/build.sh` records this file's sha256 in
`BUILD_LOG.txt` before the first mutation run. The record binds once that hash reaches the bh-modes lead.

**Predicted against:**
- `lean/BHModesZ.lean`, sha256 `05e9c532…` (`lean/SOURCES.tsv`), 165 lines, 9 theorems.
  - Lines 34–53 are the c_n layer's definitions `Hm`, `Um`, `mm` and `δ1` (lean_cn_2026-10-23, lines 24–43), byte for
    byte.
  - The theorems are `gate_q1`, `gate_H`, `g_hasDerivAt`, `deriv_g`, `z_id`, `partner`, `partner_n4`, `partner_ends` and
    `partner_no_pole`, in that order.
- `lean/mutations.json`, sha256 `5bf063c2…`: seventeen specs, all new.
- `lean/build.sh`, sha256 `10522031…`. It is lean_cn's `build.sh` with the file name, the namespace, the registration's
  name and the title changed, and nothing else.
- The vendored judge `lean/vendor/mutation.py` (`696b7864…`), the same byte copy as before.

**What is and is not blind.**
- **All seventeen specs are new.** No mutated copy has been compiled. Each was applied once as text, with the judge's
  own `apply`, to check that its old string occurs once and that it changes one line. None of those copies was compiled.
- **The unmutated file was compiled four times on the editing node:**
  1. The first failed with three errors, all in `g_hasDerivAt`. Without `Mathlib.Analysis.Calculus.Deriv.Add`
     imported, `.sub` and `.add` resolved to `HasFDerivAtFilter.sub` and `.add`.
  2. The second, with that import, was clean.
  3. The third added `partner_no_pole` and the imports it needs (`FunProp`, `Linarith`, `LinearCombination`). It
     was clean.
  4. The fourth is the final file, after a line range in two comments was corrected (25–43 to 24–43). It was clean,
     in 4 s.
- **Heartbeats** were counted on two copies of the file, compiled with `-DElab.async=false`.
  - The first placed `#count_heartbeats in` between doc comments and their theorems, which gave parse errors.
  - The second placed it before the doc comments and was clean. Its counts, in theorem order: 740, 1,054, 9,003,
    600, 18,142, 7,175, 717, 830 and 2,744. The limit is 200,000.
- **The oracle (`oracle/check_z.py`, sympy) ran on the editing node before this registration.**
  - The first run was stopped after ten minutes, because its zero test expanded the whole rational function. It now
    expands the numerator over a common denominator.
  - The next two runs, the second on the final file, gave 36/36.
  - Its section 7 checks that each mutated target is false. It says nothing about how Lean fails.

**What Lean does with a failed theorem.**
- A failed proof is kept with sorry, and later uses of it still elaborate. So a theorem that uses another theorem only
  as a statement keeps compiling while that statement is unchanged, even when the statement has become false.
- A theorem fails if it unfolds a changed definition, uses a changed statement in a proof step, or passes its own
  hypothesis where a changed one is expected.
- A `have` whose proof fails is kept with sorry inside its theorem, so the rest of that proof still elaborates.
- Errors appear in file order across declarations. "First failure" below is the declaration of the first error.

**The dependencies these predictions use.**
- `gate_q1` unfolds `mm` and `δ1`; `gate_H` unfolds `Hm`, `mm` and `δ1`. Nothing uses `gate_q1`.
- `g_hasDerivAt` restates `g` as a lambda by `rfl`; its derivative computation does not involve `nu`.
- `deriv_g` is a term proof from `g_hasDerivAt`'s statement.
- `z_id` rewrites with `deriv_g` and `gate_H` (statements) and with `W`, then unfolds `g`, `nu`, `Um`, `mm` and `δ1`.
- `partner` rewrites with `deriv_g` and unfolds `g`, `nu` and `Ut`.
- `partner_n4` unfolds `Ut`; `partner_ends` unfolds `Ut` and `nu`.
- `partner_no_pole` uses `partner` (statement) and the continuity of `Ut`, and states its function as `partner`'s left
  side.

| id | mutation | first failure | failing set (exactly) | judge-checked error text | why |
|---|---|---|---|---|---|
| ZM1 | `nu` = ℓ + n/2 + 1 | `z_id` | {`z_id`, `partner`, `partner_ends`} | (not checked) | False: ν enters g. `g_hasDerivAt` keeps `nu` folded, and its derivative does not involve ν. `partner_ends`' first conjunct is ν(ν − 1), the second does not involve ν. `partner_no_pole` uses only `partner`'s statement. |
| ZM2 | `g`: n(n + 1)Y/((ℓ − 1) + nY) | `g_hasDerivAt` | {`g_hasDerivAt`, `z_id`, `partner`} | (not checked) | `hg`'s `rfl` fails: g's body no longer is the lambda. The rest of `g_hasDerivAt` uses `hg` as stated. `z_id` and `partner` unfold the new g against `deriv_g`'s old derivative. |
| ZM3 | `W` = U₋/(63H₋²) | `z_id` | {`z_id`} | (not checked) | False. Only `z_id` uses `W`. |
| ZM4 | `δ1` = 1/((n + 2)(ℓ + n)) | `gate_q1` | {`gate_q1`, `gate_H`, `z_id`} | (not checked) | All three unfold `δ1`; all three are false, and `field_simp` has no n + 2 ≠ 0. |
| ZM5 | `mm` = (ℓ − 1)(ℓ + n − 1) | `gate_q1` | {`gate_q1`, `gate_H`, `z_id`} | (not checked) | All three unfold `mm` and are false. |
| ZM6 | `z_id` with g² + g in the bracket | `z_id` | {`z_id`} | (not checked) | False (oracle 4 and 7). Nothing uses `z_id`. |
| ZM7 | `z_id` with (n − 2)Y ∂_Y g | `z_id` | {`z_id`} | (not checked) | False. |
| ZM8 | `partner` with −(n − 1)Y ∂_Y g | `partner` | {`partner`, `partner_no_pole`} | (not checked) | False. `partner_no_pole`'s `exact (partner …).symm` now has the other sign. |
| ZM9 | `Ut`'s constant term + 1 | `partner` | {`partner`, `partner_n4`, `partner_ends`} | "unsolved goals" (at `partner_n4`) | All three unfold `Ut` and are false. `partner_n4` is `unfold Ut; ring`: `ring` falls back to `ring_nf`, which leaves the goal. `partner_no_pole` uses `partner`'s statement and `Ut`'s continuity, both unchanged. |
| ZM10 | `gate_H`: H₋(2Y) = (ℓ + n)(ℓ + nY) | `gate_H` | {`gate_H`, `z_id`} | (not checked) | False. `z_id` rewrites with it, so its denominator holds ℓ + nY, which `field_simp` cannot clear. |
| ZM11 | `gate_q1` assuming ℓ + n ≠ 1 | `gate_q1` | {`gate_q1`} | (not checked) | False at n = 1, ℓ = −1, where Lean's δ₁ = 1/0 = 0 (oracle 7). `field_simp` cannot clear ℓ + n. |
| ZM12 | `partner` assuming (ℓ − 1) + nY ≠ 1 | `partner` | {`partner`, `partner_no_pole`} | (not checked) | False at n = 4, ℓ = 3, Y = −1/2, g's pole (oracle 7). `partner`'s `rw [deriv_g … hP]` and `partner_no_pole`'s `partner … hY2` each pass a hypothesis of the wrong type. |
| ZM13 | `g_hasDerivAt` with +ℓ/(1 − Y)² | `g_hasDerivAt` | {`g_hasDerivAt`, `deriv_g`} | (not checked) | False. `deriv_g` restates the old derivative from it, a type mismatch. `z_id` and `partner` use `deriv_g`'s statement. |
| ZM14 | `W` with U₋ at x = Y | `z_id` | {`z_id`} | (not checked) | False. `gate_H` still rewrites H₋(2Y). |
| ZM15 | `W` with U₋ at K = 0 | `z_id` | {`z_id`} | (not checked) | False. |
| ZM16 | `W` with U₋ at y = 1 | `z_id` | {`z_id`} | (not checked) | False. |
| ZM17 | `partner_no_pole` with limit Ũ(Y₀) + 1 | `partner_no_pole` | {`partner_no_pole`} | (not checked) | False: the limit is Ũ(Y₀) (oracle 5 and 7). The `refine` term's limit is Ũ(Y₀). |

Every spec is predicted to pass the judge: Lean exits non-zero; no parse error and no unknown name; no error before
the mutated line; the spec's declaration among the failing ones; for ZM9, the error text.

**What the mutations show:**
- **ZM1, ZM2 and ZM13:** g and its derivative are pinned: ν, the n(n − 1) coefficient, and the sign of ∂_Y g.
- **ZM3 and ZM14–ZM16:** W is U₋/(64H₋²) at x = 2Y, K = 1 and y = 0, each of them needed.
- **ZM4, ZM5, ZM10 and ZM11:** the q = 1 point. δ₁, m and H₋(2Y) are pinned, and `gate_q1` needs ℓ + n ≠ 0.
- **ZM6 and ZM7:** Z-id's bracket, its sign of g and its factor n − 1.
- **ZM8, ZM9 and ZM12:** the partner. The sign of its ∂ term and Ũ's constant are pinned, and (ℓ − 1) + nY ≠ 0 is
  needed.
- **ZM17:** P-reg's limit is Ũ(Y₀).
