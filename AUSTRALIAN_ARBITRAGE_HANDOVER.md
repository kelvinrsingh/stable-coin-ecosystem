# Australian paper arbitrage scanner — Codex handover

The accompanying `Australian_Paper_Arbitrage_Scanner_2026-09-29.zip` is the complete implemented scanner and research package. It contains 42 files: Python source, configuration, input data, HTML reports, CSV/JSONL exports, SQLite audit databases, test log and a checksummed manifest.

## First task for Codex

Extract the archive into `research/australian-arbitrage/`, removing its single enclosing `Australian_Paper_Arbitrage_Scanner/` directory level. Preserve all existing stablecoin research. Read the extracted `README.md` before changing the implementation.

From the extracted scanner folder, run:

```sh
python3 -m unittest discover -s tests -v
python3 -m aus_arb run data/public_nrl_2026-09-29.json --out results/local_public_scan
python3 -m aus_arb run data/historical_afl_normalised.json --out results/local_historical_scan
python3 -m aus_arb run data/synthetic_t00.json data/synthetic_t02.json data/synthetic_t05.json data/synthetic_t15.json data/synthetic_t30.json --config config/demo.json --out results/local_validation
```

Python 3.10+; standard library only. Offline runs need no API key. The original reports can be opened via the extracted top-level `index.html`.

## Research objective and existing evidence

Measure conditional Australian bookmaker arbitrage after commission, stake limits, quote delays and settlement compatibility. Retain rejected comparisons and missing evidence.

- The original build passed 34 tests.
- Four public NRL quotes produced two eligible comparisons; neither was positive after configured costs.
- The official 2022 AFL sample contained 11 events and 140 quotes, producing 264 eligible comparisons; all were negative after configured costs.
- Five synthetic snapshots demonstrate positive calculations, commission eliminating an edge, missing hedges and insufficient capacity. These are invented validation cases, not real profits.
- No bets, fills, settlements, realised returns or continuous monitoring have occurred.

## Next research phase

Reproduce and review the calculations and evidence gates, then propose a costed 30-day paper-only collection study. Confirm sports, feed permissions, polling frequency and data budget before starting sustained collection. Keep a user-supplied API key only in the local `ODDS_API_KEY` environment variable.

Preserve all source labels: current provider, historical provider, public-web observation and synthetic fixture. Do not infer accepted stakes or fills from published prices. Unknown settlement rules, quote times and account capacities remain blocking conditions. Deduplicate overlapping comparisons before assessing opportunity frequency; never add their hypothetical P&L.

The configurable AUD 1,000 capital, AUD 1,000 per-venue funds and AUD 1 allocated cost are modelling assumptions. Public commission baselines remain unverified for a specific account. First-seen timestamps mean first ingestion into the ledger, not first bookmaker publication. Read the README for scope limits and original source links.

Keep this project paper-only. Do not place bets, commit credentials or start paid/sustained data collection as part of importing the package.
