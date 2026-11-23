# Exact onset for D = 6, ℓ = 2: VERIFIED (BHM-017)

*2026-10-22, the bh-modes lead. Registration: `results/onset/PREREG.md` (BHM-016, commit
`180824b`, sealed before the run). Run at `180824b`. Every check is exact arithmetic (sympy
1.14.0; python-flint 0.9.0 `fmpq`, `fmpz_poly`).*

## Exact quantities

Parametrisation (PREREG §1, ℓ = 2): w = √(1 − q²) = 7μ/(6 + μ²), s = 7(6 − μ²)/(5(6 + μ²)),
μ ∈ [0, 1]; U₋(t·x_H) = F(t, μ)/Den(μ), with F of degree (4, 104) and integer coefficients,
and Den > 0 on [0, 1].

| Claim | Certified statement |
|---|---|
| **O1** | g(μ) = F(1, μ) has exactly one root in [0, 1], and it is simple. It is the root of the irreducible factor **10μ³ − 11μ² + 228μ − 45** in an isolating interval of width 5.9·10⁻⁴⁶. Hence **q_*² is a root of 3025Y³ − 31521Y² + 99792Y − 68796**, and **q_* = 0.973056436723622598181546252320768965119704171…** (45 digits; both ends of the isolating interval agree to all printed digits). Inside the registered prediction [0.9730564367, 0.9730564368]. Arb root isolation agrees |
| **O2** | U₋(x; q) ≥ 0 for all q ∈ [0, q_*] and x ∈ [0, x_H(q)], with equality only at (q_*, x_H(q_*)). Proof: F > 0 on [0, 7/8] × [μ_lo, 1] and on [7/8, 1] × [μ_c, 1], and ∂F/∂t < 0 on [7/8, 1] × [μ_lo, μ_c], with μ_c = μ_hi + 1/64. Each region needed one Bernstein box |
| **O3** | U₋(x_H(q); q) < 0 for all q ∈ (q_*, 1]. So the onset mechanism is the horizon |
| **O4** | S5's (6.24) bracket at the horizon is > 0 for q < 3/5, = 0 at q = 3/5, < 0 for q > 3/5 |
| **O5** | E0 (S5 (5.63b) at n = 4 equals `TARGET.md`'s U₋), s² = 1 + 4mq²/25, w increasing, Den > 0 |

**Supplementary exact check** (sympy `real_roots` on host-2, after the run; not part of the registered
run): both cubics are irreducible over ℚ, and each has exactly one real root:
- μ_* = 0.19893240974605249258…;
- q_*² = 0.94683882904927334931….

So q_* is determined as the positive square root of the unique real root of
3025Y³ − 31521Y² + 99792Y − 68796.

**Consequences.**
- **FEASIBILITY P2 is complete for ℓ = 2:** V_S− ≥ 0 on the exterior for 0 ≤ q ≤ q_*.
- **For D = 6, ℓ = 2, the set where neither V ≥ 0 nor S5's (6.24) applies is exactly (q_*, 1].**
  This is relative to the sources in `results/screen/PREREG.md` §1.5, and is not a
  completeness claim (CHARTER e4).
- `TARGET.md` §4's rule for q_max can now be applied (`TARGET_ADDENDUM_1.md`).

## Controls and drills (same session; all as registered)

| Name | Outcome |
|---|---|
| NC-O1 (false onset interval μ ∈ [0.20, 0.21]) | REJECT: O1, O3 |
| NC-O2 (false positivity up to μ = 191/1000, q ≈ 0.975) | REJECT, with an exact counterexample: F(1, 191/1000) < 0 |
| PC-O1 (ℓ = 3, positivity on the exterior for q ≤ 0.999082) | VERIFIED (one Bernstein box) |
| TD-O1 (coefficient 7680 → 7681) | REJECT: E0, O1 |
| TD-O2 (the corner lemma's sign test inverted) | REJECT, with an exact counterexample |

## Runs

- **Record.** host-1, `kit/onset/run.sh` at `180824b`: KIT PASS, 31 s for the main run.
  - `runs/record/main/result.json` `d8fb597f7a461a86…`, log `d9e208d2f7894551…`.
  - Controls: NC-O1 `80142dd0…`/`39d3da62…`; NC-O2 `c7230142…`/`cefcfcb0…`; PC-O1
    `d79162dc…`/`0ca3859f…`; TD-O1 `24347f6b…`/`4c4f5958…`; TD-O2 `80e33fbb…`/`aec21ba4…`
    (result / log).
- **Reproduction.** host-2, same code: KIT PASS, identical after masking.
- **One-command re-run:** `BHM_PYTHON=[venv]/bin/python kit/onset/run.sh`.
- **Code at `180824b`:**
  - `code/onset/onset.py` `9b346258ad0375d1…`;
  - `code/onset/bernstein.py` `1a67f19164b68a51…`;
  - `kit/onset/run.sh` `ed7a69e00c2bbf40…`;
  - `code/ki/potentials.py` `7d686b40ad326544…`;
  - `code/qnm1c/common.py` `29c30345dec7b2fe…`.

## Status

- O1–O5: **certified** (exact arithmetic). Trust base: sympy 1.14.0 (polynomial algebra,
  Sturm, factorisation, resultant) and FLINT 3.6.0 (`fmpq`, `fmpz_poly`).
- The Bernstein enclosure property and the corner-lemma argument are standard pencil steps:
  *proved (pencil; audited 0×)*.
- Independent re-run by a second party: pending.
- Lean candidates: the cubic minimal polynomials, and the Bernstein coefficients (exact
  rationals in the record).
