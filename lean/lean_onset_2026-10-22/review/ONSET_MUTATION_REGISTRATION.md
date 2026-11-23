# Onset Lean layer, item (b): registered predictions for mutations ONM1 to ONM10 (session-L, 2026-10-22, before any run)

I wrote this file before running any mutation of `lean/BHModesOnset.lean`. Each spec had been checked only as text: its
old string occurs exactly once. `lean/build.sh` records this file's sha256 in `BUILD_LOG.txt` before the first
mutation run.

**Predicted against:**
- `lean/BHModesOnset.lean` (sha256 `b71e0ed8…` in `lean/SOURCES.tsv`);
- `lean/mutations.json`;
- the vendored judge `lean/vendor/mutation.py` (`696b7864…`).

A failed proof is kept with sorry, and later uses of the theorem as a statement still elaborate. The file order is: the
generated section (Fp, Qp, Kμ, B1–B3 and their splits), then O5, O1, the boxes, O2, O3, O4 and the irreducibility.

| id | mutation | first failure | failing set (exactly) | judge-checked error text | why |
|---|---|---|---|---|---|
| ONM1 | `Um`: 7680 → 7681 | `param_U` | {`param_U`} | (not checked) | Only `param_U` unfolds `Um`. `O2` and `O3` use it as a statement. |
| ONM2 | one Bernstein coefficient of `B1` | `B1_split` | {`B1_split`, `box1`} | (not checked) | Both unfold `B1`. `B1_pos` uses `B1_split` as a statement. |
| ONM3 | `box3` claimed for μ ≤ 1/3 | `box3` | {`box3`, `O2_mu`} | (not checked) | vb = 1 − (12μ − 2) ≥ 0 needs μ ≤ 1/4. `O2_mu` passes μ ≤ 1/4 where μ ≤ 1/3 is now expected. |
| ONM4 | `g_factor` with 1023 | `g_factor` | {`g_factor`} | "unsolved goals" | A false small identity. `O2_mu` and `O3_mu` still close with 1023 (positivity, the zero cases, nlinarith). |
| ONM5 | `p_lo` at 0.19893240976 | `p_lo` | {`p_lo`, `p_root_exists`, `p_root_bounds`} | (not checked) | p > 0 there. `p_root_exists` needs `p_lo` at the original point in a typed term, and `p_root_bounds` gets no contradiction. |
| ONM6 | `C_pos` from Y ≥ 0 | `C_pos` | {`C_pos`, `C_root_unique`} | "linarith failed to find a contradiction" | C(0) < 0, so the final `nlinarith` fails. `C_root_unique` passes 1 ≤ a where 0 ≤ a is now expected. |
| ONM7 | `O4_bracket` with 4μ − 2 | `O4_bracket` | {`O4_bracket`, `O4`} | (not checked) | False. `O4` uses it to prove `hb` with 4μ − 3. |
| ONM8 | `param_of_q` concludes q(μ)² = q | `param_of_q` | {`param_of_q`, `O2`, `O3`, `O4`} | (not checked) | False. The three q-level theorems pass the result to `delta_of_q`, which needs q(μ)² = q². |
| ONM9 | `Fp`'s constant 165888 → 165889 | `param_U` | {`param_U`, `g_factor`, `box1`, `box2`, `F_split`} | (not checked) | Exactly these unfold `Fp`. `box3` unfolds only `Qp`. |
| ONM10 | `C_relation` with (6 + μ²)⁵ | `C_relation` | {`C_relation`} | (not checked) | False. `q2_root` still concludes from the changed statement, because (6 + μ²)⁵ ≠ 0 too. |

**How it will be read.** Agreement means the predicted first failure, exactly the predicted failing set, and
`pass: true` from the judge, which also checks the registered error texts. Any difference is reported as it stands.
