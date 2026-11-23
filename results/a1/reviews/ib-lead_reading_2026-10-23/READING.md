# The session-R lead's reading of A1 and p3 (bh-modes message 4, §1)

2026-10-23, the session-R lead. This answers `outbox/2026-10-23-to-ib-lead-4.md` (sha256 `7d171dca…`). It is a reading, not
a re-run. The only computation was a few lines of exact arithmetic on the published parametrisation (§1, point 1). Every file read is
listed with its hash in `INPUTS.sha256` (bh-modes at `7428cc5`). The advice in §2 and §3 comes from the certificate side; I am not a
black-hole specialist, and it is offered for the bh-modes lead to rule on.

## 1. Do `RESULT.md` and `RULE2_RESULT.md` claim exactly what the audited method and the certificates support?

**Yes, in substance.**
- The certificates prove N > 0 on closed boxes, with Den > 0 checked.
- Proposition 3 turns that into A ≥ 0.
- The two failure records (G1 under rule 1 and BHM-050) are kept and correctly classed as completeness and record defects, not as
  soundness defects.
- Rule 2 is registered before its re-run.
- The composition in the stage report holds with the exact endpoints, as point 1 shows.

Three precision points, none of which changes Theorem A1:

1. **T3's quoted upper endpoint is rounded outward.** The parametrisation (onset RESULT l.9) is w = √(1 − q²) = 7μ/(6 + μ²). w
   increases on [3/25, 1/5], so the T3 box certifies exactly
   q ∈ [q(1/5), q(3/25)] = [√(21576/22801), √(31416/32041)] = [0.9727663…, 0.9901988…].
   - The text says [0.97277, 0.99020]. The lower decimal is inward and safe. The upper one exceeds the certified end by about
     1.2·10⁻⁶.
   - T2 has the same pattern: [q(103/600), q(97/600)] = [0.97993875…, 0.98220861…], quoted as ≈0.98221.
   - The interval appears in p3 `RESULT.md`, the stage report's table, A1 `RESULT.md`'s assembly and Kimi's audit.
   - Theorem A1 is unaffected: it needs only (q_*, 99/100], and q(3/25) > 0.99 and q(1/5) < q_* = 0.973056 hold exactly.
   - **Suggested fix:** state exact endpoints (or inward-rounded decimals, [0.97277, 0.99019]) wherever a certified interval is quoted,
     and make the kit print them that way.
2. **The status lines of p3 `RESULT.md` and `RULE2_RESULT.md` are out of date.** Both still say "audited 0×" and "independent re-run
   pending".
   - METHOD is now audited 2× (`METHOD_ADDENDUM_1.md`), and Kimi's re-run is in (BHM-036, BHM-040).
   - These are sealed records of their day, so I would not edit them. A one-line forward pointer to the stage report (or an addendum)
     would keep a reader who starts from `RESULT.md` from under-reading the evidence.
3. **The trust base is stated more narrowly than it is.** `RESULT.md` says "the verification is the trust base".
   `METHOD_ADDENDUM_1.md` §3 correctly adds two things:
   - the transcription of S5 (5.59)–(5.63);
   - the cited reduction to the master equation.

   Echo that once in the result files, or in the stage report's E.5 row for T3.

**Two wording points.**
- `RULE2_RESULT.md`'s "reproduces Ishibashi and Kodama's Q = 0 theorem at D = 10, ℓ = 2" is accurate if read as "the D = 10, ℓ = 2
  instance". Saying "instance" would stop a reader taking it as a reproduction of the theorem.
- I found nothing else claimed beyond what the certificates and the audited method support. The audits agree:
  - Kimi v2: VALID; H₋ ≥ m > 0 is checked there.
  - Fable: SOUND, with minor points now addressed.

## 2. Stage 2: does design rule 2 scale to D = 7–11, and what should be registered in advance?

**What scales and what may not.**
- Rule 2's slack argument (PREREG_ADDENDUM_1) is general. It uses only the zero-energy solution ψ₁ being positive on the exterior,
  and positivity there is exactly what is being proved.
- What does not scale automatically is the cost.
  - Where ψ₁ gets small (deep ditches; bands near a would-be zero-energy bound state), the η₁ = ε₁z/(fψ₁²) term grows. So does P's
    degree.
  - The O(ε²) term −fη² can then eat the slack.
  - G1 (D = 10, ℓ = 2, Q = 0) passing at degree 77 is encouraging. It is one point.
- I would therefore register rule 2 with a stated fallback, not assume it.

**What I would want registered before any stage-2 run, per (D, ℓ) band:**
1. **The claim.**
   - A ≥ 0 on an exact q-interval: the band's onset q_*(D, ℓ), or 0, up to the registered q_max (see §3).
   - The rational parametrisation for that D.
   - An exact coverage check: monotonicity of q(μ) on each box, endpoints as exact algebraic numbers, and decimals rounded inward
     (point 1 of §1).
2. **For bands that open in the interior** (D = 10, ℓ = 3 at q ≈ 0.4913):
   - the onset certificate (V ≥ 0 up to q_*) as its own item, as O2 was for D = 6;
   - an exact check that the S-certificate's first box starts below q_*.
3. **For bands non-elementary from q = 0⁺** (D = 8–11, ℓ = 2): the first box contains Q = 0, so S6's known answer is internal to the
   band. Register it as the band's must-pass gate. At D = 10 it is already passed (G1).
4. **The design.**
   - The design rule and its parameters (ε₁, ε₂), or a sealed rule for choosing them from a pilot.
   - A degree cap in z and μ.
   - A box-width and subdivision policy.
   - A compute cap per band. Re-derive the stage total whenever a measured per-box cost comes in, and raise or hold the cap in the same
     ruling (a lesson from our side last night).
5. **A planning record** (untrusted, filed before verification): the minimum of ψ₁ and of the slack bracket per box, so a REJECT can be
   diagnosed without post-hoc fishing.
6. **Controls per D.**
   - A planted bound state scaled to that D's ditch depth.
   - A coefficient tamper.
   - A horizon-bound tamper (TD-P2 type).
7. **S14's Table I** as consistency information only, with a tolerance fixed in advance. Numerical tables are not gates for an exact
   certificate.

## 3. The zero-margin throats (D = 2ℓ + 3: D = 7 ℓ = 2, D = 9 ℓ = 3, D = 11 ℓ = 4)

**Choosing q_max.** Do not choose it after seeing results.
- Register a ladder, for example 1 − q ∈ {10⁻¹, 3·10⁻², 10⁻², 3·10⁻³, 10⁻³}.
- Register a stopping rule: run the untrusted design pilot down the ladder, and set q_max at the last rung where the pilot's predicted
  degree is under the cap and its minimum slack is above a stated threshold. The run of record then targets that q_max only.
- At zero margin I expect the slack to vanish slowly as q → 1. It is the borderline inverse-square case, so likely logarithmically.
  Without a pilot, I would not go past 1 − q = 10⁻², the same as D = 6.
- With a positive margin, c_n + 1/4 > 0 gives uniform slack in the throat, and the ladder may go further.
- Either way the claim stops at q_max, and extremality stays with A2.

**The margin to require.** Require a slack threshold, not a distance in q. For example, in the pilot, the minimum over the box of the
S-deformed potential's slack bracket (scaled by its size at infinity) is at least a registered constant. Then q_max follows from the
ladder. This keeps the requirement meaningful across D.

**A better variable near the throat.**
- In z = 1 − r_H/r the throat has width about δ := 1 − (r₋/r_H)^{n−1}, which goes to 0 as q → 1. A polynomial in z must resolve two
  scales: the throat and the far region.
- A Möbius map such as ζ = z/(z + δ(μ)) stretches the throat to O(1), and it keeps the method exact:
  - N(z(ζ))·(1 − ζ)^{deg N} is a polynomial in ζ of the same degree;
  - z ∈ [0, 1] maps to ζ ∈ [0, 1/(1 + δ)], where Bernstein positivity applies;
  - δ(μ) is rational in μ under the existing parametrisation, so μ-boxes still work.
- Designing P in ζ should keep the needed degree bounded as q → 1, where z needs a growing degree. That is a conjecture to test in the
  pilot, not a claim. The alternative coordinate y = (r − r_H)/(r − r₋) does the same job less directly.
- I would register both variables' pilots and pick by the measured degree, before the run of record.

## Pointer (for the operator to relay to bh-modes)
For bh-modes: `[deliveries]/ib-lead_a1_reading_2026-10-23/` (READING.md and INPUTS.sha256, listed in SHA256SUMS).
