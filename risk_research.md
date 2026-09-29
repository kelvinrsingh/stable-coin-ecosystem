# Stablecoin research: independent risk and evidence review

As of 29 September 2026 (Australia/Melbourne). Research support; paper-only. This note separates verified source statements from analytical requirements and hypotheses. Current web pages are not archived historical snapshots; preserve retrieval dates before later comparisons.

## Principal finding

The largest analytical failure would be to equate stablecoin supply or transfer growth with investment returns. Supply is a stock of liabilities; transfers are flows; protocol fees, issuer profit, and holder income are separate measures. Owning a stablecoin normally provides a redemption claim, not equity in its issuer. Token utility does not establish attractive valuation or an enforceable claim on earnings.

## Legal status: enacted, operative, and proposed are different

- **Australia digital asset platforms:** The Corporations Amendment (Digital Assets Framework) Act 2026 received assent 8 April 2026. Its commencement table specifies **8 April 2027**. It is enacted, with commencement pending at this research cutoff. Do not describe the entire platform reform as still merely an exposure draft, or as already effective. [Act text](https://www.legislation.gov.au/C2026A00038/asmade/2026-04-08/text/original/epub/OEBPS/document_1/document_1.html).
- **Existing Australian law:** ASIC INFO225 requires analysis of the rights and arrangements attached to each product; offshore or decentralised structure does not automatically remove Australian obligations. Its reference to platform exposure drafts is stale relative to the enacted Act above. Treat guidance as explanatory, not a substitute for checking legislation. [ASIC INFO225](https://www.asic.gov.au/regulatory-resources/digital-transformation/digital-assets-financial-products-and-services).
- **Australian payments reform:** Treasury describes the full Tranche 1 package as draft legislation released for feedback. This is a separate reform stream from the enacted digital-assets platform Act. The reviewed page does not establish that the payments package is enacted. [Treasury payments licensing](https://treasury.gov.au/policy-topics/banking-and-finance/payments-licensing-reforms).
- **United States:** GENIUS is enacted law, approved 18 July 2025. Section 20 sets general effect at the earlier of 18 months after enactment or 120 days after final implementing regulations by the primary federal regulators. The 18-month date is 18 January 2027. Separate provisions have their own timing; section 3(b)(1), for example, specifies three years after enactment for its offer/sale prohibition. [Public Law 119–27](https://www.govinfo.gov/content/pkg/PLAW-119publ27/pdf/PLAW-119publ27.pdf). The OCC's 19 August 2026 statement anticipated a final rule by November. This supports an implementation-stage description, not an assertion that all requirements already operate. A complete all-agency final-rule audit remains outstanding. [OCC statement](https://www.occ.gov/news-issuances/news-releases/2026/nr-occ-2026-69.html).

**Business requirement:** before a live issuance, custody, payment, exchange or advice service, obtain a product-specific licensing map including current law, new commencement dates, transitional relief and AML obligations. No inference that one licence, offshore provider or future reform covers the entire workflow.

## Reserve, redemption and operational checks

Circle's reviewed USDC terms require an eligible Circle Mint account for direct redemption, state that holders do not receive reserve interest, disclaim deposit insurance and allow freezes in specified circumstances. An exchange holder therefore cannot assume the same direct access as an eligible institutional customer. [USDC terms](https://www.circle.com/legal/usdc-terms).

Tether's reviewed terms require verified-customer status for direct issuance/redemption, permit minimum amounts and fees, and describe redemption rights as contractual. Check the specific issuer, token and jurisdiction rather than borrowing USDC assumptions. [Tether terms](https://tether.to/en/legal/).

Minimum evidence before including a stablecoin yield or liquidity position in a paper strategy:

| Failure mechanism | Required evidence and stress test |
|---|---|
| Reserve loss or illiquidity | Latest reserve composition and attestation period; maturity, counterparties, encumbrances and cash accessible during a weekend run; distinguish reserve attestation from a full financial audit. |
| Redemption bottleneck | Actual eligibility, minimum size, fees, bank cutoffs and fallback trading venues; model a 72-hour interruption and 5% secondary-market discount. |
| Custody insolvency | Identify legal entity, segregation, beneficial ownership, withdrawal controls and recovery priority; a wallet balance alone is insufficient. |
| Bridge failure | Identify native issuance versus a third-party wrapped claim, collateral location, signer/admin control and recovery procedure; aggregate original and wrapped exposure once. |
| Contract or governance failure | Verified deployment/version, upgrade and freeze authorities, timelocks, audit scope/date, unresolved findings and emergency exit path. An audit is evidence of a review, not insurance. |
| Correlated failure | Group exposure by issuer, custodian, reserve bank, blockchain, bridge and oracle. Different ticker symbols can share the same failure source. |
| Thin exits | Executable market depth after fees and slippage, withdrawal limits and network costs; stress market depth falling 80%. |

These stress sizes are analyst-selected tests, not forecasts or claims that the loss is capped at those levels. Catastrophic loss must remain possible in scenario analysis.

## Synthetic dollars require a separate model

Ethena describes USDe backing hedged with derivatives, with revenue from staking, futures funding/basis and liquid stable assets. Its FAQ explicitly says short positions pay longs when funding becomes negative and that negative periods can persist. Off-exchange custody is an issuer-described mitigation, not independently verified elimination of exchange or settlement risk. [Ethena FAQ](https://docs.ethena.fi/resources/faq).

Analytical requirement: model 30/90/180 days of negative net funding, hedge replacement costs, basis divergence, collateral markdown, delayed settlement and redemption concentration. Verify reserve-fund coverage against each combined loss and whether the mechanism changes as backing composition changes. Historical positive funding does not establish a risk-free yield. ENA ownership, USDe ownership and staked-USDe reward entitlement must be evaluated separately.

## AUD return and tax recordkeeping

Illustrative assumptions, not current FX quotes: invest AUD100,000 at AUD/USD 0.65, obtaining USD65,000 stablecoins at par. A hypothetical 5% USD yield produces USD68,250 before costs and tax.

| Exit AUD/USD | Ending AUD value | AUD return |
|---:|---:|---:|
| 0.75 (AUD stronger) | 91,000 | -9.00% |
| 0.65 (unchanged) | 105,000 | +5.00% |
| 0.55 (AUD weaker) | 124,090.91 | +24.09% |

Formula: AUD return = (1 + USD return) × entry AUD/USD ÷ exit AUD/USD − 1. A USD peg does not stabilise Australian purchasing power. Add conversion spreads, custody/protocol fees, depeg losses and taxes separately; no current 5% product is implied.

ATO recordkeeping guidance calls for transaction dates, purpose, counterparties, exchange/wallet records and AUD values. Record gross amounts, fees, transaction hashes and AUD conversions for every leg. Disposal and income classification depends on the arrangement and investor circumstances; this note gives no personalised tax conclusion. [ATO recordkeeping](https://www.ato.gov.au/individuals-and-families/investments-and-assets/crypto-asset-investments/keeping-crypto-records?anchor=Cryptoassettransactionrecords).

## Measuring adoption without overclaiming

- Visa distinguishes raw and adjusted volume; filtering targets bots, high-frequency transfers, bridge routing and internal exchange operations. Address classifications are probabilistic. Adjusted volume still includes non-payment categories and must not be labelled merchant spending. Archive the definition/version before comparing periods. [Visa methodology](https://www.visaonchainanalytics.com/transactions).
- Dune's catalog offers stablecoin transfers, balances, holder labels and payment datasets. Availability is verified; a particular SQL query's completeness and classification are not. Require query ID/revision, chain and contract coverage, UTC window, native/bridged treatment and source-transaction samples. [Dune catalog](https://dune.com/data).
- DefiLlama separates fees, protocol revenue and holder revenue, and explains that asset prices can change TVL without corresponding flows. Use the relevant metric and adapter; do not value a token on all user fees when much goes to suppliers. [Definitions](https://docs.llama.fi/analysts/data-definitions), [adapter methodology](https://docs.llama.fi/list-your-project/other-dashboards).
- Reconcile issuer liabilities against net outstanding issuance rather than summing every chain representation. Compare identical windows and universes. Investigate discrepancies rather than averaging inconsistent definitions.

## Business opportunities: hypotheses to validate

These are analyst hypotheses, not verified demand or recommendations to launch financial services.

| Hypothesis | Buyer and paid outcome | First experiment | Evidence to continue |
|---|---|---|---|
| Reconciliation and accounting | Finance teams needing stablecoin-to-bank/ledger traceability | Interview five teams; prototype read-only reconciliation of synthetic transactions | Two buyers agree to a paid pilot; exceptions materially reduced |
| Treasury risk monitoring | Businesses holding multiple stablecoins | A dated reserve/redemption/concentration report with linked evidence | Buyers identify decisions the report improves and will pay for |
| Payment integration | Exporters with measurable settlement friction | Compare one specific corridor's bank and stablecoin end-to-end cost using provider quotes | Net benefit survives FX, liquidity, compliance, refunds and support costs |
| Compliance workflow tooling | Regulated providers needing evidence trails | Interview licensed providers about one unresolved workflow | Verifiable budget, permissioned data access and a narrow deliverable |

Do not assume token issuance is the best business: distribution, banking access, trust, compliance costs and ongoing service quality can dominate the economics. Begin with non-custodial/read-only workflows and test willingness to pay before building.

## Independent critique and acceptance gates

1. **Who captures the value?** Require a diagram from customer payment to validator/provider/issuer profit to shareholder or tokenholder. Fail if the final step is only a narrative.
2. **Can adoption rise while returns fall?** Stress reserve yields halving, distribution payouts increasing and fee revenue per transfer falling 50%, separately and jointly.
3. **What is priced in?** Use diluted supply/shares, unlock schedules and conservative terminal assumptions. No ranked buy list without current prices, liquidity and valuation inputs.
4. **What is the benchmark?** Compare each thesis with cash/T-bill exposure, broad equities and relevant crypto benchmarks in AUD. High yield alone is insufficient compensation evidence.
5. **Can the position be exited?** A stop is not a guarantee through gaps, depegs, contract freezes or venue failure. Size hypothetical positions using loss and concentration budgets, not merely stop distance.
6. **What would falsify it?** Two reporting periods of falling retained revenue despite adoption growth; loss of market share without margins improving; token dilution exceeding economic benefit; implemented holder benefits disappearing; or unresolved material reserve/redemption concerns.
7. **What remains unverified?** Product-specific Australian access, all-agency US rule status, current executable prices/depth, complete beneficial ownership and reserve legal analysis, actual user willingness to pay. Keep these visible as gates, not silently assumed facts.

Suggested reviews: monthly metrics, quarterly thesis/valuation review, and immediate review after reserve, redemption, governance, security or regulatory events. This is a monitoring specification, not an installed automation.
