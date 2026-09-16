# Raw evidence availability

**Current release: raw-v5-2026-09-14.** See the [final recovery and gap treatment](RAW_V5_CLOSURE.md). This update supersedes earlier status summaries below. Football Trends and the full primary ATP guide are now recovered. Every failed HTTP source has an explicit disposition. Remaining private or ambiguous facts use the documented scenario treatments.

Author: Competition team

Collection dates: 13–14 September 2026. Review study window: 1 January 2025 to 12 September 2026, India time. The expanded raw-v5 collection is closed with documented gaps. See [the latest recovery report](RAW_V4_RECOVERY.md) and [fourth-pass catalog](RAW_V4_SOURCE_CATALOG.md). See `THIRD_PARTY_EVIDENCE_REPORT.md` and `THIRD_PARTY_SOURCE_CATALOG.md` for the third-pass additions. The v2 detail below remains a coverage record where not updated. The original raw-v1 metadata is archived and all original bodies remain intact. See `RAW_V2_RECOVERY.md` for the second-pass changes. It is not a complete census of all matches, users or channels. Exact file totals and integrity results are in `data/manifests/release.json` and `validation_report.json`.

## Collection coverage and decision use

| Evidence block | Material preserved | Ready for next phase | Limits that must stay visible |
|---|---|---|---|
| Case and references | Original brief and all six reference PDFs, byte checked against supplied files | Brief input dictionary and question-to-deliverable map | Reference-case results are not FanCode facts |
| ATP calendar | Two-page 2026 calendar distribution copy, official event documents and 16 current September-November browser-visible event windows | Event-level baseline with explicit revisions and unknowns | Calendar copy has TBD entries and old sponsor labels. Current browser capture is a partial update and includes non-ATP-rights events, not a final annual universe |
| Viewing sessions | Some dated timing evidence for all 12 preselected editions, including full Brisbane daily orders and Madrid programme | Purposive session sample, local-time transcription and later timezone conversion | Uneven coverage, mixed ATP/WTA programmes, scheduled/not-before times. No full-season actual-start census |
| Portfolio calendar | Official F1 2026 calendar and Singapore timetable, MotoGP 22-race table, LaLiga announcement and FanCode listing | Date overlaps and a bounded future journey example | Football listing is not an exact-kickoff census. MotoGP article's original publication label does not prove all current dates were known then |
| Player results | Completed official singles draw PDFs for all 12 preselected editions, plus two secondary results archives and their documentation | Within-sample participation and round progression, broader results exploration after source reconciliation | Twelve official editions. Secondary files extend coverage but overlap, use different player IDs and have date/key inconsistencies. Do not concatenate or infer unbiased population rates |
| FanCode offers | Initial HTML, selected rendered monthly/yearly and recurring-monthly offers, and ATP event/listing observations | List/promotion distinction, public wording audit and two entitlement branches | Monthly ATP inclusion, exact ATP checkout price, renewal charge and tax invoice unresolved. No account inspection or purchase |
| Competitors | Sony LIV public subscription page, JioHotstar January price release and Tennis TV product page | Device/format/commitment-aware comparator | Jio announcement is dated. India App Store featured prices now recovered in v3. Web checkout still unverified; earlier public purchase routes reached registration |
| Android reviews | 14,800 unique mobile review IDs, 14,665 within the registered window | Raw-source parsing, sport labels and friction discovery | All sports mixed, selection bias, edited/deleted reviews possible. Not a payer cohort or tennis prevalence sample |
| Android TV reviews | 93 accessible unique review IDs, 64 in-window | Separate device-specific qualitative audit | Small sample, source exhaustion, not directly comparable to mobile counts |
| iOS reviews | 10 successful RSS pages, 500 unique review IDs, all in-window | Independent-store qualitative comparison | Bounded latest-500 sample, not the complete registered window. Uses updated timestamp |
| Company rights | ATP Media original HTML and selected official F1 rendered statement | Rights horizon and existing content-capability checks | No rights fees. Ordinary FanCode access is not automatically F1 TV Pro/Premium access |
| Indian channel costs | Media Ant YouTube, Instagram and Facebook listings plus Kofluence public report/preview | Indicative unit-cost ranges with a separate conversion scenario layer | Vendor quotes, ambiguous banner units and limited methodologies. No observed FanCode payer conversion, incrementality or channel CAC |
| Measurement | Google conversion-lift and Trends methodology pages | Experiment and evidence-boundary design | No team experiment was conducted |
| Search interest | Complete browser-visible 255-day, four-term Trends table plus query settings and selected related queries | Exploratory common-scale 2026 search-interest series | Search terms, not topics. Separate football/FanCode 2026 daily table and 2025 tennis/FanCode weekly table now recovered. Their normalization differs. No absolute search volume, subscriber attribution or WTP inference |
| Public video | Two official FanCode channel-search HTML snapshots, containing 53 distinct video IDs | Bounded content and displayed-view exploration | Ranked keyword results, mixed competitions, relative publication labels, no India-only audience or video census |
| Existing engagement features | Official ATP Collect 2025 announcement, selected rendered text | Prior-art check for collection mechanics and rewards | Historical campaign, publisher-reported participation and country-dependent reward eligibility, no proven payer retention effect |

Review figures count distinct source IDs within each app. They are not deduplicated people across apps. Raw review text and public reviewer metadata remain local. `review_window_qa.json` contains date boundaries and counts without text or names.

## The fixed 12-edition timing sample

The sample was chosen by tier and region before new session extraction. Its composition is unchanged. “Available” below means at least some reliable planned timing evidence, not every daily session.

| Tier | Edition | Best captured evidence | Coverage boundary |
|---|---|---|---|
| Masters | Indian Wells | Official 6, 7 and 15 March orders of play | Three days including final, mixed ATP/WTA. Daylight-saving boundary must be handled by date |
| Masters | Miami | Official 29 March final order, LTA 2026 preview and dated sponsor session table in public government archive | Planned ticket/session layer and final-day order. Session start does not necessarily mean ATP start |
| Masters | Madrid | Official full Spanish and English 2026 programmes and 3 May final order | Planned sessions and approximate finishes. Language versions are the same evidence |
| Masters | Rome | Official 17 May final order and broadcaster final-day article | Final day only, WTA and ATP slots distinguished |
| 500 | Rotterdam | Official 15 February final order and publisher-hosted official 11 February order | Two days. Preserve publication host and released-at timestamps |
| 500 | Doha | Official 21 February singles-final order | Final only. Stored release timestamp is after scheduled start, so no claim of ex-ante availability |
| 500 | Dubai | Official 25 and 28 February orders | Two ATP days including planned final, not entire week |
| 500 | Halle | Official 21 June order plus official rendered article excerpt | Final day. Do not use current 2027 homepage |
| 250 | Brisbane | All eight official daily orders, 4–11 January, plus final singles draw | Combined ATP/WTA/other matches, keep types separate |
| 250 | Hong Kong | Official 11 January order and 2026 booklet | Final timing verified. Booklet's page-2 timetable is village opening, not match start |
| 250 | Marrakech | Federation 31 March order, official programme and 5 April final order | Two detailed daily orders. Final ceremony time is not a match-start observation |
| 250 | Winston-Salem | Official 28–29 August pages and final-day PDF, 2026 record book | Semifinal/final end of week, not all daily starts |

Some final order files were released after their scheduled start and Dubai had a walkover in the completed draw. An order of play cannot prove that a scheduled match occurred. Later analysis should publish event/day coverage before any heatmap. Do not pool a complete Brisbane week and isolated finals elsewhere into an unqualified “share of ATP matches in Indian prime time.” Use within-source comparisons and show a sensitivity restricted to comparable rounds.

## Important unresolved facts

1. **Monthly ATP entitlement:** the monthly product description does not explicitly name ATP or tennis. The yearly description names tennis. A separate ATP event page shows “YOU HAVE A PASS FOR THIS MATCH!” alongside a “Login or sign up” button. That combination does not identify the entitlement or prove a purchased pass. The recurring monthly route also does not explicitly list ATP. Account state was not investigated. Model both monthly-includes-ATP and monthly-excludes-ATP branches.
2. **Current ATP price:** the public event route did not expose a verifiable ATP tournament or season checkout price. Keep the brief's prices explicitly marked as case inputs. The recurring monthly page shows ₹199 less ₹20 coupon = ₹179, whereas the previously captured subscription route shows ₹116. These are separate route-specific observations, not a proven universal price change. Do not replace them with inferred prices from generic metadata or a referral post.
3. **Timing semantics:** actual starts, complete durations and full-day ATP-only inventory are not available. Keep scheduled starts, not-before limits, followed-by order, gates and approximate finishes in separate fields.
4. **Marketing economics:** no FanCode payer conversion or incremental-acquisition dataset exists here. Printed channel CAC ranges must be derived scenarios with disclosed input sources and assumptions. Never label them observed benchmarks.
5. **Rights economics and tax:** rights fees and other internal costs were not supplied. The official GST table attempts failed. V3 adds a secondary tax-classification guide and public vendor fees, but no FanCode invoice. A tax-inclusive treatment remains an explicit model scenario unless separately established from applicable authoritative evidence or an invoice.
6. **Search and player continuity:** the original 2026 four-term Trends table was recovered in the browser, but the broader five-term 2025-2026 endpoint returned 429. V4 subsequently recovered a separate 53-week, two-term 2025 request. Football remains unavailable. All 12 official singles draws are now present. The original public results repository remains unavailable, so secondary archives are explicitly labelled. The Sackmann mirror stops at a June snapshot. TennisMyLife extends later, but its 2026 dates vary within events despite the dictionary saying tournament week. It also contains reused match keys. Reconcile these issues before joins or date-based claims.
7. **Surveys, subscriber cohorts and willingness to pay:** unavailable by design because there is no access to respondents or internal records. No synthetic respondent or customer data has been created.

## Source-quality decisions

- Preserve wrong-year pages as discovery evidence and mark them excluded from timing estimates.
- Prefer official tournament PDFs over search snippets and generic website headers.
- Keep the first empty iOS page-2 response and its successful retry. Use the latest manifest entry for analysis.
- Retain HTTP 403, 404, 429, 475 and failed network attempts. They do not count as substantive sources.
- Media Ant banner rows saying “Impression/Click” have an ambiguous unit and should not drive a CPM/CPC calculation. Video and install rows have separate explicit units. An app install is not a subscriber.
- Kofluence public pages provide limited vendor evidence. Its full form-gated report was not obtained. Do not use its apparent CPV-unit anomaly without clarification.
- WordStream's 2024 traffic/lead data is not an India sports-subscription benchmark. It is retained as a labelled methodological comparison only.
- Public schedules revised after their original publication date can support current descriptive planning, but not a simulation claiming that the team knew those revisions at the earlier date.

## Secondary results and video safeguards

- Do not sum the two 2025 files: each has 2,944 rows and overlapping underlying matches. Agreement does not establish independent data collection.
- The Sackmann mirror has 1,449 rows for 2026 and documents a June archival snapshot. TennisMyLife has 2,132 rows in its 2026 file and 127 in the separate ongoing US Open snapshot. These counts describe source rows, not a verified union of unique matches.
- TennisMyLife 2025 contains 489 missing match numbers and 480 repeated tournament-ID/match-number keys. Its 2026 file has two repeated keys. These are unsafe candidate identifiers, not proof of duplicate match records.
- TennisMyLife dates require reconciliation: its Winston-Salem final is labelled 30 August while the official order labels 29 August. Do not infer a timezone from that difference.
- The ongoing US Open snapshot includes a 13 September final, after the registered cutoff. Preserve the full raw snapshot and verify individual dates before selecting cutoff-eligible rows.
- Video search results contain 28 tennis-query entries and 30 ATP-query entries, 53 distinct IDs across both. Some are Challenger content. No exact upload-time or audience-geography export was obtained. The raw HTML may contain transient request metadata and remains local.

## Next phase contract

The next phase will parse and document data in notebooks, with intermediate/processed tables outside `data/raw`, followed by executed notebooks and separate outputs. It should begin with the case input dictionary, source/coverage table, review scope validation and schedule transcription. V3 documents external audience estimates and explicitly labelled arithmetic illustrations. No fitted commercial model, sentiment conclusion or observed FanCode conversion has been calculated.

## Third-pass additions and surviving limits

The v3 evidence report takes precedence for newly recovered data: India Tennis TV IAP prices, IBM/YouGov interest surveys, latest Ormax OTT context, FICCI-EY estimates, reported F1 engagement, referral terms, vendor cost references, a23-round UTC F1 feed and creator prior art. Every one of40 new HTTP IDs has a scope review. The additional browser tour route still yielded no price. General renewal terms are available, but offer-specific renewal charges, monthly ATP entitlement and price-inclusive tax treatment remain unresolved. Audience marginals are not cross-sport overlap. Vendor rates and industry conversion are not FanCode operating metrics.

## Fourth-pass additions, 14 September 2026

The latest status is [RAW_V4_RECOVERY.md](RAW_V4_RECOVERY.md). Added 22 official MotoGP session responses containing 177 records, 29 sprint/race reports, 380 plus 41 La Liga match rows, and 53 weekly India tennis/FanCode observations for 2025. Of the football records, 250 are dated in 2026 through the cutoff. Raw future and post-cutoff MotoGP records remain labelled. API timezone labels conflict with local schedules, and weekly Trends bins cross year boundaries. Monthly ATP inclusion, current ATP checkout, internal cohorts, rights costs and causal paid-conversion rates remain unresolved.
