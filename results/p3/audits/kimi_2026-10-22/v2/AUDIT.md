# AUDIT — bh-modes p3 S-certificates (BHM-023 / BHM-025)

*Auditor: Kimi (second auditor for machine results), 2026-10-22.
Brief: `results/p3/briefs/BRIEF_kimi_2026-10-22.md`, SHA-256
`3c828902dcd2d518f9eecd82b45f352446bddc5240c4024f2445d66e40700ee1` (verified against
`SEALED.sha256`). Workspace: `[kimi-folder]/bhm-p3-audit-2026-10-22/`. The
bh-modes tree was never modified. All arithmetic in my checks is exact (Fraction / fmpq /
sympy rationals).*

**Anti-anchoring.** My transcription, my derivation of N, my own positivity verdicts for all
six certificate sets, my controls and both kit re-runs were complete and on disk before I
opened `results/p3/RESULT.md`, `RULE2_RESULT.md`, or any `run.log` or `verdict` field. The
certificate JSONs were read only in the fields the brief allows (`result.P`, `result.mu`,
`result.boxes_mu[k].{mu,P}`).

## Task 1 — own transcription vs the literature: PASS

My `own/build.py` implements KI hep-th/0308128 (5.62b)/(5.63b) at general n (K = 1, y = 0),
transcribed from the rendered PDF page 25 (image kept at `own/ki_page-25.png`), and checks:

- at n = 4 it is **symbolically identical** to `TARGET.md` §1's U₋ and H₋ (as polynomials in
  x with coefficients in m, δ — stronger than the required point check);
- the parametrisation identities are exact: s² = 1 + 4mq²/25, x_H = 2/(1+w),
  q²(μ) = (1−μ)(6−μ)(1+μ)(6+μ)/(6+μ²)², κ³ = (1−w)/(1+w);
- G1's specialization (n = 8, Q = 0, m = 10): U₋ = 1327104x³ + 1741824x² − 1812480x + 192000,
  H₋ = 36x + 10.

*Self-correction 1 (recorded):* I first took m = 14 for G1 by misreading TARGET.md's
n = 4-specific "m = (ℓ−1)(ℓ+4)" as general; KI (5.39) is m = k² − nK = (ℓ−1)(ℓ+n) = 10 at
n = 8. The wrong m produced N(0) = −338504.35 for the record G1 certificate — a loud failure
that my own consistency check (the horizon value against the kit's VERIFIED) forced me to
resolve. With m = 10 everything agrees.

## Task 2 — own N: PASS

- The identity Ṽ = V + dS/dr* − S² = f·N/(64ρ²H₋²) with S = −f(1−z)P was derived with my own
  CAS for **abstract** f(z) and P(z) (`own/build.py` part 2) — it holds as an algebraic
  identity, needing only ρ(1−z) = 1.
- N built from each stored P: T1 (both rules) and G1 by a sympy route; the box certificates by
  my own QQ(μ) arithmetic module (`own/rf.py`: denominators factored as
  (μ²+6)^a(μ+1)^b(μ+6)^c, numerators exact), in the variable Y = 1−z. Den =
  (μ+1)³(μ+6) on every box; each factor proved positive on the box by my own 1-D Bernstein
  check (they are ≥ 1, ≥ 6 there anyway).
- *Self-correction 2 (recorded):* my first rf build had `(1−z)f_z = 3X − 3q²X²` instead of
  `3X − (3/2)q²X²`. My independent crosscheck (`own/crosscheck.py`: rf route vs sympy route on
  T1, all 69 coefficients) caught it before any positivity verdict was produced; after the fix
  the two routes agree exactly. This is exactly what the two-route design is for.
- *Self-correction 3 (recorded):* my first single-μ build scanned coefficients only to degree
  69, silently truncating G1's true degree 77. The truncation produced a spurious negative
  value; the fix scans to a degree bound computed from the inputs (max(deg U, 2 deg H + deg f
  + 2 deg P) + 2) and asserts nothing lives above it.
- *Self-correction 4 (recorded 2026-10-23, found by the bh-modes lead):* the delivered
  `own/crosscheck.log` was the stale pre-fix failing run; a fresh log of the passing run is now
  on disk (`CROSSCHECK OK: rf route == sympy route, 69 coefficients compared`).

## Task 3 — own positivity proofs: PASS for all six certificate sets

My own exact Bernstein verifier (`own/verify.py`, fail-closed, known-answer tested; algorithm
mine, python-flint used only as bignum rationals):

| Certificate | Domain | Verdict | Nodes | Min Bernstein coefficient (accepted boxes) |
|---|---|---|---|---|
| T1 rule 1 | z ∈ [0,1] | POSITIVE | 3 | ≈ 1.9·10⁻²¹ (exact rational in log) |
| T1 rule 2 | z ∈ [0,1] | POSITIVE | 3 | ≈ 3.2·10⁻²¹ |
| G1 rule 2 (D = 10) | z ∈ [0,1] | POSITIVE | 7 | ≈ 8.5·10⁻²³ |
| T2 rule 1 | [0,1] × [97/600, 103/600] | POSITIVE | 3 | — |
| T3 rule 1 | [0,1] × each of 8 boxes covering [3/25, 1/5] | POSITIVE | 3 each | — |
| T2 rule 2 | [0,1] × [97/600, 103/600] | POSITIVE | 3 | — |

Degrees: T1 deg 68; boxes deg (68, 12) with Den = (μ+1)³(μ+6); G1 deg 77 — consistent with
RESULT.md's 68 and RULE2_RESULT.md's 77 (their μ-degree 16 vs my 12 is a different
denominator-clearing choice; both prove the same claim with their own Den > 0). Endpoints
z = 0, 1 and the μ-box edges are included (Bernstein coefficients at the corners are the
endpoint values). T3's boxes are contiguous and cover [3/25, 1/5]; q(μ) maps this to
[0.97277, 0.99020] as claimed (checked: q²(1/5) = 1 − (35/151)² = 21576/22801 and
q²(3/25) = 1 − (175/1253)² = 1539384/1570009, giving the brief's endpoints).

## Task 4 — pencil audit of `results/p3/METHOD.md`

- **Lemma 1 (S-deformation identity): SOUND.** |φ′+Sφ|² = |φ′|² + S(|φ|²)′ + S²|φ|² for real S
  (checked for complex φ too); integration by parts has no boundary terms on C₀^∞(ℝ). The
  Corollary's step "form ≥ 0 on C₀^∞ ⇒ A ≥ 0" is valid because V is bounded continuous, so the
  form domain is H¹(ℝ) and C₀^∞ is a core.
- **Lemma 2 (the ansatz): SOUND.** Every line re-derived; in particular ρ²f′β = (1−z)f_zP
  uses ρ(1−z) = 1; my abstract-P CAS check is an independent confirmation of the same
  identity.
- **Proposition 3: SOUND.** f > 0 and H₋ ≥ m = 6 > 0 on the exterior; N ≥ 0 on the closed
  [0,1] gives Ṽ ≥ 0 on the open exterior, which is what the form integral needs.
- **Remarks:** the z = 1 formula N(1) = 64m²(m + 6 − P(1)² + P(1)) re-derived and correct
  (the condition −3 < P(1) < 4 for ℓ = 2 follows); the z = 0 horizon formula correct; the
  "why such P exist" remark is heuristic motivation, labelled as such, and not load-bearing.

**No GAPs found.**

## Task 5 — controls: all REJECT as required

- **(a)** P(0) raised to (horizon bound −32/117) + 1/10 at μ = 1/6: the exact N(0) =
  −778752/185 < 0, and my verifier REJECTS the tampered N. The certificate's actual P(0)
  ≈ −0.2935 has margin 0.0200 below the bound.
  *(Corrected 2026-10-23 on the bh-modes lead's note: the first version of my controls.py used
  the wrong f_z(0) — the same factor-of-2 slip as self-correction 2, fixed in make_boxes.py but
  not propagated there — and printed the wrong bound 64/741. The REJECT verdict was unaffected:
  the tampered value lay above either bound, and the exact N(0) came from the corrected builder.
  With the correct bound the control is now exactly the construction of the lead's TD-P2, and my
  N(0) = −778752/185 agrees with their counterexample value. The make_boxes.py docstring formula
  has been corrected as well.)*
- **(b)** U₋ coefficient 7680 → 7681 in my builder: my transcription check against KI (5.63b)
  fails immediately (diff −m(mδ+1)x²), so the pipeline rejects. (This is the same mechanism as
  the lead's E0 gate; positivity alone might or might not see a one-unit perturbation — the
  transcription check is the right place for this control.)
- **(c)** KATs on my verifier: −1, z − 1/2, z(1−z) (touches 0 at endpoints) all REJECT;
  1+z+z² POSITIVE; a tampered copy of the verifier (accept threshold min > −2 instead of > 0)
  falsely accepts −1 and is caught by the KAT harness. `own/kat.log`.

## Task 6 — reproduction

- `kit/p3/run.sh` at `782fc56` (my `runs/kit-run-782fc56/`): exit 1 with **KIT FAIL** —
  exactly the registered BHM-023 outcome: T1 VERIFIED, **G1 REJECT** (exact counterexample
  N(1/4) < 0), NC-P1 VERIFIED, TD-P1 and TD-P2 REJECT, T2 and T3 VERIFIED.
- `kit/p3/run_rule2.sh` at `094591c` (my `runs/kit-run-094591c/`): exit 0, **KIT PASS** —
  G1, T1 VERIFIED; TD-P2 REJECT; T2 VERIFIED. Exactly the registered BHM-025 outcome.
- The reproduced certificate polynomials are **byte-identical** to the records for T1, T2, T3
  (rule 1) and G1, T1, T2 (rule 2) — the design step is deterministic.
- Code hashes match RULE2_RESULT.md's list (scert.py 17954fc0…, run_rule2.sh 842bb755…).

## Reconciliation

- `RESULT.md` (BHM-023): every entry consistent with my re-run and my own checks, including
  "degree 68, 3 Bernstein boxes" for T1 (my verifier: 3 nodes) and the G1 counterexample.
- `RULE2_RESULT.md` (BHM-025): consistent; G1 degree 77 matches my rebuilt N exactly.
- The registered verdict FAIL of BHM-023 is a design-rule-1 incompleteness (the G1 ditch),
  not a certificate error: T1/T2/T3's P's verify independently of how they were designed.
  My own positivity proofs for them do not touch the design step at all.

## Findings

None against the certificates or the method. All discrepancies encountered were in my own
code and are recorded above (m for G1; the f_z coefficient; the degree cap). One observation:
`RESULT.md`'s table would be marginally clearer if it stated the μ-degree convention
(their (68,16) vs my (68,12) reflect different Den choices; both valid).

## Overall verdict

**T1, T2, T3 (BHM-023, rule 1) and G1, T1, T2 (BHM-025, rule 2): the certificates are VALID.**
Each stored P makes N > 0 on its whole closed domain, proved by my own exact arithmetic from
my own transcription of the potential and my own derivation of N. The reproduction runs
reproduce the registered outcomes bit-for-bit at the certificate level. A_{2,q} ≥ 0 for
q ∈ [0.97277, 0.99020] stands as certified.
