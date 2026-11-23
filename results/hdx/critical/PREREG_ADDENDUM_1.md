# HD-X-2, PREREG addendum 1: a control for each gate that had none

*Item BHM-153. 2026-10-26, the bh-modes lead.*
- *It answers the session-R lead's reading of the stage-3 report (BHM-151; `READING.md` §Q2, finding 2a). Six
  gates, PARAM, H, S, R, L and XN, had no planted control or tamper. That breaks RULES.md E.4 and the commitment in
  `results/hd/STAGE_REPORT_ADDENDUM_1.md` item 5.*
- *`results/hdx/critical/PREREG.md` (BHM-143) is sealed and unchanged, and BHM-144's VERIFIED run stands.*
- *The code is `code/hdx/critical.py` at the commit that holds this file. It adds six controls and leaves the none path
  and the 13 registered controls unchanged. Precondition (a) of §3 checks this, and §4 tests it.*
- *The new kit is `kit/hdx/run_critical_a1.sh`. The sealed `kit/hdx/run_critical.sh` and `code/hdx/kitcheck.py` are
  unchanged.*
- *The code was written by a fork of the lead, who wrote HD-X-2, and read by the lead: `critical.py`'s diff from
  `6cedd44`, the new kit, and the devtest's additions. The lead accepts the one allowed difference in (a),
  `archive_sha256` (§3). The lead's re-run of the development test is in §4. Sealed; any change before the run is a
  dated addendum.*
- **Not blind:**
  - The five `=` forms below assume that the band's none job is VERIFIED, as BHM-144's record shows at both kit bands.
  - The development tests ran gates() (every gate before the POS charts) on S5's potential at both kit bands for the six
    controls, td-S included, and for the 35 original jobs.
  - No POS chart of a new control ran on S5's potential.

## 1. The six controls (run on D = 7 ℓ = 2 and D = 11 ℓ = 4)

| control | change | registered form | why it can fail | how it could wrongly pass |
|---|---|---|---|---|
| td-param | the PARAM gate on `param_n(n, ℓ, "td-param")` (B = 2ℓ + n, hd.elementary's tamper); everything else on the true parametrisation | `=REJECT: PARAM` | the s² identity, δ(0) and ε's identity all fail on the tampered p | if PARAM ignored its input, or read the true p |
| td-H | the H gate on H₋ − n(n + 1)x, the gate's input only (as HD-X-S) | `=REJECT: H` | the x-coefficient becomes −n(n + 1)/2 < 0 | if H checked something other than H's coefficients |
| td-R | the R gate on −R | `=REJECT: R` | −R < 0 on [0, 1] | if R's positivity check were not run, or not strict |
| td-L | the L gate on −L | `=REJECT: L` | −L < 0 on [0, MU1] | as td-R, for L |
| td-S | ε_n → −ε_n in the design itself (as HD-X-S): the pole moves to z = +ε, inside the exterior | `+PARAM,S,THROAT,FIRST,XN\|POS-O,POS-O',POS-T,POS-C` | S fails (ε_n/μ < 0). PARAM fails (ε's identity), THROAT and FIRST fail (their pencil values use +ε̂), and XN fails (the direct N keeps +ε). The POS charts may fail too: under td-S, T(0, 0) < 0 and K(0, 0) < 0 | if S checked ε_d alone, or if any gate read the registered ε rather than the built one |
| td-XN | μ²z²(1 − z) added to NL after it is built and before XN, so XN compares the perturbed NL with the direct N | `=REJECT: XN` | XN's two routes then differ at every interior point | if XN compared NL with itself, or used too few points (it uses 27) |

**td-S's non-POS list** was found exactly with gates() on S5's potential at both kit bands, with no POS chart:
PARAM, S, THROAT, FIRST, XN. It is the same on the synthetic potential.

## 2. Why td-XN leaves everything but XN unchanged

The term t = μ²z²(1 − z):
- vanishes to second order at μ = 0, so Z0, DIV-O and FIRST's M(z, 0) are unchanged;
- vanishes at z = 1, so INF is unchanged;
- becomes μ⁴ζ²(1 − μζ) in T, which is divisible by μ² and vanishes at μ = 0, so DIV-T, THROAT and CORNER's T(ζ, 0) are
  unchanged;
- becomes z⁴σ²(1 − z) in C, which is divisible by z²σ and vanishes at z = 0, so DIV-C, CORNER's K(0, σ) and FIRST's
  K(0, 0) are unchanged.

It adds μz²(1 − z) to M, μ²ζ²(1 − μζ) to T and σz²(1 − z) to K. Each is a product of factors with non-negative Bernstein
coefficients on its chart's boxes: z ≥ 0, 1 − z ≥ 0, μ ≥ 0, σ ≥ 0, and 1 − μζ ≥ 3/4 on T's box. So each has
non-negative Bernstein coefficients there. Adding it cannot make a positive Bernstein coefficient non-positive, so the
four POS charts pass as for none (BHM-144: one Bernstein leaf each). The development tests check the chart images and
the signs of their coefficients on every box, for every MU1.

## 3. The kit: `kit/hdx/run_critical_a1.sh`

It runs 47 jobs: the 9 bands with control none, and all 19 controls on D = 7 ℓ = 2 and D = 11 ℓ = 4, with `nice -n 19` on
every Python call. KIT PASS only if:
- **(a) consistency.** Each of the 35 original jobs is IDENTICAL after masking (code/compare_runs.py) to BHM-144's record
  of the same job, `results/hdx/critical/runs/record/` by default (or BHM_A1_BASE).
  - The one allowed difference is the top-level `archive_sha256`, which differs by construction: this run comes from
    another archive. compare_runs does not mask it.
  - The kit refuses (exit 2) any output directory inside that record. Writing output there is what made the screen's
    comparisons vacuous.
- **(b)** each of the 47 jobs ends in its registered form (code/hdx/kitcheck.py), the 12 new ones included;
- **(c)** with BHM_REF set to a directory of records, each of the 47 jobs is also IDENTICAL after masking to that record.

## 4. Development tests (`code/hdx/devtest_critical.py`: 231/231 at `d0a75b2`, host-2, 119 s)

- **Runs.**
  - The fork's run is at `d0a75b2`, in its clone. Its log is `dev/devtest-a1-d0a75b2.log`.
  - The lead re-ran it at `c4de47c`, which holds this file's code (host-2, under `nice -n 19`): 231/231 as expected in
    121 s, DEVTEST PASS. Its log is `devtest-a1-c4de47c.log`, beside this file.

- **The six controls on the synthetic potential:** main() at both kit bands, each in its form, with its non-POS failures
  exact.
- **On S5's potential, gates() only:** each control's non-POS failures are exact at both kit bands, td-S included.
- **td-XN's term:** its chart images, and the signs of its Bernstein coefficients on every box.
- **The kit tables:** the sealed kit's equals BHM-143's 14 forms, and the new kit has all 20. CONTROLS is BHM-143's 14,
  then the 6.
- **Precondition of (a), without POS:** for each of BHM-144's 35 jobs, gates() on S5's potential gives exactly the
  record's checks before the POS charts, and its fields (band, design, charts, eps, q(MU1)², throat_data, C0, degrees,
  d6). All 35 equal.
- **The kit's flow,** with a stub interpreter on host-2, BHM_JOBS = 4:
  - KIT PASS against a fake base whose archive differs, and with BHM_REF set;
  - KIT FAIL when a base record is changed ((a)) and when a new control is off its form ((b));
  - refusal of an output inside the base.
  - The stub test found a defect, now fixed: a bash function shared the loop variable `c`.

## 5. Hosts and runs

- **The record:** host-1, from a `git archive` of the commit that holds this file, under `nice -n 19` in
  `[venv]`, with BHM_ARCHIVE set to that archive's SHA-256.
- **The reproduction:** host-2, with BHM_REF set to the record: (c) for all 47 jobs.
- **Time:** about a minute. BHM-144's 35 jobs took 38 s at BHM_JOBS = 4.

## 6. Outcomes (registered now)

- **KIT PASS:** every gate of HD-X-2 has a control that fails as registered, and RULES.md E.4 is met for HD-X-2.
  BHM-144's certificate is unchanged: (a) shows the 35 original jobs identical.
- **A new control off its form, or (a) failing:** the addendum's run is VOID. BHM-144 stands until a further addendum.
- **An exception or a timeout:** VOID.
