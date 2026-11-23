#!/usr/bin/env python3
"""Assemble hd_reading_draft/CHECKS.md from the saved hash listings and check outputs (no hand transcription)."""
from pathlib import Path

S = Path("[tmp]")
O = S / "hd_reading_draft"
OUT = O / "outputs"


def block(text):
    return "```\n" + text.rstrip("\n") + "\n```\n"


def rd(p):
    return Path(p).read_text(encoding="utf-8")


status = {
    "results/hd/STAGE_REPORT.md": "read in full",
    "results/hd/elementary/RESULT.md": "read in full",
    "results/hd/elementary/PREREG.md": "hashed only (not read)",
    "results/hd/pilot/RESULT.md": "read in full",
    "results/hd/pilot/PREREG.md": "read in full",
    "results/hd/pilot/PREREG_ADDENDUM_1.md": "read in full",
    "results/hd/s/RESULT.md": "read in full",
    "results/hd/s/PREREG.md": "read in full",
    "results/hd/s/briefs/BRIEF_kimi_2026-10-23.md": "read in full",
    "results/hd/s/briefs/BRIEF_ib-blind_2026-10-23.md": "read in full",
    "TARGET_HD.md": "read in full",
    "TARGET_HD_ADDENDUM_1.md": "read in full",
    "TARGET_A2.md": "read in full",
    "TARGET.md": "read l. 1-60",
    "RULES.md": "read in full",
    "REGISTRY.md": "read rows BHM-010, 017, 021-023, 025, 030, 035, 046, 058, 066-083 (grep)",
    "SEALED.sha256": "all 346 entries verified (C1)",
    "results/p3/METHOD.md": "read in full",
    "results/p3/METHOD_ADDENDUM_1.md": "read in full",
    "results/p3/audits/fable_2026-10-22/AUDIT.md": "read l. 1-60, grep",
    "results/p3/audits/kimi_2026-10-22/AUDIT.md": "grep (l. 18-29, 81-84, 112)",
    "lean/lean_p3_sdeformation_2026-10-22/lean/BHModesP3.lean": "read l. 1-30, 205-250, 350-372, grep",
    "lean/lean_p3_sdeformation_erratum_2026-10-23/ERRATUM.md": "read l. 1-60",
    "code/hd/scert.py": "read in full",
    "code/hd/pilot.py": "git diff 8c2d6d2..710488b only",
    "code/hd/elementary.py": "hashed only (prefix compared with RESULT)",
    "code/ki/potentials.py": "read l. 1-70 (U_minus, H_minus, the n = 4 forms)",
    "code/qnm1c/common.py": "read provenance(), l. 91-116",
    "code/compare_runs.py": "grep (MASK_KEYS, l. 12)",
    "code/p3/scert.py": "hashed only",
    "code/onset/bernstein.py": "hashed only (prefix compared with RESULT)",
    "kit/hd/run_pilot.sh": "read in full",
    "[deliveries]/ib-blind_hd-s_2026-10-23/VERDICT.md": "read in full",
    "[deliveries]/ib-blind_hd-s_2026-10-23/PREREG.md": "read l. 40-70, grep",
    "[deliveries]/ib-blind_hd-s_2026-10-23/TRANSCRIPTION.md": "read l. 110-122, grep",
    "[deliveries]/ib-blind_hd-s_2026-10-23/SHA256SUMS": "verified, 152 OK (C1)",
    "[deliveries]/ib-lead_a1_reading_2026-10-23/READING.md": "read l. 1-40, 85-125",
}

lines = []
for f in ("hashes_docs_code.txt", "hashes_reviews.txt"):
    for ln in rd(S / f).splitlines():
        h, p = ln.split("  ", 1)
        lines.append(f"{h}  {p}  [{status.get(p, '?')}]")

parts = []
parts.append("""# CHECKS — files read and small computations for READING.md (draft of 2026-10-23)

## A. Setting

- Host host-0 (the session's host), 2026-10-23, 12:30–13:05 EDT. Read-only everywhere except this working folder; no git
  command that changes state (only `git log`, `git show --stat`, `git diff`, `git rev-parse`); no messages; nothing on other nodes.
- bh-modes at `b22c087` (the last commit, 12:29:59 −04:00, only fills in BHM-083's commit cell; `cf129f2` before it).
- Every computation ran under `ulimit -v 4000000` and `timeout 600`. Exact checks used Python `fractions` (system
  `/usr/bin/python3 -I`); symbolic checks used sympy 1.14.0 in `[python-2]/bin/python -I` (Python 3.12.8). No bh-modes code
  was imported or run: the D = 6 formulas were copied from `TARGET.md` §1 (l. 23-24) and the general-n U₋, H₋ from
  `code/ki/potentials.py` (l. 23-42), so the A2 checks test consistency with bh-modes' transcription, not S5 itself.
- Scripts are in `[workdir]/scripts/`; outputs in `[workdir]/*.out` and `[workdir]/hd_reading_draft/outputs/` (hashes in E).

## B. Files read, with SHA-256 (paths relative to `[repository]` unless they start with `[deliveries]`)

""")
parts.append(block("\n".join(lines)))
parts.append("""
Records and logs read programmatically are listed in D.

## C. Computations (command, then output, verbatim)

**C1. Seals.** `STAGE_REPORT.md` = `a4426f34c407f9a1…` and `TARGET_A2.md` = `d8207fbfa6b8cd15…` (B). Then:
""")
parts.append(block(rd(OUT / "seals.out")))
parts.append("""
**C2. HD-S intervals and coverage, exact** (`scripts/check_intervals.py`; Fractions). For each band: q(μ)² = 1 − (Bμ/A)² from
μ_a, μ_b, compared with the record; inward test of the JSON and RESULT.md decimals; q(μ_a)² ≥ (99/100)²; onset bands q(μ_b)² ≤
q_split² and HD-E's μ_lo ≤ μ_b; contiguity; every box verified.
`$ /usr/bin/python3 -I check_intervals.py [repository]`
""")
parts.append(block(rd(S / "check_intervals.out")))
parts.append("""
**C3. HD-E bounds and coverage** (`scripts/check_hde.py`; Fractions). Quoted E3 bounds (stage report l. 31; HD-E RESULT l. 51-55)
against the record's exact rationals; E1/E2 coverage recomputed.
`$ /usr/bin/python3 -I check_hde.py [repository]`
""")
parts.append(block(rd(S / "check_hde.out")))
parts.append("""
E2's "≈" column against the exact bounds (inline, Fractions): 6 of 13 quoted values exceed the exact bound — 9-5 (3.59·10⁴ >
35853.84…), 10-3 (136 > 135.9596…; exact 1380839923/10156250), 10-4 (1.17·10⁴ > 11674.20…), 10-5 (2.72·10⁴ > 27162.68…), 11-5
(4.44·10⁴ > 44357.87…), 11-6 (1.02·10⁵ > 101870.59…). The other seven are below.

**C4. Möbius bracket and the HD-S records** (`scripts/check_mobius_and_records.py`; sympy). (1) s^{2e}·[(1−z)f_zP + f(−P +
(1−z)P_z + P²)] with P = g/s^e, s = z + δ, minus `scert.py` l. 176-179's `br`, for arbitrary g, f, f_z. (2) Scan of the 34 records.
`$ [python-2]/bin/python -I check_mobius_and_records.py [repository]`
(the `repro-equal False` entries mask only `timing`/`provenance`; C5 shows they are equal under `compare_runs.py`'s keys)
""")
parts.append(block(rd(S / "check_mobius_and_records.out")))
parts.append("""
**C5. Record = reproduction under `compare_runs.py`'s MASK_KEYS** (`scripts/jsondiff.py`, masking timing, host, platform,
git_commit, t_backward_s, t_total_s, t_design_s, t_verify_s).
""")
parts.append(block(rd(OUT / "repro_equality.out")))
parts.append("""
**C6. TD-S2's counterexamples sit at (0, μ_a)** (rationals elided).
""")
parts.append(block(rd(OUT / "tds2.out")))
parts.append("""
**C7. The pilot: VOID against VALID** (`scripts/jsondiff.py`; `diff`), and the code diff and commit order (`git`).
""")
parts.append(block(rd(OUT / "pilot_void_vs_valid.out")))
parts.append(block(rd(OUT / "pilot_git.out")))
parts.append("""
Pilot table at rung 99/100 (against `pilot/RESULT.md` l. 35-52; all match to the digits quoted; note min ψ₁ 0.48694… at
D = 11 ℓ = 2 and min δ_t 0.2472… at q = 99/100):
""")
parts.append(block(rd(OUT / "pilot_table.out")))
parts.append("""
δ_t at q = 99/100 to 20 digits and the E3 rationals, from an inline `[python-2]/bin/python -I -c` (mpmath, 30 digits;
the min ψ₁ value is the record's float):
`D=11 l=2 min psi1 (float repr): 0.48694055384768814`; `delta_t at q=99/100: 2w/(1+w) = 0.24725509600379317264`;
`19870/6561 = 3.0285017527815881725 ; 17257/2401 = 7.1874219075385256143 ; 399917/10368 = 38.572241512345679012`.

**C8. Blind-seat and bh-modes decimals for D = 7 ℓ = 2** (`scripts/blind_decimals.py`; Fractions, integer square roots, floor).
`$ /usr/bin/python3 -I blind_decimals.py`
""")
parts.append(block(rd(S / "blind_decimals.out")))
parts.append("""
**C9. A2: METHOD's N at the degenerate horizon, q = 1** (`scripts/a2_throat.py`; sympy). P = a/z + b₀ + b₁z + b₂z² (n = 4) or
a/z + b₀ + b₁z (general n); N = U − 64H²[(1−z)f_zP + f(−P + (1−z)P_z + P²)], f = (1 − (1−z)^{n−1})², x = 2(1−z)^{n−1},
δ = 1/((ℓ+n)(n+1)), m = (ℓ−1)(ℓ+n). The D = 6 run uses `TARGET.md` §1's U₋, H₋; the n = 4…9 runs use `potentials.U_minus`.
`$ [python-2]/bin/python -I a2_throat.py`
""")
parts.append(block(rd(S / "a2_throat.out")))
parts.append("""
**C10. A2: the horizon bound as q → 1 at D = 6, ℓ = 2, and the q = 1 identity at n = 2, 3** (`scripts/a2_horizon_bound.py`,
`scripts/hb_exact.py`, `scripts/hb_digits.py`; sympy; floats printed by `%g` are rounded, the exact values follow).
`$ [python-2]/bin/python -I a2_horizon_bound.py`
""")
parts.append(block(rd(S / "a2_horizon_bound.out")))
parts.append("`$ [python-2]/bin/python -I hb_exact.py`\n")
parts.append(block(rd(S / "hb_exact.out")))
parts.append("`$ [python-2]/bin/python -I hb_digits.py`\n")
parts.append(block(rd(S / "hb_digits.out")))
parts.append("""
## D. Records and logs read programmatically (SHA-256)

HD-E and the pilot:
""")
parts.append(block(rd(S / "hashes_hde_pilot_records.txt")))
parts.append("HD-S (`results/hd/s/runs/`, record and repro-host-2; 34 result.json, 34 run.log, 18 planning.jsonl each):\n")
parts.append(block(rd(S / "hashes_hds_records.txt")))
parts.append("""
## E. My scripts and outputs (SHA-256; paths relative to the working folder)

""")
own = rd(S / "hashes_scratch.txt")
parts.append(block(own))
parts.append("The files `my_mem3_test.out`, `tx_scan.out` and the many other files in the working folder are not mine (the folder is\n"
             "shared with the parent session); nothing here depends on them.\n")
(O / "CHECKS.md").write_text("".join(parts), encoding="utf-8")
print("written", O / "CHECKS.md")
