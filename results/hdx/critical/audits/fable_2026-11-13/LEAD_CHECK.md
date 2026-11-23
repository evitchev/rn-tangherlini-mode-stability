# The session-R lead's check of Fable's HD-X-2 pencil audit (2026-11-13, written 11:53 EST)

- **Filing:**
  - Snapshot of this folder at 11:51:53 EST, taken before reading (lead copy: [session-R-folder]/bhm_fable_hdx2_snap_115153/).
  - AUDIT.md sha256 `65d8b178…` and SHA256SUMS `1c7dd69a…`, as Fable reported. SHA256SUMS: 3/3 OK. Nothing is unlisted except
    STATE.md, STATE_LOG.md and MESSAGES.md, which Fable declares as live files; after the snapshot only MESSAGES.md and STATE_LOG.md
    changed (one line each, the message's msg_id).
  - The brief copy in this folder has sha256 `243c712f…`, the sealed brief's hash from the cover, and AUDIT.md quotes it.
  - Fable reports no process run, the allow-list kept, Kimi's audit not seen and SEALED.sha256 not opened. The folder holds no code,
    logs or outputs that would say otherwise.
  - Fable's SHA256SUMS is untouched; this note is covered by SHA256SUMS_LEAD.
- **Spot check of item 3 (COVER) against the code.** `code/hdx/critical.py` (sha256 `65792c1b…`) l.96-99: Z1 = 1/4, ZT = 8,
  SIG1 = 1/8, MUT = 1/32, MU1 ∈ {1/8, 13/100, 3/25}; l.450-452 check ZT·SIG1 ≥ 1, ZT·MUT ≤ Z1, Z1·SIG1 ≤ MU1, 0 < MUT < MU1 and
  0 < Z1 < 1, as AUDIT.md §3 and remark R1 say.
- **Spot check of item 5's numbers, recomputed exactly** from `param_n` (`code/hd/elementary.py` l.70-78, `b77e9215…`,
  transcribed): q(MU1)² for the nine bands equals PREREG.md's table (l.104-117) and is ≤ (99/100)² in each; the largest is
  46562824/47513449 ≈ 0.979993, at D = 10, ℓ = 3; w(1) = 1, and w′ = B((ℓ + n) − (ℓ − 1)μ²)/A² > 0 on [0, 1] in all nine.
  Q_MAX = 99/100 is at `code/hd/scert.py` l.51, and TARGET_HD_ADDENDUM_2 l.5-6 reads as quoted.
- **Spot check of §6's algebra (information in the audit):** m + n(n + 2)/4 = ν(ν + 1) with ν = ℓ + n/2 − 1 (the table's ν); the THROAT
  bracket has ζ² coefficient 0, and its ζ and constant coefficients are those printed; with R(0) = k it equals the registered
  k²R(0)²w′(0)²β exactly; the nine ε̂ are the window midpoints (1/k + 2/(k − ℓ))/2. Lead script and output: [session-R-folder]/
  bhm_fable_hdx2_check/spot_check.py (`f2df9be1…`) and spot_check.out (`48386c12…`).
- **Spot check of item 4's hypothesis list.** `prop3_Dn` (BHModesP3.lean, `2d892dcb…`, l.638-645) takes n ≥ 2, q² ≤ 1, m > 0, δ ≥ 0,
  P with derivative P′ on (0, 1) and P′ continuous there, R′ = Fn(zc(R)), R > 1, and N ≥ 0 on (0, 1), as AUDIT.md §4 lists them.
- **Read, not re-derived:** items 1 and 2 (the identity NL = N S²R²L, the exponent bookkeeping of the divisions and the edge table) and
  the tortoise-map step of item 4.
- **For the record:** seat time 11:30:59-11:51:45 EST (AUDIT.md §10 and STATE_LOG.md, from `date`; the message's "about 11:52" is the
  same end), about 21 minutes of the two-hour box.
- **Scope:** a pencil audit, with no computation. Its verdicts are conditional on Fable's §8 hypotheses: the certified gates and charts
  passed (their outcomes are in files barred to Fable), S5's transcription, the Lean statements as read, the q < 1 tortoise map, and,
  for item 5, Theorem HD on (0, 99/100], Z, HD-X-E, HD-X-S and Lemma U(n). The remarks R1-R5 are wording; none is a fix. No registered
  verdict changes.
