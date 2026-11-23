# Lean layer for Z, the extremal zero mode (bh-modes BHM-126): session-L, 2026-10-26

This answers the bh-modes lead's message 8 (`outbox/2026-10-26-to-session-L-8.md`). It asks for Lean as the second
party for the identities behind Z, under the operator's ruling of 2026-10-26 (BHM-120) and the rule of BHM-046.
- **Items (a), (b) and (c) are proved, with n symbolic.** Item (d), optional in the request, is not in this build.
- **Result: "BHModesZ: ALL CHECKS AS REQUIRED"** (`lean/BUILD_LOG.txt`). All 17 mutations pass the judge.
- **Registration against the run: 14 of 17 agree in full.** ZM4, ZM5 and ZM10 differ in their failing sets only:
  the judge credits `deriv_g` with an error that is `z_id`'s. The cause and why no verdict depends on it are under
  Checks.
- **Oracle: "ALL Z CHECKS HOLD (36/36)"** (`oracle/check_z.out`).
- **Host:** the build of record and the oracle's run of record ran on the reproduction node of the bh-modes
  environment, under `nice -n 19`.

## The definitions

`lean/BHModesZ.lean`, namespace `BHModes.Z`, 165 lines.
- **Lines 34–53 are the c_n layer's definitions, byte for byte** (lean_cn_2026-10-23, lines 24–43; oracle check 1).
  - `Hm` is S5 (5.62b) and `Um` is S5 (5.63b) at general n, with K and y, in session-L's transcription. That is the
    transcription the c_n build (BHM-049) and p3 v3–v5 used.
  - `mm n ℓ` = (ℓ − 1)(ℓ + n), and `δ1 n ℓ` = 1/((n + 1)(ℓ + n)), the q = 1 value of δ.
- **New:**

      def nu (n ℓ : ℝ) : ℝ := ℓ + n / 2 - 1
      def g (n ℓ Y : ℝ) : ℝ := -nu n ℓ - ℓ * Y / (1 - Y) + n * (n - 1) * Y / ((ℓ - 1) + n * Y)
      def W (n ℓ Y : ℝ) : ℝ := Um n 1 (mm n ℓ) (δ1 n ℓ) (2 * Y) 0 / (64 * Hm n (mm n ℓ) (δ1 n ℓ) (2 * Y) ^ 2)
      def Ut (n ℓ Y : ℝ) : ℝ :=
        (5 * n ^ 2 / 4 - n / 2) * Y ^ 2 + (-3 * n ^ 2 / 2 + 2 * n + 2 * ℓ - 2) * Y
          + (n ^ 2 / 4 + n * ℓ - 3 * n / 2 + ℓ ^ 2 - 3 * ℓ + 2)

  - g is ρ ∂_ρ log u₀ for u₀ = ρ^(−ν)(1 − Y)^(−ℓ/(n−1))/((ℓ − 1) + nY), with Y = ρ^(−(n−1)) (oracle check 6, numerically).
  - W is U₋/(64H₋²) at x = 2Y, m = (ℓ − 1)(ℓ + n), δ = δ₁, K = 1 and y = 0.
  - Ut is the quadratic Ũ of RESULT.md, for n symbolic.

## The statements

**(a) `z_id`** (l. 110–112):

    theorem z_id (n ℓ Y : ℝ) (h1 : n + 1 ≠ 0) (h2 : ℓ + n ≠ 0) (hY : 1 - Y ≠ 0) (hP : (ℓ - 1) + n * Y ≠ 0) :
        2 * (n - 1) * Y * (1 - Y) * g n ℓ Y
          + (1 - Y) ^ 2 * (g n ℓ Y ^ 2 - g n ℓ Y - (n - 1) * Y * deriv (g n ℓ) Y) = W n ℓ Y

**(b) `gate_q1`** (l. 75–76) **and `gate_H`** (l. 80–81):

    theorem gate_q1 (n ℓ : ℝ) (h1 : n + 1 ≠ 0) (h2 : ℓ + n ≠ 0) :
        (n + 1) ^ 2 * δ1 n ℓ * (1 + mm n ℓ * δ1 n ℓ) = 1
    theorem gate_H (n ℓ Y : ℝ) (h1 : n + 1 ≠ 0) (h2 : ℓ + n ≠ 0) :
        Hm n (mm n ℓ) (δ1 n ℓ) (2 * Y) = (ℓ + n) * ((ℓ - 1) + n * Y)

**(c) `partner`** (l. 124–126):

    theorem partner (n ℓ Y : ℝ) (hY : 1 - Y ≠ 0) (hP : (ℓ - 1) + n * Y ≠ 0) :
        (1 - Y) ^ 2 * (g n ℓ Y ^ 2 + g n ℓ Y + (n - 1) * Y * deriv (g n ℓ) Y) - 2 * (n - 1) * Y * (1 - Y) * g n ℓ Y
          = Ut n ℓ Y

**Also in the file:**
- `g_hasDerivAt` and `deriv_g` (l. 87–105): ∂_Y g = −ℓ/(1 − Y)² + n(n − 1)(ℓ − 1)/((ℓ − 1) + nY)², at every Y with
  1 − Y ≠ 0 and (ℓ − 1) + nY ≠ 0.
- `partner_n4` (l. 136): at n = 4, Ũ = 18Y² + (2ℓ − 18)Y + ℓ² + ℓ, as in RESULT.md.
- `partner_ends` (l. 140): Ũ(0) = ν(ν − 1) and Ũ(1) = ℓ(ℓ + n − 1), RESULT's P-asym.
- `partner_no_pole` (l. 145–147), RESULT's P-reg:

      theorem partner_no_pole (n ℓ Y₀ : ℝ) (hn : n ≠ 0) (hY : 1 - Y₀ ≠ 0) :
          Filter.Tendsto (fun Y => (1 - Y) ^ 2 * (g n ℓ Y ^ 2 + g n ℓ Y + (n - 1) * Y * deriv (g n ℓ) Y)
              - 2 * (n - 1) * Y * (1 - Y) * g n ℓ Y) (nhdsWithin Y₀ {Y₀}ᶜ) (nhds (Ut n ℓ Y₀))

  The function is (c)'s left side, character for character (oracle check 5). So at the zero Y₀ = (1 − ℓ)/n of H₋, and
  everywhere else with Y₀ ≠ 1, the partner's expression has the finite limit Ũ(Y₀): it has no pole there. W does have
  one there (oracle check 5, information).

**How they read against the request.**
- **n is symbolic.** n, ℓ and Y are real. The hypotheses are exactly the points where the definitions make sense:
  - n + 1 ≠ 0 and ℓ + n ≠ 0, for δ₁;
  - 1 − Y ≠ 0 and (ℓ − 1) + nY ≠ 0, for g. With gate_H, these also give H₋(2Y) ≠ 0.

  An identity of rational functions that holds on this dense set is the identity in ℚ(Y, ℓ, n). Each n = 4…9 is an
  instance.
- **∂_Y g** is Mathlib's `deriv (g n ℓ) Y`, the derivative of the function Y ↦ g n ℓ Y. `g_hasDerivAt` proves it is
  the stated rational function.
- **W** uses the c_n layer's `Um` and `Hm` at x = 2Y, m = `mm n ℓ`, δ = `δ1 n ℓ`, K = 1 and y = 0. Oracle check 6
  compares them with `code/ki/potentials.py`'s `U_minus` and `H_minus` at n = 2…11 (information).
- **`partner_no_pole`'s hn : n ≠ 0** is used by the proof, which needs the zero of (ℓ − 1) + nY to be a single point.
  The statement at n = 0 is not claimed.

## What this does not prove

- **Item (d)**, optional in the request: the tortoise map at q = 1 as a bijection (1, ∞) → ℝ at general n, and Lemma 1
  with S = −(log u₀)_{r*}. It is not in this build.
- **The step from (a) to the master equation in r*.** With w = (log u₀)_{r*} = f g/ρ and f = (1 − Y)², the chain rule
  gives ρ²(w² + w′)/f = (a)'s left side and ρ²(w² − w′)/f = (c)'s. These are pencil here, as in RESULT.md.
- **The transcription itself.** That `Um` and `Hm` are S5's (5.63b) and (5.62b) rests on session-L's potential check
  of 2026-10-22 and on the earlier builds, as before.
- **The physical reading,** as in RESULT.md.

## Checks

- **Oracle** (`oracle/check_z.py`, sympy 1.14.0 and mpmath 1.3.0; run of record on the reproduction node): all 36
  checks hold.
  - **Method.** The oracle reads the file's own Lean text with check_p3v5.py's parser, extended with ℓ, `HasDerivAt`
    and ∧. So the statements it checks are the file's, not a retyping. ∂_Y g is sympy's derivative of the file's g.
  1. Lines 34–53 are lean_cn's lines 24–43 (sha256 of the block). The file ends with the namespace, and its theorems
     are the expected nine.
  2. `gate_q1` and `gate_H` hold identically in n, ℓ and Y.
  3. `g_hasDerivAt`'s derivative is sympy's, and `deriv_g` holds.
  4. `z_id` holds identically in n, ℓ and Y.
     - Information: it fails without the ∂_Y g term, and with +g in the bracket.
     - Sanity: W is not constant in Y.
  5. `partner`, `partner_n4` and `partner_ends` hold identically. For `partner_no_pole`:
     - its binders are as expected, and its function is `partner`'s left side;
     - at Y₀ = (1 − ℓ)/n, the expression at Y₀ ± 10⁻²⁰ is within 2.3·10⁻¹⁸ of Ũ(Y₀), at five (n, ℓ);
     - information: W is about 10⁴⁰ there, so the pole is in V's side, not the partner's.
  6. Information.
     - g = ρ ∂_ρ log u₀ at five points, to 10⁻⁴⁹.
     - `Um` and `Hm` at K = 1 and y = 0 equal `code/ki/potentials.py`'s `U_minus` and `H_minus` for n = 2…11. The file
       compared was a byte copy kept beside the run, not in this folder: sha256 `7d686b40…`, bh-modes HEAD 10b1d9d,
       last changed in a90b83e.
  7. Controls: each of ZM1–ZM17, applied as text, makes its target false.
     - ZM11 and ZM12 weaken a hypothesis. They are shown false at a point the weakened hypotheses allow and the
       original ones exclude, with Lean's x/0 = 0: n = 1, ℓ = −1 for ZM11, and n = 4, ℓ = 3, Y = −1/2 (g's pole) for
       ZM12.
- **Build** (`lean/BUILD_LOG.txt`):
  - compile: exit 0, 4 s, 0 errors, 0 warnings, 0 sorry;
  - axioms: 9/9 theorems use only propext, Classical.choice and Quot.sound;
  - negative controls: both rejected;
  - mutations: 17/17 pass the judge.
- **Registration against the run** (`review/REGISTRATION_VS_RUN.txt`, from `review/compare_registration_z.py`):
  - **Timing.** `review/Z_MUTATION_REGISTRATION.md` (sha256 `c645d0c2…`) was written and hashed at 18:33:01Z. The
    build started at 18:33:27Z and logged the hash at 18:33:36Z, before the first mutation run.
  - **What agrees.** In all 17, the first failure and the judge's pass agree with the registration. So does the one
    registered error text: ZM9's "unsolved goals" at `partner_n4`.
  - **Failing sets: 14 of 17 agree.** For ZM4, ZM5 and ZM10 the judge's set holds `deriv_g` where the registration has
    `z_id`:
    - ZM4: {`deriv_g`, `gate_H`, `gate_q1`}, registered {`gate_q1`, `gate_H`, `z_id`};
    - ZM5: the same as ZM4;
    - ZM10: {`deriv_g`, `gate_H`}, registered {`gate_H`, `z_id`}.
  - **The cause.**
    - In these three, `z_id`'s proof exceeds the 200,000-heartbeat limit on its false identity. Lean reports
      "(deterministic) timeout at `whnf`, maximum number of heartbeats (200000) has been reached" at 109:0. That is
      the declaration's first character, the first line of `z_id`'s doc comment.
    - The judge credits an error to the nearest declaration keyword at or above its line. Above line 109 that is
      `deriv_g` (l. 103).
    - So `z_id` failed, as registered, and `deriv_g` has no error in any of the 17 runs.
    - In the other z_id mutations the error is "unsolved goals" at 112:91, inside `z_id`.
  - **No verdict depends on it.** In ZM4, ZM5 and ZM10 the expected declarations (`gate_q1`, `gate_H`) fail with
    their own errors, at 76 and 81. Every spec whose expected declaration is `z_id` has its error at line 112.
  - **What I did not foresee.** I took the timeout risk for large false identities into account by registering no
    error text for `z_id`. I did not foresee that a timeout is placed at the declaration's start, so that a doc
    comment moves it into the previous declaration's span for the judge.
- **What the mutations show:**
  - **ZM1, ZM2 and ZM13:** g and ∂_Y g are pinned: ν, the n(n − 1) coefficient, and the sign of ∂_Y g.
  - **ZM3 and ZM14–ZM16:** W is U₋/(64H₋²) at x = 2Y, K = 1 and y = 0, each of them needed.
  - **ZM4, ZM5, ZM10 and ZM11:** δ₁, m and H₋(2Y) are pinned, and `gate_q1` needs ℓ + n ≠ 0.
  - **ZM6 and ZM7:** Z-id's bracket and its factor n − 1.
  - **ZM8, ZM9 and ZM12:** the sign of the partner's ∂ term and Ũ's constant are pinned, and (ℓ − 1) + nY ≠ 0 is
    needed.
  - **ZM17:** P-reg's limit is Ũ(Y₀).
- **Error texts the registration did not fix,** for the record (first lines, as Lean printed them):
  - "unsolved goals": all but ZM17;
  - "Tactic `rfl` failed: The left-hand side": ZM2, at `hg`;
  - "Application type mismatch: The argument": ZM12, in `partner` and `partner_no_pole`;
  - "Type mismatch": ZM8 and ZM17, in `partner_no_pole`, and ZM13, in `deriv_g`;
  - the heartbeat timeout above: ZM4, ZM5 and ZM10, in `z_id`.

## Host and environment

- **The build of record and the oracle** ran on the reproduction node, under `nice -n 19`.
  - Before the run, the folder there was identical to this one, 10 files by sha256.
  - The build's inputs were unchanged after it.
  - The logs and `oracle/check_z.out` were copied back here, byte for byte.
  - The mutation runs took 3–15 s each. The build outputs (`build/`) were left on the node; `lean/build.sh`
    regenerates them in about three minutes.
- **Development on the editing node** is listed in the registration's "What is and is not blind": four compiles of the
  unmutated file, two heartbeat-count copies, and three oracle runs. No mutation was compiled there.

## Files

| file | content |
|---|---|
| `lean/BHModesZ.lean` | the source: 9 theorems, namespace `BHModes.Z`; lines 34–53 the c_n layer's definitions |
| `lean/build.sh` | lean_cn's `build.sh` with the file, namespace, registration and title names changed |
| `lean/lean-toolchain`, `lean/vendor/` | byte copies of the earlier builds' (judge `696b7864…`) |
| `lean/mutations.json` | ZM1–ZM17, all new |
| `lean/SOURCES.tsv` | the source's hash and its origin |
| `lean/BUILD_LOG.txt`, `lean/build_stdout.txt`, `lean/logs/` | the build of record |
| `review/Z_MUTATION_REGISTRATION.md`, `review/REGISTRATION_TIME.txt` | predictions, written and hashed before the run |
| `review/compare_registration_z.py`, `review/REGISTRATION_VS_RUN.txt` | the registration against the run, per mutation |
| `oracle/check_z.py`, `oracle/check_z.out` | the checks outside Lean, and their run of record |
| `SHA256SUMS` | every file except itself |
