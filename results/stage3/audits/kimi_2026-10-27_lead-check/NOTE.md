# The lead's spot check of Kimi's HD-X audit (BHM-160)

*2026-10-27, the bh-modes lead. A check of a delivery, not a registered result.*

- **What:** `lead_check_hdx_e.py` recomputes three numbers of Kimi's controls with our registered HD-X-2 code
  (`code/hdx/critical.py` `8a7b041e19c906fd`, at `6cedd44`), not with Kimi's:
  - (e), band D = 7, ℓ = 2 at μ = 1/64, on Kimi's support [209/10000, 837/10000]:
    - C = ∫b³ dz exactly;
    - U₋ < 0 on the support, exactly;
    - A = Q[b] and Q = A − K·C in Arb (256 bits), with nc-bound's integrand in z and Kimi's K = 297809182;
  - (a): U₋(x_H) and H₋(x_H) at q = 1, D = 7, ℓ = 3.
- **Where:** host-2, 2026-10-27 19:34:25–19:34:26 UTC, `nice -n 19`, `[venv]` (`python -I`, `ulimit -v`
  8 GB). It ran from `git archive 6cedd44` (tar SHA-256 `249b819a0b15ec1a…`) in `[run-folder]/lead-kimi-hdx-check/`.
  The log is that run's, copied back; both files equal the copies on host-2.
- **Results** (`lead_check_hdx_e.log`):
  - C = (157/2500)¹³/12012 exactly, = 1.96725222445138034180388401060985…·10⁻²⁰;
  - no root of U₋'s numerator in the support, U₋ < 0 at its midpoint, and the first root in (0, 1) lies in
    [144817/1382852, 88518/845255];
  - A = [2.92932886965557454329071664560e-12 ± 2.14e-42] and Q = [−2.92932888785988524034423437062e-12 ± 3.86e-42],
    each containing Kimi's logged ball: Kimi's midpoints lie 2.132·10⁻⁴² and 3.857·10⁻⁴² from ours, inside our radii
    2.14·10⁻⁴² and 3.86·10⁻⁴², and its own radii are below 10⁻¹⁰⁰;
  - U₋(x_H) = −602112 and H₋(x_H) = 56, so Kimi's F(1, 0) = −4816896 is 8·U₋(x_H).
