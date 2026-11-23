# AUDIT — bh-modes extremal checks E0–E5 (BHM-010)

*Auditor: Kimi (second auditor for machine results), 2026-10-22.
Brief: `results/a2/extremal/briefs/BRIEF_kimi_2026-10-22.md`, SHA-256
`6591db1e5f6a4e85df418224f06c8bef9cb24deb7f74cbd9a87d81b3ba9852b4` (verified against
`SEALED.sha256`). Workspace: `[kimi-folder]/bhm-a2-extremal-audit-2026-10-22/`.
The bh-modes tree was never modified.*

**Anti-anchoring.** All own checks were complete and on disk before I opened
`results/a2/extremal/RESULT.md` or the run of record.

## E0 — PASS

My own transcription of KI hep-th/0308128 (5.62b)/(5.63b), read from the rendered PDF page 25
(image kept in the p3 audit workspace), equals TARGET.md §1's H₋ and U₋ as polynomials in
(x, m, δ) — a symbolic identity, not a point check (re-run here from
`../bhm-p3-audit-2026-10-22/own/build.py`).

## E1 — PASS

25 + 4m = (2ℓ+3)² identically (m = (ℓ−1)(ℓ+4)); with δ = 1/(5(ℓ+4)): 1 + 2mδ = (2ℓ+3)/5 > 0
for ℓ ≥ 2, and (1+2mδ)² = 1 + 4m/25 = 1 + 4mq²/25 at q = 1 — the positive branch of KI (5.58).

## E2 — PASS

f = 1 − x + x²/4 = (1 − x/2)² = (1 − r⁻³)², so f(1) = 0. The limit is exhibited by a rational
function, as the brief asks: (r−1)²/f = **r⁶/(r²+r+1)²** (exact cancellation), whose value at
r = 1 is 1/9.

## E3 — PASS

c(ℓ) := U₋(2)/(576H₋(2)²) at q = 1 equals **ℓ(ℓ−3)/9** identically in ℓ (symbolic).

## E4 — PASS

c(ℓ) + 1/4 = (2ℓ−3)²/36 identically.

## E5 — PASS

For ψ″ + (f′/f)ψ′ − (V/f²)ψ = 0: (r−1)f′/f = 6/(r(r²+r+1)) is regular at r=1 with value 2,
and (r−1)²V/f² = U₋(2/r³)·r⁴/(64H₋(2/r³)²(r²+r+1)²) is a rational function regular at r=1
with value ℓ(ℓ−3)/9 = c(ℓ). So r = 1 is a regular singular point with indicial equation
s(s−1) + 2s − c(ℓ) = 0, whose roots are exactly (ℓ−3)/3 and −ℓ/3 (s²+s−c = 0,
1+4c = (2ℓ−3)²/9 by E4).

## Controls — both REJECT as required

- (a) The negative branch of KI (5.58) at q = 1 (1+2mδ = −(2ℓ+3)/5) gives
  c = (ℓ+3)(ℓ+6)/9 ≠ ℓ(ℓ−3)/9: my E3 check rejects it.
- (b) U₋'s coefficient 7680 → 7681: my E3 identity fails: rejected.

## Reproduction — PASS

`kit/a2/extremal.sh` at `8a19e06` in my workspace (`runs/kit-run-8a19e06/`), exit 0,
KIT PASS: main VERIFIED; the three registered controls (wrong-branch, false-claim, tamper-U)
all REJECT. My `main/result.json` is identical to the run of record in every substantive
field (timings/provenance masked); the record's SHA-256 matches the brief's `44b352fa…`.

## Overall verdict

**BHM-010 (E0–E5) stands.** All identities re-derived by my own CAS route, the two limits
exhibited by regular rational functions, controls rejected. No fixes.
