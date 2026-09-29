# Australian operator research inventory

ACMA snapshot retrieved 2026-09-29T10:09:45.223763+00:00 (page updated 2026-09-07).

**Complete reconciliation of 219 ACMA register rows**, including 173 URL-bearing rows grouped into **167 services on 166 hosts**. This verifies register coverage, not the number of currently active gambling sites. Seven rows share TAB; PlayUp betting and Draftstars fantasy retain different service paths.

These URL-bearing services name 121 normalized licence-holder strings; these are not independently resolved corporate entities. Betfair is classified as exchange and Draftstars as fantasy; other product categories remain individually unverified. Feed/API coverage is unverified by this inventory for every service.

30 telephone-only, 15 explicitly non-operational and 1 no-URL records are classified in [register_reconciliation.json](register_reconciliation.json). All 219 JSON-export records match the table after status-suffix, HTML-entity and whitespace/punctuation normalization.

The scanner has 8 existing enabled operator entries and 9 entries in total (Unibet disabled). **159 registered services are outside the enabled set; 158 are absent from all config.** Research inventory additions do not enable collection, adapters or betting. An enabled config entry is only the existing licence/source gate, not proof of technical support or current operability.

Commercial directories contribute 277 records; 274 match register records and 3 remain unverified candidates. BetShop is reconciled as a 123bet redirect alias, not an extra site. Directory links and active claims are retained as unverified evidence; they never replace the registered URL. Read [verification notes](2026-09-29-operator-verification.md).

This scope includes registered wagering/exchange/fantasy services. It is not a census of lotteries, land-based casinos or offshore sites. The claimed total of 130 is not an acceptance target. Operational status remains unverified for every row pending individual review.

Rebuild: `python3 research/build_operator_inventory.py`; verify without changes: `python3 research/build_operator_inventory.py --check` (from the scanner folder). No network access or third-party packages are used. Input SHA-256 hashes and export parity are checked before output generation. Full provenance, holder/authority arrays and raw rows are in [JSON](operator_inventory.json); [CSV](operator_inventory.csv) preserves all fields.

| Site/service | Registered domain/path | Licence holder(s) | Evidence | Existing runtime config |
|---|---|---|---|---|
| 123bet | 123bet.com.au | Winners Bookmaking Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 1 | not configured |
| Allbets | allbets.com.au | Allbets.com.au Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 2 | not configured |
| BaggyBet | baggybet.com | BaggyBet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 6 | not configured |
| Ballr Bet | ballrbet.com | Ballr Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 7 | not configured |
| BearBet | bearbet.com.au | Bet Holdings Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 9 | not configured |
| BeastBet | beastbet.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 10 | not configured |
| Bet Alpha | betalpha.au | Mintsports Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 12 | not configured |
| Bet Bunker | betbunker.com.au | W Woodcock and V Moriarty Partnership | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 13 | not configured |
| Bet Buzz | betbuzz.au | Mintsports Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 14 | not configured |
| Bet Dash | betdash.com.au | Oke, Norman | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 15 | not configured |
| Bet Dragon | betdragon.au | Mintsports Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 16 | not configured |
| Bet Legends | betlegends.com.au | Beirne Racing Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 17 | not configured |
| Bet Nation | betnation.com.au | Amused Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 18 | not configured |
| Bet Right | betright.com.au | IRPSX Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 19 | enabled: betright |
| Bet Rush | betrush.com.au | Bet Rush Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 20 | not configured |
| Bet Supreme | betsupreme.com.au | Bet Supreme Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 21 | not configured |
| Bet You Can | betyoucan.au | Bet You Can Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 22 | not configured |
| bet365 | bet365.com.au | Hillside (Australia New Media) Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 23 | not configured |
| Bet777 | bet777.com.au | Bet777 Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 24 | not configured |
| Betabets | betabets.com.au | Graham, William | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 25 | not configured |
| BetAces | betaces.com.au | Millet, Carl | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 26 | not configured |
| Betaroo | betaroo.com.au | Betaroo Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 27 | not configured |
| BetAus Pty Ltd | betaus.com.au | BetAus Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 28 | not configured |
| BetBetBet | betbetbet.net.au | Betbetbet Partnership | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 29 | not configured |
| BetBlitz | betblitz.com.au | Frank Hudson Partnership | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 30 | not configured |
| BetBull | betbull.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 32 | not configured |
| Betchamps | betchamps.com.au | Millett, Carl | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 33 | not configured |
| Betcoin | betcoin.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 34 | not configured |
| BetDeluxe | betdeluxe.com.au | Amused Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 35 | not configured |
| BetEstate | betestate.com.au | Betestate Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 37 | not configured |
| BetExpress | betexpress.com.au | Amused Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 38 | not configured |
| Betfair | betfair.com.au | Betfair Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 39 | enabled: betfair_ex_au |
| BetFans | betfans.com.au | BetFans Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 40 | not configured |
| Betfocus | betfocus.com.au | Betfocus Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 41 | not configured |
| BetGalaxy | betgalaxy.com.au | Track Pursuits Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 42 | not configured |
| BetGold | betgold.com.au | Betgold Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 43 | not configured |
| Betit | betit.com.au | Booki.com.au Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 44 | not configured |
| BetJet | betjet.com.au | Amused Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 45 | not configured |
| BetJoey | betjoey.com.au | Engellener, Gregory John | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 46 | not configured |
| BetLocal | betlocal.com.au | Betlocal Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 48 | not configured |
| Betnova | betnova.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 51 | not configured |
| Betnow | betnow.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 52 | not configured |
| BetPinnacle | betpinnacle.com.au | Winners Bookmaking Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 53 | not configured |
| BetProfessor | betprofessor.com.au | Giant Bet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 54 | not configured |
| betr | betr.com.au | Betr Entertainment Aus Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 55 | not configured |
| BetRaven | betraven.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 56 | not configured |
| BetReal | betreal.com.au | Crownsport Aust. Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 57 | not configured |
| BetStation | betstation.com.au | Mansour, Gavin | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 58 | not configured |
| BetStorm | betstorm.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 59 | not configured |
| Betzooka | betzooka.com.au | Bossbet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 60 | not configured |
| BigBet | bigbet.com.au | Amused Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 61 | not configured |
| BlondeBet | blondebet.com.au | Pendlebury Bookmaking Pty Limited | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 62 | not configured |
| BookiePrice | bookieprice.com | Michener, Steven | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 63 | not configured |
| Boostbet | boostbet.com.au | Boostbet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 65 | not configured |
| BossBet | bossbet.com.au | Bossbet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 66 | not configured |
| Business-Bet | businessbet.com.au | Doughty, Anthony | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 68 | not configured |
| CapitalBet | capitalbet.com.au | Capital Bet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 69 | not configured |
| Cash Cage | cashcage.com.au | Cash Cage Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 70 | not configured |
| Chasebet | chasebet.com.au | Harris Bookmaking Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 71 | not configured |
| ChromaBet | chromabet.com.au | G & T Mansour | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 72 | not configured |
| ClubBet | clubbet.au | ClubBet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 74 | not configured |
| Colossalbet | colossalbet.com.au | Ryman, Mark | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 75 | not configured |
| Cricketbet | Unverified (see directory evidence) | Unverified | [Regulator match unresolved](2026-09-29-operator-verification.md) | not configured |
| CrownBet | crownbet.com.au | Betfair Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 76 | not configured |
| Dabble | dabble.com.au | Dabble Sports Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 77 | not configured |
| Dafabet | dafabet.com.au | BaggyBet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 78 | not configured |
| DashBet | dashbet.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 80 | not configured |
| DependaBet | dependabet.com.au | Pendlebury Bookmaking Pty Limited | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 81 | not configured |
| Donnie Bet | donniebet.com.au | Mcgrath & Mcgrath | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 82 | not configured |
| Draftstars | playup.com.au/fantasy | Nextbet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 83 | not configured |
| EarlyCrow | earlycrow.bet | Booki.com.au Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 84 | not configured |
| EliteBet | elitebet.com.au | Paolini, Daniel | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 85 | not configured |
| EpicOdds | epicodds.com.au | Vuka Global Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 87 | not configured |
| FalconBet | falconbet.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 88 | not configured |
| FatBet | fatbet.com.au | FatBet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 89 | not configured |
| Favbet | Unverified (see directory evidence) | Unverified | [Regulator match unresolved](2026-09-29-operator-verification.md) | not configured |
| FireBet | firebet.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 90 | not configured |
| GemBet | gembet.com.au | GemBet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 93 | not configured |
| GoldBet | goldbet.com.au | Goldbet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 95 | not configured |
| GoldenBet888 | goldenbet888.com.au | Fortuna Felicitas Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 96 | not configured |
| GRSBet | grsbet.com.au | Crispe, Stephen | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 97 | not configured |
| HAVABET | havabet.com.au | Havabet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 98 | not configured |
| HOT Bet | hotbet.com.au | Deguara Bookmaking Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 99 | not configured |
| HueyBet | Unverified (see directory evidence) | Unverified | [Regulator match unresolved](2026-09-29-operator-verification.md) | not configured |
| IceBet | icebet.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 100 | not configured |
| Infomarket | infomarket.com.au | IRPSX Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 101 | not configured |
| Jimmy Bet | jimmybet.com.au | Jimmybet Partnership | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 103 | not configured |
| JuicyBet | juicybet.com.au | Juicybet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 105 | not configured |
| Junglebet | junglebet.com.au | Jungle Strategic Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 106 | not configured |
| JustBet | justbet.com.au | Justbet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 107 | not configured |
| Knucklebet | knucklebet.com.au | Booki.com.au Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 108 | not configured |
| Ladbrokes | ladbrokes.com.au | Entain Group Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 109 | enabled: ladbrokes |
| LaserBet | laserbet.com.au | LaserBet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 110 | not configured |
| Let's Bet | letsbet.net.au | Let's Bet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 111 | not configured |
| LightningBet | lightningbet.com.au | Lynch, Grant | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 112 | not configured |
| MarantelliBet | marantellibet.com | MarantelliBet Partnership | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 115 | not configured |
| McBet | mcbet.com.au | D McLauchlan & L McLauchlan Partnership | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 117 | not configured |
| Midasbet | midasbet.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 119 | not configured |
| MightyBet | mightybet.com.au | Amused Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 120 | not configured |
| Millennial Bet | millennialbet.com.au | Pendlebury Bookmaking Pty Limited | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 121 | not configured |
| MintBet | mintbet.au | Mintsports Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 122 | not configured |
| MoonBet | moonbet.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 123 | not configured |
| Multis.com.au | multis.com.au | Multis.com.au Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 124 | not configured |
| MyBet | mybet.com.au | Mybet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 127 | not configured |
| Neds | neds.com.au | Entain Group Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 128 | enabled: neds |
| Next2Go | next2go.com.au | Zinger Bookmaking Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 129 | not configured |
| Nextbet | nextbet.com.au | Nextbet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 130 | not configured |
| Ninjabet | ninjabet.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 131 | not configured |
| Noisy | noisy.com.au | Amused Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 132 | not configured |
| Oke Bet | okebet.com.au | Opie, Mark | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 133 | not configured |
| OnlyBets | onlybets.com.au | OnlyBetting Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 134 | not configured |
| Palmerbet | palmerbet.com | Palmer Bookmaking Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 135 | enabled: palmerbet |
| Pandabet | pandabet.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 136 | not configured |
| Picklebet | picklebet.com | Puntaa Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 142 | not configured |
| Picnicbet.com | picnicbet.com | Boncorp Holdings Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 143 | not configured |
| PlayUp | playup.com.au/betting | Nextbet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 145 | not configured |
| PlayWest | playwestbet.com | PlayWest Pty Limited | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 146 | not configured |
| PointsBet | pointsbet.com.au | Pointsbet Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 147 | enabled: pointsbetau |
| PonyBet | ponybet.com.au | Booki.com.au Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 148 | not configured |
| Premiumbet | premiumbet.com.au | Hudson, Frank | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 149 | not configured |
| PulseBet | pulsebet.com.au | Amused Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 150 | not configured |
| Punt123.bet | punt123.bet | Harrak, Michael | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 151 | not configured |
| Puntnow | puntnow.com.au | Puntnow Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 153 | not configured |
| PuntSport | puntsport.com.au | Winners Bookmaking Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 154 | not configured |
| PuntX | puntx.com.au | Zinger Bookmaking Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 155 | not configured |
| PuntZone | puntzone.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 156 | not configured |
| QuestBet | questbet.com.au | Questbet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 157 | not configured |
| Readybet | readybet.com.au | Readybet Partnership | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 160 | not configured |
| RealBookie | realbookie.com.au | Realbookie.com.au Partnership | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 161 | not configured |
| RedBet | redbet.com.au | G & N Oke Partnership | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 162 | not configured |
| Ripper Bet | ripperbet.au | Mintsports Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 163 | not configured |
| RiverBet | riverbet.com.au | RiverBet Partnership | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 164 | not configured |
| Rob Waterhouse | robwaterhouse.com | Waterhouse, Robert | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 165 | not configured |
| Rooster Bet | roosterbet.com.au | Rooster Bet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 166 | not configured |
| RoyalBet | royalbet.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 167 | not configured |
| RushBet | rushbet.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 168 | not configured |
| SonicBet | sonicbet.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 174 | not configured |
| SpicyBet | spicybet.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 175 | not configured |
| Sportsbet | sportsbet.com.au | Sportsbet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 176 | enabled: sportsbet |
| Sprintbet | sprintbet.com.au | Sprintbet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 177 | not configured |
| StableBet | stablebet.com.au | VistaBet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 178 | not configured |
| Star Sports | starsports.com.au | Star Sports Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 179 | not configured |
| SteakBet | steakbet.com.au | SteakBet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 180 | not configured |
| StrikeBet | strikebet.com.au | Betting Services Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 182 | not configured |
| Surge | surge.com.au | Amused Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 183 | not configured |
| Swift Bet | swiftbet.com.au | Swift Bet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 184 | not configured |
| TAB | tab.com.au | TAB Limited; Tabcorp ACT Pty Ltd; Tabcorp Vic Pty Ltd; UBET NT Pty Ltd; UBET QLD Limited; UBET SA Pty Ltd; UBET Tas Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 185, 186, 187, 188, 189, 190, 191 | enabled: tab |
| TabTouch | tabtouch.mobi | Racing and Wagering Western Australia | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 192 | not configured |
| Teambet | teambet.com.au | Bet Focus Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 193 | not configured |
| TechBet | techbet.com.au | Doherty, Leah-Jane | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 194 | not configured |
| TempleBet | templebet.com.au | McLauchlan, David | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 195 | not configured |
| Terrybet | terrybet.com.au | Coelli, Terrence | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 196 | not configured |
| Titanbet | titanbet.com.au | TitanBet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 197 | not configured |
| Topbet | topbet.au | Betsmarter Group Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 198 | not configured |
| TradieBET | tradie.bet | Bonus Kingdom Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 200 | not configured |
| TrueBet | truebet.com.au | Truebet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 201 | not configured |
| UltraBet | ultrabet.com.au | UltraBet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 202 | not configured |
| Unibet | unibet.com.au | Betchoice Corporation Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 203 | disabled: unibet |
| UPCOZ | upcoz.com | UPCOZ Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 204 | not configured |
| UpYaGo | upyago.com.au | Zinger Bookmaking Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 205 | not configured |
| VicBet | vicbet.com | Vicbet Partnership | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 206 | not configured |
| Wannabet | wannabet.com.au | Phillips, Eric Roger | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 210 | not configured |
| Wellbet | wellbet.com.au | Wellbet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 211 | not configured |
| Winners | winners.com.au | Winners Bookmaking Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 212 | not configured |
| WinnersBet | winnersbet.com.au | Winnersbet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 213 | not configured |
| Wishbet | wishbet.com.au | J.S Walsh, J.D Walsh, M.J O'toole & P.W Jones | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 214 | not configured |
| WizBet | wizbet.com.au | Wizbet Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 215 | not configured |
| XBet | xbet.net.au | Millett, Carl | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 217 | not configured |
| Xcelbet | xcelbet.com.au | Dwyer, David Darcy | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 218 | not configured |
| YesBet | yesbet.com.au | Amused Australia Pty Ltd | [ACMA](https://www.acma.gov.au/check-if-gambling-operator-legal) rows 219 | not configured |
