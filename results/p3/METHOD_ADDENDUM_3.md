# p3 METHOD addendum 3: Proposition 3 for a P that is C¹ on (0, 1) only, q = 1 included

*Item BHM-147. 2026-10-26, the bh-modes lead.*
- *It answers the GAP-MINOR in item A3 of Fable's second pencil audit (BHM-146,
  `results/stage3/audits/fable_2026-10-26/AUDIT.md` §A3). `METHOD.md` and addenda 1 and 2 are sealed and unchanged.*
- *Status: proved (pencil). The proof is addendum 2's, with step 3 in the form Fable gives. Lean's `prop3_Ioo` and
  `prop3_Dn` state exactly this hypothesis (*machine-checked*, BHM-090/091). No claim changes. Sealed.*

## The gap

Addendum 2 states Proposition 3 for "P C¹ on an open interval containing [0, 1]". The singular designs of A2-S and
HD-X-S at μ = 0 (q = 1) do not meet this. There ε = 0, so the pole z = −ε sits at the horizon z = 0. That point lies in
[0, 1], but outside (0, 1). The files cite Lean's (0, 1) form for this case, and that form applies. The pencil statement
in that form was not written down (Fable, A3).

## The statement

Let D = n + 2 with n ≥ 2, K = 1, Λ = 0, and **0 ≤ q ≤ 1**. Work in units r_H = 1, with ρ ∈ (1, ∞) and
z = 1 − 1/ρ ∈ (0, 1).

Let **P be C¹ on (0, 1)**, and put β = (1 − z)P and S(r*) = −f(ρ)β(ρ). Define, as in addendum 2,
N = U₋ − 64H₋²[(1 − z)f_zP + f(−P + (1 − z)P_z + P²)]. **If N ≥ 0 on (0, 1), then A_{ℓ,q} ≥ 0.**

## Proof

Addendum 2's five steps, with two changes.
- **Step 3 needs only (0, 1).** z(ρ) = 1 − 1/ρ maps (1, ∞) into (0, 1), where P is C¹. So β, f and S are C¹ in ρ, and
  in r* through the C^∞ tortoise map. P's behaviour at z = 0 or z = 1, and any pole at z ≤ 0, never enter. Lemma 1
  needs only S ∈ C¹(ℝ), real.
- **At q = 1:**
  - Step 1 holds, since f = (1 − y)² > 0 for y ∈ (0, 1).
  - Step 2 is the tortoise map at q = 1, where the zero of f at the horizon is double. At general n it is in
    `results/extremal/PREREG.md` §2, and it is *machine-checked* (`tortoise_q1`, BHM-135). At n = 4 it is
    `METHOD_ADDENDUM_1.md` §1.
  - Steps 4 and 5 are unchanged, with δ = δ₁ > 0.

## Where it is used, and the wording it corrects

- **A2-S and HD-X-S at μ = 0** (q = 1) need this addendum. For μ > 0 their pole z = −ε < 0 lies outside [0, 1], and
  addendum 2 applies as written.
- **HD-X-2** has μ > 0 throughout, so addendum 2 applies as written. Its PREREG cites the (0, 1) form anyway (§2).
- **Where the singular design at μ = 0 is meant, "outside [0, 1]" should read "outside (0, 1)".** These sealed files
  stay as they are:
  - `results/hdx/s/PREREG.md` §2, "The reduction": "P's pole z = −ε lies outside [0, 1]". At μ = 0 the pole lies at
    z = 0.
  - `results/stage3/briefs/BRIEF_fable_2026-10-26.md`, item A3.
  - `TARGET_A2_ADDENDUM_1.md` §3 already says "outside (0, 1)".
- **No claim changes.** The reduction holds at every μ ∈ [0, μ₁], and the certificates prove more than it needs: NL > 0
  on the closed boxes.
