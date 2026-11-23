# PREREG — my audit of bh-modes HD-E, D = 7–11 (BHM-063)

*Auditor: Kimi. 2026-10-23.*

Brief: `results/hd/elementary/briefs/BRIEF_kimi_2026-10-23.md`, SHA-256
`999576eb7dfe64713ad0ea2972de84d032b44128904cb04d5cb867bd6494307c` (verified against
`SEALED.sha256`; the brief's artifact and code hashes all verified).

## Anti-anchoring

Before opening `results/hd/elementary/RESULT.md`, `results/hd/elementary/runs/`, anything else
under `results/hd/` (including HD-PILOT and HD-S), `TARGET_HD_ADDENDUM_*`, `REGISTRY.md` rows
>= BHM-063, the lead's commit messages, `outbox/`, `lean/`, `results/*/audits/` (my archived
`build.py` excepted), `[deliveries]/` or `[session-R-folder]/`, I will have on disk:

1. my own per-(n, ell) exact F/Den builds from my own general-n KI (5.62b)/(5.63b)
   transcription (p3 audit, BHM-036), with parametrisation identities and w increasing checked
   exactly, mu_lo = k/10000 with exact coverage;
2. my own E1 proofs (ell_el .. my own l0(n)) and E2 proofs (13 bands) with my own exact
   Bernstein verifier;
3. my own Lemma U(n) derivations with l0(n) = 10, 10, 11, 13, 14 for n = 5..9 (already
   computed before this PREREG was written; the values stand);
4. controls: (a) D = 7, ell = 2 to 951/1000 must REJECT at the horizon corner; (b) D = 10,
   ell = 3 to 99/200 must REJECT at an interior point; (c) a planted bump must REJECT;
   (d) verifier tamper caught by the KATs;
5. the reproduction of `kit/hd/run_elementary.sh` at `6fe9689` on host-1 or host-2.

## Note on the verifier (recorded honestly)

Development revealed a defect in my own verifier's box substitution (`hz**i` for `hz**k`),
caught by control (b) of this very brief (an interior counterexample the verifier initially
failed to see). The fix is in place, with new coefficient-level KATs (KAT6–KAT8) that fail
under the old code. Every result quoted in my audits that used the verifier has been
re-produced with the fixed code before this audit's own checks were considered complete. See
the HD-E AUDIT.md for the full account.

## Hosts and verdict rule

Runs of record: host-1 (own suite) and host-2 (kit reproduction), `nice -n 19`, the pinned
`[venv]`. Each of E1 (per D), E2 (per band), E3 (per n) passes only on my own exact
computation; failures are reported with exact counterexamples. Overall PASS additionally
requires the kit reproduction green.
