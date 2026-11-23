# AUDIT — bh-modes HD-X-E / HD-X-S / HD-X-2, D = 7–11 through extremality (BHM-127, BHM-131, BHM-143)

*Auditor: Kimi (second auditor for machine results), 2026-10-27.
Brief: `results/stage3/briefs/BRIEF_kimi_2026-10-26.md`, SHA-256
`efdfd025595b04290c15933929be39199781d689332d4004fe092d28065765ef` (the cover message's value;
per the brief, `SEALED.sha256` was not opened). The artifact and code hashes listed in the
brief were all verified.
Workspace: `[kimi-folder]/bhm-hdx-audit-2026-10-27/`.
Runs of record: own suite on **host-1** (`own/*.host-1.log`), kit reproductions on **host-2**;
`nice -n 19`, the pinned venv; copies kept on the nodes under `[kimi-folder]/`.
The bh-modes tree was never modified.*

**Anti-anchoring (allow-list).** Only the brief's listed files (the pilot record only its
`designs` field) and my own earlier workspaces were read before my own checks were complete.
`SEALED.sha256` was not opened, per the brief.

## Task 1 — transcription

My own general-n KI (5.62b)/(5.63b) transcription (BHM-036/109), validated against the
rendered PDF.

## Task 2 — HD-X-2 (the 9 critical bands): PASS

My own build (`own/hdx2.py`): the registered design P = −ν − ℓy/((z+ε)R) − (1−z)H_z/H + cμ,
ν = ℓ + n/2 − 1, R = (1−y)/z, H = H₋(x_H y), ε = ε̂w/(1+w), ε̂ = (1/k + 2/(k−ℓ))/2, c = 1/4;
Π = P·D with D = S·R·H, S = ε_d z + ε_n; my NL = N·S²R²·Den with my own Den. All on my exact
QQ(μ) arithmetic and my fixed Bernstein verifier.

Per band (`own/hdx2_check.host-1.log`):
- **Z0**: NL(z, 0) ≡ 0 exactly — the zero-mode identity in this formulation. (I also verified
  the identity directly in sympy during development: the design at μ = 0 equals
  (1−z)(log u₀)_z and N with it is ≡ 0. During that work I found and fixed a bug of my own —
  an extra x_H² in the (1−z)f_z term — before any verdict was produced.)
- **Divisions** M = NL/μ, T = NL(μζ, μ)/μ², K = NL(z, zσ)/(z²σ): all exactly polynomial.
- **Charts** O, O′, T, C all POSITIVE on their closed boxes.
- **Coverage**: the registered argument, checked: z ≥ 1/4 → O; z < 1/4, μ ≥ 1/32 → O′;
  z ≤ 8μ → T; else C. Every (z, μ) ∈ (0, 1) × (0, MU1] lies in a chart, where NL > 0, and
  S, R, Den > 0 there (S: ε_d > 0 always, ε_n = ε̂w ≥ 0 with equality only at μ = 0, off the
  claim's domain; R > 0 verified per band by my verifier).
- **q(MU1)² ≤ (99/100)²** exactly per band; my values equal the PREREG's table
  (e.g. 197505/201601 for 7-2).

| D | ℓ | verdict | q(MU1)² |
|---|---|---|---|
| 7 | 2 | VERIFIED | 197505/201601 |
| 8 | 2 | VERIFIED | 698908729/714118729 |
| 9 | 2 | VERIFIED | 7961448561/8130448561 |
| 9 | 3 | VERIFIED | 2404864/2455489 |
| 10 | 2 | VERIFIED | 9829338561/10033828561 |
| 10 | 3 | VERIFIED | 46562824/47513449 |
| 11 | 2 | VERIFIED | 1321538729/1348578729 |
| 11 | 3 | VERIFIED | 2961/3025 |
| 11 | 4 | VERIFIED | 1015861/1038361 |

## Task 3 — HD-X-S (the 11 non-critical bands): PASS

My own build at general n (`own/hdxs.py`): P = a(1+ε)/(z+ε) + p₀, ε = w/((n−1)(1+w)), a and
p₀ per band from the pilot record's `designs` field; NL = N·S²·Den; the A2-S chart scheme.
Per band (`own/hdxs.host-1.log`): Den > 0, both divisions exact, all four charts POSITIVE,
q(1/8)² ≤ (99/100)² exactly.

| D | ℓ | a | verdict |
|---|---|---|---|
| 7 | 3 | −7/20 | VERIFIED |
| 8 | 3 | −11/25 | VERIFIED |
| 8 | 4 | −8/25 | VERIFIED |
| 9 | 4 | −2/5 | VERIFIED |
| 9 | 5 | −3/10 | VERIFIED |
| 10 | 4 | −16/35 | VERIFIED |
| 10 | 5 | −13/35 | VERIFIED |
| 10 | 6 | −2/7 | VERIFIED |
| 11 | 5 | −17/40 | VERIFIED |
| 11 | 6 | −7/20 | VERIFIED |
| 11 | 7 | −11/40 | VERIFIED |

## Task 4 — HD-X-E (the 33 cases): PASS

`own/hdxe.py` (my HD-E machinery): the parametrisation identities and w increasing per case;
Den > 0; F > 0 on [0, 1] × [0, μ_lo] for ℓ ≥ n (one box each); the exact splitting
F = μK + sG with K > 0, G > 0 for the five touching cases ℓ = n−1 (D = 7 ℓ = 4, D = 8 ℓ = 5,
D = 9 ℓ = 6, D = 10 ℓ = 7, D = 11 ℓ = 8); μ_lo on the 1/10000 grid, exact coverage. The EXT
gate verified symbolically in (ℓ, n): H₋(x_H) = (ℓ+n)(ℓ+n−1) and
U₋(x_H) = 64ℓ(ℓ−n+1)H₋(x_H)² at q = 1 — so the touching cases are exactly ℓ = n−1.

33/33 POSITIVE (`own/hdxe.host-1.log`).

## Task 5 — pencil verdicts

- **(a) the reduction for both singular designs at general n: SOUND.** HD-X-S: the pole
  z = −ε ≤ 0 is off the open exterior (0, 1); at q = 1 it sits at the horizon endpoint, where
  f's double zero keeps S = −f(1−z)P smooth (S ~ −(n−1)²a·z). HD-X-2: for μ > 0 the pole is
  at z = −ε < 0; R > 0 on [0, 1] (a polynomial with R(0) = k, checked per band); H > 0. In
  both, Proposition 3 at general n (METHOD_ADDENDUM_2) applies: N > 0 on (0, 1) suffices.
- **(b) the tortoise map for 0 < q < 1 at general n: SOUND.** f = (1−y)(1−ky),
  y = (1−z)^{n−1}: f > 0 on the exterior; f_z(0) = (n−1)(1−k) > 0 (re-derived), so r* → −∞
  logarithmically at the horizon; f → 1 at infinity. C^∞ diffeomorphism onto ℝ.
- **(c) the composition of Theorem HD-X: SOUND.** The ℓ-split per D is complete and exact:
  bands ℓ ≤ n−2 (HD-X-S for 2ℓ > n−1, HD-X-2 for 2ℓ ≤ n−1; the two families meet at the
  boundary ℓ = n/2 − 1/2 which no integer crosses... the split 2ℓ > n−1 vs 2ℓ ≤ n−1 is
  exhaustive); n−1 ≤ ℓ ≤ ℓ₀(n) by HD-X-E; ℓ > ℓ₀ by Lemma U(n) (all q ≤ 1); q = 1 by Z (out
  of this audit's scope, machine-checked per the brief). The q-range ends compare exactly:
  q(μ_lo)² ≥ (99/100)² ≥ q(1/8)² and ≥ q(MU1)² per band, so the μ-ranges meet. The step from
  U₋ ≥ 0 to A ≥ 0 uses only f > 0 and H₋ > 0 on the exterior, including at q = 1.

## Task 6 — controls: all reject as required (`own/hdx_controls.host-1.log`)

- **(a)** HD-X-E at D = 7, ℓ = 3 (a band): REJECT, corner F(1, 0) = −4816896 < 0 (the
  band's ditch reaches the extremal horizon). Could not have passed.
- **(b)** strict bound for ℓ = n−1 (D = 7, ℓ = 4): refused with the value exactly 0 at
  (t, μ) = (1, 0) — the touching corner; the strict check's node evaluation catches it.
- **(c)** HD-X-2's ε̂ outside the window (1/k, 2/(k−ℓ)) = (1/4, 1) at band 7-2, below
  (ε̂ = 1/5) and above (ε̂ = 9/8): the T chart rejects both — at (ζ, μ) = (4, 1/64) below
  (the T₁ < 0 side) and at (0, 0) above (T₀ < 0), exactly the THROAT formula's two failure
  modes.
- **(d)** HD-X-S's design with a = −4/5 (outside the window (−3/4, −1/4) at band 7-3):
  REJECT on all four charts.
- **(e)** planted bound state in the throat, band 7-2 at μ = 1/64: the support
  [209/10000, 837/10000] lies inside the U₋ < 0 region (first root z_U = 0.10472…);
  Q[b] = A − K·C < 0 rigorously at 100-digit acb precision (A = 2.929328870e-12 > 0 is the
  unplanted energy, C = 1.967252224e-20 > 0, K = 297809182, Q's upper bound < 0); the planted
  certificate is refused on the T chart (exact negative value at (ζ, μ) = (4, 1/64)), and
  N′ < 0 exactly at the bump centre. (This matches the PREREG's nc-bound in shape; mine was
  built independently, with K from my own A and C.)
- **(f)** verifier tamper: caught by the KAT suite (KAT1–KAT8).

## Task 7 — reproductions

All on the pinned venv under `nice -n 19`, with output outside the snapshots:
- `kit/hdx/run_elementary.sh` at `8679d8b` on **host-2**: exit 0, KIT PASS — main VERIFIED,
  nc-band, nc-strict, nc-bump, td-coeff, td-verifier, td-mulo all REJECT as registered
  (td-coeff's full predicted list matches).
- `kit/hdx/run_s.sh` at `bf23bfc` on **host-2**: exit 0, KIT PASS — all 11 bands VERIFIED,
  all 17 controls per band as registered. `run_s.sh --gate`: KIT PASS, the gate band D = 6
  ℓ = 2 IDENTICAL to A2-S's record.
- `kit/hdx/run_critical.sh` at `6cedd44` on **host-1**: exit 0, KIT PASS — all 9 bands
  VERIFIED, every control on both kit bands in its registered form.
- Reconciliation (`own/reconcile_hdx.py`, log in the delivery): my reproductions' per-job
  records are substantively identical to the runs of record (timings/provenance masked):
  HD-X-E 7/7 jobs, HD-X-S 198/198, HD-X-2 9/9.

## Overall verdict

**HD-X-E, HD-X-S and HD-X-2 all stand** — every claim re-derived by my own exact route, the
zero-mode identity (HD-X-2's Z0) verified independently, all corners handled by charts I
re-verified, the pencil points SOUND, my controls reject, and all three kits reproduce the
records. With Theorem HD (BHM-109/110) and Z (out of scope here, machine-checked per the
brief), **Theorem HD-X (D = 7–11, every ℓ ≥ 2, every q ∈ (0, 1]) is now second-party
checked** on the parts I was briefed to cover.

Pointer for the operator: audit workspace `[kimi-folder]/bhm-hdx-audit-2026-10-27/`
(AUDIT.md, audit_record.json, SHA256SUMS).
