# Australian arbitrage research plan: establish the operator universe first

Reviewed 29 September 2026, Australia/Melbourne. Research and paper-only. This is the next-stage plan for the imported scanner; its original README, configuration and manifest remain the archived baseline.

## Review outcome

The initial handover moved directly from reproducing three example scans to a 30-day collection study. That skips the market inventory and data-coverage work needed to judge whether a study is representative. The default configuration has eight enabled operators and one disabled historical entry. It is an eligibility allowlist, not a national operator directory; adding names there would not make the existing Odds API adapter fetch their prices.

**Objective 1 is to identify and reconcile the Australian online wagering universe, then verify which sites are operating.** Do not stop at 130 names or treat 130 as a confirmed total. The count must follow the evidence and have an explicit denominator.

Working scope, inferred from this scanner: Australian-registered online sports/racing wagering services and exchanges. Retain fantasy products, telephone-only providers, inactive records and unresolved discoveries with separate classifications. Lotteries, physical gambling venues and offshore casino/poker sites are a separate census scope and are not counted as comparable bookmakers here. This delivery does not claim to identify every gambling business in those broader categories.

## Objective 1 — inventory and coverage reconciliation

The dated baseline is in [OPERATOR_INVENTORY.md](OPERATOR_INVENTORY.md), [operator_inventory.csv](operator_inventory.csv), and [operator_inventory.json](operator_inventory.json). Every ACMA record is retained in [register_reconciliation.json](register_reconciliation.json), including records excluded from the URL-service inventory.

1. Capture ACMA's complete register and downloadable JSON, with retrieval timestamps, page date and checksums. Cross-check national and state/territory records; preserve contradictory evidence instead of silently overwriting it.
2. Keep trading name, source URL, licence-holder name, jurisdiction, aliases, registration evidence, operational evidence and scanner mapping distinct. Shared licence holders do not automatically mean identical prices; separate brands do not automatically mean independent prices.
3. Reconcile commercial directories as discovery inputs. Record matched aliases, redirects, newly discovered brands and unresolved names. Never use an affiliate claim as licensing verification.
4. Verify each candidate website in batches: correct Australian domain, currently offered wagering product, launch/closure/rebrand status, public market availability and supporting source/date. A reachable home page is insufficient evidence of quote coverage. Record access failures as unknown, not closed. Do not create accounts or bypass access restrictions.
5. Publish separate counts for register rows, URL-service entries, domains, named licence holders, independently confirmed operating services, and scanner coverage. Preserve TAB's jurisdiction records but count its shared domain once; preserve PlayUp betting and Draftstars fantasy as different services on one host.

Acceptance: every source row has a disposition, no unresolved duplicate IDs, all aliases retain evidence, every licensing assertion is sourced, and all unresolved names/status conflicts are visible. **Register capture/reconciliation is complete for the saved snapshot; confirmation of every site's operational status remains open.** Do not claim a complete active-site census until the remaining checks are resolved or explicitly accounted for.

Refresh proposal: recheck licensing and operation before any new feed onboarding; take a weekly snapshot during an approved study and retain additions/removals/status changes. No refresh automation has been scheduled.

## Objective 2 — map obtainable prices to that universe

Build a coverage matrix per site: sport, market, exchange/bookmaker side, provider key, feed source, access permission, timestamps, refresh frequency, delay, missingness and cost. Separate `listed`, `feed_documented`, `observed_in_test_response`, and `paper_integrated`. Verify provider coverage using documentation and bounded, authorized test responses. A provider's AU-region flag does not prove coverage of every Australian site.

Prioritise a pilot after inventory coverage is visible, using achievable market overlap, pricing independence, data permission and all-in cost. Record unsupported sites as coverage gaps. Do not promise to scan all inventory entries with the current adapter.

## Objective 3 — verify market compatibility and paper controls

Review each included market's settlement contract, exhaustive outcomes, quote age/skew, commission, account-specific capacity evidence and any additional costs. Keep unknowns blocking. Retain rejected comparisons and execution-risk stress tests. The current scanner supports limited two/three-outcome fixed-odds and back/lay comparisons; a complete operator inventory does not expand those market types.

Do not bulk-enable inventory names in `config/default.json`. Add a provider mapping and reviewed evidence only when integrating a particular operator. Preserve historical fixtures and the disabled historical Unibet setting as baseline research until a separate config change is reviewed. Current register listing and historical fixture eligibility answer different questions.

## Objective 4 — run a bounded paper pilot, then assess a 30-day study

Propose the pilot's sports, providers, operator coverage, interval, request budget, duration and storage before starting sustained collection. Success is a reproducible measurement of data quality and conditional opportunities, including negative results. Track comparable coverage, quote freshness, missing evidence, cost-adjusted results, delay survival, failed-hedge exposure and shared-capital constraints. Deduplicate overlapping comparisons; never sum their hypothetical P&L as realised performance.

Proceed to a 30-day study only after the pilot establishes usable data and costs and Kelvin approves collection scope/budget. No wagers, deposits, account creation or paid/sustained collection are part of this plan update.

## Immediate next action

Resolve the three unmatched candidates and the Picklebet/PuntCity domain discrepancy, then verify operational status and feed coverage for the registered inventory. The full source reconciliation and limitations are in [2026-09-29-operator-verification.md](2026-09-29-operator-verification.md).
