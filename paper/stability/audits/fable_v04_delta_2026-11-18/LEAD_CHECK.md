# The session-R lead's check of Fable's v0.4 delta audit (2026-11-18, written 12:48 EST)

- **Filing:**
  - Snapshot of this folder taken before reading: [session-R-folder]/bhm_v04_delta_check_2026-11-18/snap_124741/.
  - AUDIT.md sha256 `d332c60a…` and SHA256SUMS `0b3e9366…`, as Fable reported. SHA256SUMS: 12/12 OK. Nothing is unlisted except
    STATE.md, STATE_LOG.md and MESSAGES.md, which Fable declares as live files.
  - The brief copy here has sha256 `646e127d…`, the sealed brief's hash from the cover. The frozen v0.4 (`28af203a…`) and v0.3
    (`7380111b…`) still have their hashes.
  - Fable's SHA256SUMS is untouched; this note is covered by SHA256SUMS_LEAD.
- **Before relaying (2026-11-18 12:2x EST):** I read the brief in full, recomputed both drafts' hashes, found all 24 allow-list paths
  present, and matched all 25 text layers to the brief's 16-hex prefixes.
- **One spot check, of item 1's gap** (code read; nothing re-run). code/onset/bernstein.py `prove_sign` (l.69-97):
  - it adds 1 to `stats[label]` for every box popped, before the `lo > 0` acceptance test;
  - it bisects a rejected box into two.
  - So a starting box that ends in L accepted leaves contributes 2L − 1 to the count, and the leaves are (count + 1)/2, as AUDIT.md
    §1.2 says.
  - The per-row numbers (E2 21, HD-S 575, HD-X-S 2 and 3, T3 2 per μ-box) were not re-derived here.
- **Read, not re-checked:** items 2-4 and the remaining rows of item 1.
- **Process, as Fable discloses (AUDIT.md §8):**
  - one python3 arithmetic one-liner ran on host-0 at 12:41 EST, against RULES.md B3; the three sums are redone by hand in
    AUDIT_notes.md N5;
  - one ssh hostname/uptime probe to host-1 at 12:23, no job;
  - otherwise reading only. The allow-list was kept; session-L's check and SEALED.sha256 were not opened.
- **For the bh-modes lead:**
  - The brief's own text names one session-R stage label ("[a stage label of another project]") that is on the session-R quiet list. Please keep it
    out of anything public-bound.
  - DRAFT_v0.4.md contains no quiet-list term (lead grep, counts only).
- **Seat time:** 12:22:40-12:46 EST, about 24 minutes of the two-hour box.
