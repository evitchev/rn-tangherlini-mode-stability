# The session-R lead's check of Fable's assembly audit (2026-11-13, written 12:29 EST)

- **Filing:**
  - Snapshot of this folder at 12:28:07 EST, taken before reading (lead copy: [session-R-folder]/bhm_fable_assembly_snap_122807/).
  - AUDIT.md sha256 `717df536…` and SHA256SUMS `4c9cda39…`, as Fable reported. SHA256SUMS: 3/3 OK. Nothing is unlisted except
    STATE.md, STATE_LOG.md and MESSAGES.md, which Fable declares as live files.
  - The brief copy in this folder has sha256 `b71e1349…`, the sealed brief's hash from the cover. AUDIT.md quotes it and the frozen
    draft's `4441e48a…`; the draft still has that hash.
  - Fable reports no process run, the allow-list kept (every audits/ and reviews/ folder pruned), Kimi's composition audits not
    seen and SEALED.sha256 not opened. The folder holds no code, logs or outputs that would say otherwise.
  - Fable's SHA256SUMS is untouched; this note is covered by SHA256SUMS_LEAD.
- **Independence from my reading.** My READING.md (603c61c1, [deliveries]/ib_lead_reading_assembly_2026-11-13/) was sealed
  at 12:08 EST, before this folder was opened. It sat under [deliveries]/, which the brief bars to Fable, and Fable reports
  no reviews/ folder opened. The two reads agree where they overlap: T3's provenance (Fable's R6), the decimals (Fable's §6 items 2-4),
  E1's sliver above 99/100 (R9) and the L² clause (R7). Each found points the other did not:
  - only Fable: l.154's "≈ 54.86" (inward 54.85) and §4.5's chart cover;
  - only my reading: Theorem 1's double label (RULES.md A3), and "the interior band" left undefined.
- **Spot checks against the records (read with jq/Python, nothing re-run):**
  - D = 6: P1's `part1[].mu_lo` and A2-E's `parts[].mu_lo` are identical for ℓ = 3-10 (11/100 … 43/500), with `covers_q_max`
    true in all eight. Lemma U's `part2` has ell0 = 10 and bound 959747/17496 = 54.8552…, so 54.85 is the inward value (Fable's §6.1).
  - D = 7-11, HD-S: the 18 band records are all VERIFIED, with "q(mu_a) >= q_max" and "q(mu_b) <= q_lo or mu_b = 1" true in all
    18. μ_b = 1 exactly for 8-2, 9-2, 10-2, 11-2 and 11-3 (the five from 0⁺); the other 13 have an onset.
  - HD-E: E1 has 35 entries and E2 13, all with covers true; E3's l0 = 10, 10, 11, 13, 14; L_EL = 4, 5, 6, 6, 7.
  - HD-X-E: MEET has 33 entries, with `equal` and `meets` true in all.
  - The four tightest cross-multiplications (8-4, 10-5, 11-5, 11-6: q(μ_b)² ≤ q_split²) recomputed exactly: all hold, with margins
    of 3·10⁻⁶ to 2·10⁻⁵.
  - §6.5: results/a2/s/PREREG.md l.45 and results/hdx/s/PREREG.md l.39 state the cover on (0, 1) × [0, μ₁], as Fable says.
  - Earlier today, for HD-X-2: the nine q(MU1)², with 46562824/47513449 the largest, and the D = 6 ends against O1, T3 and A2-S.
- **Read, not re-checked:** the remaining rows of the per-D tables (the HD-S μ_a/μ_b values and decimals beyond the four tightest
  comparisons), item 4's routes table against each piece's claim text, and item 5's H² argument (which agrees with my reading's
  finding 6).
- **For the record:** seat time 12:05:40-12:28:00 EST (STATE_LOG.md, from `date`), about 22 minutes of the three-hour box; items 1-3
  first.
- **Scope:** a pencil audit, with no computation. Its verdicts are conditional on Fable's §8 hypotheses: the certified pieces as
  recorded, the pencil steps inside the routes with their listed audits, S5's transcription, the shared parametrisation w = Bμ/A,
  and q_max = 99/100. The differences of §6 and the remarks R6-R10 are wording or disclosure; none is a fix to the logic. No
  registered verdict changes.
