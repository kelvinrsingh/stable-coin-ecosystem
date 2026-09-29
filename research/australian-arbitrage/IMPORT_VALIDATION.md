# Import validation

Imported on 29 September 2026 from `Australian_Paper_Arbitrage_Scanner_2026-09-29.zip` on `origin/codex/australian-paper-arbitrage`.

Archive SHA-256: `c24178b38c26c25b7ff3f4683f16bebfeda25cb59634afa81da8887db071a97f`.

All 42 archive files were extracted unchanged, removing the enclosing directory. All 41 entries in `MANIFEST.json` passed byte-size and SHA-256 validation. Existing repository files were preserved. Read the scanner README and repository handover before running validation.

Validation with Python 3.9.6:

- `python3 -m unittest discover -s tests -v`: 34 tests passed.
- Public snapshot: 4 observations, 2 comparisons, both rejected.
- Historical snapshot: 140 observations, 264 comparisons, all rejected.
- Five synthetic snapshots: 44 observations, 19 comparisons; 9 synthetic candidates, 7 rejected, 3 blocked as unverified.
- All three scans reported zero input errors and zero bets placed.

Reproduction commands are in `AUSTRALIAN_ARBITRAGE_HANDOVER.md` at the repository root. Fresh outputs were written to `results/local_public_scan/`, `results/local_historical_scan/`, and `results/local_validation/`, which are ignored to preserve the original bundled reports.

This validates package integrity and offline execution. It does not independently verify external source claims or establish executable betting opportunities. No live collection was started.
