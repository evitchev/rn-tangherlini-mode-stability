# The session-R lead's reading of the stability draft's §5 (the assembly), frozen v0.2

*2026-11-13, reading 12:05-12:08 EST, written 12:08 EST, before opening Fable's audit folder (not opened). Object:
`paper/stability/versions/DRAFT_v0.2.md`, sha256 `4441e48a3d487c70b618d94f8c65b40c67045916be491ac7d77992b9924e9bd0`. As for a stage report
(RULES.md E): a reading, not a re-run. Exact comparisons were done by hand or with exact rational arithmetic on numbers taken from
the RESULT files; no certificate was re-run.*

## Summary

§5 composes Theorem 1 correctly as far as I read it. I found no gap in the coverage of (0, 1] for any D = 6-11 and ℓ ≥ 2. Two
findings concern what the paper must disclose (1, 2), one concerns precision (3), and three are wording (4-6). None changes a
range or a verdict.

## Findings

1. **Theorem 1's label (RULES.md A3).** Theorem 1 and §5's conventions say *certified*. But the proof also rests on pencil steps:
   - the tortoise map for q < 1 (§4.1: proved, pencil; audited 2×);
   - Lemma U(n)'s steps (§4.3: proved, pencil; audited 2×);
   - HD-X-2's reduction and cover (§4.6: proved, pencil; audited 2×).
   It also rests on machine-checked parts: Proposition 3 (with the tortoise map as a hypothesis) and Theorem 2. A3 says a certified
   computation that rests on a pencil lemma carries both labels. Fix: e.g. "Theorem 1 (*certified*; its pencil steps *proved*,
   audited 2×; Proposition 3 and Theorem 2 *machine-checked*)", or the same as a sentence in §5's conventions.
2. **T3's history (§5.1, ℓ = 2 at D = 6).** T3 is needed: O2 ends at q_* = 0.97306 and A2-S starts at 0.98936, and T3 fills the
   gap.
   - T3's certificate comes from p3's registration, whose verdict as registered is FAIL: the must-pass known-answer gate G1 failed
     (results/p3/RESULT.md l.8, l.30-40).
   - Design rule 2 was then registered (BHM-024) and passed G1 (results/p3/RULE2_RESULT.md, BHM-025), which records that "the T1,
     T2 and T3 certificates of BHM-023 stand; a certificate's validity does not depend on its design". T3's own certificate is
     fail-closed and VERIFIED.
   - The reasoning is sound. But §5.1 presents T3 as a plain piece, and §5's conventions say every statement has "its own
     registration". The paper relies on T3, and §6 says failed runs stay on the record, so §5.1 or §6 should say so in one
     sentence. Fable's brief asks it to read this; I flag it independently.
3. **E1's end (§5.2 against §5.3).** §5.2 states E1 as "U₋ > 0 for q ≤ 99/100". §5.3 meets it at HD-X-E's lower end q(μ_lo),
   and gate MEET says each μ_lo equals E1's sealed end (results/hdx/elementary/RESULT.md l.12). E1's μ-boxes [μ_lo, 1] certify
   q ∈ [0, q(μ_lo)], with the coverage of q ≤ 99/100 checked exactly (results/hd/elementary/RESULT.md l.22-23).
   - So the two pieces meet at q(μ_lo), not at 99/100, and §5.2's wording does not show that the stretch between 99/100 and
     q(μ_lo) is E1's.
   - Fix: write E1's range as (0, q(μ_lo(D, ℓ))] with q(μ_lo) ≥ 99/100 exactly, as §5.1 does for P1.
   - The same holds for the two other bands (D = 10 ℓ = 6, D = 11 ℓ = 7): E1's [0, q(μ_lo)] meets HD-X-S's [q(1/8), 1], since
     q(1/8)² ≤ (99/100)².
   - In §5.1, name the gate that makes A2-E's lower end equal P1's μ_lo(ℓ) (§5.3 names MEET for its case). I did not read A2-E's
     records.
4. **Decimals (§5's convention "Decimals are inward").**
   - A2-S's lower end is printed "0.98936…". But √(2961/3025) = 0.9893649…, so 0.98936 is outward; A2-S's own
     RESULT_ADDENDUM_1 l.33 gives the inward value, 0.98937 ("rounded up").
   - T3's lower end is printed "0.97277…", which is the inward rounding (√(21576/22801) = 0.9727663…), but "…" reads as
     truncated digits.
   - Suggest: inward roundings without "…" (lower ends rounded up, upper ends rounded down), or truncated digits with "…" and no
     inward claim. q_* = 0.97305… and 0.99019… are right either way (upper ends, truncated).
5. **"The interior band" (§5.2)** is not defined in the draft. hd/s RESULT l.36 and l.50 use it for D = 10 ℓ = 3, whose onset
   (0.4913) is interior.
   - Suggest: "the band whose onset is interior (D = 10, ℓ = 3, onset q ≈ 0.4913)".
   - For the other 12 bands with an onset, §5.2 asserts q(μ_b) ≤ q_split without saying where the comparison is made. Name the
     gate or JSON field.
6. **From A ≥ 0 to "no mode" (§2, §3).** A mode is defined as an L² solution of A φ = −κ²φ. To use A ≥ 0 one needs every such
   solution to lie in A's domain. That holds because V is bounded, so −d²/dr*² + V is essentially self-adjoint on C₀^∞(ℝ) (limit
   point at both ends), and A is its only self-adjoint realization. One clause would make this explicit, or the citation [S6,
   l.640–643] can be checked to say exactly this.

## What I checked, and found consistent

- **Counts.**
  - D = 7-11: the bands are ℓ = 2, …, n − 2, 20 in all (2, 3, 4, 5, 6 per D).
  - Below ℓ_el = 4, 5, 6, 6, 7 lie 18 of them (2, 3, 4, 4, 5), plus the two above (D = 10 ℓ = 6, D = 11 ℓ = 7); 13 bands have an
    onset and 5 start from 0⁺.
  - 2ℓ ≤ n − 1 picks 9 bands (1, 1, 2, 2, 3), the keys of HD-X-2's MU1, and 11 others.
  - ℓ_el = n − 1 at D = 7-9 and n − 2 at D = 10, 11. E1's 35 (D, ℓ) (results/hd/elementary/RESULT.md l.14-20) are HD-X-E's 33
    plus those two.
  - ℓ₀ = 10, 10, 11, 13, 14 as in E1's table.
- **The ℓ-partition** closes at each D, both below and above 99/100.
- **D = 6, ℓ = 2:**
  - q_*² is a root of 3025Y³ − 31521Y² + 99792Y − 68796, with q_* = 0.9730564367… (results/onset/RESULT.md l.15).
  - √(21576/22801) < q_* and √(2961/3025) < √(31416/32041), both exact; the T3 ends agree with results/p3/RESULT_ADDENDUM_1.md
    l.16.
- **D = 10, ℓ = 3:** q(μ_b)² = 91914991536373201/383045380761373201, so q(μ_b) = 0.4898556… < 0.490 = q_split (results/hd/s/RESULT.md
  l.50; results/hd/elementary/RESULT.md l.36).
- **HD-X-2:**
  - the nine q(MU1)² equal the PREREG's table, and each is ≤ (99/100)²; the largest is 46562824/47513449 (my exact check of today,
    for Fable's HD-X-2 audit);
  - [q(MU1), 1) is open at 1, and Theorem 2 covers q = 1;
  - §4.6's constants and cover conditions match code/hdx/critical.py l.96-99 and l.450-452.
- **Routes (§5's conventions).** Each piece named in §5 uses the route its claim type supports (U₋ ≥ 0, N > 0 through
  Proposition 3, or Theorem 2 at q = 1). I read the types as §5 states them, not from each piece's claim text (Fable's item 4).

## Not done in this hour

- A2-E's records and the D = 6 meeting with P1.
- HD-S's per-band q(μ_a) ≥ 99/100, and q(μ_b) ≤ q_split for the 12 bands other than D = 10 ℓ = 3.
- Lemma U's ℓ₀ = 10 at D = 6 against its record.
- Each piece's claim text against its route.
These are within Fable's items 1-4.
