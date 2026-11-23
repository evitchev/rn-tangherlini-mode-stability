# Lean layer, labelled build v4: A2-S's gate G-RES and the D = 4 Darboux identities (bh-modes): session-L, 2026-10-24

This answers the bh-modes lead's message 7 (`outbox/2026-10-24-to-session-L-7.md`, §3), which offered two optional
Lean items. I took both:
- **(a)** A2-S's gate G-RES (`code/a2/scert.py`, `g_res`; `results/a2/s/PREREG.md` §3);
- **(b)** the D = 4 Darboux identities of the [another line of this project] job `chandrasekhar` (`[code of another line of this project]`;
  `[a record of another line of this project]` §3).

Both are appended to the p3 file as a labelled build. G-RES's N is then literally `Nz`, Proposition 3's N, with
`prop3_D6`'s data at q = 1. The Darboux identities use v3's general-n `UmN` and `HmN` at n = 2, which the lead has
already read.
- **The earlier builds stay on the record, unchanged:** v3, `lean_p3_sdeformation_v3_2026-10-23` (SHA256SUMS
  `2af9f79f…`); v2 (`a6fd891d…`); the first build (`cd718ac9…`), with its erratum.
- **This build's result: "BHModesP3: ALL CHECKS AS REQUIRED"** (`lean/BUILD_LOG.txt`). 37/37 mutations pass the judge,
  and all thirty-seven agree with the registration in full.
- **Oracle.** "ALL P3 V4 CHECKS HOLD (34/34)" (`oracle/check_p3v4.out`).
- **Host.** The build of record and the oracle's run of record ran on the reproduction node of the bh-modes
  environment, under `nice -n 19`.

## What changed

- **Lines 1–681 of `lean/BHModesP3.lean` are v3's, byte for byte** (oracle check 1). Every line reference into v3
  stays valid.
- **Lines 682–900 are new:** eight definitions and twelve theorems. The file now has 59 theorems.
- **Byte copies of the earlier builds:** `build.sh`, `lean-toolchain` and the vendored judge.
- **`mutations.json`** keeps v3's twenty-four specs byte for byte and adds thirteen.

## (a) G-RES

**The claim** (PREREG §3): at q = 1 and P = a/z + b₀ + b₁z, N is a polynomial in z with
N(0) = 576H₋(2)²(ℓ(ℓ − 3)/9 − a(a + 1)), symbolically in ℓ, a, b₀ and b₁.

**The new definitions** (l. 696–724):

    def mEll (ℓ : ℝ) : ℝ := (ℓ - 1) * (ℓ + 4)
    noncomputable def dEll (ℓ : ℝ) : ℝ := 1 / (5 * (ℓ + 4))
    noncomputable def Pres (a b0 b1 z : ℝ) : ℝ := a / z + b0 + b1 * z
    noncomputable def Pres' (a b1 z : ℝ) : ℝ := -a / z ^ 2 + b1

`mEll` and `dEll` are scert.py's m and δ, and the c_n layer's `mm 4` and `δ1 4`. Everything else is the file's own
since the first build: `Nz` (METHOD.md's N), `Um` and `Hm` (TARGET.md's U₋ and H₋), and `U6`, `H6`, `F6`, `F6'` and
`xH`.

**`g_res`** (l. 746–750):

    theorem g_res (ℓ a b0 b1 : ℝ) (hℓ : ℓ + 4 ≠ 0) :
        ∃ p : Polynomial ℝ,
          (∀ z, z ≠ 0 → Nz (U6 1 (mEll ℓ) (dEll ℓ)) (H6 1 (mEll ℓ) (dEll ℓ)) (F6 1) (F6' 1) (Pres a b0 b1) (Pres' a b1) z
            = p.eval z)
          ∧ p.eval 0 = 576 * Hm (mEll ℓ) (dEll ℓ) 2 ^ 2 * (ℓ * (ℓ - 3) / 9 - a * (a + 1))

**`g_res_tendsto`** (l. 793–796):

    theorem g_res_tendsto (ℓ a b0 b1 : ℝ) (hℓ : ℓ + 4 ≠ 0) :
        Filter.Tendsto
          (fun z => Nz (U6 1 (mEll ℓ) (dEll ℓ)) (H6 1 (mEll ℓ) (dEll ℓ)) (F6 1) (F6' 1) (Pres a b0 b1) (Pres' a b1) z)
          (nhdsWithin 0 {0}ᶜ) (nhds (576 * Hm (mEll ℓ) (dEll ℓ) 2 ^ 2 * (ℓ * (ℓ - 3) / 9 - a * (a + 1))))

**How they read against the claim.**
- **"N is a polynomial in z."** P = a/z is not defined at z = 0. (Lean's a/0 = 0, so `Nz … 0` is not the gate's
  N(0).) So `g_res` says that N agrees with a polynomial p at every z ≠ 0. p is unique: two polynomials that agree at
  infinitely many points are equal.
- **"N(0)"** is p(0), N's continuous extension to z = 0. `g_res_tendsto` says the same as a limit.
- **"Identically in ℓ, a, b₀, b₁":** for all real a, b₀ and b₁, and every real ℓ ≠ −4, where δ has its pole. Lean's
  1/0 = 0 makes the statement false at ℓ = −4 (mutation P3M30; oracle check 5).
- **N is `prop3_D6`'s Nz at q = 1,** with m = `mEll ℓ`, δ = `dEll ℓ`, P = `Pres a b0 b1` and P′ = `Pres' a b1`
  (oracle check 3).
  - `Pres'` is P's derivative wherever z ≠ 0 (`Pres_hasDerivAt`).
  - `F6' 1` is f's derivative (`F6_hasDerivAt`, first build).
- **The supporting theorems** (exact statements; binder types omitted):

| theorem | statement |
|---|---|
| `mEll_dEll_S5` | `ℓ + 4 ≠ 0 → mEll ℓ = ℓ * (ℓ + 3) - 4 ∧ 1 + 2 * mEll ℓ * dEll ℓ = (2 * ℓ + 3) / 5 ∧ (1 + 2 * mEll ℓ * dEll ℓ) ^ 2 = 1 + 4 * mEll ℓ * 1 ^ 2 / (4 + 1) ^ 2`: m = ℓ(ℓ + n − 1) − n, and S5 (5.58) at n = 4, q = 1, on the branch 1 + 2mδ > 0 for ℓ > −3/2 |
| `D6_extremal` | `x6 1 z = 2 * (1 - z) ^ 3 ∧ F6 1 z = (1 - (1 - z) ^ 3) ^ 2 ∧ F6' 1 z = 6 * (1 - z) ^ 2 * (1 - (1 - z) ^ 3)`: x_H = 2 at q = 1, and scert.py's x = 2y, f = (1 − y)² and f_z, with y = (1 − z)³ |
| `Pres_hasDerivAt` | `z ≠ 0 → HasDerivAt (Pres a b0 b1) (Pres' a b1 z) z` |
| `H2_ell` | `ℓ + 4 ≠ 0 → Hm (mEll ℓ) (dEll ℓ) 2 = (ℓ + 3) * (ℓ + 4)`, as the A2-S record gives H₋(2) |
| `U2_ell` | `ℓ + 4 ≠ 0 → Um (mEll ℓ) (dEll ℓ) 2 = 576 * Hm (mEll ℓ) (dEll ℓ) 2 ^ 2 * (ℓ * (ℓ - 3) / 9)`: the c_n layer's `C1_n4` (there for ℓ ≥ 2), here with TARGET.md's U₋ and H₋, for every ℓ ≠ −4 |

**How the proof goes.** With g = 3 − 3z + z² and Q = a + b₀z + b₁z², f = z²g² and zP = Q. So N's bracket is a
polynomial B with no 1/z, and N = U₋ − 64H₋²B at every z ≠ 0. The witness p is that expression, written as a
`Polynomial ℝ`. Then p(0) = U₋(2) − 576H₋(2)²a(a + 1), since B(0) = 9a(a + 1), and `U2_ell` gives the rest.

## (b) The D = 4 Darboux identities (`chandrasekhar`)

**The claim** (PREREG §3, at n = 2 and δ = 0):
- with F = f/(r(mr + 6M)), β = 6M, κ = m(m + 2) and 𝒲 = βF + κ/(2β), 𝒲² + 𝒲_* − κ²/(4β²) is our V_S−;
- 𝒲² − 𝒲_* − κ²/(4β²) = f((m + 2)/r² − 6M/r³), Regge–Wheeler's form;
- the latter is analytic at r₀ = −6M/m.

**The new definitions** (l. 817–827), in the job's variables r and M:

    noncomputable def f4 (M r : ℝ) : ℝ := 1 - 2 * M / r
    noncomputable def VKI4 (m M r : ℝ) : ℝ :=
      f4 M r * UmN 2 1 m 0 (2 * M / r) 0 / (64 * r ^ 2 * HmN 2 m 0 (2 * M / r) ^ 2)
    noncomputable def VRW4 (m M r : ℝ) : ℝ := f4 M r * ((m + 2) / r ^ 2 - 6 * M / r ^ 3)
    noncomputable def W4 (m M r : ℝ) : ℝ := 6 * M * (f4 M r / (r * (m * r + 6 * M))) + m * (m + 2) / (2 * (6 * M))

`VKI4` is our V_S− = fU₋/(64r²H₋²) at n = 2, K = 1, δ = 0 and y = 0, with x = 2M/r. `UmN` and `HmN` are v3's: the
c_n layer's S5 (5.63b) and (5.62b), which oracle check 3 of v3 compared with `potentials.py`. 𝒲_* is f·d𝒲/dr, written
`f4 M r * deriv (W4 m M) r`.

**The statements** (l. 852–884):

    theorem darboux_KI (m M r : ℝ) (hM : M ≠ 0) (hr : r ≠ 0) (hH : m * r + 6 * M ≠ 0) :
        W4 m M r ^ 2 + f4 M r * deriv (W4 m M) r - (m * (m + 2)) ^ 2 / (4 * (6 * M) ^ 2) = VKI4 m M r

    theorem darboux_RW (m M r : ℝ) (hM : M ≠ 0) (hr : r ≠ 0) (hH : m * r + 6 * M ≠ 0) :
        W4 m M r ^ 2 - f4 M r * deriv (W4 m M) r - (m * (m + 2)) ^ 2 / (4 * (6 * M) ^ 2) = VRW4 m M r

    theorem H_zero_iff (m M r : ℝ) (hr : r ≠ 0) : HmN 2 m 0 (2 * M / r) = 0 ↔ m * r + 6 * M = 0

    theorem RW_regular_at_r0 (m M : ℝ) (hm : m ≠ 0) (hM : M ≠ 0) :
        HmN 2 m 0 (2 * M / (-6 * M / m)) = 0 ∧ AnalyticAt ℝ (VRW4 m M) (-6 * M / m) ∧
          ∀ᶠ r in nhdsWithin (-6 * M / m) {-6 * M / m}ᶜ,
            W4 m M r ^ 2 - f4 M r * deriv (W4 m M) r - (m * (m + 2)) ^ 2 / (4 * (6 * M) ^ 2) = VRW4 m M r

and the helper `W4_deriv` (l. 830–833), the quotient rule for d𝒲/dr where r ≠ 0 and mr + 6M ≠ 0.

**How they read against the claim.**
- **The two identities hold wherever both sides are defined:** r ≠ 0, and H₋ ≠ 0. For r ≠ 0, H₋ ≠ 0 is exactly
  mr + 6M ≠ 0 (`H_zero_iff`). M ≠ 0 is needed for β ≠ 0.
- **"The latter is analytic at r₀ = −6M/m"** is `RW_regular_at_r0`:
  - its first part: r₀ is a zero of H₋;
  - its second part: Regge–Wheeler's potential is analytic at r₀ (r₀ ≠ 0);
  - its third part: near r₀, off r₀, the Darboux partner 𝒲² − 𝒲_* − κ²/(4β²) equals that analytic function, so its
    singularity at r₀ is removable. This is the Lean form of the job's own check, that mr + 6M does not divide the
    denominator of 𝒲² − 𝒲_*.
- **The KI side is singular there.** V_S− itself has a double pole at r₀: oracle check 4 finds
  (r − r₀)²V_S− → 98/9 = 2f(r₀)² at m = 4, M = 1, an information check at that one point. So the Darboux partner
  removes a singularity that V_S− really has.

## What this does not prove

- **(b)'s pencil step:** that a Darboux partner of a potential regular at r₀ has trivial monodromy there. The
  intertwining identity behind it, (−∂² + V_S−)(∂ + 𝒲) = (∂ + 𝒲)(−∂² + V_RW) with ∂ = f d/dr, could be added in
  Lean if useful. The monodromy statement itself is not attempted.
- **(a)'s place in A2-S.** G-RES is a gate about the extremal limit with P = a/z + b₀ + b₁z. It says nothing about the
  certificate's charts, its Bernstein bounds, or the design's p₀.
- **As in the earlier READMEs:** the existence of the inverse tortoise map R, C^∞ smoothness, the scaling to absolute
  units, and that the form determines A.

## Checks

- **Oracle** (`oracle/check_p3v4.py`, sympy 1.14.0; run of record on the reproduction node): all 34 checks hold.
  1. Lines 1–681 are v3's (prefix sha256 `92aaa876…`). The v4 section starts at l. 682, and the file ends with the
     namespace.
  2. G-RES recomputed from scert.py's `g_res`, typed into the oracle as it stands at `2416726`. N is a polynomial in z,
     N(0) − 576H₋(2)²(ℓ(ℓ − 3)/9 − a(a + 1)) = 0, and H₋(2) = (ℓ + 3)(ℓ + 4).
  3. The file's own pieces, parsed:
     - `Um` and `Hm` are `potentials.py`'s U_TARGET and H_TARGET;
     - `mEll` and `dEll` are scert.py's m and δ, and satisfy (5.58) at q = 1;
     - `Pres'` is d/dz `Pres`;
     - `D6_extremal`'s right sides are x6, F6 and F6′ at q = 1;
     - N built from the file's `Nz` and data is a polynomial in z, with `g_res`'s value at 0;
     - `g_res`'s `Nz` arguments are `prop3_D6`'s at q = 1.
  4. The Darboux identities, recomputed two ways: from apparent.py's `chandrasekhar` as typed, with `potentials.py`'s
     U_minus(2) and H_minus(2) at δ = 0; and from the file's own definitions, parsed, with `UmN` and `HmN` at n = 2.
     - Both identities hold.
     - `W4_deriv`'s right side is d𝒲/dr.
     - H₋ = (mr + 6M)/r, with its zero at r₀.
     - The Darboux partner's denominator is r⁴, which mr + 6M does not divide.
     - V_S− has a double pole at r₀ (information).
  5. Controls: each new mutated statement, P3M25–P3M37, is false.
- **Build** (`lean/BUILD_LOG.txt`):
  - compile: exit 0, 8 s, 0 errors, 0 warnings, 0 sorry;
  - axioms: 59/59 theorems use only propext, Classical.choice and Quot.sound;
  - negative controls: both rejected;
  - mutations: 37/37 pass the judge.
- **Registration against the run: all thirty-seven agree in full.**
  - `review/P3_MUTATION_REGISTRATION.md` (sha256 `974fd576…`) was written and hashed at 04:35:54Z. The build started at
    04:36:17Z and logged the hash at 04:36:47Z, before the first mutation run.
  - First failure, exact failing set and the judge's pass all agree. So do the eight registered error texts: P3M1,
    P3M5, P3M7, P3M13, P3M14 and P3M22 as in v3, and the new P3M25 and P3M28, both "unsolved goals".
  - **P3M1–P3M24 are not blind,** and the registration says so. Four of their failing sets gained new theorems, each
    as predicted:
    - P3M1 gained `g_res`;
    - P3M7 gained `D6_extremal`;
    - P3M16 gained `darboux_KI`;
    - P3M17 gained `darboux_KI` and `H_zero_iff`.
  - **P3M25–P3M37 are new.** No mutated copy was compiled before the registration was hashed.
- **What the new mutations show:**
  - **P3M25 and P3M26.** G-RES's value is checked: its normalisation 576H₋(2)², and its dependence on a.
  - **P3M27 and P3M31.** m and δ are S5's at n = 4 and q = 1. A wrong one breaks (5.58), H₋(2) and U₋(2).
  - **P3M28.** With a double pole, N is no longer a polynomial.
  - **P3M29.** Away from extremality (q = 1/2), N has a pole at the horizon.
  - **P3M30.** ℓ ≠ −4 cannot be dropped in Lean, where 1/0 = 0.
  - **P3M32 and P3M33.** β and κ are each needed in both identities. With a wrong κ, `W4_deriv` still holds, since it
    does not involve κ.
  - **P3M34 and P3M35.** Regge–Wheeler's form, and the sign that separates the two partners.
  - **P3M36 and P3M37.** The point r₀ of the analyticity claim, and that it is H₋'s zero.
- **Error texts the registration did not fix,** for the record:
  - "unsolved goals": P3M26, P3M27, P3M31, P3M33, P3M34 and P3M35;
  - "Tactic `rewrite` failed: Did not find an occurrence of the pattern": P3M29;
  - "Application type mismatch: The argument": P3M30 and P3M37;
  - "Type mismatch": P3M32;
  - "`fun_prop` was unable to prove `AnalyticAt ℝ (…) 0`": P3M36.

## Host and environment

- **The build of record and the oracle** ran on the reproduction node. The folder there was identical to this one
  before the run (10 files, by sha256). The build's inputs were unchanged after it. The logs and
  `oracle/check_p3v4.out` were copied back here.
- **Development on the editing node:**
  - four compiles of the unmutated file with the v4 section. The first two failed on development faults, which the
    registration lists. The third was clean, and so was the fourth, after one long line was wrapped.
  - one probe file, for lemma names and two tactic calls;
  - one copy of the final file with `#count_heartbeats`. The largest count was 29,705, for `g_res`.
  - development runs of the oracle. The first two hit bugs in the oracle's own parsing: a placeholder prefix hash and
    a statement split at the wrong colon, then a replacement that turned `VRW4 m M r` into `VR(W)`. The later runs
    gave 34/34.

  No mutation was run there.

## Files

| file | content |
|---|---|
| `lean/BHModesP3.lean` | v4 source: 59 theorems, namespace `BHModes.P3`; lines 1–681 v3's |
| `lean/build.sh`, `lean/lean-toolchain`, `lean/vendor/` | byte copies of the earlier builds' (judge `696b7864…`) |
| `lean/mutations.json` | v3's twenty-four specs, byte for byte, and P3M25–P3M37 |
| `lean/SOURCES.tsv` | the v4 source hash and its origin, with the hashes of the bh-modes files it was written from |
| `lean/BUILD_LOG.txt`, `lean/build_stdout.txt`, `lean/logs/` | the build of record |
| `review/P3_MUTATION_REGISTRATION.md`, `review/REGISTRATION_TIME.txt` | predictions, written and hashed before the run |
| `oracle/check_p3v4.py`, `oracle/check_p3v4.out` | the checks outside Lean, and their run of record |
| `SHA256SUMS` | every file except itself |

- `build.sh` is the first build's, so its log header still reads "item (a)". This build is v4 by its folder and
  `SOURCES.tsv`.
- The build outputs (`build/`) were left on the node; `lean/build.sh` regenerates them in about six minutes.
