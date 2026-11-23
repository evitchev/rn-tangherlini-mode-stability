# p3 design rule 2: re-runs, PASS as registered (BHM-025)

*2026-10-22, the bh-modes lead. Registration: `results/p3/PREREG_ADDENDUM_1.md` (BHM-024, commit
`094591c`, sealed before any re-run). Run at `094591c` with `kit/p3/run_rule2.sh`: record on
host-1, reproduction on host-2. Both print KIT PASS, and every JSON is identical after masking
timings. The failure of record of the original design, BHM-023's G1, stands.*

| Item (rule 2) | Registered | Outcome |
|---|---|---|
| **G1** (D = 10, ℓ = 2, Q = 0: deep negative region of V; known answer, S6) | must pass | **VERIFIED.** N has degree 77 in z; 5 Bernstein boxes; design 0.35 s, verification 0.25 s |
| **T1** (μ = 1/6) | must pass | **VERIFIED.** Degree 68; 3 boxes |
| TD-P2 (P(0) raised by 1/10) | must reject | REJECT, with an exact counterexample at z = 0 |
| T2 (μ-box around T1) | either way | VERIFIED. Degree (68, 16); 3 boxes |

**Meaning.**
- **The S-certificate passes its known-answer gate.** With rule 2 it reproduces Ishibashi and
  Kodama's Q = 0 theorem at D = 10, ℓ = 2, where V has a deep negative region and the
  registered rule 1 failed.
- **Rule 2 is the design rule for A1's PREREG.** The T1, T2 and T3 certificates of BHM-023
  stand; a certificate's validity does not depend on its design.

**Files.**
- **Records** (`rule2/record/<item>/result.json`):
  - G1 `ad68721b90521258`;
  - T1 `0c91e7a2222f31c2`;
  - TD-P2 `e81c6e1b5133f832`;
  - T2 `1c5fe3035d687601`.
- **Reproduction:** `rule2/repro-host-2/`.
- **Code at `094591c`:** `code/p3/scert.py` `17954fc041e11193`, `kit/p3/run_rule2.sh`
  `842bb7554b1f263a`.

**Status.** G1, T1 and T2 under rule 2: **certified** (exact). Reduction proved (pencil;
audited 0×). Independent re-run pending.
