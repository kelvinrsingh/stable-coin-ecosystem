"""Rebuild local research tables from preserved snapshots. No network, accounts or trades."""
import csv,json,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research'
def write_csv(name,rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
raw=json.loads((OUT/'raw/binance_book.json').read_text())
quotes={x['symbol'].removesuffix('USDT'):x for x in raw['data']}
trades=json.loads((OUT/'raw/alpaca_latest_trades.json').read_text())['trades']
# Ordinal research priorities: not expected-return rankings or buy signals.
items=[
('CRCL',1,'issuer','Direct reserve and distribution economics','Supply growth must exceed lower yields and distribution costs','Complete scenario model using current fully diluted capital; do not rely on higher terminal multiple','Two quarters retained economics per diluted share deteriorate or reserve/redemption impairment','Balances;reserve yield;distribution ratio;service revenue;SBC','High reported economics;low return confidence'),
('COIN',2,'distributor','Owns customer access and stablecoin distribution','USDC balances must grow retained contribution after rewards','Mid-cycle sum-of-parts works after rewards and allocated costs; avoid double counting Circle payouts','Two quarters lower net contribution with growing balances;adverse distribution renegotiation','USDC balances;rewards ratio;stablecoin revenue;trading cyclicality','High reported economics;low return confidence'),
('ETH',3,'settlement','Settlement gas and base-fee burn','Stablecoin use must improve economics per diluted ETH including L2 settlements','Reconcile 90-day fees attributable to stablecoins and net issuance;valuation holds at constant multiple','Adoption up but retained fees per diluted token down for two quarters;major security failure','Stablecoin gas;L1/L2 fee split;burn;issuance','High mechanism;incomplete valuation'),
('SOL',4,'settlement','Low-cost settlement;validator fees and base-fee burn','Real user retention must support fee economics after inflation','Separate burns from validator receipts and staking issuance;reconcile supply schedule and user retention','Economic growth only incentive-driven;two quarters declining per-token benefit','Payment users;base/priority fees;issuance;validator commissions','High mechanism;incomplete valuation'),
('TRX',5,'settlement','Energy and bandwidth economics','Stablecoin activity must support net burn/resource demand','Reconcile 90-day burn versus issuance and resource-rental economics;review issuer concentration','Issuer withdrawal or resource policy change defeats model','USDT concentration;burn;issuance;resource prices','High mechanism;medium completeness'),
('LINK',6,'data_interoperability','Paid services may fund reserve accumulation','External fee-funded purchases must matter relative to token releases','Reconcile 90-day reserve purchases and source of funds against release schedule','Reserve funded by treasury recycling;unexplained withdrawals;dilution overwhelms benefits','Paid services;reserve flows;70m annual stated releases','Medium;purchase attribution incomplete'),
('SKY',7,'stablecoin_protocol','Surplus can fund repurchases and holder rewards','Net surplus after savings rewards and losses must support net retirement','Verify executive execution and net retirements after distributions;reconcile credit costs','Negative sustainable surplus;depeg;governance diverts holder benefit','USDS demand;surplus;savings costs;burns;distributions','Medium;execution pending'),
('AAVE',8,'lending','Lending and GHO economics','Holder benefit must survive credit costs and governance','Verify buyback restart receipts or value without repurchases;reconcile incident losses','New bad debt or treasury shortfall;holder benefit redirected','Borrow demand;net revenue;bad debt;buyback receipts','Evidence hold: restart unverified'),
('V',9,'payments','Distribution network with stablecoin optionality','Core payments value must stand without speculative stablecoin revenue','Core-business valuation acceptable with zero incremental stablecoin profit assumed','Cannibalisation and costs exceed new fees','Core revenue;crossborder margins;settlement run rate;net take rate','High corporate data;low stablecoin attribution'),
('MA',10,'payments','Distribution and acquired stablecoin services','Incremental service profit must exceed acquisition and integration cost','Core valuation works;BVNK integration economics evidenced','Integration underperforms or legacy fee cannibalisation dominates','BVNK integration;services margins;capital returns','High corporate data;low stablecoin attribution'),
('PYPL',11,'payments','Checkout and PYUSD distribution optionality','Checkout and margin thesis must work independently','Core valuation works without assigning invented PYUSD earnings','Checkout/margins weaken;PYUSD rewards exceed retained economics','Checkout;transaction margin;rewards;PYUSD contribution','High corporate data;low stablecoin attribution'),
('XRP',12,'comparator','XRPL fees and account reserves','Stablecoin success must create material XRP demand','Quantify economic demand relative to float;partnerships alone fail gate','Stablecoin principal moves without material native-token demand','Fees;reserves;escrow net releases;native inventory','Mechanism known;holder capture weakly evidenced'),
('XLM',13,'comparator','Stellar fees and minimum balances','Stablecoin use must create material XLM demand','Quantify demand versus distribution;fee-pool accumulation not holder income','Usage rises without material native-token economics','Fees;minimum balances;SDF distributions','Mechanism known;holder capture weakly evidenced'),
('XPL',14,'new_chain','Stablecoin-oriented network','Incentive-free activity must fund security and token demand','Verify scheduled cliff actual release;liquidity retention;current fees and supply','Post-incentive outflows;dilution exceeds economic benefit','Cliff receipts;net releases;users;fee income','Conditional;unpriced and release unverified')]
rows=[]
for symbol,rank,layer,thesis,edge,entry,invalidation,monitor,confidence in items:
    if symbol in quotes:
        q=quotes[symbol];mark=(float(q['bidPrice'])+float(q['askPrice']))/2
        currency='USDT';timestamp=raw['retrieved_utc'];kind='Binance bid-ask midpoint; retrieval timestamp, not exchange trade time'
    elif symbol in trades:
        q=trades[symbol];mark=q['price'];currency='USD';timestamp=q['timestamp'];kind='Alpaca IEX last trade; prior US session; CRCL after-hours'
    else:mark='';currency='';timestamp='';kind='not_acquired'
    rows.append(dict(symbol=symbol,research_priority=rank,layer=layer,status='research_only_no_position',thesis=thesis,edge_hypothesis=edge,reference_price=mark,quote_currency=currency,reference_timestamp=timestamp,reference_kind=kind,entry_gate=entry,exit_or_invalidation=invalidation,monitoring_metrics=monitor,confidence=confidence,holding_period='3-5 years conditional on thesis',review_date='2026-12-29',paper_weight_now=0,paper_max_weight_of_research_sleeve_pct=10 if symbol in trades else 5,position_size_rule='Min(single-name cap;20pct shared-failure cap remaining);100pct loss assumption;no leverage',source_packet='equities_research.md' if symbol in trades else 'tokens_research.md'))
write_csv('paper_watchlist.csv',rows)
assets=json.loads((OUT/'raw/stablecoins.json').read_text())
snap=[]
for a in assets['data']['peggedAssets']:
    if a['symbol'] in ['USDT','USDC','USDS','USDe','DAI','PYUSD','RLUSD','USYC','BUIDL','GHO']:
        snap.append(dict(symbol=a['symbol'],nominal_usd_pegged_units=a.get('circulating',{}).get('peggedUSD'),provider_classification=a.get('pegMechanism'),retrieved_utc=assets['retrieved_utc'],source=assets['source_url'],status='provider_snapshot_not_issuer_audited;categories_not_equivalent'))
write_csv('stablecoin_snapshot.csv',snap)
chains=json.loads((OUT/'raw/stablecoin_chains.json').read_text())
write_csv('chain_snapshot.csv',[dict(chain=c['name'],provider_total_usd=sum(c['totalCirculatingUSD'].values()),retrieved_utc=chains['retrieved_utc'],source=chains['source_url'],status='provider_snapshot;no_market_share_until_universe_reconciled') for c in sorted(chains['data'],key=lambda x:sum(x['totalCirculatingUSD'].values()),reverse=True)[:15]])
sources=[]
for f in ['equities_sources.json','tokens_sources.json','risk_sources.json']:
    for s in json.loads((ROOT/f).read_text()):s['retrieved_date']='2026-09-29';s['research_packet']=f.replace('_sources.json','_research.md');sources.append(s)
for ident,url,title,claim,status in [
('M01','https://defillama.com/stablecoins','DefiLlama webpage','306.306bn headline; different from API snapshot','provider_snapshot_scope_unresolved'),
('M02',assets['source_url'],'DefiLlama assets API','427 records; nominal USD-peg subtotal313.019bn; contains heterogeneous products','provider_snapshot_scope_unresolved'),
('M03',chains['source_url'],'DefiLlama chain API','Chain totals from current API','provider_snapshot'),
('M04',raw['source_url'],'Binance bookTicker','Bid ask snapshots in USDT','primary_market_snapshot'),
('M05','https://docs.alpaca.markets/docs/market-data','Alpaca IEX connector','Latest trade response preserved; no execution suitability claimed','primary_market_snapshot'),
('M06','https://www.bis.org/publications/iii-anchoring-trust-money-innovation-beyond-stablecoins','BIS tokenisation countercase','Tokenised bank money competes with stablecoins','primary_institutional_analysis'),
('M07','https://www.circle.com/transparency','Circle reserve transparency','Reserve categories and report scope','primary_issuer_disclosure'),
('M08','https://stablecoins.llama.fi/stablecoincharts/all','DefiLlama aggregate chart','312.963bn USD-equivalent at2026-09-29T00:00Z; differing universe/time','provider_snapshot_scope_unresolved')]:
 sources.append(dict(id=ident,url=url,title=title,period='Retrieved 2026-09-29',claim=claim,status=status,retrieved_date='2026-09-29',research_packet='STABLECOIN_INVESTMENT_MAP.md'))
assert len({s['id'] for s in sources})==len(sources)
(OUT/'source_register.json').write_text(json.dumps(sources,indent=2))
write_csv('source_register.csv',sources)
print('Built',len(rows),'watchlist rows and',len(sources),'source entries.')
