# Australian wagering inventory: verification record

Checked 29 September 2026, Australia/Melbourne. Confidence: high in the captured register counts and reproduced joins; incomplete for the number of independently operating betting websites, per-site market coverage and ownership beyond the named licence holder.

## What the primary source establishes

The [ACMA register](https://www.acma.gov.au/check-if-gambling-operator-legal), whose page states last updated 7 September 2026, supplies 219 records. The direct [JSON export](https://www.acma.gov.au/data/interactive-gambling/json) also contains 219 records. The HTML table preserves status labels which the JSON export omits for some entries, so both were captured.

Table classification: 173 rows contain a URL; 30 are telephone-only; 15 explicitly non-operational; one (Pendlebury Bet) has no current URL without either label. Seven TAB jurisdiction rows share one URL. Two PlayUp-hosted products have different paths. This produces 167 distinct URL-service entries across 166 hostnames, **not 166 verified active betting sites**. Hostname normalization removes `www.`; it does not establish corporate ownership.

The original scanner configuration has eight enabled operators and one disabled historical Unibet entry. Register-derived inventory adds 159 service entries beyond the enabled eight (158 absent from all nine configuration records). The runtime configuration is unchanged. Current source evidence lists Unibet, so its historical disabled flag must not be mistaken for a statement that its current licence is absent.

## Discovery comparison and exceptions

The first table of [MyBettingSites](https://mybettingsites.com/au/articles/list-of-all-online-betting-sites-australia) contains 139 names; the page reports 23 September 2026. [PuntGuide](https://puntguide.com.au/all-betting-sites) supplied 138 cards in the captured HTML, including a coming-soon card, despite differing displayed headline counts. These commercial counts are not an authoritative census. The user's 130 estimate is therefore not adopted as an exact target.

| Item | Evidence and decision |
|---|---|
| BetShop | [ABN Lookup](https://abr.business.gov.au/ABN/View?id=35652847875) associates the business name with Winners Bookmaking. A fresh HTTPS request to `https://betshop.com.au` returned 200 after redirecting to `https://www.123bet.com.au:443/`. Retain as an observed 123bet alias, not another distinct active service. See `sources/domain_observations.json`. A business registration alone does not establish a wagering licence. |
| Cricketbet | [First-party VIP page](https://vip.cricketbet.com.au/) describes a restricted service and old regulator wording. No match established in the captured ACMA register. Keep discovered-but-unverified; current authorisation and operational access require further evidence. |
| Favbet | Australian name/domain found in a commercial directory with no captured ACMA brand match. [ABN Lookup](https://abr.business.gov.au/ABN/View?id=35652847875) also lists Favbet as a Winners Bookmaking business name from 29 July 2024; that does not establish a separate wagering service or current authorisation. A direct domain request failed TLS hostname verification. This is an access observation, not proof of closure or illegality. Keep unverified; do not infer Australian permission from a similarly named foreign operator. |
| HueyBet | Discovery card and indexed [first-party page](https://hueybet.com.au/) indicate coming soon; direct DNS resolution failed during this check. Keep unlaunched/unresolved, not active. |
| betr | [NT register](https://dth.nt.gov.au/boards-and-committees/wagering-commission/licensed-wagering-operators) marks its NT entry not trading; ACMA lists Tasmania. The [Tasmanian Government's 7 July 2026 announcement](https://www.premier.tas.gov.au/latest-news/2026/july/independent-commission-grants-new-licence) confirms a Tasmanian licence. Treat the NT entry as prior-jurisdiction evidence, not a national closure. |
| MyBet | ACMA has a non-operational NT record and a Victorian URL record. Preserve both jurisdiction records; do not apply the NT status to the Victorian entry just because names match. |
| Picklebet / PuntCity | ACMA lists `picklebet.com`; the NT register points PICKLEBET to `puntcity.com.au`. Retain the latter as an alternative domain requiring reconciliation, not an additional independent brand. |
| Draftstars / PlayUp | ACMA and NT show different fantasy/betting products under one PlayUp hostname. Preserve the product distinction; fantasy is outside the current scanner comparison scope. |
| Name variants | BetAus / BetAus Pty Ltd, Star Sports Australia / Star Sports, Punt123 / Punt123.bet, RobWaterhouse.com / Rob Waterhouse and PicnicBet / Picnicbet.com are recorded as explicit matching aliases. TAB is matched to its shared domain. |

## Jurisdiction cross-check coverage and limits

- [NT official register](https://dth.nt.gov.au/boards-and-committees/wagering-commission/licensed-wagering-operators): 50 numbered entries, including 10 marked not trading. This is not 50 independent active sites. Checked for the named discrepancies above.
- [WA regulator](https://www.wa.gov.au/organisation/racing-gaming-and-liquor/gaming-and-wagering-commission): identifies TABtouch and PlayWest, consistent with their presence in ACMA. TABtouch's ACMA mobile hostname is retained; other aliases are not assumed verified.
- [SA interstate authorisation register](https://www.cbs.sa.gov.au/sections/LGL/current-authorised-interstate-betting-operators): supplementary licence/jurisdiction evidence. It retains historical names and has some undated notices; it was not substituted for the national census. SA's [114 interstate operators in 2024–25 statistics](https://www.cbs.sa.gov.au/sections/LGL/gambling-regulation-statistics) measures a different population and time period.
- [Victoria online wagering guidance](https://www.vgccc.vic.gov.au/for-gambling-providers/wagering-and-betting/online-wagering-and-sports-betting-providers): registration and approval to operate online are separate checks. The linked live register endpoint timed out during independent review; a full row-level reconciliation remains open.
- [Racing NSW race-field approvals page](https://www.racingnsw.com.au/industry-forms-stakes-payment/race-field-copyright/approved-licensed-wagering-operators/) exposed 2020–21 lists; these were not accepted as current completeness evidence.
- ABN Lookup also lists Blokesbet, Betplay and Cracking odds under Winners Bookmaking. These are business-name discoveries, not identified additional websites, and are not counted as sites without domain/operational evidence.
- No full independent row-by-row census was completed for every state/territory register. ACMA remains the captured national baseline; this limitation must remain visible.

## Evidence states and remaining work

**Primary-source verified:** captured ACMA listing, row classification/counts, sourced jurisdiction facts above, and BetShop's observed redirect. This does not validate every operator's current activities or all site aliases.

**Curated project evidence:** generated CSV/JSON inventory, register and directory reconciliation, reproducible normalization, plus the revised plan. Source hashes and retrieval timestamps are in `sources/source_manifest.json`; full fetched HTML is retained locally and ignored by Git.

**Discovered-but-unverified:** three unmatched candidates, broad directory activity claims, per-site data access, operational status, product coverage, fees, settlement rules and capacity.

**Searched-but-not-found gaps:** an official exact national total of 130; current ACMA matches for the three candidates; complete operational checks of all domains.

**Unresolved questions:** Picklebet/PuntCity canonical domain, website activity/launch state, additional domain aliases and independent price formation. Lotteries and physical venues are outside this wagering inventory and require their own scope if desired.

Rebuild/validate with `python3 research/build_operator_inventory.py` from the scanner folder; the script uses saved inputs and no network. Run `python3 -m unittest discover -s tests -v` for the original scanner. This research does not validate commercial viability or authorise live betting.

## Validation and review receipt

- Existing scanner: 34 offline unit tests passed after the research additions.
- All 41 original archive-manifest file entries still match their original byte sizes and SHA-256 hashes.
- Independent review reproduced 219/173/167/166 source-row, URL-row, service and hostname counts, and the 274 matched / 3 unmatched directory reconciliation. No material issue found for the explicitly bounded register-snapshot scope.
- Objective-one operational verification is still open; neither the review nor passing tests promotes unknown sites to trusted runtime eligibility.
