# Z, pencil addendum 1: the intertwiner at the extremal horizon, in every sector

*Item BHM-148. 2026-10-26, the bh-modes lead.*
- *It answers the GAP-MINOR in item B1 of Fable's second pencil audit (BHM-146,
  `results/stage3/audits/fable_2026-10-26/AUDIT.md` §B1). The step below is Fable's, and the lead re-derived it.*
- *`PREREG.md` §2 ("The intertwiner") and `RESULT.md` are sealed and unchanged.*
- *Status of the intertwiner statement: proved (pencil; audited 1×, by Fable's audit with this step). No claim changes.
  Sealed.*

## The gap

`PREREG.md` §2 shows that w = (log u₀)_{r*} tends to 0 at both ends along the real r*-axis. For Im ω < 0, though, the
ingoing solution e^{−iωr*} dominates on the real axis as r* → −∞. So at the extremal horizon, an irregular singular point
of rank 1, the quasinormal-mode condition is recessiveness in a sector of the complex (ρ − 1)-plane:
arg(ρ − 1) ∈ (arg ω − π, arg ω), with r* ≈ −1/(k²(ρ − 1)) and k = n − 1. A limit along the real axis does not show
that L preserves recessiveness in that sector.

## The step

Units r_H = 1 and q = 1, with Y = ρ^{−k}, f = (1 − Y)² and h = (ℓ − 1) + nY.
1. **w is analytic at ρ = 1, with a simple zero.**
   - w = fg/ρ with g = ρu₀,ρ/u₀ = −ν − ℓY/(1 − Y) + n(n − 1)Y/h.
   - So fg = −ν(1 − Y)² − ℓY(1 − Y) + n(n − 1)Y(1 − Y)²/h. The simple pole of g at Y = 1 is cancelled by the double
     zero of f.
   - h(1) = ℓ + n − 1 ≠ 0. The zeros of h, ρ^k = −n/(ℓ − 1), are off ρ = 1.
   - So fg = −ℓ(1 − Y) + O((1 − Y)²), with 1 − Y = k(ρ − 1) + O((ρ − 1)²). Hence w = −ℓk(ρ − 1) + O((ρ − 1)²) in a
     full neighbourhood of ρ = 1: w = O(ρ − 1) in every direction.
2. **L preserves the recessive solution of each sector.**
   - Let H be the solution of A − ω² recessive in the horizon's sector, normalised by H ~ e^{−iωr*}(1 + o(1)) there. By
     the standard theory at a rank-1 irregular point, this expansion holds with its derivatives in the sector.
   - So LH = H′ − wH ~ −iω e^{−iωr*}(1 + o(1)) there, since wH = O(ρ − 1)·H.
   - LH solves Ã − ω² (intertwining), and the recessive solutions in the sector form a line. So LH = −iωH̃, where H̃
     is Ã's recessive solution with the same normalisation.
   - At infinity w = O(1/ρ), and in the same way Lψ_∞ = iωψ̃_∞.
3. **The Wronskians agree.**
   - For ψ in Sol_A(ω), (Lψ)′ = −wLψ − ω²ψ. So W[Lψ₁, Lψ₂] = ω²W[ψ₁, ψ₂].
   - Hence D_Ṽ := W[H̃, ψ̃_∞] = W[LH, Lψ_∞]/ω² = W[H, ψ_∞] = D_V for ω ≠ 0, with the same r* on both sides.
4. **So V and Ṽ have the same quasinormal-mode conditions at q = 1 for every ω ≠ 0,** as `PREREG.md` §2 states. At
   ω = 0 the map degenerates (Lu₀ = 0), which the statement excludes.

The hypotheses are Fable's (AUDIT.md §B1):
- the standard asymptotic theory at rank-1 irregular singular points (recessive expansions valid, with their
  derivatives, in sectors), not re-proved here;
- u₀ > 0 on (1, ∞) (Z-pos, certified), so w is real and C^∞ on ℝ.

## The lead's check

The lead re-derived steps 1 and 3 by hand: g from u₀'s closed form, the cancellation and the simple zero of fg at
Y = 1, the location of h's zeros, and the Wronskian identity from (Lψ)′ = −wLψ − ω²ψ. Step 2 is the standard theory
applied as Fable states it.
