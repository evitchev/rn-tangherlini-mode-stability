# RESULT — Z: the extremal zero mode, and its Darboux partner

*Item BHM-126. 2026-10-26, the bh-modes lead. Registration: `PREREG.md` (BHM-123), with addendum 1 (BHM-125) after the
VOID run at `a188aba` (BHM-124). Sealed.*

## Verdict: VERIFIED as registered, KIT PASS

- **The record:** host-1 at `8967b5f`, from its `git archive` (SHA-256 `0b92a6aa69c4476b…`), 18:00:57–18:00:59 UTC.
- **The reproduction:** host-2, with `BHM_REF` set to the record. All 19 jobs are IDENTICAL after masking.

| Job | Verdict |
|---|---|
| claim: n = 4, 5, 6, 7, 8, 9 (D = 6–11) | VERIFIED, each |
| n symbolic (N) | VERIFIED |
| information: n = 2, 3 (D = 4, 5) | VERIFIED, each |
| nc-nu, at n = 4 and 9 | REJECT: Z-inf, Z-id, P-reg, P-asym, as registered |
| nc-exp, at n = 4 and 9 | REJECT: Z-thr, Z-id, P-reg, P-asym, as registered |
| td-U, at n = 4 and 9 | REJECT: Z-inf, Z-thr, Z-id, P-reg, P-asym, as registered |
| td-zid, at n = 4 and 9 | REJECT: Z-id, P-reg, P-asym, as registered |
| td-preg, at n = 4 and 9 | REJECT: P-reg, P-asym, as registered |

## What is certified, and what rests on pencil

**The identity** (*certified*, exact). Put Y = ρ^{−(n−1)}. Then

  u₀ = ρ^{−ν}(1 − Y)^{−ℓ/(n−1)} / ((ℓ − 1) + nY),  ν = ℓ + n/2 − 1,

solves the q = 1 zero-energy master equation of V_S−. This holds symbolically in ℓ, for each n = 2…9, and symbolically
in n. Every gate holds:
- q1, the extremal point of (5.58);
- H, i.e. H₋ = (ℓ + n)((ℓ − 1) + nY), so u₀ ∝ 1/H₋;
- Z-pos;
- Z-inf, the decaying exponent at infinity;
- Z-thr, the throat exponent ℓ/(n − 1), whose indicial equation reproduces c_n(ℓ) (BHM-049).

**The consequence** (*certified*; the ground-state step by Lemma 1, *machine-checked* (BHM-030); the tortoise map at
general n *proved (pencil; audited 0×)*). For every ℓ ≥ 2, A_{ℓ,1} ≥ 0 on C₀^∞(ℝ):
- for each D = 6–11, the registered claim;
- by the N job, for every D ≥ 4 covered by S5's general-n forms.

The physical reading is Theorem A2's at q = 1: S5's reduction, *cited*. This is relative to the sources read, and it
makes no novelty claim (RULES.md A7). Session-L's literature check of the zero mode is not ruled (BHM-120).

**The partner** ([another line of this project] (b′); *certified* that it is regular, exact). Let w = (log u₀)_{r*}. Then V = w² + w′, and the
partner Ṽ = w² − w′ = fŨ/ρ² has **no pole at the zeros of H₋** (P-reg), for each n and for n symbolic.
- **Ũ is a quadratic polynomial in Y,** with Ũ(0) = ν(ν − 1) and Ũ(1) = ℓ(ℓ + n − 1) (P-asym). For n symbolic, as
  recorded:

  Ũ = (5n²/4 − n/2)Y² + (−3n²/2 + 2n + 2ℓ − 2)Y + (n²/4 + nℓ − 3n/2 + ℓ² − 3ℓ + 2),

  and at n = 4, Ũ = 18Y² + (2ℓ − 18)Y + ℓ² + ℓ.
- **So the partner potential has no H₋ in its denominator.** At infinity it behaves like the ℓ − 1 centrifugal term.
  At the throat its coefficient is ℓ(ℓ + n − 1)/(n − 1)² > 0, where V's is c_n(ℓ).
- **The comparisons** (information) are all false. Ũ is not W₊ at the same ℓ, and not W₋ at ℓ ± 1.
- **The pencil reason held:** BHM-098's b₋₁ = 0 at the apparent points forces w₀ = 0 (PREREG §2).
- **The intertwiner,** L = ∂_{r*} − w with A = L†L and Ã = LL†, maps solutions at every ω, and for ω ≠ 0 it preserves
  the quasinormal-mode conditions. This is *proved (pencil; audited 0×)*; the step at the extremal horizon's irregular
  point is the one to audit.
- **So at q = 1 the apparent points of V_S− come from a Darboux transformation** of a potential without them. That
  answers, at q = 1, the question left open in `[a note of another line of this project]`.

**The throat classification** (facts, for each integer n): u₀ is throat-principal exactly when 2ℓ ≤ n − 1.
- In the bands those are ℓ = 2 at n = 5 and 6; ℓ = 2, 3 at n = 7 and 8; and ℓ = 2, 3, 4 at n = 9. That is the critical
  set 𝒦 of `TARGET_HD_ADDENDUM_2.md`, 9 bands.
- At n = 4, ℓ = 2 it is not principal, which fits A2-S's slack at q = 1.

## What it means (PREREG §6)

- **D = 6:** a second route to Theorem A2 at q = 1.
- **D = 7–11:** HD-X's endpoint q = 1 is settled for every ℓ, including the 9 critical bands. Nothing here covers
  q ∈ (99/100, 1).
- **[another line of this project]:** the extremal partner equation, without the apparent points, is the input for the functional-relations
  work.
- **Second party: pending** (RULES.md A4). The natural one for an exact identity is session-L's Lean (CHARTER changelog,
  sixth entry, item 2), with the lead reading the Lean statements against this claim.

## Records

- `runs/record/` (host-1) and `runs/repro-host-2/`: one directory per job, each with `result.json`, `run.log` and, for
  the reproduction, `compare.txt`.
- Kit logs: `logs/kit-record-host-1.log` and `logs/kit-repro-host-2.log`. Hosts and UTC times: `logs/host-*.txt`.
- The SHA-256 of every record and log are in `SEALED.sha256` under BHM-126.
- The VOID attempt at `a188aba` is in `attempt-a188aba/` (BHM-124).
