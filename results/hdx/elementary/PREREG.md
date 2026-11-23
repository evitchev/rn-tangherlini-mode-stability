# PREREG — HD-X-E: D = 7–11 near extremality, by U₋ ≥ 0 (stage 3, HD-X-1)

*Item BHM-127. 2026-10-26, the bh-modes lead. Step 2 of `TARGET_HD_ADDENDUM_2.md` §4 (BHM-121).*
- *Registered before any run of this code on S5's potential at the claimed (D, ℓ). The development tests (§5) used
  synthetic inputs, plus S5's potential at n = 4, where A2-E's record and A2's gates are known answers.*
- *Not blind in one respect: the scoping's planning runs (`results/planning/stage3_2026-10-25/hdx/elem_plan_D*.log`,
  floats) saw, for these (D, ℓ), positive grid minima and no root of F(t, 0) in [0, 1] other than the touching corner.*
- *The code was written by a fork of the lead (BHM-120) and read by the lead: `code/hdx/elementary.py` and
  `kit/hdx/run_elementary.sh`, at the commit that holds this file. Sealed; any change before the run is a dated
  addendum.*

## 1. The claim

> **HD-X-E.** For D = 7–11 (n = 5…9), every ℓ ∈ {n − 1, …, ℓ₀(n)} with ℓ₀ = 10, 10, 11, 13, 14, and every
> q ∈ [q(μ_lo), 1], U₋ ≥ 0 on the closed exterior 0 ≤ x ≤ x_H.
> - For ℓ ≥ n the inequality is strict.
> - For ℓ = n − 1 its only zero is at the extremal horizon (x = x_H = 2, q = 1).
>
> Hence V_S− ≥ 0 on the exterior, and A_{ℓ,q} ≥ 0.

- **μ_lo(D, ℓ)** is HD-E's E1 lower end (BHM-063): the largest k/10000 with w(k/10000)² ≤ 1 − (99/100)². So
  q(μ_lo) ≥ 99/100, and HD-E's E1 covers [μ_lo, 1] in μ, i.e. q ∈ [0, q(μ_lo)].
  - The grid is HD-E's k/10000, not A1's k/1000. A k/1000 end would lie below HD-E's wherever HD-E's value is off the
    1/1000 grid (e.g. 1061/10000 at D = 7 ℓ = 4), and would leave a gap.
  - k/1000 is used only at n = 4, for gate A2E4.
- **With Theorem HD and Lemma U(n)** (E3, every q ≤ 1, ℓ > ℓ₀): every ℓ ≥ n − 1 is then covered for every q ∈ (0, 1],
  at D = 7–11. The ℓ ≤ n − 2 are the 20 bands: HD-X-S for the 11 with 2ℓ > n − 1, and HD-X-2 for 𝒦.

## 2. Method (exact; HD-E's parametrisation `hd.elementary.param_n`, μ = 0 at q = 1)

- **The setup.** With x = t·x_H, U₋ = F(t, μ)/Den(μ) in lowest terms, from S5's U₋ at general n (`ki.potentials`).
- **Gates:**
  - **KAT,** the verifier's known-answer tests (`a1.p1.kats`, KAT1–8);
  - **E0n:** S5's U₋ and H₋ at n = 2…12 equal Kimi's independent transcription (HD-E's gate, BHM-063);
  - **PARAM4,** HD-E's parametrisation check;
  - **H:** every coefficient of H₋ is > 0, for n = 4…9;
  - **EXT** (q = 1, symbolic in ℓ, n = 4…9): param_n gives q² = 1, x_H = 2 and δ = 1/((ℓ + n)(n + 1)). Then
    H₋(x_H) = (ℓ + n)(ℓ + n − 1) and U₋(x_H) = 64ℓ(ℓ − n + 1)H₋(x_H)²;
  - **MEET.** HD-E's record (`results/hd/elementary/runs/record/main/result.json`) is checked by its sealed SHA-256.
    For each claimed (D, ℓ), its E1 entry has q_hi = 99/100 and covers = true, and its μ_lo is at most this code's (the
    record shows equality). Its E3 ℓ₀(n) equals the hand-off;
  - **A2E4.** This code at n = 4, with A1's k/1000 rule, reproduces A2-E's sealed record (BHM-097) for ℓ = 3…10, field
    by field, with the record checked by its SHA-256.
- **Per part:**
  - the parametrisation identities (s² = 1 + 4mq²/(n + 1)², q(1) = 0, q(0) = 1, δ(1) = 0);
  - w increasing on [0, 1];
  - q(μ_lo)² ≥ (99/100)²;
  - Den > 0 on [0, μ_lo].
- **ℓ = n…ℓ₀(n):** F > 0 on [0, 1] × [0, μ_lo], by exact Bernstein bisection (`onset.bernstein.prove_sign`). The record
  gives the certified lower bound min F / max Den.
- **ℓ = n − 1,** the five touching cases (D = 7 ℓ = 4, D = 8 ℓ = 5, D = 9 ℓ = 6, D = 10 ℓ = 7, D = 11 ℓ = 8). F(1, 0) = 0
  by EXT. With s = 1 − t:
  - F(1 − s, μ) = μK(μ) + sG(s, μ), with K = F(1, μ)/μ and G = (F(1 − s, μ) − F(1, μ))/s exact polynomial divisions,
    both remainders 0, and the identity checked;
  - K > 0 on [0, μ_lo] and G > 0 on [0, 1] × [0, μ_lo], by exact Bernstein;
  - so F ≥ 0, with F = 0 only at s = μ = 0.

**Verdict.** VERIFIED if every check holds, otherwise `REJECT: <checks>`, fail-closed.

## 3. Controls (same kit; each must give its registered verdict)

| Control | Registered verdict | Why |
|---|---|---|
| nc-band: D = 7 ℓ = 3 and D = 11 ℓ = 7, S-bands, on the strict path | REJECT: E D=7 l=3, E D=11 l=7 | U₋(x_H) = 64ℓ(ℓ − n + 1)H₋(x_H)² < 0 at q = 1: −602112 and −25804800 |
| nc-strict: D = 7 ℓ = 4 and D = 11 ℓ = 8, touching, with a strict bound on F itself | REJECT: E D=7 l=4, E D=11 l=8 | F(1, 0) = 0 at a corner of the box |
| nc-bump: D = 7 ℓ = 5 and D = 11 ℓ = 9, F − c·64t³(1 − t)³Den with c = 2\|U₋(½, 0)\| + 1 | REJECT: E D=7 l=5, E D=11 l=9 | At (½, 0) the value is Den(0)(U₋ − c) < 0, by a rule rather than a tuned constant |
| td-coeff: U₋ + 16nm² (HD-E's tamper) | REJECT, beginning with E0n | The transcription gate. Predicted in full: E0n, EXT, A2E4 and the five touching parts (F(1, 0) ≠ 0 breaks the division by μ); the strict parts still pass, since U₋ only grows |
| td-verifier: the threshold lowered to −1 | REJECT, beginning with KAT | The known-answer tests catch it |
| td-mulo: 995/1000 in place of 99/100 in the μ_lo rule | REJECT, beginning with MEET | Each [0, μ_lo] stops short of HD-E's lower end. Predicted in full: `REJECT: MEET` |

The kit matches the last three by prefix (`kit/hdx/run_elementary.sh`). The predicted full lists are recorded here and
will be compared with the record.

## 4. Runs, hosts

- **One command:** `kit/hdx/run_elementary.sh`.
- **The record** runs on host-1, from a `git archive` of the commit that holds this file, under `nice -n 19` in
  `[venv]`.
- **The reproduction** runs on host-2, with `BHM_REF`; every JSON must be identical after masking.
- **The records** carry the UTC start time (masked) and the archive's SHA-256 (`BHM_ARCHIVE`).
- MEET and A2E4 read two sealed records from the archive, and E0n reads Kimi's `build.py`, as in HD-E. A run from an
  archive without them rejects.

## 5. Development tests (`code/hdx/devtest_elementary.py`)

These use synthetic U at n = 5 and 9, and S5's potential only at n = 4.
- Every path, on synthetic U:
  - the splitting;
  - the strict path, which refuses a touching corner and proves a positive U;
  - the bump and a negative U, each refused;
  - a splitting whose F(1, 0) ≠ 0, which is refused.
- The KATs, with and without the tamper.
- EXT at n = 4, a known answer, which fails on synthetic U and under td-coeff.
- MEET: the 99/100 rule reproduces HD-E's μ_lo at all 33 (D, ℓ), and the 995/1000 rule fails at all 33.
- **A2E4: n = 4 reproduces A2-E's record field by field**, and fails under td-coeff.
- The record writer twice, with `compare_runs` IDENTICAL after masking.
- Each control end to end on synthetic U.

**Results:**
- 32/32 as expected at `72d4221`, in the fork's clone, on host-1.
- The rerun at `8f42e0e`, the same files in this repository, on host-1: 32/32 as expected, DEVTEST PASS, in 41 s
  (`[run-folder]/dev-hdxe-8f42e0e/devtest.log`).
