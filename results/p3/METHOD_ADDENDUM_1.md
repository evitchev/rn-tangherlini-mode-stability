# p3 METHOD addendum 1 (after Fable's audit)

*Item BHM-054. 2026-10-23, the bh-modes lead.*
- **What this is.** It answers points (1), (2) and (4) of Fable's audit (BHM-042,
  `results/p3/audits/fable_2026-10-22/AUDIT.md`), as the operator ruled (BHM-046). `METHOD.md` is
  sealed and unchanged.
- **The other points.** Point (3), `onset.bernstein.Q` refusing floats, is in the code from P1's
  version on (BHM-047, `code/onset/bernstein.py`); the certified records were made with the
  earlier code, in which no float reaches `Q` on the trust path. Point (5), the Lean README's
  wording, goes to session-L.
- **What does not change.** No claim and no proof changes.
- **Status of METHOD.md:** proved (pencil; **audited 2×**, by Kimi and by Fable). Lemmas 1–2 and
  Proposition 3 are also machine-checked in Lean (BHM-030). Sealed.

## 1. Lemma 2: why r* ↦ r is a diffeomorphism (Fable's point 1)

- **The map is monotone and smooth.** f = (1 − x/x_H)(1 − x/x₋) with 0 < x < x_H ≤ x₋ on the
  exterior, so f > 0 on (1, ∞). Hence r*(ρ) = ∫dρ/f is C^∞ and strictly increasing, with a C^∞
  inverse (its derivative f is > 0).
- **It is onto ℝ.**
  - At the horizon, f(1) = 0. For q < 1 the zero is simple, f_z(0) = 3(1 − κ³) > 0, so r* → −∞
    like log(ρ − 1). For q = 1 it is double, and r* → −∞ like −1/(ρ − 1).
  - At infinity, f → 1, so r* → +∞.
- So r* ↦ ρ is a C^∞ diffeomorphism ℝ → (1, ∞) for every q ∈ [0, 1].

## 2. The remark "Why such P exist" (Fable's point 2)

The identity is correct:

  ρ²(Ṽ/f) = ε[ρf′ + f(2P_true − 1 − ε)],  with ρf′ = (1 − z)f_z,

when N(P_true) = 0. But its sign is that of the bracket (1 − z)f_z + f(2P_true − 1), which can be
negative where ψ₁ decreases (P_true < 0). The sentence "> 0 for small ε where ψ₁ > 0" is replaced by:
- the remark gives slack where that bracket is positive;
- the planning data show this for D = 6's band, and `PREREG_ADDENDUM_1.md`'s diagnosis refutes it
  for G1 (the bracket reaches −1.288 there, and stays ≥ 0.992 for T1);
- design rule 2 removes the dependence.

The remark is heuristic and not load-bearing: the design step is untrusted by registration.

## 3. Trust base: the transcription of S5 (Fable's point 4)

- **The addition.** The trust base includes S5's (5.59)–(5.63), as transcribed in
  `code/ki/potentials.py` and `TARGET.md` §1. The certificates also inherit S5's reduction to the
  master equation (`TARGET.md`'s physical reading, *cited*).
- **E0's limit.** E0 compares two transcriptions by the same hand. It catches a discrepancy between
  them (TD-P1 shows it does), but not an error common to both.
- **The independent checks** now cover that gap:
  - Kimi's own transcription of (5.62b) and (5.63b) from the rendered PDF agrees symbolically (BHM-036);
  - session-L's comparison with the potential printed in 1001.0019 agrees term by term (BHM-031).
