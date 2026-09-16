# Fourth-pass recovery: alternate sources and methods

Author: Competition team  
Collection date: 14 September 2026  
Scope: Raw evidence recovery and source QA. Business analysis notebooks and presentation remain subsequent deliverables.

The strongest recoveries are usable data, not another set of unsupported market estimates: official MotoGP session records and race-control reports, complete prior-season La Liga records, and a 2025 India Google Trends series. This pass attempted **92 additional public HTTP sources: 86 downloaded and six failed**. Every response body, including errors, is preserved with a URL, timestamp and SHA-256. Some downloaded pages are intentionally excluded from estimates.

Read the [complete source catalog](RAW_V4_SOURCE_CATALOG.md) for all 92 attempts. The [machine-readable QA report](../data/manifests/recovery_v4_qa.json) records coverage, source IDs and observed data defects. The [external evidence register](../config/external_evidence_registry.json) now contains 35 selected observations and explicitly qualified proxies across the collection.

## What changed

| Missing item | Different approach | Evidence recovered | What it enables |
|---|---|---|---|
| MotoGP session times | Followed a public calendar repository to the official results API, then followed its report links | 22 weekend responses, 177 MotoGP-class session records, 29 official sprint/race PDFs | A much stronger cross-sport calendar and actual-start checks, with explicit timezone repair |
| Football kickoff data | Downloaded Football-Data season CSVs, then checked clock semantics against club announcements | 380 La Liga 2025/26 matches and 41 in the 2026/27 snapshot | A La Liga viewing-time comparison using 250 recorded matches dated in 2026 through the research cutoff |
| 2025 India search baseline | Reduced the failed five-term request to a two-term, single-year request | Original Google Trends response containing 53 weekly bins for tennis and FanCode | Within-2025 seasonality analysis and a historical brand-interest comparison with scope limits |
| Football audience scale | Used a reported AIFF audience figure in Mint and searched the official tender index | Reported 5.79m online and 9.39m linear ISL audience | A qualified football context point, not a subscriber or cross-sport overlap estimate |
| Bundle alternatives | Read partner help pages instead of relying on standalone checkout | Official Vi offer descriptions and Jio delivery instructions | Separate direct subscriptions from partner-delivered content in the entitlement map |
| Engagement originality | Used the implementation partner's announcement after ATP pages failed | ATP Fantasy launch design and existing private/swing leaderboards | Avoid presenting an existing ATP product as a novel recommendation |
| Channel acquisition cost | Inspected affiliate conditions and actual business context of conversion case studies | Paused SonyLIV payout listing and merchandise-only FanCode cases | Excludes misleading cost/conversion inputs and sharpens the remaining experiment requirements |

## 1. MotoGP: official data recovered, timezone defect exposed

The [public repository](https://github.com/micheleberardi/racingmike_motogp_import) supplied discoverable endpoint syntax. Collection used the [official public seasons endpoint](https://api.motogp.pulselive.com/motogp/v1/results/seasons), followed by its 2026 category and event identifiers. Only the MotoGP category was requested. Test events were excluded when registering the 22 weekend session requests. The registration scripts preserve that lineage and do not execute the downloaded third-party code.

The raw API contains **177 unique session IDs**: 44 free-practice records, 22 practice records, 44 qualifying records, 22 sprints, 22 warm-ups and 23 race records. The extra race record is Catalunya's second race part. At retrieval, 113 records were marked finished and 64 not started. The 14 completed weekends include San Marino on 13 September, which falls after the original 12 September research cutoff. Retain it in raw data but exclude its Sunday outcomes from any analysis claiming that cutoff.

The API's offset is unsafe to use literally. For Assen it records the race as `2026-06-28T14:00:00+00:00`. The [official circuit timetable](https://res.cloudinary.com/ttcircuit/image/upload/v1777967079/DRAFT_2026_NLD_Time_Schedule_on_April_29_8559bc49aa.pdf) explicitly says UTC+2 and schedules the race at 14:00 local. The [race-week MotoGP announcement](https://www.motogp.com/en/news/2026/06/24/time-schedule-tissot-grand-prix-of-the-netherlands/1074755) also lists 14:00. This is a two-hour conflict. The March secondary ICS repeats 14:00Z, so its apparent UTC field does not independently validate the API.

The combined session PDFs are more valuable than the API for actual race starts. All **29 sprint/race reports** contain race-start log entries in their first three pages. Assen's report page 2 records **14:02:03**. Catalunya RAC2 repeats the original start at **14:02:17**, another start at **14:53:06**, and on page 3 a further start at **15:16:58**. Assen page 2 and Catalunya RAC2 page 2 were visually inspected. These are race-control clock entries, not prices, inferred match times or automatically clean timestamps. [Assen official report](https://resources.motogp.com/files/results/2026/NED/MotoGP/RAC/Session.pdf), [Catalunya part 2 report](https://resources.motogp.com/files/results/2026/CAT/MotoGP/RAC2/Session.pdf).

**Processing requirements for the later notebook:** preserve the raw API timestamp, provider status, session ID, source PDF page, start/restart label, event date, circuit timezone and conversion evidence. Validate local-clock interpretation per circuit before converting. Deduplicate repeated race history across report parts. Keep planned API times and actual report times separate. Do not infer the actual finish from a generic 60-minute calendar block. Future sessions remain planned, and historical API clocks may reflect revisions made after original scheduling.

The third-party MotoGPRaceTimes page is also saved. Its title advertises a full 22-round season, but the captured event list contains the **eight remaining weekends**, with explicit offsets. It can help check future schedules. Its fixed session end times are not race-duration evidence. The official future-event responses reflect Qatar on 8 November, Portugal on 22 November and Valencia on 29 November, so a March calendar is not a reliable current date source.

## 2. Football: a usable La Liga calendar, with a qualified timezone rule

The [Football-Data Spain index](https://football-data.co.uk/spainm.php) links to the preserved season CSVs and [schema notes](https://football-data.co.uk/notes.txt). All 421 rows have parseable date/time fields and unique date/home/away keys. The complete 2025/26 season contributes 209 matches dated in 2026. The 2026/27 file contributes 41, ending on 7 September. It is not a complete snapshot through 12 or 14 September and contains no rest-of-season kickoff forecast.

The source's notes define the `Time` field but omit its timezone. Two independent fixture checks support **Europe/London**, including daylight-saving changes:

| Fixture | Raw CSV clock | Primary club announcement | Interpretation |
|---|---|---|---|
| Espanyol–Barcelona, 3 January 2026 | 20:00 | 21:00 CET | 20:00 UK winter time |
| Barcelona–Real Madrid, 10 May 2026 | 20:00 | 21:00 CEST | 20:00 UK summer time |

The [Barcelona preview](https://www.fcbarcelona.com/en/football/first-team/news/4427015/preview-rcd-espanyol-v-fc-barcelona) and [Real Madrid announcement](https://www.realmadrid.com/en-US/news/football/first-team/latest-news/el-barcelona-real-madrid-se-jugara-el-domingo-10-de-mayo-a-las-21-00-h-22-03-2026) establish those local clocks. An [independent data integration](https://georgedouzas.github.io/sports-betting/overview/user_guide/dataloader/) also describes this provider's clocks as UK time. The conversion is therefore a supported inference, not a timezone declared in the provider's own dictionary or a full row-by-row audit.

Use date-aware timezone conversion, with the IST date rollover retained. This dataset supports **La Liga**, not every football competition on FanCode. Recorded kickoff clocks are not proof of the actual opening whistle. Preserve the original odds/statistics columns in raw data, but the viewing-time analysis only needs fixture identity, date, clock and provenance.

## 3. Google Trends: 2025 recovered, football still unavailable

The smaller India request for `tennis` and `FanCode`, covering 1 January to 31 December 2025, returned a public widget definition. Following its time-series request returned **53 weekly observations**, with two values per row, unique timestamps and values in the 0–100 range. Both original responses are in `data/raw/search_interest/`.

Google's weekly bins cross the requested calendar-year edges: the first is **29 December 2024–4 January 2025**, and the last is **28 December 2025–3 January 2026**. Do not describe this as 53 complete weeks wholly inside 2025 or prorate the boundary bins into daily observations.

The 2025 response uses a different time window, term set and frequency from the saved four-term daily 2026 table. It supports within-request seasonality. It does **not** establish a direct percentage increase in FanCode demand between years. Any later bridge between exports requires a justified normalization method and matching time coverage. Google Trends itself measures relative search interest, not sports audience size, paid conversion or willingness to pay. [Google's methodology](https://support.google.com/trends/answer/4365533?hl=en).

The separate smaller `football`/`FanCode` 2026 request still returned **HTTP 429**. That response is preserved. No football search series, player series or topic-based comparison was invented to replace it.

## 4. Pricing and distribution: more evidence, no false closure

The [Vi Movies & TV page](https://www.myvi.in/vi-movies-and-tv/all-ott-in-one-app) lists FanCode among partner services. Its postpaid FAQ gives Pro at **₹199/month** and Plus at **₹248/month**, with monthly auto-renewal. Its prepaid Pro entry is **₹202**. Hero cards and FAQ text differ on OTT counts, so neither a single universal plan price nor an exact current app count should be inferred across variants. ATP-specific access, the tax breakdown and FanCode's wholesale proceeds remain unknown.

The [Jio ₹200 OTT Pass help page](https://www.jio.com/help/faq/mobile/prepaid-offerings/jio200-ott-pass/how-do-i-watch-content-from-sonyliv-zee5-and-the-other-bundled-otts-using-the-jio-ott-pass-200/) says FanCode content is watched inside the **JioTV mobile app**. This is useful evidence that a bundled brand entitlement and a standalone FanCode subscription are not automatically the same product. It does not enumerate ATP coverage.

The 134-page Vi terms PDF downloaded, but its extracted text has severe font-mapping gaps. The readable official web page is the evidence source for the above prices. This avoids treating a mostly blank text extraction as a completed audit.

Three FanCode help routes were tested, including the helpdesk URL found in public page configuration and its canonical form. They returned shells without the needed answers. A public promotion deep link reached the BMW Open 2026 tour, but exposed no checkout price. Search snippets mentioned historic Munich/season prices, but the mirrored post could not be retrieved, so those are not elevated to verified price observations.

**Still unresolved:** current ATP tournament/season checkout prices, whether each monthly product includes ATP, offer-specific eligibility and renewal charges, and invoice-level GST treatment. Preserve the existing case-input/current-offer distinction and the monthly-inclusion branches.

## 5. Cost benchmarks: tempting numbers rejected after inspection

The [SonyLIV Cuelinks listing](https://www.cuelinks.com/campaigns/sony-liv-affiliate-program) shows two maxima, ₹234 and ₹135, but marks the campaign **paused** and withholds plan-specific rates and validation details. These are not endpoints of a usable CAC range. They provide evidence that affiliate payout models exist, but not an available campaign, FanCode quote, incremental acquisition cost or guaranteed cost per new payer.

The [FanCode affiliate listing](https://www.cuelinks.com/campaigns/fancode-affiliate-program) is explicitly **FanCode Shop** and is also paused. The [Xpert case](https://www.xpert.chat/case-study-details.php?pg=boosting-fancodes-aov-with-xperts-high-value-audiences) concerns merchandise, while the [GoKwik case](https://www.gokwik.co/case-studies/fancode-reduced-rto-using-gokwik?_gc=1) concerns cash-on-delivery orders and returns. None estimates streaming subscription conversion.

The [CleverTap SonyLIV case](https://clevertap.com/blog/how-sonyliv-converted-the-art-of-personalized-mobile-marketing-into-user-engagement-science/) offers a relevant behavioral segmentation and reminder precedent. Its reported notification conversion concerns content engagement and does not establish paid-subscription conversion. Page update date is not the campaign measurement date.

The earlier external ad, creator, payment, messaging and delivery cost sources remain available. **No new defensible FanCode paid-conversion rate or all-in channel CAC emerged in this pass.** Later CAC ranges must still separate sourced unit prices from assumed conversion and incrementality, with the acquisition ceiling and break-even conversion shown alongside them.

## 6. Audience and originality

[Mint's 7 August 2026 report](https://www.livemint.com/mint-lounge/ideas/isl-indian-super-league-clubs-commercial-rights-media-bids-11786023505026.html) attributes ISL 2025/26 audiences of **5.79m online** and **9.39m linear TV** to an AIFF document. The original document and measurement method were not found in the [public tender index](https://www.the-aiff.com/documents/tenders-and-rfps). These values can be cited as reported figures, with that limitation. Do not add them without overlap data, treat them as payers, substitute them for La Liga demand, or use ISL rights costs as ATP economics.

After both ATP announcement routes failed, [Deltatre's primary announcement](https://www.deltatre.com/about/news-and-insights/atp-launches-official-fantasy-game-in-collaboration-with-deltatre) recovered the existing ATP Fantasy design: eight-player teams, a 100-credit budget, 23 tournament weeks announced at launch and private, monthly, swing and overall leaderboards. A generic fantasy game or swing leaderboard is therefore **prior art**. A distinctive recommendation would need to show a new FanCode-specific discovery, entitlement, timing or retention mechanism and a testable outcome. The announcement does not prove causal retention lift.

## What remains unavailable and how to proceed

| Remaining gap | Status after alternatives | Honest treatment in the analysis |
|---|---|---|
| Tennis × F1/football/MotoGP overlap | Public marginal audience estimates exist, no joint customer distribution | Segment hypotheses and bounded overlap scenarios, no invented intersections |
| Tennis-specific payers, conversion, renewal cohorts and incrementality | No disclosed FanCode cohort dataset or reliable third-party substitute found | Use brief inputs with definitions, sensitivity analysis and a proposed holdout design |
| ATP rights fee and FanCode operating/wholesale costs | Other rights and public supplier rates are available, company-specific values are not | Contribution thresholds per cost unit, with supplier proxies kept separate |
| Willingness to pay and price elasticity | No respondents or observed price experiment | Break-even uplift curves and explicit test cells, no synthetic survey findings |
| Current ATP/monthly entitlement and invoiced tax | Public help routes and partner terms did not settle it | Branch the switch map and price model |
| Full-year actual ATP start-time census | Twelve purposive editions remain unevenly documented | Published-session sample with coverage chart, no invented match chaining |
| Complete football portfolio calendar | La Liga partly recovered, other leagues and future exact kickoffs incomplete | Label league and date coverage, expand only if needed for a specific decision |
| Google Trends football/topics/player series | Football request still rate-limited | Exclude missing series, do not substitute a different metric silently |
| India-only YouTube demand and complete public review population | Existing keyword videos and storefront reviews are limited samples | Diagnostic analysis with sample limits, not market sizing or willingness to pay |
| Independent campaign causal impact | Vendor cases lack equivalent outcomes or controls | Feasibility precedents and an experiment design, no transferred lift claim |

This closes the fourth raw-data recovery pass. It materially improves what can be measured, while keeping the few decision-critical unknowns visible. The next analytical work can now use these preserved sources offline, with a data-quality notebook before any pricing, calendar or acquisition model.

## Verification

Run `python scripts/validate_recovery_v4.py` for this pass, `python scripts/validate_external_evidence.py` for the selected evidence register, and `python scripts/validate_raw.py` for the full raw inventory. The sealed release is checked with `python scripts/verify_release.py`. Earlier releases remain checkable with `--archive raw-v1-2026-09-14`, `--archive raw-v2-2026-09-14` and `--archive raw-v3-2026-09-14`.

Raw bodies remain local under the existing sharing boundary. No repository has been published, no report purchased, and no account or respondent dataset created.
