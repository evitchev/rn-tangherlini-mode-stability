# AUDIT — bh-modes A2-E and A2-S, D = 6 through extremality (BHM-096, BHM-100)

*Auditor: Kimi (second auditor for machine results), 2026-10-25.
Brief: `results/a2/briefs/BRIEF_kimi_2026-10-24.md`, SHA-256
`6a818337dbfccc19f31b775a930dbe7fa84f01af8f8274987346e3935531c86f` (verified against
`SEALED.sha256`; all artifact and code hashes in the brief verified).
Workspace: `[kimi-folder]/bhm-a2-audit-2026-10-25/`.
Runs of record: own suite on **host-1** (logs `own/*.host-1.log`, copies kept on the node),
reproductions on **host-2**; `nice -n 19`, the pinned venv. Development spot checks (< 1 min)
on host-0. The bh-modes tree was never modified.*

**Anti-anchoring (allow-list).** Only the brief's listed files and my own earlier workspaces
were read before my own checks were complete. The pilot record was read only in its `design`
field.

## Task 1 — transcription

My own KI (5.62b)/(5.63b) transcription (p3 audit, BHM-036), validated against the rendered
PDF.

## Task 2 — A2-E: PASS for every ℓ = 3…10

My own machinery (`own/a2e.py`, on my a1-audit rf arithmetic and fixed Bernstein verifier):
per ℓ, F(t, μ)/Den(μ) built exactly, the parametrisation identities and w increasing checked,
μ_lo(ℓ) by the registered rule with exact coverage q(μ_lo)² ≥ (99/100)², Den > 0 on
[0, μ_lo].

- ℓ = 4…10: F > 0 on [0, 1] × [0, μ_lo], strict, one Bernstein box each.
- ℓ = 3: the exact splitting F(1−s, μ) = μK(μ) + sG(s, μ) — both polynomial divisions exact
  (remainders verified 0), K > 0 on [0, μ_lo] and G > 0 on [0, 1] × [0, μ_lo] proved — so
  F ≥ 0 with equality only at s = μ = 0, i.e. (x, q) = (x_H, 1) = (2, 1). The exact gate fact
  U₋(x_H) = 64ℓ(ℓ−3)(ℓ+3)²(ℓ+4)² at q = 1 verified identically in ℓ (so F(1, 0) = 0 at ℓ = 3
  and only there among ℓ ≥ 3).

Logs: `own/a2e.host-1.log` (host host-1).

## Task 3 — A2-S: PASS

My own build (`own/a2s.py`): p₀ = Σ c_j T_j(2z−1) from the pilot record's `cheb` strings via
`float.fromhex` (exact binary rationals), converted by my own Chebyshev recurrence;
P = Π/S with S = ε_d z + ε_n, Π = a(ε_d + ε_n) + p₀S, a = −2/5, ε_n = 7μ,
ε_d = 3(6 + 7μ + μ²). NL := N·S² is a polynomial in (z, μ); cleared by Den(μ) = (μ+1)³(μ+6)
> 0 (proved factorwise on [0, 1/8]).

- NL(0, 0) = 0 exactly, as registered (the corner).
- Gates: S > 0 off the corner (ε_d > 0 proved; ε_n = 7μ ≥ 0, zero only at μ = 0, and z > 0 on
  the domain); q(1/8)² = 2961/3025 ≤ (99/100)² exactly; w increasing; the exact divisions
  NL(μζ, μ)/μ² and NL(z, zσ)/z² are polynomial (remainders 0).
- Charts, each positive on its closed box by my verifier (`own/a2s_charts.host-1.log`):
  O = [1/4, 1]×[0, 1/8], O′ = [0, 1/4]×[1/32, 1/8], T(ζ, μ) on [0, 8]×[0, 1/32],
  C(z, σ) on [0, 1/4]×[0, 1/8] — one Bernstein box each.
- Coverage (my own pencil argument, with the inequalities checked exactly): for z < 1/4 and
  μ < 1/32, either z ≤ 8μ and (z/μ, μ) lies in T, or μ < z/8 and (z, μ/z) lies in C; the rest
  is O or O′. On T, NL = μ²T > 0 (μ > 0 since z > 0); on C, NL = z²C > 0 (z > 0). Hence
  N > 0 on (0, 1) × [0, 1/8].
- G-RES re-derived symbolically in (ℓ, a, b₀, b₁) (`own/controls_a2.host-1.log`): at q = 1,
  N(0) = 576H₋(2)²(ℓ(ℓ−3)/9 − a(a+1)); the b₀, b₁ independence and the limit
  9a(a+1) of the bracket were derived from my own transcription.

## Task 4 — pencil verdicts

- **(a) The reduction for the singular design: SOUND.** For μ ∈ [0, 1/8] the pole
  z = −ε ≤ 0 lies off the open exterior (0, 1); at μ = 0 it sits at the horizon endpoint,
  where f has a double zero and S = −f(1−z)P ∼ −9az stays smooth (C¹ is all METHOD's Lemma 1
  needs; the test functions live on compact subsets of the open interval). Proposition 3 then
  applies per μ.
- **(b) The tortoise map at q = 1: SOUND.** f = (1 − x/2)² has a double zero at the horizon;
  r* ~ −1/(9(ρ − 1)) → −∞ there (the 1/9 limit I verified exactly in BHM-038's E2), and
  r* → +∞ at infinity; monotone C^∞ onto ℝ.
- **(c) The composition of Theorem A2: SOUND.** ℓ = 2: A2-S covers [q(1/8), 1] with
  q(1/8)² = 2961/3025 ≤ (99/100)² exactly, so [99/100, 1] ⊂ it. ℓ = 3…10: A2-E covers
  [q(μ_lo(ℓ)), 1] and A1's P1 covers [0, q(μ_lo(ℓ))]; they meet at q(μ_lo(ℓ)), included in
  both (closed boxes). ℓ ≥ 11: Lemma U, q ∈ [0, 1]. The step from U₋ ≥ 0 to A ≥ 0 uses only
  f > 0 and H₋ > 0 on the exterior, at q = 1 too (f = (1−x/2)² > 0 for x < 2).

## Task 5 — controls: all REJECT as required (`own/controls_a2.host-1.log`)

- **(a)** A2-E at ℓ = 2: REJECT, corner F(1, 0) = −691200 < 0 (the ℓ = 2 ditch at q = 1).
- **(b)** strict bound for ℓ = 3 on its full box: refused, with the value exactly 0 at
  (t, μ) = (1, 0).
- **(c)** design with a = −7/10 (residue outside (−2/3, −1/3)): REJECT — negative values in
  both the T chart (at (ζ, μ) = (4, 1/64)) and the C chart (at (1/8, 1/16)), exact.
- **(d)** zero-margin: the design moved to the window's edge (a = −1/3, where
  a(a+1) = −2/9 = c(2) exactly) with the planted p₀ → p₀ − 1/10: N(0) = 0 exactly at q = 1,
  the rest positive (N/z > 0 on [0, 1] verified exactly), and the strict check refuses with
  the exact value 0 at z = 0.
- **(e)** planted bound state in the throat at q = 1 (b = ((z−1/20)(1/5−z))², support
  z ∈ [1/20, 1/5] i.e. r ∈ [20/19, 5/4], K = 3435248): Q[b] = A − K·C < 0 rigorously
  (A = [2.757418085e-9 ± 9.1e-19], C = [1.6e-15 ± 3.5e-17], whole support, weights derived
  from the quadratic form); the certificate at q = 1 against V + W then REJECTs exactly at
  z = 1/2.
- **(f)** verifier tamper: caught by the KAT suite (KAT1–KAT8, including the
  coefficient-level substitution checks).

*Self-corrections recorded during this audit:* (i) my first (d) construction (a U-tamper at
a = −1/2) achieved the exact zero but not the rest-positive premise; the final construction
(window-edge residue + p₀ lift) achieves both, and is what is logged. (ii) A δ-slip (1/25 for
1/30 at ℓ = 2) in early development versions of (d)/(e), caught by the G-RES cross-check
(N(0) ≠ 0 when it had to be 0); the logged runs use the correct δ.

## Task 6 — reproductions

- `kit/a2/run_elementary.sh` at `e422d74` on **host-2**: exit 0, **KIT PASS** (main VERIFIED;
  nc-ell2, nc-strict, nc-bump, td-coeff, td-verifier REJECT as registered).
- `kit/a2/run_s.sh` at `25c796e` on **host-2**: exit 0, **KIT PASS** (main VERIFIED; nc-a2,
  nc-zm, nc-res reject by POS charts as registered; nc-bound rejects as `nc-bound (b)`;
  td-coeff, td-verifier, td-chart, td-cover reject as registered). Both reproductions' main
  `result.json` are substantively identical to the records (timings/provenance masked).

## Overall verdict

**A2-E and A2-S stand:** every claim
re-derived by my own exact route, the corner structures handled explicitly, the pencil
extensions SOUND, my controls reject, and both kits reproduce the records bit-for-bit at the
substantive level. With P1/Lemma U (BHM-065), the ℓ = 2 band
(BHM-023/036), the onset (BHM-017/037) and E0–E5 (BHM-010/038), Theorem A2's inputs are all
second-party checked.

Pointer for the operator: audit workspace `[kimi-folder]/bhm-a2-audit-2026-10-25/`
(AUDIT.md, audit_record.json, SHA256SUMS).
