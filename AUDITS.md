# Independent checks of the proof

The paper's §6 and §9 summarise these checks; this file lists each one with its record in this repository.

**Every check here was made by an AI model.** No mathematician besides the author has checked the argument. The
computations, their code and their records were produced by Claude Opus 5.5 (Anthropic) in the project's own Claude
Code session. The checks were made by other agents, which the records name as follows:

| Name in the records | Who |
|---|---|
| Kimi | Kimi K3 (Moonshot AI). Its last check, of 2026-11-21, ran on Kimi K3.1 Pro. |
| Fable | Claude Fable 5.1 (Anthropic). |
| session-L | A separate Claude Opus 5.5 session. It wrote and checked the Lean formalisations, re-ran T3's certificate with its own code, and checked the citations. |
| session-R ("the IB lead"; folders `ib-…`) | Another Claude Opus 5.5 session. It read the assembly of each part, and a Claude Opus 5.5 subagent of it made the blind replication. |
| the cold reader | A Claude Fable 5.2 session. It read the paper as an outside referee would, and checked its appendices against their sources. |

A *check* here re-derives a computation with independently written code, or reads a proof and reports on each step.
Where a record says "audit", "second party", "pencil" or "certified", these are the project's working words for
check, independent check, by hand and verified by exact computation.

## 1. The computations

Each piece of Table 1 was also re-run on a second computer from a clean archive (§6), and the reproduction package
re-runs it again (`kit/stability/`). Independently of that:

| Piece | Independent check | Record |
|---|---|---|
| O1, O2 | Kimi re-derived the onset certificate with its own code, including its own corner argument for O2. O2 is also proved in Lean. | `results/onset/audits/kimi_2026-10-22/`; `lean/lean_onset_2026-10-22/` |
| T3 (with T1 and T2) | Kimi re-verified the six ℓ = 2 certificates from the stored designs; the project re-ran Kimi's cross-check. session-L re-ran T3's certificate in exact arithmetic with its own code. | `results/p3/audits/kimi_2026-10-22/`; `results/p3/audits/recheck_2026-10-22/`; `results/p3/audits/session-L_T3_registration_2026-10-22/` and `session-L_T3_rerun_2026-10-23/` |
| P1 and Lemma U(4) | Kimi, with its own code. Lemma U at n = 4 is also proved in Lean. | `results/a1/audits/kimi_2026-10-23/`; `lean/lean_lemmaU_2026-10-23/` |
| A2-E and A2-S | Kimi, with its own code. A2-S's check G-RES is also proved in Lean. Kimi also checked the early extremal checks of A2. | `results/a2/audits/kimi_2026-10-25/`; `results/a2/extremal/audits/kimi_2026-10-22/`; `lean/lean_p3_sdeformation_v4_2026-10-24/` |
| HD-E (E1–E3) | Kimi, with its own code. | `results/hd/elementary/audits/kimi_2026-10-23/` |
| HD-S (18 bands) | Kimi, with its own code. The first band of D = 7 was also replicated blind, from the replicator's own transcription of Kodama–Ishibashi, without our code; it reached the same result. | `results/hd/s/audits/kimi_2026-10-23/`; `results/hd/s/audits/ib-blind_2026-10-23/` |
| HD-X-E, HD-X-S, HD-X-2 | Kimi, with its own code (its checks (a)–(c)), and the project's check of that delivery. | `results/stage3/audits/kimi_2026-10-27/`; `results/stage3/audits/kimi_2026-10-27_lead-check/` |
| Z (q = 1) | Lean, end to end: Theorem 2's identities, u₀ > 0, and the tortoise coordinate at q = 1. | `lean/lean_z_2026-10-26/`; `lean/lean_z_d_2026-10-26/` |
| U₋'s transcription (Appendix A) | Kimi's own transcription of Kodama–Ishibashi's (5.62b) and (5.63b) agrees symbolically with the code's; HD-E's check E0n compares them for n = 2, …, 12. At n = 4, Lean proves its own transcription equal to the code's. | `results/p3/audits/kimi_2026-10-22/`; `results/hd/elementary/PREREG.md` (E0n); `lean/lean_a1_2026-10-22/` |

## 2. The proofs by hand

| Step (paper) | Checks | Record |
|---|---|---|
| Lemmas 1–2 and Proposition 3 at n = 4 (§4.1, Appendix B.1) | Kimi; Fable. Also proved in Lean. | `results/p3/audits/kimi_2026-10-22/`; `results/p3/audits/fable_2026-10-22/`; `lean/lean_p3_sdeformation_2026-10-22/` |
| Proposition 3 at every n, for P C¹ on (0, 1) (§4.1) | Proved in Lean, with the inverse of the tortoise coordinate as a hypothesis; Fable. | `lean/lean_p3_sdeformation_v2_2026-10-23/`, `lean/lean_p3_sdeformation_v3_2026-10-23/`; `results/stage3/audits/fable_2026-10-26/` |
| The tortoise coordinate for q < 1 (Appendix B.2) | Fable; Kimi. | `results/stage3/audits/fable_2026-10-26/`; `results/stage3/audits/kimi_2026-10-27/` |
| The tortoise coordinate at q = 1 | Proved in Lean for every n; Kimi at n = 4. | `lean/lean_z_d_2026-10-26/`; `results/a2/audits/kimi_2026-10-25/` |
| Lemma U, steps (a)–(d) (§4.3, Appendix B.3) | Kimi at n = 4 and at n = 5–9; Fable at every n. The whole lemma is proved in Lean at n = 4. | `results/a1/audits/kimi_2026-10-23/`; `results/hd/elementary/audits/kimi_2026-10-23/`; `results/stage3/audits/fable_2026-10-26/`; `lean/lean_lemmaU_2026-10-23/` |
| HD-S's reduction, with the designs in η (§4.1) | Kimi; Fable. The algebra is also in Lean. | `results/hd/s/audits/kimi_2026-10-23/`; `results/stage3/audits/fable_2026-10-26/`; `lean/lean_p3_sdeformation_v3_2026-10-23/` |
| The singular designs' reduction and the chart cover, for A2-S and HD-X-S (§4.5) | Kimi at n = 4 and at every n; Fable. | `results/a2/audits/kimi_2026-10-25/`; `results/stage3/audits/kimi_2026-10-27/`; `results/stage3/audits/fable_2026-10-26/` |
| HD-X-2's reduction, cover and charge argument (§4.6, Appendix B.4) | Kimi; Fable, who derived the identity NL = N·S_ε²R²L and made the cover's conditions explicit. | `results/stage3/audits/kimi_2026-10-27/`; `results/hdx/critical/audits/fable_2026-11-13/` |

## 3. The assembly (§5)

| Part | Checks | Record |
|---|---|---|
| A1 | A reading by session-R; Fable, within the paper's assembly; Kimi, a second check. | `results/a1/reviews/ib-lead_reading_2026-10-23/`; `paper/stability/audits/fable_assembly_2026-11-13/`; `paper/stability/audits/kimi_assembly_2026-11-21/` |
| A2 | Kimi, with the range ends compared exactly; Fable; a reading by session-R. | `results/a2/audits/kimi_2026-10-25/`; `paper/stability/audits/fable_assembly_2026-11-13/`; `results/a2/reviews/ib-lead_reading_2026-10-24/` |
| HD | A reading by session-R; Fable; Kimi, a second check. | `results/hd/reviews/ib-lead_reading_2026-10-23/`; `paper/stability/audits/fable_assembly_2026-11-13/`; `paper/stability/audits/kimi_assembly_2026-11-21/` |
| HD-X | Kimi, with the range ends compared exactly; Fable; a reading by session-R. | `results/stage3/audits/kimi_2026-10-27/`; `paper/stability/audits/fable_assembly_2026-11-13/`; `results/stage3/reviews/ib-lead_reading_2026-10-26/` |
| §5 as a whole | Fable's check of an earlier draft: all five points sound. A reading by session-R: no gap. | `paper/stability/audits/fable_assembly_2026-11-13/`; `paper/stability/reviews/ib-lead_reading_2026-11-13/` |

## 4. The paper's text

| What | Check | Record |
|---|---|---|
| The citations | session-L checked each citation at its anchor: the references new in an earlier draft, then every citation of the posted text, with any fix made before posting. Its copies of the cited papers are not published. | `literature/stability-v04-citecheck-2026-11-18/` and `literature/stability-v08-citecheck-2026-11-23/` (reports and ledgers) |
| §§1, 4 and 7 of an earlier draft | Fable. | `paper/stability/audits/fable_v04_delta_2026-11-18/` |
| The language and notation | The cold reader, from the PDF alone. | `paper/stability/audits/cold_read_2026-11-22/COLD_READ.md` |
| Appendices A–B and the new statements | The cold reader, against their sources: no difference, no error. | `paper/stability/audits/appendix_check_2026-11-22/CHECK.md` |

The records quote the draft versions they checked, which are not published. Their hashes are in the records.
