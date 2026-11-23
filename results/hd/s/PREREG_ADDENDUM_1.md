# HD-S, PREREG addendum 1: controls on the Möbius branch, and an identity check of every certificate

*Item BHM-088. 2026-10-23, the bh-modes lead. Registered **after** HD-S's run of record (BHM-078) and **before** these
checks run.*
- *It answers the session-R lead's reading (BHM-085, §1.4): no control of record touched the e > 0 branch,
  the ζ-designs.*
- *`PREREG.md` is sealed and unchanged. No certificate is re-made; these checks act on the sealed records.*
- *Sealed.*

## X1: the controls on the three ζ-bands

The controls `td-horizon` and `nc-bound` of `PREREG.md` §4, run with `hd.scert` at this commit (its code is unchanged
since `0aa2673`) on D = 9 ℓ = 5, D = 10 ℓ = 5 and D = 11 ℓ = 6, whose designs are in ζ.

**Registered verdicts:** `REJECT: td-horizon` and `REJECT: nc-bound (b)`, for each band. Why each must give it:
- **td-horizon.** The tamper adds c(1 − z)s^e to P̂, i.e. c(1 − z) to P, with c set so that P(0) is 1/10 above
  W(0)/f_z(0) at μ_a. Then N(0, μ_a) = −64H₋²f_z(0)/10 < 0 at a corner of the first box, and the verifier's
  corner check refuses it.
- **nc-bound.** K = ⌈2I₁/I₂⌉ gives the trial function b the energy I₁ − KI₂ ≤ −I₁ < 0, certified in Arb (part (a)).
  So no N ≥ 0 can exist for the planted potential, since Proposition 3 would then give A ≥ 0 against that energy.
  The certificate's check on the bump must therefore fail (part (b)).

## X2: the identity check (`code/hd/scheck.py`)

**What is compared.** For every verified box of each band's sealed record (its SHA-256 checked against
`SEALED.sha256`), at 8 seeded random rational points (z, μ) in [0, 1] × box, with denominators 2³⁰, exactly:
- **LHS:** the certificate's N·L·s^{2e}, rebuilt from the stored P̂ by `hd.scert.Exact`, which is the verified
  pipeline, divided by L·s^{2e}.
- **RHS:** N computed directly:
  - U₋ and H₋ of `ki.potentials` at (m, δ(μ), x), with x = x_H(1 − z)^{n−1};
  - f = 1 − x + q²x²/4 with q² = 1 − w(μ)², rather than the factored f of `hd.scert`, and f_z by the chain rule;
  - P = P̂/s^e, with P_z by the quotient rule.

**What it tests.** Together, it tests `hd.scert`'s assembly of U, H and f and its N·L·s^{2e} algebra, in both branches.
By Schwartz–Zippel, a wrong polynomial of these degrees agrees at 8 random points of this size with probability below
10⁻⁴⁰.

**Registered verdict:** `VERIFIED` for each of the 18 bands, i.e. agreement at 8/8 points in every box.

**Drill TD-X2** (`--control td-direct`, on D = 7 ℓ = 2, a z-band, and on D = 11 ℓ = 6, a ζ-band). The RHS uses
U₋ + 16nm². It must give `REJECT: X2`.

## Pass criterion, and what follows

- **VERIFIED requires:** every X1 control and the TD-X2 drill with its registered verdict, and X2 `VERIFIED` in all 18
  bands.
- **Record and reproduction:** the record on host-1 and the reproduction on host-2, from a `git archive` of this
  commit (`kit/hd/run_s_check.sh`), with identical verdicts.
- **On VERIFIED:** the Möbius branch has its controls, and every stored certificate polynomial is confirmed against a
  second route. HD-S's status is unchanged otherwise.
- **On a failure of X2 in a band:** that band's S(D, ℓ) is suspended, reported as it stands, and investigated.
- **On a failure of an X1 control:** it is reported. Since the certificates are exact, a failure would mean the
  control's mechanism, not a certificate, is wrong; the record shows which.

## What ran before this registration

- **Development, on host-1,** from a `git archive` of `8d60596`:
  - syntax checks;
  - `python -m hd.devtest_scheck`, synthetic inputs only: U = 64m³ + 400x² + x⁴ and H = m + 15x at (n, ℓ) = (5, 4), one
    box in z and one in ζ at degree 16;
  - the outcomes: the identity at 8/8 points in both branches, and 0/8 with the direct route tampered.
- **Not run:** no sealed record was read by `hd.scheck`, and S5's U₋ was not evaluated.
