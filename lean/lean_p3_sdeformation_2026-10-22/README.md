# Lean layer, item (a): METHOD.md Lemmas 1–2, Proposition 3 and the Remarks (bh-modes): session-L, 2026-10-22

This answers §3 item (a) of the bh-modes lead's second message (`outbox/2026-10-22-to-session-L-2.md`): "the
S-deformation identity and the ansatz algebra (`results/p3/METHOD.md`, Lemmas 1–2)". I added Proposition 3 and the
Remarks, because they connect Lemmas 1–2 to item (c)'s certificates.

| file | content |
|---|---|
| `lean/BHModesP3.lean` | 27 theorems, namespace `BHModes.P3`; the header lists what is proved and what is not |
| `lean/build.sh`, `lean/BUILD_LOG.txt` | the audited build: compile, axioms, two negative controls, nine mutations (the A1 format) |
| `lean/SOURCES.tsv`, `lean/mutations.json`, `lean/vendor/` | the source hash, the mutation specs, the vendored judge (byte copy, `VENDOR.sha256`) |
| `review/P3_MUTATION_REGISTRATION.md`, `review/REGISTRATION_TIME.txt` | predictions for every mutation, written and hashed before the first run |
| `oracle/check_p3.py` and `.out` | the same mathematics outside Lean: sympy (with sympy doing the chain rule) and one mpmath quadrature |
| `SHA256SUMS` | every file except itself |

## The Lean statements (quoted from `lean/BHModesP3.lean`)

**Lemma 1** (`sdef_identity`). For V, S, S′ : ℝ → ℝ and φ, φ′ : ℝ → ℂ, with V continuous, S′ continuous and S′ the
derivative of S everywhere, and φ′ continuous, the derivative of φ, with φ compactly supported:

    ∫ x, (‖φ' x‖ ^ 2 + V x * ‖φ x‖ ^ 2) =
      (∫ x, ‖φ' x + (S x : ℂ) * φ x‖ ^ 2) + ∫ x, (V x + S' x - S x ^ 2) * ‖φ x‖ ^ 2

- φ ∈ C¹ with compact support covers C₀^∞(ℝ), as TARGET.md §2 has it.
- `sdef_identity_real` is the real case.
- The Corollary is `form_nonneg_of_sdef`: if V + S′ − S² ≥ 0 everywhere, the form is ≥ 0.

**Lemma 2** (`ansatz_identity`). Units r_H = 1, z = `zc ρ` = 1 − ρ⁻¹, with U, H, F, F′, P, P′ : ℝ → ℝ as functions of
z. For ρ ≠ 0 and H(z) ≠ 0:

    F z * U z / (64 ρ² H z²) + F z * (−(f′ β + F z β′)) − (−(F z β))²  =  F z * Nz … z / (64 ρ² H z²)

- Here f′ = (1 − z)² F′ z, β = (1 − z) P z and β′ = (1 − z)²(−P z + (1 − z) P′ z).
- `Nz` is METHOD's N: `U z − 64 H z² ((1 − z) F′ z P z + F z (−P z + (1 − z) P′ z + P z²))`.
- The derivative facts are theorems: `zc_hasDerivAt` (dz/dρ = (1 − z)²), `f_hasDerivAt`, `beta_hasDerivAt` and
  `Srho_hasDerivAt`.

**Proposition 3** (`prop3`; D = 6 instance `prop3_D6`). Assume:
- F and P are differentiable with continuous derivatives F′ and P′;
- U and H are continuous;
- R : ℝ → ℝ has dR/dt = F(zc(R t)) and R t > 1 for all t;
- 0 ≤ F, H ≠ 0 and 0 ≤ Nz on (0, 1).

Then for every C¹ compactly supported φ : ℝ → ℂ:

    0 ≤ ∫ t, (‖φ' t‖ ^ 2 + Vrho U H F (R t) * ‖φ t‖ ^ 2)

Here `Vrho U H F ρ = F(zc ρ) U(zc ρ)/(64 ρ² H(zc ρ)²)`. `prop3_D6` discharges every hypothesis except R and N ≥ 0, for
q² ≤ 1, m > 0, δ ≥ 0 and TARGET.md's f, U₋ and H₋. `Vrho_D6` and `F6_zc_TARGET` show that its V is TARGET.md's
f U₋/(64 r² H₋²), and its f is 1 − 2M/r³ + (qM)²/r⁶, in units r_H = 1.

**The Remarks:**
- `N_at_horizon`, `N_at_horizon_D6`: N(0) = U₋(x_H) − 64 H₋(x_H)² f_z(0) P(0).
- `N_at_infinity_D6`: N(1) = 64m²(m + 6 − P(1)² + P(1)).
- `N_at_infinity_ell2`: for m = 6, 0 < N(1) ⟺ −3 < P(1) < 4.
- `N_eps_shift`: N(P − ε) = N(P) + 64H²ε[(1 − z)f_z + f(2P − 1 − ε)].
- `rho_fprime`: ρ f′ = (1 − z) f_z.

## What this does not prove

- **That the inverse tortoise map exists.** `prop3` takes R as a hypothesis and holds for every R with dR/dr* = f(R)
  and R > 1. TARGET.md §1 takes the tortoise coordinate as given.
- **C^∞ smoothness.** Only C¹ is used.
- **The scaling to absolute units.** The statements are in units r_H = 1. TARGET.md's form scales uniformly.
- **That the form determines A.** That is TARGET.md's reading.
- **N ≥ 0 for a concrete P.** That is item (c). `prop3_D6` is the interface: given (c)'s N ≥ 0 on [0, 1] for each μ in
  a box, it gives the form ≥ 0 for every q in that box's image.

## Checks

- **Oracle.** `oracle/check_p3.py`: all 13 checks hold, including its two negative controls (`oracle/check_p3.out`).
- **Build.** `lean/BUILD_LOG.txt`: "BHModesP3: ALL CHECKS AS REQUIRED".
  - Lean 4.24.0 with the prebuilt Mathlib v4.24.0.
  - Compile: exit 0, 0 errors, 0 warnings, 0 sorry, 7 s.
  - `#print axioms`: 27/27 theorems use only propext, Classical.choice and Quot.sound.
  - Both checker negative controls are rejected.
- **Mutations.** `review/P3_MUTATION_REGISTRATION.md` (sha256 `16d5b0a6…`) registered, for every mutation, its first
  failure, its exact failing set and, for three of them, the error text. Its hash was logged at 18:42:03Z
  (`review/REGISTRATION_TIME.txt`) and again by the build at 18:42:30Z, before the first mutation run.
  - All nine agree in full: the first failure, the failing set and the judge's `pass`.
  - P3M6's error, not registered, was the expected "linarith failed to find a contradiction".
- **One statement-level slip, caught before the record.** My first draft of Lemma 1 wrote
  `∫ x, A + ∫ x, B` without brackets. Lean parses that as `∫ x, (A + ∫ x, B)`, and the proof failed. The statements
  now bracket the first integral. I checked every other integral in the file for the same parse.

**Files.** `SHA256SUMS` covers every file except itself.
- The build outputs (`lean/build/`, `lean/.trash/`) are not kept here. `lean/build.sh` regenerates them in about two
  minutes.
- The privacy screen covers binary files. On the compiled `.olean`, one screen term (index 6) matched as a substring of a
  Mathlib identifier. That is not personal data, but I moved the outputs out of the folder anyway.
