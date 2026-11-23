# A1 Lean layer: registered predictions for mutations A1M1 to A1M8 (session-L, 2026-10-22, before any run)

This file was written before any mutation of `lean/BHModesA1.lean` had been run. Each spec had only been checked as text:
its old string occurs exactly once. The times are self-recorded. `lean/build.sh` records this file's sha256 in
`BUILD_LOG.txt` before the first mutation run, and the record binds once that hash reaches the operator.

**Predicted against:** `lean/BHModesA1.lean`, `lean/mutations.json`, and the vendored judge `lean/vendor/mutation.py`
(696b7864…, the IBCertificates judge of the client's item 414, with the `error_text` check). The sha256s are those in
`lean/SOURCES.tsv` and `BUILD_LOG.txt` of the run.

**What Lean does with a failed theorem.** A failed proof is kept with sorry, and later uses still elaborate. This was
established for S1c (C2 registration and evidence). Here no theorem uses another theorem, so each failing set is just
the theorems whose own statement or definitions change.

| id | mutation | first failure | failing set (exactly) | judge-checked error text | why |
|---|---|---|---|---|---|
| A1M1 | `KI_Um` (the transcription of (5.63b)): 64m³ → 63m³ | `KI_Um_n4` | {`KI_Um_n4`} | "unsolved goals" | Only `KI_Um_n4` unfolds `KI_Um`. Its final `ring` cannot close a false identity, so the goal stays open. |
| A1M2 | `Um` (TARGET.md's U₋): 7680 → 7681 | `KI_Um_n4` | {`KI_Um_n4`, `c_extremal`} | "unsolved goals" (at `KI_Um_n4`) | Both unfold `Um`. At x = 2 the change adds 4·m(1 + mδ) ≠ 0 to U₋, so c changes too. |
| A1M3 | `delta_extremal` states δ = 1/(5(ℓ + 5)) | `delta_extremal` | {`delta_extremal`} | (not checked; expected "linarith failed …") | The true root is 1/(5(ℓ + 4)), and the final `linarith` cannot reach the false goal. |
| A1M4 | `kappa_extremal`: 42M²/r⁸ → 41M²/r⁸ | `kappa_extremal` | {`kappa_extremal`} | (not checked; expected "unsolved goals") | At r³ = M the left side becomes 17/2 ≠ 9. The derivative lemmas are separate statements and are unchanged. |
| A1M5 | `BF_margin` with (2ℓ + 3)² | `BF_margin` | {`BF_margin`} | "unsolved goals" | This is a false polynomial identity, so `ring` fails. `nonvacuity_ell_two` has its own literals. |
| A1M6 | `f_horizon` with q²x_H²/3 | `f_horizon` | {`f_horizon`} | "ring failed, ring expressions not equal" | `linear_combination 4 * hs` leaves a nonzero remainder. `f_pos_exterior` states its own f. |
| A1M7 | `delta_relation`'s (5.58) with (n + 2)² | `delta_relation` | {`delta_relation`} | "ring failed, ring expressions not equal" | `linear_combination 25 * h58` no longer cancels. |
| A1M8 | `s_param` with 4mq²/24 | `s_param` | {`s_param`} | "Tactic `rewrite` failed: Did not find an occurrence of the pattern" | `rw [← h]` looks for h's right side, 1 + 4mq²/25, which no longer occurs in the goal. |

**How it will be read.**
- Agreement means the predicted first failure and exactly the predicted failing set, with `pass: true` from the judge,
  which also checks the registered error text where one is given.
- Any difference is reported as it stands, without changing a spec.
