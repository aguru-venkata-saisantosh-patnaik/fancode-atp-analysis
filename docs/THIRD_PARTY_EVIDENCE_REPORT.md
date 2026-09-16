# FanCode ATP: expanded evidence and estimation plan

Author: Competition team  
Research snapshot: 14 September 2026  
Release: raw-v3-2026-09-14

## What this research changes

The third pass adds **40 public-source requests, including original research reports, specialist reporting, vendor rate cards and structured data**. Of these requests, 37 retrieved substantive or reviewable responses and 3 failed. One additional browser observation is preserved. The complete collection contains 295 raw files, 244,791,967 bytes, 191 HTTP source IDs, 14 browser observations and the seven supplied PDFs. Offline integrity and selected evidence checks passed. Original responses are preserved before interpretation. All earlier raw files remain unchanged. The [source catalog](THIRD_PARTY_SOURCE_CATALOG.md) lists every addition, including failures and rejected quantitative evidence.

We now have a substantially stronger basis for market context, competitor comparisons, campaign cost scenarios and schedule analysis. We still do not have FanCode customer-level conversion, cross-sport ownership, incremental lift, willingness to pay or contract costs. No third-party article found in this pass establishes those internal quantities. They must remain explicit unknowns, with decision thresholds replacing unsupported point estimates.

The most valuable additions are:

1. A direct India Tennis TV App Store price listing.
2. India-specific sports-interest surveys with identifiable populations and methods.
3. The latest Ormax OTT release, published on 10 September, plus the full FICCI-EY 2026 report.
4. A reported FanCode F1 engagement figure, carefully separated from paid subscribers.
5. FanCode's published referral reward schedule and existing creator-partnership evidence.
6. Public payment, streaming and messaging cost references.
7. A structured F1 calendar with UTC clocks and a tennis-results clock sample whose timezone remains ambiguous.

## 1. Audience sizing: stronger sources, incompatible denominators

| Source | Accepted observation | Appropriate use | Prohibited inference |
|---|---|---|---|
| IBM / Morning Consult, June 2025 | India adult sports-fan sample: tennis 37%, soccer 60%, F1 22%, cricket 91%. Online, unweighted, n=2,209 | Within-survey interest comparison and hypotheses for content pathways | Percentages of all Indians, paid subscribers, or cross-sport overlap |
| YouGov, data extracted January 2025 | Page-6 chart: 2024 tennis 23%, football 23%, cricket 55%. Chart N≈30,000, labelled Nat Rep, while headline refers to urban Indians | Separate population context, with the source's definition tension visible | Averaging with IBM or treating this as a survey of cricket fans only |
| Ormax sports research, 2024 | 678 million annual TV/OTT sports viewers, 305 million football viewers. Sports viewing threshold: at least 30 minutes in a year | Broad historical reach context | Addressable ATP subscriber market |
| Ormax OTT release, September 2026 | 664.9 million monthly online-video viewers, 172.6 million active paid subscriptions, 206.9 million CTV viewers | Current distribution context. Paid subscriptions include bundles and must have been used in the last month | 172.6 million unique paying people |
| FICCI-EY 2026, reporting 2025 | 216 million year-end video subscriptions, 143 million subscribing households, 71% of subscriptions bundled | Explain distribution through bundles and why subscription counts differ across studies | Combining EY contracts and Ormax active subscriptions into a growth series |

Sources: IBM PDF pp. 3, 60–61 [1], YouGov pp. 4, 6 [2], Ormax [3–4], FICCI-EY p. 45 [5]. The IBM and YouGov charts were visually checked against their PDF pages, rather than inferred from extracted text order.

**The decision implication:** market size should be presented as a ladder of different populations: sports attention → relevant sports interest → eligible reachable audience → incremental paid buyers. Only the first two layers have credible public estimates. Later layers require scenarios or internal measurement. Do not multiply unrelated surveys to manufacture a precise subscriber TAM.

The IBM marginal percentages can support a useful future notebook on **bounds for audience overlap**. Given two marginal shares on the same base, their intersection lies between `max(0, a+b−1)` and `min(a,b)`. These are mathematical limits, not measured cross-sport overlap. Broad limits would itself demonstrate why ownership and expressed interest must determine the targeting rule. MotoGP is not a separate option in the IBM table and must not inherit the F1 share.

## 2. Company scale: evidence of reach, not a payer denominator

A 20 January 2026 Mint interview attributes to FanCode's cofounder a figure of **more than 21 million fans engaging with F1 on the platform**, up 18% year on year. The article does not provide the measurement window or a paying-user definition. Use it as a reported scale indicator, never as the F1 subscriber cohort. [6]

The Google Cloud case study, dated December 2024, describes real-time personalisation and reports more than 160 million users. The older AWS case study reports more than 80 million users in 2022 and a cricket-event peak of six million concurrent viewers. These demonstrate historical platform capability. They do not establish current monthly actives, ATP audience, supplier exclusivity or cost per viewer. [7–8]

The Inc42 FY25 financial report is for **Dream Sports as a group**. Goods-and-services revenue is not a clean FanCode streaming segment, and group marketing spending cannot be assigned to ATP. The rights announcement and Moneycontrol coverage establish ATP rights through 2028 but disclose no fee. [9–10]

**Action for analysis:** maintain separate fields for registered/reported users, engaged audience, viewers, subscriptions and unique payers. No unit-economics model should divide by one merely because another is missing.

## 3. Prices and entitlements: one gap closed, others remain

Tennis TV's India App Store featured subscriptions show **₹449 monthly, ₹2,500 for six months and ₹4,499 annually**, with automatic renewal. These are India in-app listing prices, not verified web checkout prices. The competitor table can now use a dated, route-specific comparator. It must preserve content and device differences. [11]

FanCode's additional public tour route `/content/subscribe/tour/5832` produced a generic page without an identifiable offer. Its TimesPrime page and terms did not explicitly settle ATP inclusion in the monthly pass. Generic “all applicable” services wording is insufficient to close that question. [12–13]

Retain the existing two branches:

- **Monthly includes ATP:** compare tournament purchases against applicable monthly offers, renewal conditions and the remaining viewing calendar.
- **Monthly excludes ATP:** compare tournament versus season access, with yearly access as a separate multisport option.

Keep the brief's ₹399 ATP season and ₹79–99 tournament prices labelled **case inputs**. The current ATP checkout price remains unverified. Public FanCode monthly/yearly offers already collected are route-specific observations. Neither a footer naming tennis nor a coupon/referral anecdote proves entitlement.

The public terms describe recurring monthly/annual renewal in general, but do not identify the next charge for a particular promotional offer. They also allow prices to vary by time and purchase device. This supports a route-aware price audit, not a claim that a proposed pricing rule has already been implemented. [13]

## 4. Acquisition economics: replace guessed CACs with visible cost drivers

| Cost component | Public evidence | How to use it |
|---|---|---|
| Payment processing | Razorpay standard 2% plus GST, with enterprise pricing available | External gateway-rate scenario. Distinguish fee from tax on the fee and input credits |
| Streaming delivery | Cloudflare Stream: US$1 per 1,000 delivered minutes | External usage-cost reference. Not a quote for FanCode's sports infrastructure |
| Video storage | Cloudflare: US$5 per month per 1,000 stored minutes | Separate stored content from viewer consumption |
| WhatsApp marketing | ₹0.8631 per message in the January 2026 INR card, also reported by a July vendor study | Dated rate reference. Add provider charges and tax separately. Current official docs refer to July cards but the captured table omitted numeric download links |
| SMS | Rival-written August comparison quotes MSG91 ₹0.16–0.25 per SMS by volume, excluding GST | Lower-confidence vendor quote range. Direct SMS rate table was not recovered |
| Meta prospecting | Agency D2C article reports category-specific CPCs spanning ₹5–18 and CPMs ₹70–210 | External sensitivity envelope only. No audited sports-subscription benchmark |
| Creators | Previously saved Kofluence public report: nano creators ₹500–5,000 per reel, micro ₹2,500–80,000 per campaign | Preserve different deliverables and wide variation. Not named-creator quotations |
| Install campaigns | Previously saved Media Ant quotes include Instagram ₹33–37 and Facebook ₹37–41 per install | Install cost is not payer CAC. Keep base and offered rates separate |

Sources: [14–20] and existing v2 vendor snapshots. The [machine-readable register](../config/external_evidence_registry.json) records selected values and limits. Supplier prices are not independent measurements of FanCode spending.

A future channel table should print **both a derived cost range and the threshold required to meet the case target**:

- Click campaign: `media CAC = CPC / click-to-first-payer conversion`.
- Impression campaign: `media CAC = CPM / (1000 × CTR × click-to-first-payer conversion)`.
- Install campaign: `media CAC = CPI / install-to-first-payer conversion`.
- Creator campaign: `(fee + production + amplification + incentive costs) / incremental first payers`.
- Messaging: `(delivered messages × unit rate + platform + creative costs) / incremental first payers`.
- Owned channels: assign creative, engineering, delivery and measurement costs. Zero media buying does not mean zero total cost.

Use one internally consistent funnel at a time. Do not independently combine a favourable CPC, CPM and CTR from incompatible campaigns. Separate paid-channel media CAC from fully loaded CAC, and attributed buyers from incremental buyers.

RevenueCat's 2026 report provides useful external conversion and renewal comparisons, but its apps, regions and subscription structures differ from FanCode. Its 1.4% D35 conversion statistic is grouped by **developer headquarters in India/Southeast Asia**, not by Indian consumers. Use it only as a clearly labelled stress comparison, not a FanCode conversion estimate. [21]

**Derived illustration, not a forecast:** at the existing ₹33–37 Instagram install quotes, an overall ₹200 media-CAC limit requires 16.5–18.5% of installs to become first payers, before overhead or incrementality adjustments. This threshold is more decision-useful than claiming install campaigns will meet ₹200. The calculation must later be reproduced in the economics notebook.

## 5. Referral rewards: a material new audit item

FanCode's published referral matrix lists voucher face values of ₹25, ₹75, ₹150 and ₹500 against purchase bands ₹1–25, ₹26–75, ₹76–199 and ₹200+. It specifies new-payer eligibility. **Live availability, redemption, actual procurement cost and partner funding are not known.** [13]

Do not call referral traffic inherently cheap. A first-purchase contribution test should include `reward face value × funded cost fraction × payout probability`, plus buyer discounts and fraud/administration costs. A published reward is prior art, not proof of observed CAC or causal lift. Referred users who would have purchased anyway remain a measurement problem.

The creative opportunity is a carefully capped, measurable mechanism with a clear benefit to users. Its originality must come from the eligibility, timing, economics and experiment, rather than claiming to invent referrals.

## 6. Retention, willingness to pay and novelty

Public app reviews remain suitable for identifying viewing and purchase friction, with the previously documented selection limits. They cannot supply churn rates, segment prevalence or price elasticity. No respondents are available, so no conjoint or price-sensitivity survey will be represented as conducted.

The COTT white paper's 78% churn statement was **excluded from numerical inputs** because its passage does not define a usable horizon, cohort or comparison. A precise-looking percentage without those definitions is less useful than an explicit scenario. [22]

The Desi Racing Co portfolio reports a FanCode partnership covering F1 in 2024 and MotoGP in 2025, using reels, tweets and stories to explain passes. Creator education is therefore feasible prior art, but the portfolio provides no price, conversion or lift. [23]

Tennis TV already offers player following, alerts, highlights, replay formats and spoiler controls. The previously captured ATP Collect announcement also establishes existing collection mechanics. The presentation should distinguish ordinary capabilities from the proposed improvement in **which person gets which offer, at which viewing opportunity, with what contribution and test**. [11]

Ormax Sports Track demonstrates that professional sports research already distinguishes awareness, reach, appeal and perceived strength of a property. Its live tournament estimates are paid and unavailable here. Use the public methodology to sharpen measurement definitions, not to fabricate ATP scores. [24]

## 7. Timing and sport-to-sport journeys

The Jolpica snapshot contains **23 F1 rounds with UTC race clocks** and additional session fields. Its documentation explicitly defines the timezone. The unusual Bahrain-in-Malaysia entry is corroborated by an official F1 announcement for 2–4 October 2026. That check prevents an incorrect rejection based on an outdated calendar. [25–27]

This supplies a stronger F1 comparison layer for the planned ATP viewing-session sample. The future notebook must distinguish race-start points from viewing intervals, account for UTC date rollovers, and show assumed durations separately. A Sunday clash requires overlapping intervals, not merely matching dates.

Tennis Explorer supplied a public 29 August results page with displayed clocks. However, the header says GMT+1 while its tooltip names Berlin/Prague/Vienna, creating a summer-time ambiguity. The page also does not establish whether clocks are actual or scheduled starts. Retain it for reconciliation, but **do not promote it into a complete actual-start dataset**. [28]

The official ATP session sample remains the principal timing evidence. Full-season exact match starts, a comprehensive football kickoff export and equivalent MotoGP session timing remain incomplete. Additional secondary timestamps only become eligible after timezone, edition, match identity and schedule semantics are verified.

## 8. What remains unavailable, and how we will handle it

| Missing fact | Status after third pass | Treatment in subsequent analysis |
|---|---|---|
| ATP rights fee and allocated production cost | Not disclosed in retrieved rights coverage | Contribution frontier and required payers per ₹1 crore of fixed cost. Do not estimate from unrelated sports rights |
| FanCode tennis payer counts and pass ownership | No qualifying external disclosure recovered | Cohort sizes remain variables. No market-share inference from downloads or engaged users |
| F1/football/MotoGP-to-tennis overlap | Public marginal interest only | Ownership-by-sport decision matrix, overlap bounds and testable targeting hypotheses |
| Actual channel payer conversion and incrementality | Unit costs and broad external comparisons available | Scenario CAC ranges, required conversion thresholds and holdout design |
| Tennis renewal definition and cohort survival | Brief plus outside subscription comparisons | Clarify model horizon, use the brief as given, show sensitivity and rights expiry |
| Willingness to pay and price elasticity | No primary respondent data | Price experiments and break-even response thresholds. No fitted demand curve |
| Current ATP checkout and monthly entitlement | Still unresolved | Preserve two entitlement branches and case versus live-price labels |
| Taxes included in displayed FanCode prices | Secondary 18% classification support, no invoice | Model invoice-inclusive and other justified treatments explicitly. Do not treat missing tax line as proof |
| Actual streaming/payment/support costs | Public vendor price references only | Transparent unit-cost model with negotiated-rate, usage and refund sensitivities |
| Creator fees and sponsor contributions for a proposed campaign | Generic ranges and existing partnership evidence | Quote-dependent budget ranges, capped spending and kill rules |
| Full actual-start calendar | Partial official planned sessions and secondary clock sample | Coverage-first session analysis. No extrapolation to a match census |
| Broader Trends history and India-only YouTube metrics | No additional qualified export in this pass | Keep existing four-term 2026 series and bounded video sample. No subscriber attribution |

## 9. Source-quality decisions

- Preserve source disagreements instead of averaging them. Ormax active subscriptions and EY year-end contracts answer different questions.
- Keep source age and measurement age separate. A 2026 publication may report 2025 or 2024 observations.
- Exclude Superads' unreconciled CPM narrative because its header and narrative windows conflict.
- Treat the Wimbledon trade article as context: its growth statements and TV/digital attribution are insufficiently clear for a central audience calculation.
- Do not use third-party templated business-model pages, referral promotions or unsourced rights estimates as company financial evidence.
- Preserve every failed response. Do not count it as a substantive source.
- Original public reports remain local research snapshots. Publication rights differ by source. The vendor comparison CSV advertises CC BY 4.0, which requires attribution and does not make its claims independently verified.

## 10. Handoff to the notebook stage

The raw evidence is ready for a documented processing phase, not a final causal conclusion. Recommended order:

1. Build the brief input dictionary, source hierarchy and question-to-evidence map.
2. Transcribe prices, entitlements, costs and audience definitions with source IDs.
3. Parse the ATP session sample and revised F1 calendar, then publish coverage and timezone checks before charts.
4. Analyse review friction and bounded search/video attention separately from payer behaviour.
5. Build contribution, pass-switching and channel-CAC sensitivities with visible assumptions.
6. Assemble the sport-by-ownership recommendations, experimental thresholds and a connected presentation narrative.

All generated tables and figures belong outside `data/raw`. Notebooks must be executed and export their outputs. No fitted model, cleaned customer dataset or fabricated respondent file has been added to this raw release.

## References

The following IDs link the argument to the original sources. Local copies, exact URLs, collection timestamps, hashes and detailed qualifications are indexed in [the source catalog](THIRD_PARTY_SOURCE_CATALOG.md) and the HTTP manifest.

[1] [IBM and Morning Consult, Sports Survey 2025](https://filecache.mediaroom.com/mr5mr_ibmnewsroom/199459/IBM_Sport_Survey_Report_2025.pdf). Source ID: `v3_ibm_sports_survey_2025`.
[2] [YouGov, Indian Cricket Fandom Report 2025](https://commercial.yougov.com/rs/464-VHH-988/images/YouGov-India-Cricket-Fandom-Report-April-2025-new.pdf?content_name=Indian+cricket+fandom+report+2025&version=0). Source ID: `v3_yougov_cricket_2025`.
[3] [Ormax, sports audience research, March 2024](https://www.ormaxmedia.com/insights/stories/678-million-sports-audiences-in-india-game-on.html). Source ID: `v3_ormax_sports_2024`.
[4] [Ormax, OTT Audience Report highlights, September 2026](https://www.ormaxmedia.com/insights/stories/the-ormax-ott-audience-report-2026.html). Source ID: `v3_ormax_ott_2026`.
[5] [FICCI-EY, Stories, scale and impact, March 2026](https://creativefirst.film/wp-content/uploads/2026/03/FICCI-EY-Report-March-2026.pdf). Source ID: `v3_ficci_ey_2026`.
[6] [Mint, non-cricket sports creators and FanCode interview, January 2026](https://www.livemint.com/news/sports-creators-cultivating-followings-beyond-cricket-brands-swoop-in-basketball-volleyball-f1-chess-running-11768808839225.html?openSearch=true). Source ID: `v3_mint_fancode_f1`.
[7] [Google Cloud, FanCode case study, December 2024](https://cloud.google.com/blog/products/databases/fancode-migrates-from-aws-to-memorystore-for-redis-cluster/). Source ID: `v3_google_cloud_fancode`.
[8] [AWS, FanCode historical case study](https://aws.amazon.com/solutions/case-studies/fancode-case-study/). Source ID: `v3_aws_fancode`.
[9] [Inc42, Dream Sports FY25 group financials](https://inc42.com/buzz/dream11-parent-slips-into-loss-in-fy25-on-reverse-flipping-cost/). Source ID: `v3_dreamsports_fy25`.
[10] [Moneycontrol, ATP rights announcement, January 2026](https://www.moneycontrol.com/news/business/startup/fancode-strikes-exclusive-multi-year-deal-to-broadcast-atp-tour-events-in-indian-subcontinent-13757010.html/amp). Source ID: `v3_atp_rights_moneycontrol`.
[11] [Apple India App Store, Tennis TV listing](https://apps.apple.com/in/app/tennis-tv-live-streaming/id1114471030?platform=vision). Source ID: `v3_tennistv_india_iap`.
[12] [FanCode, TimesPrime public subscription page](https://www.fancode.com/content/timesprime). Source ID: `v3_timesprime_fancode`.
[13] [FanCode, terms and referral matrix](https://www.fancode.com/about/tnc). Source ID: `v3_fancode_terms`.
[14] [Razorpay, standard payment pricing](https://razorpay.com/pricing/). Source ID: `v3_razorpay_pricing`.
[15] [Cloudflare Stream, pricing documentation](https://developers.cloudflare.com/stream/pricing/). Source ID: `v3_cloudflare_stream_pricing`.
[16] [January 2026 INR WhatsApp rate card, third-party mirror](https://bulkymarketing.com/wp-content/uploads/2026/01/meta-price.pdf). Source ID: `v3_meta_inr_ratecard_jan2026`.
[17] [UDO, MSG91 price comparison, August 2026](https://uniquedigitaloutreach.in/msg91-vs-udo-sms-pricing-full-cost-comparison/). Source ID: `v3_msg91_comparison`.
[18] [Nurdd, Indian D2C advertising benchmarks, September 2026](https://www.nurdd.club/blogs/paid-media-benchmarks-for-indian-d2c-brands-2026-cpm-cpc-ctr-and-roas-by-category). Source ID: `v3_nurdd_india`.
[19] [Kofluence, public 2025 report highlights](https://www.kofluence.com/the-2025-influencer-marketing-report/). Source ID: `kofluence_2025_report`.
[20] [Media Ant, Instagram advertising quotes](https://www.themediaant.com/digital/instagram-advertising). Source ID: `mediaant_instagram`.
[21] [RevenueCat, State of Subscription Apps 2026](https://www.revenuecat.com/state-of-subscription-apps/). Source ID: `v3_revenuecat_2026`.
[22] [COTT, 2025 industry white paper](https://chromedm.com/assets/byCOTT2025.pdf). Source ID: `v3_cott_2025`.
[23] [Desi Racing Co, FanCode portfolio case](https://portfolio.desiracingco.in/articles/fancode). Source ID: `v3_desiracing_fancode_case`.
[24] [Ormax, Sports Track research design](https://www.ormaxmedia.com/stories/product-launch-ormax-sports-track.html). Source ID: `v3_ormax_sports_track`.
[25] [Jolpica, 2026 race feed](https://api.jolpi.ca/ergast/f1/2026/races/). Source ID: `v3_jolpica_races_2026`.
[26] [Jolpica, race endpoint documentation](https://raw.githubusercontent.com/jolpica/jolpica-f1/main/docs/endpoints/races.md). Source ID: `v3_jolpica_documentation`.
[27] [Formula 1, Bahrain GP in Malaysia confirmation](https://www.formula1.com/en/latest/article/formula-1-and-fia-confirm-formula-1-and-fia-confirm-malaysia-will-join-2026-calendar-as-host-venue-for-the-bahrain-grand-prix.6lL7vjFEM2VVynRHvg1TCf). Source ID: `v3_f1_malaysia_confirmation`.
[28] [Tennis Explorer, 29 August 2026 results](https://www.tennisexplorer.com/results/?day=29&month=08&year=2026). Source ID: `v3_tennisexplorer_aug29`.

Additional qualification sources: [Meta official pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing), [July vendor study](https://www.richautomate.in/research/state-of-whatsapp-business-api-pricing-india-2026), [vendor CSV](https://www.richautomate.in/research/whatsapp-bsp-pricing-india-2026.csv), [BUSY tax guide](https://busy.in/sac-code-9984/), [Media Ant Facebook](https://www.themediaant.com/digital/facebook-advertising).
