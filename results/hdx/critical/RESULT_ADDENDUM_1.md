# RESULT addendum 1 — HD-X-2: the six new gate controls

*Item BHM-154. 2026-10-26, the bh-modes lead. Registration: `PREREG_ADDENDUM_1.md` (BHM-153), with `PREREG.md`
(BHM-143). `RESULT.md` (BHM-144) is sealed and unchanged. Sealed.*

## Verdict: as registered, KIT PASS

- **The record:** host-1 at `768ba3d`, from its `git archive` (SHA-256 `c502023463832135…`), 03:21:21–03:21:50 UTC
  (23:21 EDT on 2026-10-26), `BHM_JOBS = 8`. It ran `kit/hdx/run_critical_a1.sh`: 47 jobs, KIT PASS.
- **The reproduction:** host-2, with `BHM_REF` set to the record, 03:22:08–03:22:24 UTC. KIT PASS, and all 47 jobs are
  IDENTICAL after masking.
- **(a), the consistency requirement, holds in both runs.** Each of BHM-144's 35 jobs comes out IDENTICAL after masking
  to its record. The one difference in each is the top-level `archive_sha256`, as registered, since this run is from
  another archive. So the 9 bands are VERIFIED again, and the 26 original controls give BHM-144's verdicts.
- **(b): every one of the 47 jobs ends in its registered form** (`hdx.kitcheck`, 47 "match").

**The six new controls**, the same at D = 7 ℓ = 2 and D = 11 ℓ = 4:

| Control | Change | Registered form | Observed, at both bands |
|---|---|---|---|
| td-param | PARAM on param_n's tamper (B = 2ℓ + n) | `=REJECT: PARAM` | REJECT: PARAM |
| td-H | H on H₋ − n(n + 1)x | `=REJECT: H` | REJECT: H |
| td-R | R on −R | `=REJECT: R` | REJECT: R |
| td-L | L on −L | `=REJECT: L` | REJECT: L |
| td-S | ε_n → −ε_n in the design | `+PARAM,S,THROAT,FIRST,XN\|POS-O,POS-O',POS-T,POS-C` | REJECT: PARAM, S, THROAT, FIRST, XN, POS-O, POS-O′, POS-T, POS-C |
| td-XN | μ²z²(1 − z) added to NL before XN | `=REJECT: XN` | REJECT: XN |

## What it means

- **Every gate of HD-X-2 now has a control that fails as registered.** RULES.md E.4 is met for HD-X-2, and the
  reading's 2a (BHM-151) is closed.
- **td-XN** is a perturbation of NL that passes every other gate by construction. XN alone refused it, so the
  independent route of XN is what guards the assembly of NL.
- **td-S** moves the pole inside the exterior. S refused it, and so did the gates whose exact values assume +ε̂ (THROAT,
  FIRST and XN), PARAM through ε's identity, and all four POS charts.
- **BHM-144's certificate is unchanged.** (a) shows its 35 jobs identical under the new code, and this addendum adds
  controls only. HD-X-2 stays *certified* (exact), as in BHM-144 and STAGE_REPORT_ADDENDUM_1 §1.

## Records

- `runs/record-a1/` (host-1) and `runs/repro-a1-host-2/`: one directory per job, each with `result.json`, `run.log`
  and `kitcheck.txt`. Each of the 35 original jobs also has `compare-bhm144.txt`, and the reproduction has
  `compare.txt` for every job.
- The kit logs and hosts, with UTC times, are in `logs/` (`*-a1*`).
- Every copy in the repo was hashed against its node copy (host-1, host-2): all match.
- The SHA-256 of every record and log are in `SEALED.sha256` under BHM-154.
