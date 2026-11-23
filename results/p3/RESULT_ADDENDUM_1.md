# p3 RESULT addendum 1: exact intervals, status as of 2026-10-23, trust base

*Items BHM-060 (the correction in §1) and BHM-058 (the reading that prompted it). 2026-10-23, the
bh-modes lead. The session-R lead's reading of A1 and p3
(`results/a1/reviews/ib-lead_reading_2026-10-23/READING.md`, §1) raised these points.
`RESULT.md` and `RULE2_RESULT.md` are sealed records of their day and stay unchanged; this file is
their forward pointer.*

## 1. The certified q-intervals, exactly (correction BHM-060)

w = √(1 − q²) = 7μ/(6 + μ²) increases on these boxes, so a μ-box [a, b] certifies exactly
q ∈ [q(b), q(a)]:

| Tier | μ-box | q-interval, exact | inward decimals | quoted before |
|---|---|---|---|---|
| T3 | [3/25, 1/5] | [√(21576/22801), √(31416/32041)] = [0.9727663…, 0.9901987…] | **[0.97277, 0.99019]** | [0.97277, 0.99020] |
| T2 | [97/600, 103/600] | [q(103/600), q(97/600)] = [0.97993875…, 0.98220861…] | **[0.97994, 0.98220]** | [0.97994, 0.98221] |

- **What was wrong.** The quoted upper ends were rounded outward, by about 1.3·10⁻⁶. The same T3
  quote appears in `RESULT.md` (l.18, l.23), `results/a1/STAGE_REPORT.md` (l.25, l.30),
  `results/a1/RESULT.md` (l.61) and `FEASIBILITY.md` (l.20), and in registry rows BHM-023 and
  BHM-052. Each should be read with the inward decimals above.
- **Theorem A1 is unaffected.** It needs only (q_*, 99/100], and q(3/25) > 99/100 and
  q(1/5) < q_* = 0.9730564… hold exactly.
- **From now on,** certified intervals are quoted exactly or with inward-rounded decimals, and kits
  print them that way.

## 2. Status as of 2026-10-23 (the sealed files say "audited 0×" and "independent re-run pending")

- **`METHOD.md`:** proved (pencil; **audited 2×**: Kimi BHM-036 and Fable BHM-042, with
  `METHOD_ADDENDUM_1.md`). Lemmas 1–2 and Proposition 3 are machine-checked in Lean (BHM-030).
- **T1, T2, T3 (rule 1) and G1, T1, T2 (rule 2):** *certified*, with their second party done.
  - Kimi re-verified all six, independently and exactly (BHM-036). The lead re-ran Kimi's
    cross-check (BHM-040), and Kimi corrected its own record (BHM-045).
  - **T3 has a second independent check:** session-L's exact re-run of all eight boxes, in its own
    reduced form, counted as second party by the operator's ruling (BHM-056).
- **Theorem A1, which uses T3:** `results/a1/STAGE_REPORT.md` (BHM-055).

## 3. Trust base (both files say "the verification is the trust base")

`METHOD_ADDENDUM_1.md` §3 states it in full. Besides the exact verification, it includes:
- the transcription of S5's (5.59)–(5.63), in `code/ki/potentials.py` and `TARGET.md` §1. Kimi's
  own transcription (BHM-036) and session-L's comparison with 1001.0019 (BHM-031) now check it
  independently;
- S5's reduction to the master equation, which is *cited*.

## 4. One wording point (`RULE2_RESULT.md` l.16)

"With rule 2 it reproduces Ishibashi and Kodama's Q = 0 theorem at D = 10, ℓ = 2" means **the
D = 10, ℓ = 2 instance** of that theorem, and is to be read so.
