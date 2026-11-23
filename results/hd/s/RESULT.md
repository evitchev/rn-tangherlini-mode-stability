# RESULT — HD-S: S-certificates on the 18 bands of D = 7–11 (BHM-078)

*Registered as BHM-076 (`PREREG.md`), with q_max and the designs of `TARGET_HD_ADDENDUM_1.md` (BHM-075). The run of
record was on host-1 and the reproduction on host-2, both from a `git archive` of `0aa2673` with
`kit/hd/run_s.sh`.*
- *Both kits print KIT PASS.*
- *All 34 records are identical after masking (`compare_runs.py`), and every `run.log` and planning record is
  byte-identical between the nodes.*
- *The 34 jobs, 8 at a time, took about three minutes; each band took 6–82 s.*
- *The blind brief for the first band went to the session-R lead before the run (BHM-077).*

**VERIFIED as registered.** All 18 bands are VERIFIED, and every control and drill ends with its registered verdict.

## The certified bands

**S(D, ℓ): A_{ℓ,q} ≥ 0 for every q in the interval shown.** The interval's ends are √(q(μ_b)²) and √(q(μ_a)²),
exact rationals inside the root, which are in `runs/record/<D>-<ℓ>/result.json` under `claim_q`; the table gives
them in inward decimals.
- Every box verified at the registered degree on its first attempt, so no fallback was used.
- "N·L degree" is the largest degree in (z, μ) over the band's boxes.
- "Leaves" counts the Bernstein leaves for N > 0.
- "Min ψ₁" and "min σ" come from the planning records (untrusted).

| D | ℓ | kind | q, inward | design | boxes | N·L degree | leaves | min ψ₁ | min σ (fit) |
|---|---|---|---|---|---|---|---|---|---|
| 7 | 2 | onset | [0.94798, 0.99000] | z 20 | 9 | (56, 16) | 27 | 0.891 | 0.0506 |
| 7 | 3 | onset | [0.97699, 0.99000] | z 16 | 5 | (48, 16) | 17 | 0.986 | 0.00625 |
| 8 | 2 | from 0⁺ | [0, 0.99000] | z 24 | 22 | (68, 16) | 84 | 0.742 | 0.0452 |
| 8 | 3 | onset | [0.94399, 0.99001] | z 20 | 10 | (60, 16) | 30 | 0.901 | 0.0150 |
| 8 | 4 | onset | [0.98300, 0.99001] | z 20 | 3 | (60, 16) | 11 | 0.996 | 0.00299 |
| 9 | 2 | from 0⁺ | [0, 0.99001] | z 28 | 22 | (80, 16) | 80 | 0.625 | 0.0403 |
| 9 | 3 | onset | [0.92100, 0.99001] | z 24 | 11 | (72, 16) | 33 | 0.799 | 0.0180 |
| 9 | 4 | onset | [0.95198, 0.99000] | z 24 | 9 | (72, 16) | 27 | 0.930 | 0.00947 |
| 9 | 5 | onset | [0.98699, 0.99001] | ζ 20 | 2 | (64, 16) | 10 | 1.000 | 0.00151 |
| 10 | 2 | from 0⁺ | [0, 0.99000] | z 32 | 22 | (92, 16) | 100 | 0.545 | 0.0409 |
| 10 | 3 | onset (interior) | [0.48986, 0.99001] | z 28 | 21 | (84, 16) | 63 | 0.699 | 0.0149 |
| 10 | 4 | onset | [0.91998, 0.99000] | z 24 | 11 | (76, 16) | 63 | 0.847 | 0.00278 |
| 10 | 5 | onset | [0.96099, 0.99001] | ζ 24 | 8 | (76, 16) | 24 | 0.954 | 0.00390 |
| 11 | 2 | from 0⁺ | [0, 0.99000] | z 32 | 22 | (96, 16) | 174 | 0.487 | 0.00089 |
| 11 | 3 | from 0⁺ | [0, 0.99000] | z 32 | 23 | (96, 16) | 75 | 0.618 | 0.0133 |
| 11 | 4 | onset | [0.89697, 0.99001] | z 28 | 13 | (88, 16) | 39 | 0.762 | 0.00770 |
| 11 | 5 | onset | [0.92900, 0.99001] | z 28 | 11 | (88, 16) | 39 | 0.884 | 0.00186 |
| 11 | 6 | onset | [0.96800, 0.99001] | ζ 24 | 7 | (80, 16) | 23 | 0.971 | 0.00214 |

In all, the 18 bands use 231 μ-boxes and 919 Bernstein leaves.

**The gates held in every band:** KAT, E0n, PILOT, H and coverage.
- **G-S6** held for each band from 0⁺: the box ending at μ = 1 (q = 0) verified, so S6's Q = 0 answer is
  reproduced as part of the band.
- **The interior band** (D = 10 ℓ = 3) starts at q(μ_b) = √(91914991536373201/383045380761373201) = 0.48986…,
  below its onset 0.4913 and below HD-E's q_split = 0.490. That is the check `TARGET_HD.md` §5 asks for.

## Controls and drills (all as registered)

| Name | D = 7 | D = 8 | D = 9 | D = 10 | D = 11 |
|---|---|---|---|---|---|
| NC-S, a planted bound state: (a) Q[b] certified < 0, (b) the certificate is rejected on it | K = 174912, Q = −1.16·10⁻⁶; REJECT (b) | K = 201776, Q = −1.34·10⁻⁶; REJECT (b) | K = 231801, Q = −1.54·10⁻⁶; REJECT (b) | K = 266104, Q = −1.77·10⁻⁶; REJECT (b) | K = 304036, Q = −2.02·10⁻⁶; REJECT (b) |
| TD-S1, a coefficient (`REJECT: E0n`) | REJECT: E0n | REJECT: E0n | REJECT: E0n | REJECT: E0n | REJECT: E0n |
| TD-S2, the horizon bound (`REJECT: td-horizon`), with an exact counterexample at z = 0 | at μ = 1237/10000 | at μ = 157/1250 | at μ = 1271/10000 | at μ = 321/2500 | at μ = 259/2000 |
| TD-S3, the verifier (D = 7 only) | REJECT: KAT | | | | |

The values of Q[b] are Arb balls; their radii are below 10⁻¹⁵.

## S14's Table I (consistency information, `PREREG.md` §5)

S14 reports the ℓ = 2 scalar-type modes damped for D = 7–11 at Λ = 0 (*cited*, *numerical*). The certified ℓ = 2
bands agree: no growing mode for q ≤ 0.99.

## Status, and what follows

- **Each S(D, ℓ):** *certified* (exact). The reduction (METHOD.md, Proposition 3) is proved (pencil; audited 2×),
  and machine-checked in Lean (BHM-030).
- **Theorem HD is certified**, with HD-E (BHM-063): for D = 7, 8, 9, 10, 11, every ℓ ≥ 2 and every q ∈ (0, 99/100],
  A_{ℓ,q} ≥ 0.
- **Still pencil only:** Lemma U(n)'s steps (audited 0×; Kimi's HD-E brief is pending).
- **Second parties, pending:**
  - Kimi for HD-E (the brief is written and to be relayed);
  - a Kimi brief for HD-S;
  - the blind replication of D = 7 ℓ = 2 (BHM-077).

## Hashes (SHA-256, first 16 hex)

- Code at `0aa2673`: `code/hd/scert.py` `8a67a9e6d381a6a2`; `kit/hd/run_s.sh` `8384b906fd5e6570`.
- The records are under `runs/record/` and the reproduction under `runs/repro-host-2/`. Each band's `result.json`
  holds its certificates P̂(z, μ) as exact rationals; `SEALED.sha256` lists all 34 records.
