# Australian paper arbitrage scanner

Research build • 29 September 2026 • Python 3.10+ • standard library only

**Start by opening `index.html`.** It links to the three completed scans and their full audit exports. No installation is needed to read the results. Unzip the entire folder first so the links work.

This package compares cash fixed-odds bets and bookmaker-back / exchange-lay pairs. It records negative calculations, missing evidence and unsupported markets. It has no order-placement interface, betting login, deposit or withdrawal function.

## What was actually run

| Data | Coverage | Result |
|---|---|---|
| Public NRL pages observed 29 Sep 2026 | 2 bookmakers, 4 quotes, 2 cross-book comparisons | Both negative after the configured costs; exact quote timestamps, account limits and matching settlement rules unavailable |
| Official historical AFL sample, 24 Apr 2022 | 11 events, 140 quotes, 264 eligible comparisons | All negative after the configured costs; historical data is never presented as a current opportunity |
| Invented validation fixtures | 5 snapshots, 44 quotes, 19 comparisons | Exercises positive, negative, blocked and disappearing-hedge cases; no real profits |

The best public comparison used 1.45 and 2.80: reciprocal sum 1.046798, so it is not an arbitrage even before the illustrative AUD 1 cost. On approximately AUD 1,000 of assumed capital, the model's worst normal-settlement result is **−AUD 45.71** including that cost. These page types have not been verified as identical betting contracts.

The tests passed: **34 automated tests**, including commission, two- and three-outcome coverage, liability, rounding, per-venue capital, stale prices, mismatched rules, missing limits, partial fills, delayed quotes, unilateral voids, audit persistence and redacted API errors.

No continuous collection has been started. No live authenticated feed, accepted stake, fill, settlement or realised return has been measured. The limited snapshots cannot establish how often Australian arbitrage occurs or whether it would be commercially viable.

## Run locally

From the unzipped folder, in a terminal:

```sh
python3 -m unittest discover -s tests -v
python3 -m aus_arb run data/public_nrl_2026-09-29.json --out results/my_public_scan
python3 -m aus_arb run data/historical_afl_normalised.json --out results/my_historical_scan
python3 -m aus_arb run data/synthetic_t00.json data/synthetic_t02.json data/synthetic_t05.json data/synthetic_t15.json data/synthetic_t30.json --config config/demo.json --out results/my_demo
```

On Windows, replace `python3` with `py -3` if appropriate. The provided snapshots run offline. Public observations become stale on later runs; the scanner preserves the original observation time. Historical and synthetic calculations are evaluated at their labelled snapshot times.

Each output folder includes:

- `index.html`: local interactive table; filter by source, status, event or reason.
- `candidates.csv` and `candidates.jsonl`: every enumerated comparison, including rejected ones.
- `observations.jsonl`: every supplied price, including invalid and unsupported quotes.
- `issues.jsonl`: missing outcomes, invalid data, unsupported markets or incomplete enumeration.
- `summary.json`: counts, explicit assumptions and configuration.
- `audit.sqlite3`: append-only snapshots, first-ingestion records, configuration versions, decisions and issues from each run.

The HTML is a local file and loads no external scripts. Synthetic data uses invented operator names.

## Collect new AU prices

The optional integration uses the documented **The Odds API v4** read-only endpoint with `regions=au`, `markets=h2h`, decimal prices and ISO dates. Obtain your own key from the provider and set the `ODDS_API_KEY` environment variable locally. Do not put it into the configuration, source code or chat. No key is included or required for the offline examples.

```sh
python3 -m aus_arb collect --sport rugbyleague_nrl --out results/my_collection
```

This makes one request. To explicitly request repeated collection:

```sh
python3 -m aus_arb collect --sport rugbyleague_nrl --polls 10 --interval 5 --out results/my_collection
```

The process must remain running. It is not installed as a background service and does not resume itself after a restart. It stops on a provider error instead of retrying or spending more quota silently. Raw responses and normalised snapshots are retained; quota headers are printed. The latest collection report covers a rolling window of roughly the longest delay, while the SQLite ledger and saved raw files preserve earlier data and decisions. A later `run` over selected saved snapshots can create a separate combined report.

Each API request can consume credits; provider coverage and update frequency depend on the feed. Requesting every two seconds does not imply new bookmaker prices every two seconds. At a nominal two-second interval, continuous collection is approximately 43,200 requests/day or 1,296,000 over 30 days, before accounting for request duration. Configure a data budget first. This build has not spent API credits or purchased a feed.

The feed alone will generally **not** satisfy all the evidence checks: account-specific capacities, exact settlement rules and account charges are not inferred from published odds. API-reported `bet_limit` is preserved separately as unverified until its unit, side, freshness and applicability are confirmed.

## Mathematics

For exhaustive, mutually exclusive outcomes with compatible decimal prices `o_i`, calculate `Q = sum(1 / o_i)`. A price-only fixed-odds arbitrage requires `Q < 1`.

For total stake `C`, the unconstrained equal-payout stakes are `s_i = C / (Q * o_i)`. Gross return on stake is `1/Q - 1`; it is not `1 - Q`. The scanner scales this allocation down to satisfy supplied maximum stakes and aggregate paper balances by venue, rounds stakes down to cents, then recalculates every outcome's profit after configured costs. This is a conservative equal-payout sizing method, not a general optimiser of every possible stake allocation.

For bookmaker back odds `B`, exchange lay odds `L`, back stake `b` and commission `c` on positive net exchange winnings:

```text
lay stake = b * B / (L - c)
exchange liability = lay stake * (L - 1)
P&L if backed outcome wins = b * (B - 1) - liability - other costs
P&L if backed outcome loses = lay stake * (1 - c) - b - other costs
capital required = back stake + exchange liability
```

Before other costs, a back/lay edge requires `B > (L - c) / (1 - c)`. Merely having `B > L` is insufficient. The code compares the adjacent cent hedge sizes and retains the feasible choice with the better worst-outcome result. Capital includes lay liability, not just the lay stake. An observed lay limit must be supplied in **lay-stake units**; an account balance is a separate constraint.

The default budget is AUD 1,000 per comparison, an assumed AUD 1,000 per venue, and an illustrative AUD 1 overhead per comparison. These are modelling inputs, not verified funds or measured fees. Change them in `config/default.json`. Account-specific charges, allocated data subscriptions, turnover charges, tax treatment and any additional fees must be assessed and configured separately. Settlement-level currency rounding may differ between operators; the model rounds stakes and retains full-precision calculated P&L. Do not rely on a sub-cent edge.

## Evidence required for a paper candidate

`paper_candidate` means a **conditional model result**, never an accepted or guaranteed trade. It requires all configured checks to pass:

1. A current provider snapshot and known pre-event start time.
2. A documented exhaustive outcome list, including a draw when applicable.
3. A reviewed Australian operator allowlist entry.
4. Fresh provider quote timestamps and acceptable cross-book timestamp skew.
5. Compatible, documented settlement signatures covering period, overtime, draw, push, retirement, postponement, dead heat and void policy.
6. Fresh, evidenced maximum capacity and known minimum stake for each leg.
7. Confirmed applicable commission for an exchange quote.
8. Positive P&L after costs, cent rounding and minimum profit/ROI thresholds.

The public configuration deliberately contains no verified real settlement profiles, outcome manifests or account stake observations. The bundled public standard commission baselines remain unverified for any particular account. Unknown facts remain blocking reasons rather than favourable assumptions.

Statuses are `rejected` (non-positive calculation), `blocked_unverified` (positive calculation with an evidence or research-threshold failure), `paper_candidate` (current provider data passes configured paper assumptions) and `synthetic_candidate` (invented validation data passes its invented assumptions). Historical and public web observations can never receive `paper_candidate` status.

## Supplying evidence

The normalised schema is demonstrated in `data/public_nrl_2026-09-29.json` and the synthetic files. For the API adapter, configuration lookup keys are:

| Configuration map | Key | Value |
|---|---|---|
| `event_market_manifests` | `event_id|market_key` | `expected_outcomes`, `verified`, `evidence` |
| `market_rule_assignments` | `sport_key|market_key|bookmaker_key` | A settlement profile ID |
| `settlement_profiles` | Profile ID | `verified`, `signature`, `evidence_by_bookmaker` |
| `observed_limits` | `event_id|market_key|bookmaker_key|outcome|side` | `max_stake`, `min_stake`, `basis`, `source`, `updated_at` |
| `exchange_commissions` | Sport key | `rate` as a fraction, `verified`, `source` |
| `paper_venue_balances` | Bookmaker key | Assumed funds available at that venue |

The `signature` must provide all eight rule fields named above. Evidence should identify the exact market contract, rule URL/version, capture time and any applicable exception. Do not mark two rules identical merely because both are labelled “winner”. The profiles are user-supplied assertions checked for completeness and equality; the program does not interpret legal rule text. A practical rules review may require additional restrictions beyond these eight fields. For a real limit, use `basis: "observed"` or `"manual_verified"`; `"synthetic"` is only allowed for fixture data. `max_stake` is still evidence about capacity at a moment in time, not proof of a future fill.

The default operator list is a research allowlist checked against the ACMA register on 29 September 2026, not a recommendation or complete market directory. Unibet is retained only as a historical sample label and is not enabled as a verified current operator. Review licences, ownership and account terms before updating the configuration; the code does not recheck the register automatically.

## Delay and execution-risk analysis

The scanner tests 2, 5, 15 and 30 seconds. It fixes the first leg at the original quote and stake, then looks for later observations of the remaining legs, without using a quote captured after the target time. It accepts a snapshot at most one second before that target by default. Missing observations produce `not_observed`, not an assumed successful hedge. Feed timestamp freshness still applies.

The first-leg fill is an explicit hypothetical assumption. There are no actual fills. Stake sizes stay fixed for replay; the program does not optimise a rescue hedge. Repriced hedge legs must satisfy updated capacities, per-venue funds, total capital and rules. A missing hedge shows the possible unhedged loss. Separate stress scenarios apply adverse decimal-odds changes of 0, 0.01 and 0.05 and remaining-leg fill fractions of 0%, 50% and 100%. Each leg is also voided in turn to show asymmetric settlement exposure.

The synthetic two-way fixture illustrates the distinction: about AUD 36.35 under initial quotes and costs, −AUD 90.15 after the second price deteriorates at five seconds, and an unavailable hedge at 15 seconds. These are invented examples proving the checks work, not a successful betting record.

## Scope and interpretation

- V1 evaluates two- and three-outcome fixed-odds `h2h`/`outrights` markets and a cash back / same-selection exchange lay pair. The API collector requests `h2h` only.
- Exchange back prices are retained but not used to construct fixed-odds portfolios. Racing fields with more than three runners, totals, handicaps, each-way bets, promotions, middles, model-based value betting and multi-exchange portfolios are outside this version.
- A maximum combination count prevents runaway enumeration. Reaching it creates an explicit incomplete-coverage issue. Duplicate selection quotes cause the affected market to be rejected as ambiguous.
- Comparisons can share quotes and capital. Do not add their P&L or count them as independent opportunities. There is no simultaneous portfolio allocation, account restriction forecast or withdrawal-risk model.
- First seen means **first ingestion into this local ledger**, not the first time a bookmaker offered that price. Source timestamps, capture times, ingestion times and analysis times are distinct.
- The ledger preserves scan runs and rejected comparisons. Re-running on an old snapshot can change freshness decisions without overwriting the earlier run. This is not a tamper-proof third-party audit.

For a 30-day investigation, keep raw captures and the audit database; deduplicate overlapping opportunities; report missing/stale quote rates, limits/rule failures, delay coverage and survival, worst failed-hedge loss, and all data/subscription costs. Report any hypothetical model return separately from executed profit. This package does not establish successful real-money examples or promise low-risk income.

## Sources and provenance

- [The Odds API v4 documentation](https://the-odds-api.com/liveapi/guides/v4/) — API shape, timestamps, AU region and bet-limit fields; checked 29 Sep 2026.
- [Official historical odds sample page](https://the-odds-api.com/historical-odds-data/) and [AFL sample JSON](https://public-odds-api-sample-data.s3.amazonaws.com/historical-afl.json) — raw response included unchanged as `data/historical_afl_raw.json`; provider snapshot time 2022-04-24T23:55:00Z, downloaded 29 Sep 2026.
- [ACMA operator register](https://www.acma.gov.au/check-if-gambling-operator-legal) — research allowlist source; checked 29 Sep 2026.
- [Betfair Australia commission and charges](https://www.betfair.com.au/hub/help/commissions-charges/) — public standard rate baselines, not verified account-specific charges.
- [Sportsbet 2026 NRL Grand Final page](https://www.sportsbet.com.au/betting/rugby-league/nrl/nrl-grand-final-winner-2026-9699133) — observed 1.45 / 2.80; precise odds-update time unavailable.
- [Ladbrokes NRL tipping page](https://www.ladbrokes.com.au/blog/betting-info/nrl/tipping/) — observed 1.44 / 2.80; page dates its prices to 29 Sep 2026 without a precise quote time.

The scanner implements the paper-investigation recommendation in the earlier Australian betting research report. It is not affiliated with a bookmaker, exchange, odds supplier or Imperial Wealth.
