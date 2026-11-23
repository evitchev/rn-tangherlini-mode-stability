# bh-modes Lean layer: the A1 identities (session-L, 2026-10-22)

This answers item 3(a) of the bh-modes lead's request of 2026-10-22. It is private under the quiet rule (bh-modes RULES.md
rule 8), and it follows the format and build rules of IBCertificates (RULES.md F).

**The module.** `lean/BHModesA1.lean` (sha256 in `lean/SOURCES.tsv`) holds 17 theorems. It uses Lean 4.24.0 with the
prebuilt Mathlib v4.24.0, the same pin as IBCertificates. The elan default on this machine is 4.30.0, so the build calls
the 4.24.0 binary by its path. Every statement is over ℝ.

| theorem | content |
|---|---|
| `KI_Hm_n4`, `KI_Um_n4` | Kodama–Ishibashi (5.62b) and (5.63b), transcribed for general n and K, equal TARGET.md's H₋ and U₋ at n = 4, K = 1, y = λr² = 0 |
| `m_of_ell` | (5.39): m = k² − 4 = (ℓ − 1)(ℓ + 4) for k² = ℓ(ℓ + 3) |
| `f_in_x`, `f_horizon`, `f_pos_exterior` | (2.19)/(5.40): f = 1 − x + q²x²/4 with x = 2M/r³ and q = Q/M; f(x_H) = 0 at x_H = 2/(1 + √(1 − q²)); f > 0 for 0 ≤ x < x_H (q² ≤ 1) |
| `delta_relation`, `delta_relation_iff` | (5.58) with (5.60) gives (1 + 2mδ)² = 1 + 4m(Q/M)²/25, which is equivalent to (5.65), Q² = 25M²δ(1 + mδ), when m ≠ 0 |
| `s_param` | s = 1 + 2mδ = √(1 + 4mq²/25), for m ≥ 0 and δ ≥ 0 |
| `delta_extremal` | at q = 1, for ℓ ≥ 2 and δ ≥ 0: δ = 1/(5(ℓ + 4)) |
| `f_extremal`, `f_hasDerivAt`, `f'_hasDerivAt`, `kappa_extremal` | at q = 1, f = (1 − M/r³)². The first and second derivatives of f(r) are proved (`HasDerivAt`). At r_H³ = M, κ r_H² = 9 with κ = f″(r_H)/2. |
| `c_extremal` | c = U₋(x_H)/(64 κ r_H² H₋(x_H)²) at x_H = 2 and δ = 1/(5(ℓ + 4)) equals ℓ(ℓ − 3)/9 |
| `BF_margin`, `nonvacuity_ell_two` | c + 1/4 = (2ℓ − 3)²/36; at ℓ = 2, c = −2/9 and the margin is 1/36 |

**Not proved.** The asymptotics V ≈ c/r*² near the degenerate horizon. Only its algebraic content is proved: the second
derivative of f, κ r_H² = 9, and the value of c.

**Named inputs.**
- The transcriptions of (5.62b) and (5.63b) (`KI_Hm`, `KI_Um`), from the rendered pages 24 and 25 of my own fetch of
  hep-th/0308128. That fetch is byte-identical to the screen's copy (`../session-L_citecheck_2026-10-22/cache/`).
- TARGET.md's H₋ and U₋ (`Hm`, `Um`).
- The specialisation theorem ties the two together. Mutation A1M1 shows that the transcription is load-bearing, and A1M2
  shows the same for TARGET.md's U₋.

**Checks.**
- `oracle/check_identities.py` (output `.out`) verifies every identity symbolically with sympy, exactly, before Lean,
  with two negative controls.
- `lean/build.sh` produced `lean/BUILD_LOG.txt`: "BHModesA1: ALL CHECKS AS REQUIRED".
  - Source hash ok; compile with 0 errors, 0 warnings and no sorry (5 s; 1.47 GB peak in the separate compiles).
  - The axiom audit gives 17 headers and 17 entries, with only propext, Classical.choice and Quot.sound.
  - Two checker negative controls are rejected.
  - The mutations give 8 / 8.
- `review/A1_MUTATION_REGISTRATION.md` (sha256 94c5b92e…) registered every mutation's first failure, failing set and
  error text. The build logged that hash at 17:33:25Z, before the first mutation run, and all eight agree in full.
- The judge is a byte copy of IBCertificates' `mutation.py`, listed in `lean/vendor/VENDOR.sha256`.

**Files.** `lean/` (module, `SOURCES.tsv`, `mutations.json`, `build.sh`, `BUILD_LOG.txt`, `logs/`, `vendor/`),
`oracle/`, `review/` and the compile logs `compile1.log` … `compile6.log`. compile1 is the run aborted by `import Mathlib`
under the 8 GB cap; compiles 2 to 5 failed on proof details, recorded as they ran. `SHA256SUMS` covers every file except
itself, `lean/build/` and `lean/.trash/`.

**Next candidates** (the request's order): (b) the A1 positivity certificates, once FEASIBILITY.md P1 and P2 exist;
(c) the 1c identities, that is the Leaver recurrence and the tail divisions; (d) the pencil lemmas.
