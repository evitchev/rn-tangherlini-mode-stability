# PREREG_AMEND_1_2026-10-23 — process additions for phase 2

*ib-blind seat, 2026-10-23. It is written and sealed (`chmod 0444`) before any run of record. Its sha256 is
recorded in `runs.json`.*

**Base.** `PREREG.md`, sha256 `7addc5911fdda10724a222558d26421dc05e8b016b12eb650e9d9f38ddfb1b87`. The
coordinator approved it together with the transcription (GO for phase 2, 2026-10-23).

**Brief.** sha256 `1339b7fbd0c0761e055e375501bbb857485fc728c40c5c2b2bf2e0e19a8703dd`.

This amendment adds the coordinator's three process rules, A1–A3. It also writes down how I will carry out a few
PREREG steps, X1–X5. **It does not change the mathematics (§2), the method (§3), the controls (§4), the caps (§5),
the stopping rules (§6) or the verdict rules (§7)**, except where A3 tightens S1.

## A1 — node gate (every run of record)

- **Logging.** The same shell command first runs `date -u; hostname; uptime; nproc; free -g` (no process listing).
  It then starts Python, and prints `date -u; hostname` again at the end.
- **Workers.** Python reads `/proc/loadavg`, `nproc` (os.cpu_count) and MemAvailable from `/proc/meminfo`, and sets
  w ≤ min(8, nproc − 2 − ⌈load1⌉). It then requires MemAvailable ≥ 16 GB + 2 GB × w, lowering w until this holds.
- **Fallback.** If w < 1, the run does not start on that node. I retry on host-1, through the same gate.
- **Record.** The gate's inputs, the chosen w and the pass or fail are printed in the log and copied into
  `runs.json`.

## A2 — no in-place edits after a run of record

- Code for runs of record lives in `code/rec/`, as versioned files (`*_v1.py`). It is made read-only (0444) before
  its first run of record.
- A fix is a byte copy under a new name (`*_v2.py`, …) with its own hash. A file used by a run of record is never
  edited again.
- `runs.json` lists the files and hashes each run used.
- The frozen phase-1 files (`code/ki_s5.py`, `code/check_transcription.py`) are imported as they are.

## A3 — immediate stop (tightens PREREG §6, S1)

**Triggers.** Either of these stops all work at once:
- in NEG1, the **unperturbed** I₁ + I₂ < 0 (a variational witness at q = 97/100 without the well);
- any q_i with Z ≥ 1 on which both integrators agree.

**Then.** Hand back immediately to the session-R lead with the q and the witness. Do not finish the other
parts first.

## Execution clarifications (no change to method or verdict rules)

- **X1 — development runs.** Runs that are not of record (debugging, timing) use only parameters outside the band:
  q ∈ {0, 0.5, 0.9, 0.94}, µ_T-cells inside [0.29, 0.33], the planted-well setup, and generic test polynomials.
  Every in-band computation is a run of record, made with frozen code.
- **X2 — TP1.** TP1 is also run, before any band run, on an out-of-band certified cell in µ_T ∈ [0.29, 0.33]
  (q ≈ 0.93–0.946). It is run again, as PREREG §4 says, on the first certified band cell.
- **X3 — NEG1 certifier-refusal attempts.**
  - (a) Apply the standard Part C fitting procedure to the well-perturbed problem, at the 4 retry settings. Where
    ψ₀ has a zero, P_true has a pole, so its samples are capped to [−50, 50] before fitting.
  - (b) After Part C, re-verify with the well every P tried on the unperturbed cell that contains q = 97/100.
  - Every one of these must be rejected. A certification is a verifier bug (S3).
- **X4 — parameters.**
  - Part N computes w = √(1−q²) and s = √(1 + 7q²/9) in mpmath at the run's precision.
  - Parts C and E use rational µ_T, so w = 8µ/(7+µ²) and δ = (1−µ²)/(6(7+µ²)) are exact.
  - In both, f = (1 − ρ^{−4})(1 − κρ^{−4}) with κ = (1−w)/(1+w). This is algebraically 1 − x + q²x²/4 with
    x = x_H ρ^{−4}, written to avoid cancellation at the horizon. U₋ and H₋ come from `ki_s5.py` via sympy at run
    time, through the transcription guard (TP2).
- **X5 — records.**
  - `runs.json` is the live record. Its phase-1 state is kept byte-exactly as `records/runs_phase1_3ea47ab2.json`
    (sha256 `3ea47ab2…`), which is the state that `PHASE1_SHA256SUMS` refers to.
  - Delivery: `[deliveries]/ib-blind_hd-s_2026-10-23/` (VERDICT.md, code, logs, runs.json, SHA256SUMS). Then
    hand back to the session-R lead with a one-line pointer and the SHA256SUMS hash. Nothing is sent
    anywhere else.
