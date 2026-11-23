# AUDIT — bh-modes exact onset (BHM-017)

*Auditor: Kimi (second auditor for machine results), 2026-10-22.
Brief: `results/onset/briefs/BRIEF_kimi_2026-10-22.md`, SHA-256
`318e709c00a91cb807dc4ef4652d73cba5101264ead256c2c0ba293f27ee81df` (verified against
`SEALED.sha256`). Workspace: `[kimi-folder]/bhm-onset-audit-2026-10-22/`.
The bh-modes tree was never modified. All my checks are exact (Fraction / fmpq / sympy
rationals); my Bernstein verifier and rf arithmetic are the ones I wrote and cross-validated
in the p3 audit (`../bhm-p3-audit-2026-10-22/own/`, KAT-tested).*

**Anti-anchoring.** All own checks below were complete and on disk before I opened
`results/onset/RESULT.md` or the run of record.

## Task 1 — own derivation of U_-(x_H(q); q)

Using my own QQ(μ) arithmetic (`own/rf.py`, denominators factored as (μ²+6)^a(μ+1)^b(μ+6)^c)
and my own KI (5.63b) transcription (validated against the rendered PDF in the p3 audit):

- U_-(t·x_H) = F(t,μ)/Den(μ) with **Den(μ) = (μ+1)³(μ+6) = μ⁴+9μ³+21μ²+19μ+6** (> 0 on
  [0,1], proved by my Bernstein verifier: min coefficient 6);
- **g(μ) := F(1,μ) = 1024·(μ+15)·(10μ³ − 11μ² + 228μ − 45)** — the registered cubic factor
  appears exactly (`own/g_factor.log`).

## O1 — PASS

- The cubic 10μ³ − 11μ² + 228μ − 45 is irreducible over ℚ (sympy factor); it has **exactly
  one real root on the whole line** (my own Sturm sequence over ℚ, V(−∞)−V(+∞) = 1), which is
  therefore simple and is the only root in [0,1]; the other factor μ+15 has none.
- g(0) = −691200 < 0, g(1) = 2981888 > 0.
- Isolation (my bisection, exact rationals, width 7·10⁻⁴⁶):
  μ_* = 0.1989324097460524925…
- Resultant (mine, sympy `resultant`): Res_μ(cubic, Y(6+μ²)² − ((6+μ²)² − 49μ²)) =
  9529569·(3025Y³ − 31521Y² + 99792Y − 68796) — the registered minimal polynomial of q_*²,
  irreducible, with exactly one real root (my Sturm).
- q_*² = 0.94683882904927334931…, q_* = 0.97305643672362259818154625232076896511970417…,
  inside the registered prediction [0.9730564367, 0.9730564368] and digit-identical to the
  value in TARGET_ADDENDUM_1.md.
- Independent Arb isolation (flint `complex_roots`): real roots 0.198932409746052 ± 5e-16 and
  0.946838829049273 ± 4e-16 — agree.
- *Self-correction recorded:* an intermediate print of my q_* interval showed garbage beyond
  digit 17 (float formatting of an exact value); the exact rationals were always correct, and
  the mpmath comparison confirms agreement to 4·10⁻⁴².

## O2 — PASS

With my own choices τ = 1/16, μ_c = 21/100 (each successful choice is a proof), my exact 2-D
Bernstein verifier (`own/verify.py`) proves, on F with integer-coefficient numerator:
- R1: F > 0 on [0, 15/16] × [μ_lo, 1] — 1 node;
- R2: F > 0 on [15/16, 1] × [21/100, 1] — 1 node;
- R3: −∂F/∂t > 0 on [15/16, 1] × [μ_lo, 21/100] — 1 node.

Then for μ ∈ [μ_*, 21/100] and t < 1: F(t,μ) > F(1,μ) = g(μ) ≥ 0 (strictly, by R3), with
equality only at (t,μ) = (1, μ_*); elsewhere R1/R2 apply. Hence U₋ ≥ 0 on the closed region
with equality only at (q_*, x_H(q_*)). (The lead's own choices τ = 1/8, μ_c = μ_hi + 1/64
differ; that is the implementation freedom the PREREG allows.)

## O3 — PASS

Sturm count 1 on [0,1] plus g(0) < 0 gives g < 0 on [0, μ_*), i.e. U₋(x_H(q); q) < 0 for all
q ∈ (q_*, 1].

## O4 — PASS

My exact simplification: b = 2m − 10(1+mδ)x_H = 4(4μ − 3)/(μ + 1) at m = 6, so b > 0 iff
μ > 3/4. And w(3/4) = 4/5 exactly, i.e. q(3/4) = 3/5, with w increasing (O5): b > 0 iff
q < 3/5, b = 0 at q = 3/5.

## O5 — PASS

Transcription vs KI (5.63b) at n = 4: symbolic identity (p3 audit `build.py`). The
parametrisation identities s² = 1 + 4mq²/25, x_H = 2/(1+w), κ³ = (1−w)/(1+w): exact
(p3 audit). Den > 0 on [0,1] and w′ = 7(6−μ²)/(6+μ²)² > 0 on [0,1]: my Bernstein verifier.

## Controls — both REJECT as required

- Perturbed U₋ coefficient (7680 → 7681, i.e. my builder's U2 46080 → 46086): the claimed
  cubic no longer divides the recomputed g, and the certified μ_* interval no longer brackets
  a sign change — the perturbed claim is rejected by my code (`own/control_perturb.log`).
- Onset moved by 10⁻⁶: my Sturm count of the cubic on [μ_lo + 10⁻⁶, μ_hi + 10⁻⁶] is 0 —
  the moved claim is rejected.

## Reproduction — PASS

`kit/onset/run.sh` at `180824b` in my workspace (`runs/kit-run-180824b/`), exit 0, KIT PASS:
main VERIFIED; NC-O1, NC-O2, TD-O1, TD-O2 all REJECT; PC-O1 VERIFIED. My `main/result.json`
is identical to the run of record in every substantive field (timings/provenance masked); the
record's SHA-256 matches the brief's `d8fb597f…`.

## Reconciliation

`RESULT.md`'s table matches my independent findings on every row: the same cubic factor, the
same μ_* and q_* digits, the same minimal polynomial, the same control outcomes. Their F has
declared degree (4, 104) in (t, μ) with integer coefficients vs my μ-degree-12 numerator with
Den = (μ+1)³(μ+6): different denominator-clearing choices, both with positivity proved; same
content.

---

*2026-10-23 addendum (verifier defect, found and fixed by me after this audit was delivered):*
the first version of my Bernstein verifier's box substitution (`substitute_1d`/`substitute_2d`)
used a wrong power of the box width (`h**j` for `h**k`), corrupting every check on a non-unit
or subdivided box. Caught by the HD-E audit's interior-band control (a known negative value the
verifier initially missed); fixed, with coefficient-level regression KATs (KAT6–KAT8). Every
verifier-dependent verdict in this audit was re-produced with the fixed code
(`own/*_v2.log`, and the runs of record on host-1: `own/kat.host-1.log`, `own/o2345.host-1.log`): no verdict changed. The exact-arithmetic results
(transcription, the N identity, Sturm counts, resultants, isolations, the kit reproductions)
never touched the verifier and are unaffected.

---

## Overall verdict

**BHM-017 (O1–O5) stands.** All claims re-derived by my own exact route; the reproduction is
bit-consistent with the record. No fixes.
