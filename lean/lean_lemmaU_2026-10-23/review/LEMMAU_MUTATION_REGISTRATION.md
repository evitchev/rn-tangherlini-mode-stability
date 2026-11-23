# Lemma U Lean layer (bh-modes BHM-052): registered predictions for mutations LUM1 to LUM10 (session-L, 2026-10-23, before any run)

I wrote this file before running any mutation of `lean/BHModesLemmaU.lean`.
- **Development.** The unmutated file was compiled during development on the editing node: exit 0, no messages, 7 s.
- **Mutations.** Each spec has been checked only as text: its old string occurs exactly once. None has been run.
- **Logging.** `lean/build.sh` logs this file's sha256 in `BUILD_LOG.txt` before the first mutation run.

**Predicted against:**
- `lean/BHModesLemmaU.lean`: sha256 `e788d32421f9066a…`, in `lean/SOURCES.tsv`;
- `lean/mutations.json`: `7f4e3e042f956c41…`;
- the vendored judge `lean/vendor/mutation.py`: `696b7864…`;
- `lean/build.sh`: `88ac716f4199adfe…`.

**What a failed proof does.** A failed `by` block is replaced by sorry, so later uses of its theorem as a statement
still elaborate. The file order is: `split`, `Pos_zero`, `kappa_identity`, `Pos_ge`, `Neg_mono`, `corner`,
`corner_margin`, `lemmaU`, `lemmaU_ell`, `xH_le_two`.

| id | mutation | first failure | failing set (exactly) | judge-checked error text | why |
|---|---|---|---|---|---|
| LUM1 | `Um`: 7680 → 7681 | `split` | {`split`} | (not checked) | Only `split` unfolds `Um`. `lemmaU` uses `split` as a statement. |
| LUM2 | `Pos`: constant 64 → 65 | `split` | {`split`, `Pos_zero`} | (not checked) | Both unfold `Pos`. `Pos_ge` still holds, since 65 ≥ 64. |
| LUM3 | `Neg`: 7680ε⁴x → 7681ε⁴x | `split` | {`split`, `corner`} | (not checked) | Both unfold `Neg`, and the corner value changes. `Neg_mono` compares the mutated `Neg` with itself and still holds. `corner_margin` and `lemmaU` use `corner`'s statement. |
| LUM4 | `kappa_identity` states q²/25 − 2δ | `kappa_identity` | {`kappa_identity`, `lemmaU`} | "linarith failed to find a contradiction" (at `kappa_identity`) | The final `linarith` would need δ = 0. `lemmaU` states `hκsq` with − δ, so the changed theorem no longer has that type: a mismatch inside `lemmaU`. |
| LUM5 | `lemmaU` assumes 140 ≤ m | `lemmaU` | {`lemmaU`} | "linarith failed to find a contradiction" (at `lemmaU`) | 144 ≤ m, which √m ≥ 12 needs, no longer follows. `lemmaU_ell` proves the threshold by `linarith`, which still works. |
| LUM6 | `hκ5` claims κ ≤ 1/6 | `lemmaU` | {`lemmaU`} | "linarith failed to find a contradiction" (at `lemmaU`) | False for large m, where κ → 1/5, so `nlinarith` cannot prove it. The later `Neg_mono` application then mismatches too, inside `lemmaU`. |
| LUM7 | `lemmaU` assumes x ≤ 3 | `lemmaU` | {`lemmaU`} | (not checked) | `Neg_mono` needs x ≤ 2: an application type mismatch. `lemmaU_ell` supplies the bound by `linarith`. |
| LUM8 | `hε12` claims ε ≤ 1/13 | `lemmaU` | {`lemmaU`} | (not checked) | √m ≥ 12 gives only 1/12, so the `exact` mismatches, and so does the `Neg_mono` application. |
| LUM9 | `corner` states 159998/17496 | `corner` | {`corner`, `corner_margin`} | (not checked) | `corner_margin` rewrites with `corner`'s false statement, and its `norm_num` fails. `lemmaU` uses `corner_margin`'s statement. |
| LUM10 | `lemmaU_ell` assumes 10 ≤ ℓ | `lemmaU_ell` | {`lemmaU_ell`} | (not checked) | `exact_mod_cast` cannot give 11 ≤ ℓ; at ℓ = 10, m = 126 < 150. The rest elaborates with the stated fact. |

**How it will be read.**
- Agreement means three things: the predicted first failure, exactly the predicted failing set, and `pass: true` from
  the judge, which also checks the registered error texts.
- The build must also pass its other checks: compile with exit 0 and no errors, warnings or sorry; the axiom audit;
  both negative controls.
- Any difference is reported as it stands.
- The build of record runs on the reproduction node, as the operator ruled on 2026-10-23.
