# RESULT: re-run of Kimi's cross-check of its two routes to N (BHM-040)

*Registered as BHM-039 (`PREREG.md` in this folder). Run 2026-10-22 on host-1 in `[venv]`
(Python 3.12.8, sympy 1.14.0), from a `git archive` of `8eaf290`, under `nice -n 19`. Files in this
folder: `env.txt`, `crosscheck.log`, `nc-rc1.diff`, `nc-rc1.log`; their hashes on host-1 and here
agree.*

| Check | Registered | Outcome |
|---|---|---|
| Kimi's `own/crosscheck.py`, unmodified | `CROSSCHECK OK`, exit 0 | `CROSSCHECK OK: rf route == sympy route, 69 coefficients compared`, exit 0 |
| NC-RC1: U₂ = 46081(1 + mδ) in a scratch copy (`nc-rc1.diff`, one line) | `CROSSCHECK FAILED`, exit 1 | `CROSSCHECK FAILED`, exit 1 |

**PASS as registered.** For T1's stored P at μ = 1/6, Kimi's two routes to N agree in all 69
coefficients, exactly. One route has (1 − z)f_z entered by hand and is the one behind its T2 and T3
verdicts; the other differentiates f symbolically. The delivered `own/crosscheck.log`, which reads
`CROSSCHECK FAILED`, is the log of the run before Kimi's fix. With the code reading recorded in
BHM-036, the evidence for Kimi's T2 and T3 verdicts is complete.
