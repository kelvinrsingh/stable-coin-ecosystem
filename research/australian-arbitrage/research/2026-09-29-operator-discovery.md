# Australian wagering universe: discovery packet

Date: 29 September 2026 (Australia/Melbourne). Status: discovered-but-unverified; verification follows separately.

## Intent and scope

Review the imported scanner plan and add missing Australian sites. Treat objective 1 as an inventory of Australian licensed online wagering brands and domains relevant to paper arbitrage, while retaining telephone-only and non-operational register entries for reconciliation. The user supplied a working estimate of 130 sites, not an acceptance target. Broader gambling (lotteries, fantasy products, physical venues and offshore casino sites) needs explicit classification and must not inflate the comparable wagering universe.

## Search landscape

Terms: Australian gambling sites, online bookmakers, betting brands, interactive wagering services, licence holder, corporate bookmaker, on-course bookmaker, exchange, telephone-only, inactive, acquired, unlaunched, lottery, fantasy.

| Source | URL | Role and discovery status |
|---|---|---|
| ACMA register | https://www.acma.gov.au/check-if-gambling-operator-legal | National official register; extract trading names, licence holders, URLs and authorities; listing alone does not prove an active website or available feed. |
| Northern Territory licensing | https://nt.gov.au/ | Official jurisdiction cross-check; exact register URL being located. |
| State racing/wagering authorities | Links from ACMA | Independent cross-check of licensing and scope; exact sources to be recorded in verification. |
| MyBettingSites directory | https://mybettingsites.com/au/articles/list-of-all-online-betting-sites-australia | Commercial discovery source claims 139 online sites as of 23 September 2026 plus unlaunched sites; not licensing evidence. |
| PuntGuide directory | https://puntguide.com.au/all-betting-sites | Commercial discovery source shows differing 130+/131/132 counts; not licensing evidence. |
| Betseeker directory | https://www.betseeker.com.au/list-of-all-online-betting-sites-in-australia/ | Broad commercial directory includes former/on-course brands; denominator differs from online active sites. |
| Existing scanner | ../README.md and ../config/default.json | Eight enabled current names and one disabled historical Unibet label; selected feed allowlist, not a national census. |

## Gaps and unresolved questions

- No authoritative exact count of 130 located in initial discovery.
- A register can mix trading names, telephone services, non-operational records and more than one domain per brand.
- Several brands can share one licence holder; this neither makes them one brand nor proves independent prices.
- Need compare commercial discovery names against ACMA and retain unmatched names as unresolved, not mark them licensed.
- Need separate register-listed status from operational website, product coverage, lawful/permissioned data access, quote quality and scanner integration.
- No access, feed permission, account capacity or settlement checks have yet been performed for the expanded universe.

## Verification pass

Capture the full ACMA table with source hash and timestamp; preserve raw names and URLs. Deduplicate exact domains, count registry rows/brands/entities separately, reconcile the existing configuration, and cross-check jurisdiction and directory differences. Produce CSV/JSON plus a readable inventory and a phased plan. Keep the imported runtime allowlist and evidence gates unchanged until operator integration is explicitly reviewed.
