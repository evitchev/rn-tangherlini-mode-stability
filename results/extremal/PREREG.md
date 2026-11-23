# PREREG — Z: the extremal zero mode, and its Darboux partner (stage 3; [another line of this project] (b′))

*Item BHM-123. 2026-10-26, the bh-modes lead.*
- *The operator's ruling, 2026-10-26 (BHM-120), items 1 and 2.*
- *Not blind for the identity: Z-id has already been seen to hold in planning, for n = 4…9 with ℓ symbolic
  (`results/planning/stage3_2026-10-25/hdx/zero_mode.log`) and in 8 cases (`…/critical/out/closed_form_exact.log`).*
- *Not yet run on S5's potentials: the gates, the partner (P-reg, P-asym), the n = 2, 3 and n-symbolic jobs, and every
  control. The development test (§5) used synthetic inputs only.*
- *Code at the commit that holds this file: `code/extremal/` and `kit/extremal/run.sh`. Sealed; any change before the
  run is a dated addendum.*

## 1. Setting

- D = n + 2, K = 1, Λ = 0, q = 1, r_H = 1. Put Y = ρ^{−(n−1)}, so x = 2Y and f = (1 − Y)².
- At q = 1, S5 (5.58) gives m = (ℓ − 1)(ℓ + n) and δ = 1/((ℓ + n)(n + 1)), on the branch 1 + 2mδ > 0.
- The master equation at ω = 0 is (f u′)′ = (W/ρ²)u, with W = U₋/(64H₋²), i.e. V = fW/ρ².
- U₋ and H₋ are S5's (5.62b)–(5.63b) as transcribed in `code/ki/potentials.py`. For n symbolic, `code/kimaster/master.py`'s
  forms are used; its gate `gen` (BHM-094/098) ties them to the integer-n forms.

## 2. The claim, the checks, and the pencil steps

**The candidate:** u₀ = ρ^{−ν}(1 − Y)^{−α}/h, with ν = ℓ + n/2 − 1, α = ℓ/(n − 1) and h = (ℓ − 1) + nY.

**Claim Z.** For each n = 4…9 and every integer ℓ ≥ 2, u₀ solves the q = 1 zero-energy equation, so A_{ℓ,1} ≥ 0 on
C₀^∞(ℝ).

**Z-id, the identity** (exact, in ℚ(Y, ℓ)). With g = ρu₀′/u₀ = −ν − ℓY/(1 − Y) + n(n − 1)Y/h,

  2(n − 1)Y(1 − Y)g + (1 − Y)²(g² − g − (n − 1)Yg_Y) = W.

Dividing the equation by u₀ gives this identity, since ρ d/dρ = −(n − 1)Y d/dY (pencil). It is a rational identity, so
it holds at every integer ℓ ≥ 2 and every Y ∈ (0, 1), where h ≥ 1 and 1 − Y > 0.

**The gates,** in the code's order:
- **q1:** (n + 1)²δ(1 + mδ) = 1 and 1 + 2mδ = (2ℓ + n − 1)/(n + 1). This is the extremal point of (5.58).
- **H:** H₋(2Y) = (ℓ + n)h, so u₀ = ρ^{−ν}(1 − Y)^{−α}(ℓ + n)/H₋.
- **Z-pos:** h has positive coefficients in (t, Y) at ℓ = 2 + t, and also in s at n = 2 + s when n is symbolic. So h ≥ 1 on
  the exterior.
- **Z-inf:** W(0) = ν(ν + 1), the decaying exponent at infinity.
- **Z-thr:** α(α − 1)(n − 1)² = W(1). So u₀'s throat exponent solves the throat's indicial equation, with c = W(1)/(n − 1)²
  = c_n(ℓ) (BHM-049).
- **Z-id**, as above.

**From Z to A ≥ 0** (pencil; audited 0×).
- **The tortoise map at q = 1,** r* = ∫dρ/f, is a smooth increasing bijection (1, ∞) → ℝ.
  - Near ρ = 1, f ≈ (n − 1)²(ρ − 1)², so r* → −∞.
  - As ρ → ∞, f → 1, so r* → +∞.
  - At n = 4 this was audited 1× (BHM-116).
- **u₀ is smooth and positive** on (1, ∞): every factor of its explicit form is positive there, and h ≥ 1 (Z-pos). In
  r*, u₀ solves −u₀″ + Vu₀ = 0 (Z-id).
- **Lemma 1** of `results/p3/METHOD.md` (*machine-checked*, BHM-030), with S = −(log u₀)_{r*}, gives V + S′ − S² ≡ 0.
  So Q[φ] = ∫|φ′ + Sφ|² ≥ 0 for every φ ∈ C₀^∞(ℝ).
- **So A_{ℓ,1} ≥ 0 on C₀^∞(ℝ).** Its physical reading is that of Theorem A2 at q = 1 (S5's reduction, *cited*).

**The N job.** The same checks in ℚ(Y, ℓ, N). If it verifies, claim Z holds for every integer n ≥ 2 that S5's
general-n forms cover.

**Information jobs:** n = 2 and 3 (D = 4 and 5). They are recorded, not claimed.

**The partner** ([another line of this project] (b′)). Let w = (log u₀)_{r*} = fg/ρ. Then V = w² + w′. The partner is

  Ṽ = w² − w′ = fŨ/ρ²,  with Ũ = (1 − Y)²(g² + g + (n − 1)Yg_Y) − 2(n − 1)Y(1 − Y)g

(this follows from the definitions; pencil).
- **P-reg** (registered prediction: holds). Ũ has no pole at the zero of h, i.e. at the zeros of H₋.
  - The pencil reason: at an apparent point with exponents (−1, 2), u₀ ~ 1/s. So w = −1/s + w₀ + O(s), and
    V = 2/s² − 2w₀/s + O(1), while Ṽ = −2w₀/s + O(1).
  - BHM-098 certified b₋₁ = 0 there, so w₀ = 0.
  - If P-reg fails, that pencil step is wrong, and the record shows how.
- **P-asym:** Ũ(0) = ν(ν − 1) and Ũ(1) = ℓ(ℓ + n − 1). These follow from the candidate's form, so they check the code
  path.
- P-reg and P-asym are computed only when Z-id holds; otherwise they are recorded as failed.
- **Facts recorded** (information, no prediction):
  - Ũ, factored, and whether it is a polynomial in Y;
  - Ũ compared with W₊ at the same ℓ, and with W₋ at ℓ ± 1, all at q = 1;
  - for integer n, whether u₀ is throat-principal in each band ℓ = 2…n − 2. The planning data say: exactly when
    2ℓ ≤ n − 1.
- **The intertwiner** (pencil; audited 0×; a statement recorded with the result, not a check).
  - With L = ∂_{r*} − w, A = L†L and Ã = LL†, so L(A − ω²) = (Ã − ω²)L for every ω.
  - Lψ = 0 only for ψ ∝ u₀, which is a solution only at ω = 0. So for ω ≠ 0, L maps the solutions at ω bijectively.
  - w → 0 at both ends: like −ν/ρ at infinity, and like −α/s at the throat, where s = −r*. So L maps a solution
    ~ e^{±iωr*} at either end to ±iω·e^{±iωr*}(1 + o(1)).
  - So V and Ṽ have the same quasinormal-mode conditions at q = 1 for ω ≠ 0. At the extremal horizon these conditions
    are set at an irregular singular point; that is the part to audit.

## 3. Controls (registered verdicts), at n = 4 and n = 9

| Control | Registered verdict | Why |
|---|---|---|
| nc-nu: ν + 1 in the candidate | REJECT: Z-inf, Z-id, P-reg, P-asym | W(0) = ν(ν + 1) ≠ (ν + 1)(ν + 2). g → g − 1 changes the identity's left side by 2 + 2ν at Y = 0. P is not computed |
| nc-exp: α = (ℓ + 1)/(n − 1) | REJECT: Z-thr, Z-id, P-reg, P-asym | α(α − 1)(n − 1)² = (ℓ + 1)(ℓ − n + 2) ≠ ℓ(ℓ − n + 1) = W(1), so the left side misses W at Y = 1. g(0) is unchanged, so Z-inf holds |
| td-U: U₋ + 64m² | REJECT: Z-inf, Z-thr, Z-id, P-reg, P-asym | W gains m²/H₋². That is 1 at Y = 0, and m²/H₋(x_H)² ≠ 0 at Y = 1 |
| td-zid: the identity's first term with 1 in place of 2 | REJECT: Z-id, P-reg, P-asym | The left side loses (n − 1)Y(1 − Y)g ≢ 0. Z-inf and Z-thr read W directly |
| td-preg: Ũ computed with V's signs | REJECT: P-reg, P-asym | Then Ũ = W, which has a double pole at the zeros of H₋ (exponents (−1, 2), BHM-098), and W(0) = ν(ν + 1) ≠ ν(ν − 1) |

The controls' verdicts assume that Z holds at that n, i.e. that the `none` job's Z checks pass. If Z fails at that n,
the controls there are VOID.

## 4. Runs, hosts, records

- **One command:** `kit/extremal/run.sh`.
  - The claim jobs (n = 4…9), the N job and the information jobs (n = 2, 3) must each end in an answer.
  - Every control must give its registered verdict.
- **The answer forms of a claim job:**
  - `VERIFIED`: Z holds, and the partner is regular at the zeros of H₋.
  - `REJECT: P-reg`: Z holds, but the partner is not regular there, so §2's pencil reason is wrong.
  - a REJECT that names any of q1, H, Z-pos, Z-inf, Z-thr or Z-id: Z fails at that n, i.e. it is *refuted* there.
  - Any exception, timeout or other verdict is VOID for that job.
- **Hosts:**
  - the record on host-1, from a `git archive` of the commit that holds this file, under `nice -n 19` in
    `[venv]`;
  - the reproduction on host-2, with `BHM_REF` set to the record. Every job's JSON must be identical after masking
    (`code/compare_runs.py`).
- **The records** carry the UTC start time (masked) and the SHA-256 of the archive (`BHM_ARCHIVE`, not masked).
- **Timeout:** 6 h per job. A timeout is VOID for that job.

## 5. Development tests (synthetic only)

`code/extremal/devtest.py` replaces S5's `master()` by a function that raises. It uses two synthetic candidates, each
with its potential built from the identity's left side, so that Z-id holds by construction:
- A has no pole, so its partner is regular;
- B has a pole whose double-pole term does not cancel.

It exercises every check, control and drill path, the n-symbolic path, the throat classification, the JSON writer and
`compare_runs`.

**Result:** 44/44 as expected, in 2.8 s, at `2120590` on host-1 (`[run-folder]/dev-z-2120590/devtest.log`). In the
synthetic A case, td-preg gives `REJECT: P-asym` alone, because A's W has no pole. That is why the real case's
registered verdict for td-preg rests on BHM-098.

## 6. What each outcome means (registered now)

- **Z holds for n = 4…9:** the identity is *certified* (exact) for each D = 6–11, with ℓ symbolic. With §2's pencil
  steps, A_{ℓ,1} ≥ 0 for every ℓ ≥ 2. The label is: *certified; the ground-state step and the tortoise map at general n
  proved (pencil; audited 0×)*.
  - For D = 6 it is a second route to Theorem A2 at q = 1.
  - For D = 7–11 it is HD-X's endpoint q = 1, including the critical set 𝒦. It says nothing about q ∈ (99/100, 1).
- **The N job verifies:** the same holds for every integer n ≥ 2 that S5's general-n forms cover.
- **P-reg holds:** at q = 1 the apparent points of V_S− are removed by a Darboux transformation with an ω-independent
  intertwiner. That answers, at q = 1, the question left open in `[a note of another line of this project]`. The partner's
  form and the comparisons go to the functional-relations work.
- **A second party** is pending (RULES.md A4): Kimi, or session-L's Lean, after the run.
- **No novelty wording.** Session-L's literature check of the zero mode is not ruled (BHM-120).
