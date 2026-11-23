# A2 extremal checks E0–E5: VERIFIED (BHM-010)

*2026-10-22, the bh-modes lead. Registration: `TARGET_A2.md` §3 (BHM-009, SHA-256
`d8207fbfa6b8cd15…`, commit `a90b83e`), sealed before the first run. Run at commit `8a19e06`
(the registered code plus the kit script).*

## Exact quantities (D = 6, q = 1, M = 1)

| Check | Quantity | Certified value |
|---|---|---|
| E0 | S5 (5.63b), (5.62b) at n = 4 minus the `TARGET.md` §1 forms | 0, 0 |
| E1 | δ at q = 1 (branch 1 + 2mδ > 0) | 1/(5(ℓ + 4)) |
| E2 | lim_{r→1} (r − 1)²/f, f = (1 − r⁻³)² | 1/9 |
| E3 | c(ℓ) = U₋(2)/(576 H₋(2)²) | **ℓ(ℓ − 3)/9** |
| E4 | c(ℓ) + 1/4 | **(2ℓ − 3)²/36** |
| E5 | p(1), q̃(1); indicial roots at r_H | 2, c(ℓ); **(ℓ − 3)/3 and −ℓ/3** |

E1, E3 and E4 also hold in an independent `fmpq` evaluation for every ℓ = 2, …, 1000. By-product
(information): H₋(x_H) = (ℓ + 3)(ℓ + 4) at q = 1.

## Controls (same session; each had to REJECT)

| Control | Verdict | Log SHA-256 |
|---|---|---|
| Other root of (5.58) at q = 1 | REJECT: E1, E3, E4, E5, flint | `3d6b4a2c5ac3f0a2…` |
| False claim ℓ(ℓ − 3)/9 + 1/100 | REJECT: E3, flint | `e47f5b26795542e2…` |
| Tamper: coefficient 7680 → 7681 | REJECT: E0, E3, E4, E5, flint | `c1ecf3457e9e32a0…` |

## Runs

- **Record** (host-1): `runs/record/main/result.json` `44b352fa2917e3d8…`, log
  `90a1336642239a78…`.
- **Reproduction** (host-2, same code): identical after masking (`code/compare_runs.py`); the
  log is byte-identical.
- **One-command re-run:** `BHM_PYTHON=[venv]/bin/python kit/a2/extremal.sh`.
  Exit 0 only if the main check is VERIFIED, the three controls REJECT, and the JSON matches
  the record.
- **Code at `8a19e06`:**
  - `code/a2/extremal.py` `83b61fd5bce302db…`;
  - `code/ki/potentials.py` `7d686b40ad326544…`;
  - `code/qnm1c/common.py` `29c30345dec7b2fe…`;
  - `code/compare_runs.py` `dc5d722e89b3b643…`;
  - `kit/a2/extremal.sh` `39f3b0ff358f6daa…`.

## Status

- **E0–E5: *certified*** (exact arithmetic). Trust base: sympy 1.14.0 and FLINT 3.6.0 `fmpq`.
  Independent re-run by a second party pending (CHARTER e5). These are Lean candidates
  (session-L, `outbox/2026-10-22-to-session-L.md` §3(a)).
- **`TARGET_A2.md` §3's pencil consequences:** the throat limit lim r*²V_{ℓ,1} = c(ℓ), and the
  margin as a necessary condition for A2 at q = 1. Status: *proved (pencil; audited 0×)*.
- **Theorem A2 itself:** *conjecture*.
