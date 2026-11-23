# D = 7–11 stage report, addendum 2: second parties complete

*Item BHM-112. 2026-10-24, the bh-modes lead. `STAGE_REPORT.md` (BHM-079) and `STAGE_REPORT_ADDENDUM_1.md` (BHM-087)
are sealed and unchanged. This addendum replaces the report's status table with today's second parties. No certificate
and no claim changes. Sealed.*

Theorem HD reads as in addendum 1: for D = 7, 8, 9, 10, 11, every integer ℓ ≥ 2 and every q ∈ (0, 99/100], the master
equation for Φ₋ has no mode e^{κt}φ(r*) with κ > 0 and φ ∈ L²(ℝ, dr*).

## Status (replaces `STAGE_REPORT.md`, "Status, and what is pencil-only")

| Claim | Label | Second party |
|---|---|---|
| HD-E E1, E2 | *certified* (exact) | Kimi, by its own exact route and the kit's reproduction (BHM-109) |
| HD-E E3, Lemma U(n), n = 5…9 | *certified* (exact), with the inward bounds of BHM-084; steps (a)–(d) proved (pencil; audited 1×) | Kimi: its own ℓ₀(n) and corner bounds, equal to ours; steps (a)–(d) all SOUND (BHM-109) |
| HD-S, all 18 bands | *certified* (exact) | Kimi: all 231 boxes by its own exact route, with exact coverage, and the kit's reproduction (BHM-110); the blind replication of D = 7 ℓ = 2 (BHM-083) |
| HD-S's reduction | at n = 4 for a polynomial P: proved (pencil; audited 2×; Lean). Its extension to n = 5…9 and to the ζ-design: proved (pencil; audited 1×) and machine-checked (Lean, BHM-091), with R's existence pencil | Kimi: both extensions SOUND (BHM-110) |
| Theorem HD | *certified*, resting on the rows above | **complete**: every row has its second party |

**What is still pencil only.** The existence of R, the inverse tortoise map, as at n = 4 (`results/p3/METHOD_ADDENDUM_1.md`
§1, `METHOD_ADDENDUM_2.md` step 2). Lean takes it as a hypothesis (BHM-091); Kimi's general-n verdict covers it.

**Cited, not reproved,** as in the report: S5's reduction of the perturbation equations to the master equations, and S5's
results for the other sectors.

## Notes from the second parties

- **Kimi's verifier.** Kimi's own Bernstein verifier had a defect in its earlier audits (p3, the onset, A1). Its HD-E
  control (b) exposed the defect, and Kimi fixed it. Kimi then re-produced those audits' verdicts, and none changed
  (BHM-111). Kimi's HD-E and HD-S verdicts come from the fixed verifier.
- **Corrections to Kimi's write-ups,** none affecting a verdict (BHM-109, BHM-110):
  - HD-S control (a)(i): the printed trial energy is not that of its planted bump. The exact REJECT of (a)(ii) stands.
  - HD-S's builder cross-check: AUDIT.md cites a log that was not delivered, and a ζ-design case that the script
    does not contain. Our own check of every certificate against a direct N is unaffected (BHM-089: 1848 of 1848
    points, including the 17 ζ-boxes).
  - Two stale or mistyped numbers.
- **Hosts.** Kimi's runs of record went to host-1 (its own checks) and host-2 (the kits). The delivered logs are
  byte-identical to the copies on those nodes.

## Next

As in the report: D = 7–11 beyond q = 0.99 is not in the operator's order. `TARGET_HD.md` §4.1 caps q_max at 0.99, so
going further needs the operator's ruling.
