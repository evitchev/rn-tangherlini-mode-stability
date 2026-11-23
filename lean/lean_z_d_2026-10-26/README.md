# Lean layer for Z, item (d): the tortoise map at q = 1 and A_{ℓ,1} ≥ 0 (bh-modes BHM-126): session-L, 2026-10-26

This answers the bh-modes lead's message 9 (`outbox/2026-10-26-to-session-L-9.md`, item 3): item (d) of message 8, and
the chain-rule step that lean_z's README listed as pencil. It is a separate build; lean_z (BHM-134) is unchanged.
- **Result: "BHModesZd: ALL CHECKS AS REQUIRED"** (`lean/BUILD_LOG.txt`). All 15 mutations pass the judge, and all
  fifteen agree with the registration in full.
- **Oracle: "ALL ZD CHECKS HOLD (34/34)"** (`oracle/check_zd.out`).
- **Host:** the build of record and the oracle's run of record ran on the reproduction node of the bh-modes
  environment, under `nice -n 19`.

## The file

`lean/BHModesZd.lean`, namespace `BHModes.Z`, 773 lines, 46 theorems, in three parts (oracle check 1):
- **Lines 36–174** are lean_z_2026-10-26's `BHModesZ.lean` lines 25–163, byte for byte: the definitions and (a)–(c)
  as receipted in BHM-134.
- **Lines 180–239** are p3 v5's `BHModesP3.lean` lines 86–145, byte for byte: Lemma 1 (`sdef_identity`) and its
  Corollary (`form_nonneg_of_sdef`), as receipted before.
- **From line 241 on is the new section (d), with 35 theorems.**
  - **Units.** r_H = 1 at q = 1. In S5's x = 2M/r^(n−1), the extremal horizon x = 2 gives M = 1, so x = 2Y with
    Y = ρ^(−(n−1)).
  - **n** is an integer ≥ 2 (`n : ℕ`, `2 ≤ n`), and ℓ is real, so integer ℓ is included.

**The new definitions:**

    def Yr (n : ℕ) (ρ : ℝ) : ℝ := ρ⁻¹ ^ (n - 1)                       -- Y = ρ^(−(n−1))
    def fr (n : ℕ) (ρ : ℝ) : ℝ := (1 - Yr n ρ) ^ 2                    -- f at q = 1
    def tort (n : ℕ) (ρ : ℝ) : ℝ := ∫ s in (2 : ℝ)..ρ, 1 / fr n s      -- r*(ρ), base point ρ = 2
    def Rt (n : ℕ) : ℝ → ℝ := Function.invFunOn (tort n) (Set.Ioi 1)  -- R = (r*)⁻¹
    def wr (n : ℕ) (ℓ ρ : ℝ) : ℝ := fr n ρ * g n ℓ (Yr n ρ) / ρ        -- w = f g/ρ
    def Vr (n : ℕ) (ℓ ρ : ℝ) : ℝ := fr n ρ * W n ℓ (Yr n ρ) / ρ ^ 2    -- V_S− = f W/ρ²
    def Vtr (n : ℕ) (ℓ ρ : ℝ) : ℝ := fr n ρ * Ut n ℓ (Yr n ρ) / ρ ^ 2  -- the partner f Ũ/ρ²
    def u0 (n : ℕ) (ℓ ρ : ℝ) : ℝ :=
      ρ ^ (-nu n ℓ) * (1 - Yr n ρ) ^ (-(ℓ / ((n : ℝ) - 1))) / ((ℓ - 1) + n * Yr n ρ)   -- real powers
    def Vstar (n : ℕ) (ℓ t : ℝ) : ℝ := Vr n ℓ (Rt n t)                  -- V_S− as a function of r*

- `dg` is ∂_Y g, as stated in `g_hasDerivAt`, and `dwr` is dw/dρ, written out.
- `fr_S5` shows `fr` is S5's f = 1 − x + q²x²/4 at q = 1 and x = 2Y.
- `Vr_S5` shows `Vr` is S5's V_S− = f U₋/(64 r² H₋²) at q = 1, K = 1, y = 0 and x = 2Y, with r = ρ.

## The statements

**The tortoise map** (`tortoise_q1`, l. 463–465):

    theorem tortoise_q1 (n : ℕ) (hn : 2 ≤ n) :
        StrictMonoOn (tort n) (Set.Ioi 1) ∧ Set.BijOn (tort n) (Set.Ioi 1) Set.univ ∧
          ∀ ρ, 1 < ρ → HasDerivAt (tort n) (1 / fr n ρ) ρ

The bounds behind the bijection, `tort_ge` and `tort_le`:
- r*(ρ) ≥ ρ − 2 for ρ ≥ 2;
- r*(ρ) ≤ (1 − 1/(ρ − 1))/(n − 1)² for 1 < ρ ≤ 2, from f ≤ (n − 1)²(ρ − 1)² (`fr_le_sq`, by Bernoulli's
  inequality).

**The inverse** (`Rt_spec`, `Rt_tort`, `Rt_hasDerivAt`): for every t, 1 < R(t) and r*(R(t)) = t; for every ρ > 1,
R(r*(ρ)) = ρ. R is strictly increasing and continuous, and

    theorem Rt_hasDerivAt (n : ℕ) (hn : 2 ≤ n) (t : ℝ) : HasDerivAt (Rt n) (fr n (Rt n t)) t

**The chain-rule step** (`riccati_plus`, l. 552–556, and `riccati_minus`, l. 574–577). With w′ = dw/dr* =
f·dw/dρ:

    theorem riccati_plus (n : ℕ) (hn : 2 ≤ n) (ℓ : ℝ) (hℓ : 1 ≤ ℓ) (ρ : ℝ) (hρ : 1 < ρ) :
        ρ ^ 2 * (wr n ℓ ρ ^ 2 + fr n ρ * deriv (wr n ℓ) ρ) / fr n ρ
          = 2 * ((n : ℝ) - 1) * Yr n ρ * (1 - Yr n ρ) * g n ℓ (Yr n ρ)
            + (1 - Yr n ρ) ^ 2 * (g n ℓ (Yr n ρ) ^ 2 - g n ℓ (Yr n ρ)
              - ((n : ℝ) - 1) * Yr n ρ * deriv (g n ℓ) (Yr n ρ))

- The right side is (a)'s left side, `z_id`'s, at Y = ρ^(−(n−1)).
- `riccati_minus` is the same with w² − w′ on the left and (c)'s left side, `partner`'s, on the right.
- With (a) and (c) these give `V_eq`, V = w² + f·dw/dρ (for ℓ ≥ 2), and `Vt_eq`, Ṽ = w² − f·dw/dρ (for ℓ ≥ 1), at
  every ρ > 1.

**S = −(log u₀)_{r*}** (`log_u0_hasDerivAt`, `w_log_deriv`, `S_eq`):
- d(log u₀)/dρ = g/ρ on (1, ∞);
- the r*-derivative of log u₀(R(r*)) is w(R(r*));
- so −w(R) = −(log u₀ ∘ R)′.

**The zero mode in r*** (`zero_mode`): U = u₀ ∘ R has U′ = w(R)U and (w(R)U)′ = V(R)U. That is U″ = V U, the q = 1
zero-energy master equation of BHM-126, now in r*.

**A_{ℓ,1} ≥ 0** (`A_nonneg`, l. 751–753):

    theorem A_nonneg (n : ℕ) (hn : 2 ≤ n) (ℓ : ℝ) (hℓ : 2 ≤ ℓ) (φ φ' : ℝ → ℂ)
        (hφ : ∀ x, HasDerivAt φ (φ' x) x) (hφ' : Continuous φ') (hc : HasCompactSupport φ) :
        0 ≤ ∫ x, (‖φ' x‖ ^ 2 + Vstar n ℓ x * ‖φ x‖ ^ 2)

- **The proof** applies `form_nonneg_of_sdef`, p3's Corollary of Lemma 1, with V = V_S−(R(r*)) and S = −w(R), which
  is −(log u₀)_{r*} by `S_eq`.
- S′ = −f(R)·(dw/dρ)(R), which is −(V(R) − w(R)²) by `V_eq`. Then V + S′ − S² = 0 everywhere.
- V and S′ are continuous, from those of V on (1, ∞), of w and of R.

**How they read against the request.**
- **The tortoise map at q = 1 as an increasing bijection (1, ∞) → ℝ, for every integer n ≥ 2:** `tortoise_q1`, with
  dr*/dρ = 1/f.
  - The base point ρ = 2 is a choice. r* is defined up to a constant, and A_{ℓ,1} does not depend on it.
- **Lemma 1 with S = −(log u₀)_{r*}, giving A_{ℓ,1} ≥ 0 on C₀^∞(ℝ):** `A_nonneg`.
  - It covers C¹ functions with compact support, so C₀^∞ is included, as in p3's `prop3`.
  - The form is ∫(‖φ′‖² + V‖φ‖²) dr*, with V = V_S− at q = 1 composed with R.
- **The chain-rule step ρ²(w² ± w′)/f, with w = f g/ρ:** `riccati_plus` and `riccati_minus`, stated with the
  derivative of the function ρ ↦ w, so nothing about w′ is assumed.

## What this does not prove

- **C^∞ smoothness.** C¹ is all that is used, as in p3.
- **Absolute units.** The statements are in units r_H = 1. A_{ℓ,1} ≥ 0 does not depend on the scale, but the
  rescaling is pencil, as in the earlier READMEs.
- **The operator reading.** That the quadratic form determines A (TARGET's reading) is not proved here, as before.
- **The rest of RESULT's partner section.** The intertwiner L = ∂_{r*} − w, its action on solutions and the
  quasinormal-mode conditions stay pencil. They were not asked.

## Checks

- **Oracle** (`oracle/check_zd.py`, sympy 1.14.0 and mpmath 1.3.0; run of record on the reproduction node): all 34
  checks hold.
  - **Method.** The oracle reads the file's own Lean text with check_z.py's parser, extended with ⁻¹, type
    ascriptions, `Real.log` and ∧. ρ-derivatives are taken two ways:
    - for n symbolic, with Y a symbol and d/dρ = ∂_ρ − ((n − 1)Y/ρ)∂_Y;
    - for n = 2…9, with Y = ρ^(−(n−1)).
  1. The two copied blocks have the sha256 of their sources. The file ends with the namespace, and its theorems are
     the expected 46, in order.
  2. `fr_S5` and `Vr_S5` hold identically, and `dg` is ∂_Y g.
  3. The derivatives stated in `Yr_hasDerivAt`, `fr_hasDerivAt` and `wr_hasDerivAt` are the derivatives.
  4. `riccati_plus`, `riccati_minus`, `V_eq` and `Vt_eq` hold identically, with deriv w and deriv g computed by the
     oracle.
  5. `log_u0_hasDerivAt` holds. Information: V − Ṽ is not 0.
  6. Information, numerically at n = 2, 4 and 9:
     - r*(2) = 0; r* increases; r* ≥ ρ − 2; and r* ≤ (1 − 1/(ρ − 1))/(n − 1)²;
     - R inverts r*, and dR/dt = f(R) at t = −1000…1000, to 4·10⁻²⁷;
     - the S-deformation identity ∫(fφ_ρ² + Vφ²/f)dρ = ∫(fφ_ρ − wφ)²/f dρ, for a bump at n = 4, ℓ = 2. Both sides are
       1.21984534828.
  7. Controls: each of ZD1–ZD15, applied as text, makes its target false.
     - Algebraic targets are checked in sympy.
     - Analytic targets are checked numerically: r*(2) = 0 with r* increasing (ZD1, ZD2), dr*/dρ = 1/f (ZD3) and
       dR/dt = f(R) (ZD4).
     - For ZD11 (A_{ℓ,1} − 1 ≥ 0), a bump on ρ ∈ (100, 300) makes the form negative.
- **Build** (`lean/BUILD_LOG.txt`):
  - compile: exit 0, 5 s, 0 errors, 0 warnings, 0 sorry;
  - axioms: 46/46 theorems use only propext, Classical.choice and Quot.sound;
  - negative controls: both rejected;
  - mutations: 15/15 pass the judge.
- **Registration against the run: all fifteen agree in full** (`review/REGISTRATION_VS_RUN.txt`).
  - **Timing.** `review/ZD_MUTATION_REGISTRATION.md` (sha256 `0f12a18a…`) was written and hashed at 19:06:12Z. The
    build started at 19:06:16Z and logged the hash at 19:06:47Z, before the first mutation run.
  - **Agreement.** First failure, exact failing set and the judge's pass agree for every spec.
  - **No timeouts.** No proof hit the heartbeat limit, so no error was placed at a declaration's start (lean_z's
    ZM4/5/10). `riccati_plus` and `riccati_minus` carry line comments rather than doc comments for that reason.
- **What the mutations show:**
  - **ZD1–ZD3:** the tortoise map is increasing, a bijection from (1, ∞), and dr*/dρ = 1/f.
  - **ZD4:** dR/dr* = f(R).
  - **ZD5–ZD7 and ZD12:** the chain-rule step needs w′ = f·dw/dρ; (c)'s bracket is pinned; V = w² + w′ with its sign;
    and V = fW/ρ².
  - **ZD8, ZD9 and ZD15:** d(log u₀)/dρ = g/ρ, u₀'s throat exponent ℓ/(n − 1), and ∂_Y g inside dw/dρ.
  - **ZD10 and ZD11:** the zero mode solves the equation with V, not Ṽ, and A_{ℓ,1} ≥ 0 does not extend to A_{ℓ,1} − 1.
  - **ZD13 and ZD14:** the throat bound (n − 1)², and Bernoulli's factor n − 1.
- **Error texts, for the record** (first lines, as Lean printed them; none was registered):
  - "Application type mismatch: The argument": ZD1, ZD2, ZD3, ZD12;
  - "Type mismatch": ZD3, ZD11, ZD14;
  - "Type mismatch: After simplification, term": ZD3, ZD4;
  - "unsolved goals": ZD4–ZD9, ZD12, ZD15;
  - "ring failed, ring expressions not equal": ZD5, ZD7;
  - "Tactic `rewrite` failed: Did not find an occurrence of the pattern": ZD6, ZD12, ZD13;
  - "Tactic `apply` failed: could not unify the conclusion": ZD8;
  - "Tactic `unfold` failed to unfold `Vstar`": ZD10;
  - "linarith failed to find a contradiction": ZD14.

## Host and environment

- **The build of record and the oracle** ran on the reproduction node, under `nice -n 19`.
  - Before the run, the folder there was identical to this one, 11 files by sha256.
  - The build's inputs were unchanged after it.
  - The logs and `oracle/check_zd.out` were copied back here, byte for byte.
  - The build took about two minutes (19:06:16Z to 19:08:25Z), with mutation runs of 5–15 s each.
  - The build outputs (`build/`) were left on the node; `lean/build.sh` regenerates them.
- **Development on the editing node** is listed in the registration's "What is and is not blind":
  - four compiles of the unmutated file;
  - two heartbeat-count copies;
  - one oracle run, 34/34, on the final file.

  No mutation was compiled there.

## Files

| file | content |
|---|---|
| `lean/BHModesZd.lean` | the source: 46 theorems, namespace `BHModes.Z`; lines 36–174 lean_z's, lines 180–239 p3 v5's Lemma 1 |
| `lean/build.sh` | lean_z's `build.sh` with the file, registration and title names changed |
| `lean/lean-toolchain`, `lean/vendor/` | byte copies of the earlier builds' (judge `696b7864…`) |
| `lean/mutations.json` | ZD1–ZD15, all new |
| `lean/SOURCES.tsv` | the source's hash and its origin |
| `lean/BUILD_LOG.txt`, `lean/build_stdout.txt`, `lean/logs/` | the build of record |
| `review/ZD_MUTATION_REGISTRATION.md`, `review/REGISTRATION_TIME.txt` | predictions, written and hashed before the run |
| `review/compare_registration_zd.py`, `review/REGISTRATION_VS_RUN.txt` | the registration against the run, per mutation |
| `oracle/check_zd.py`, `oracle/check_zd.out` | the checks outside Lean, and their run of record |
| `SHA256SUMS` | every file except itself |
