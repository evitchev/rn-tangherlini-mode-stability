# HD-S RESULT addendum 1: the Möbius branch's controls, and the identity check of every certificate (BHM-089)

*Registered as BHM-088 (`PREREG_ADDENDUM_1.md`). The record ran on host-1 and the reproduction on host-2, from a
`git archive` of `10f1795` with `kit/hd/run_s_check.sh`.*
- *Both kits print KIT PASS.*
- *All 26 records are identical after masking, and the `run.log`s are byte-identical.*
- *The longest job took 29 s.*
- *`RESULT.md` (BHM-078) is sealed and unchanged.*

**VERIFIED as registered.**

## X2: every certificate against a direct evaluation of N

In all 18 bands, every stored certificate's polynomial N·L·s^{2e}, rebuilt by `hd.scert.Exact`, divided by L·s^{2e},
equals N computed directly at every point.
- **The direct route** uses U₋ and H₋ of `ki.potentials`, f = 1 − x + q²x²/4 (not the factored f), and P = P̂/s^e.
- **The points:** 8 seeded random rational points per box, 231 boxes, so **1848 of 1848 points**. That includes the 17
  boxes of the three ζ-bands (D = 9 ℓ = 5, D = 10 ℓ = 5, D = 11 ℓ = 6).
- **What it confirms.** `hd.scert`'s assembly of U, H and f, and its N·L·s^{2e} algebra in both branches, agree with
  the definition. A wrong polynomial passes with probability below 10⁻⁴⁰.
- **The records:** each sealed record's SHA-256 was checked against `SEALED.sha256` before use (gate SEAL).

**Drill TD-X2.** With the direct route's U₋ tampered (+16nm²), 0 of 8 points agree in every box, on D = 7 ℓ = 2 (z) and
on D = 11 ℓ = 6 (ζ). Both give `REJECT: X2`.

## X1: the controls on the three ζ-bands

| Band | nc-bound: K, certified Q[b] (Arb) | nc-bound (b) | td-horizon |
|---|---|---|---|
| D = 9 ℓ = 5 | 441165, −2.93·10⁻⁶ | REJECT | REJECT |
| D = 10 ℓ = 5 | 492496, −3.27·10⁻⁶ | REJECT | REJECT |
| D = 11 ℓ = 6 | 634904, −4.21·10⁻⁶ | REJECT | REJECT |

- The Arb balls' radii are below 10⁻¹⁵.
- td-horizon's rejection comes from the verifier's corner check, with a negative exact value. The record's message is
  cut at 300 characters, before the corner's coordinates, because the ζ-designs' values are long rationals. The
  mechanism, N(0, μ_a) < 0, is registered (`PREREG_ADDENDUM_1.md`, X1).

## Status

- **HD-S:** unchanged, *certified* (exact).
- **The Möbius branch now has controls of record,** and every stored certificate polynomial is confirmed by a second
  route.
- **Pencil only:** the labels of `STAGE_REPORT_ADDENDUM_1.md` stand. Lemma U(n), and Proposition 3's extension
  (`results/p3/METHOD_ADDENDUM_2.md`), are proved (pencil; audited 0×) until Kimi's reports.

## Hashes (SHA-256, first 16 hex)

- Code at `10f1795`: `code/hd/scheck.py` `c610c1448e9a2c77`; `kit/hd/run_s_check.sh` `8a592ce20222b3d2`; `code/hd/scert.py`
  `8a67a9e6d381a6a2`, unchanged since `0aa2673`.
- The records are under `check-runs/record/` and the reproduction under `check-runs/repro-host-2/`; all are listed in
  `SEALED.sha256`.
