# D = 7–11 stage report, addendum 1: corrections from the session-R lead's reading, and the blind result

*Item BHM-087. 2026-10-23, the bh-modes lead. `STAGE_REPORT.md` (BHM-079) is sealed and unchanged. This addendum
corrects it as the reading (BHM-085) asks, and adds the blind replication (BHM-083). No certificate changes. Sealed.*

## The result, restated with its labels (`RULES.md` A3)

> **Theorem HD (certified).** For D = 7, 8, 9, 10, 11, every integer ℓ ≥ 2 and every q ∈ (0, 99/100], the quadratic
> form ∫(|φ′|² + V_{ℓ,q}|φ|²)dr* is ≥ 0 on C₀^∞(ℝ). So there is no κ > 0 and no 0 ≠ φ ∈ L²(ℝ) with
> A_{ℓ,q}φ = −κ²φ: the master equation for Φ₋ has no mode e^{κt}φ(r*) with κ > 0.

**What it rests on beyond exact computation.** Two pencil steps, neither yet audited:
- Lemma U(n)'s steps (a)–(d) at n = 5…9 (proved, pencil; audited 0×; Kimi's brief BHM-068);
- Proposition 3's extension to n = 5…9 and to the Möbius design (proved, pencil; audited 0×;
  `results/p3/METHOD_ADDENDUM_2.md`; Kimi's brief BHM-080).

The n = 4 polynomial case of Proposition 3 keeps its labels: audited 2×, and Lean.

## Corrections

1. **The certified E3 bounds.** The report's "m⁻³U₋ ≥ 38.6, 23.6, 7.19, 4.84, 3.03" rounds three of them up. The
   inward values are **38.57, 23.61, 7.187, 4.841, 3.028**; the exact rationals are in
   `results/hd/elementary/RESULT_ADDENDUM_1.md` (BHM-084).
2. **The status of HD-S's reduction.** The report's row "the reduction proved (pencil; audited 2×; Lean, BHM-030)"
   should read: proved (pencil; audited 2×; Lean) at n = 4 for a polynomial P; its extension, proved (pencil;
   audited 0×). The same holds for `results/hd/s/RESULT.md` and REGISTRY rows BHM-076, BHM-078 and BHM-079.
3. **"18 bands in which V has a negative region."** The 18 bands come from the screen, which is *numerical*
   (BHM-014). Exact negative points are certified for three of them only: HD-E's NC-E1 to NC-E3. The theorem does not
   use V's sign.
4. **A scope remark, from the reading's §3(ii)** (checked there on our transcription for n = 2…9; not yet checked
   here). At the zero-margin throats D = 2ℓ + 3, a strict S-certificate of HD-S's type cannot reach q = 1, because its
   best horizon slack is proportional to c_n + 1/4 = 0. The certified range stops at q = 0.99 in any case.
5. **Gates without a planted control.** HD-S's coverage, PILOT and H gates have no control of their own (`RULES.md`
   E.4). For this step the reading's exact recomputation of every interval and of the coverage (§1.1) stands in. From
   A2 on, each gate's registration carries a control.
6. **Planning wording** (untrusted data; `results/hd/pilot/RESULT.md`): "min ψ₁ ≥ 0.49" should be ≥ 0.486 (it is
   0.48694…), and "δ_t ≥ 0.25" should be ≥ 0.247 at q ≤ 0.99 (δ_t(0.99) = 0.24725…).

## The blind replication (BHM-083)

- **The verdict:** the session-R lead's blind seat finds D = 7 ℓ = 2 "holds (certified)" on q ∈ [0.948, 0.99],
  with its own transcription and pipeline. That agrees with S(7, 2). So S(7, 2) has a blind second party.
- **The seat's erratum** (the reading, §1.6). Its E0 range is q ∈ [0.947979, 0.949341] and its Part C range is
  q ∈ [0.949342, 0.990000]. VERDICT.md and REGISTRY row BHM-083 printed the upper ends 0.949342 and 0.990001, which
  are outward. The exact ends are q(2817/10000) = 0.947978589…, q(2780/10000) = 0.949341971… and
  q(1237/10000) = 0.990000611….

## The Möbius branch's controls

No control of record touched the ζ-designs (e > 0): every HD-S control ran on an ℓ = 2 band, all designed in z.
- **What covers it now.** The reading checked symbolically that the e > 0 formula equals s^{2e} times METHOD's
  bracket.
- **What comes next.**
  - Kimi's brief asks for all 231 certificates.
  - A registered run of the controls on the three ζ-bands, with a random-point identity check of every certificate
    against a direct evaluation of N, follows as BHM-088.

## For A2 (the reading's §3; adopted when A2 is registered)

1. **No bounded design reaches q = 1 at ℓ = 2.** At q = 1, N(0) = U₋(x_H) < 0 for every P that is C¹ at z = 0.
2. **A pole carries the margin.** A simple pole P = a/z + p(z) makes N(0) proportional to c(ℓ) − a(a + 1). At a = −1/2
   this is exactly the Breitenlöhner–Freedman margin.
3. **What A2's PREREG needs:**
   - a singular ansatz;
   - a throat chart with q = 1 inside a closed box;
   - a pilot first;
   - controls on the singular branch;
   - the kill criteria K1–K4 of the reading.
