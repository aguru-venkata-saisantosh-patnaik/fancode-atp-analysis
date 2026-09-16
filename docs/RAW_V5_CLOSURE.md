# Final raw collection recovery and closure

Author: Competition team  
Release: raw-v5-2026-09-14

The collection step is complete with explicit fallbacks. This means every attempted source and required input has a documented analytical treatment. It does not mean that confidential company metrics or ambiguous entitlements have become observable. Raw-v1 through raw-v4 remain preserved. Notebooks, cleaned analytical tables and slides have not been produced in this step.

## What this pass recovered

| Recovery | Preserved source and verification | Permitted use |
|---|---|---|
| Football search interest | `google_trends_football_table_v5`, complete India football/FanCode table, 255 dates from 1 January to 12 September 2026. Saved TSV matches the rendered table's 4,343 characters and FNV-1a checksum 6705d050 | Explore football-linked timing. Rounded relative values on a separate scale. FanCode zeros are not proof of no searches. Do not splice into the four-term series |
| Full ATP media guide | [ATP 2026 guide hosted by LTA](https://www.lta.org.uk/siteassets/events/birmingham/media/2026-atp-media-guide-full-updated.pdf), 160 pages. Found using LTA's own search after ATP returned 403 and an indexed pagination link changed | Primary calendar on PDF pages 15–16 and tournament directory from 17. Annual publication, not a live calendar. Reconcile later announcements and orders of play. Selected text is readable, some fonts need care |
| Primary tax reference | [GST Council service-rate table](https://www.gstcouncil.gov.in/sites/default/files/2024-02/gstservicerates.pdf), PDF page 33, visually checked | Heading 9984(ii) carries 9+9 / 18 for the specified service category. Supports an 18% model scenario. Historical hosted table, not a full subsequent-amendment audit or a FanCode invoice. Does not resolve whether displayed price includes tax |
| Wimbledon creator precedent | [Wearisma campaign report](https://www.wearisma.com/all-resources/top-influencers/the-top-influencers-at-wimbledon-2026/) | Documents Star Sports India and JioHotstar creator activity. Prior art for execution. Vendor Media Value is not spend, revenue or payer conversion. No numerical CAC imported |
| Repeated official offer audit | `fancode_monthly_final_v5` and `fancode_japan_entitlement_v5` browser observations | Monthly list ₹199, initial discount ₹70, coupon ₹13, payable ₹116 at capture. Japan event says a pass is held while a Login button is present, but identifies no pass. Monthly ATP coverage remains unverified |

The GST reference is an improved source for a financial-model assumption, not a tax opinion. Price snapshots were collected on 14 September and must not be described as known before the 12 September review cutoff.

## Required inputs and the final treatment

| Input wanted | What is available | Treatment in the analysis |
|---|---|---|
| ATP dates and tier | Primary annual guide, distribution calendar, event documents and later browser windows | Build a versioned event master. Prefer dated event corrections. Preserve disagreements |
| Every ATP match's actual start | Uneven primary session and order-of-play evidence across the fixed 12 editions, plus results and durations | Use scheduled/session opportunities. No chaining durations into supposedly actual starts. Mark unknown cells, retain sample coverage, test timing uncertainty |
| F1 and MotoGP overlaps | F1 race feed and official calendar, MotoGP 22-weekend API, 29 combined session PDFs with race-control clocks, Assen timezone cross-check | Convert only with validated timezone semantics. MotoGP API UTC labels are suspect. Separate planned starts from actual logs, restarts and post-cutoff outcomes |
| Football kickoff times | Two Football-Data La Liga files, 250 rows dated in 2026 through latest captured 7 September, primary winter/summer clock checks | Partial observed fixture sample. Europe/London interpretation is supported by checks, not provider-declared metadata. Do not call it an all-season exact census |
| Current ATP pass and monthly inclusion | Brief prices, official public offers and repeated ambiguous event pages | Brief-price base model plus both monthly-entitlement branches. Retain list/promo/date/channel. Recommendations must hold across branches or be explicitly conditional |
| ATP rights fees and true contribution cost | Rights horizon and public vendor payment/delivery prices, no contract economics | Normalize contribution coverage per ₹1 crore of fixed cost. Model variable fees and tax separately. Do not call revenue coverage breakeven |
| FanCode tennis audience, cohorts and sport overlap | Case figures, third-party India sports/OTT estimates, public engagement proxies | Keep case inputs separate. No invented overlap percentage or payer count. Use scenario bounds and feasibility thresholds rather than a point forecast |
| Observed willingness to pay and price elasticity | No respondents, no transaction experiment | No synthetic survey. Break-even demand uplift and cannibalization scenarios. Published price menu is supply evidence, not WTP |
| Channel payer CAC | Indian media/influencer benchmarks, messaging/payment rate cards, no matched FanCode paid conversion | Label modeled CAC ranges. Carry CPM/CPC, CTR, payer conversion and incrementality as separate inputs. Observed cost input does not make conversion observed. Show channel ceilings and kill rules |
| Retention and incremental acquisition | Brief renewal/repurchase statements without complete cohort definitions | Alternative cohort interpretations, finite rights horizon, contribution-based retention thresholds and holdout design. No causal attribution from promo codes |
| Search interest | Four-term 2026 daily table, separate football pair, 2025 two-term 53-week response | Exploratory signals only. Different normalization and date granularity. Do not infer YoY level growth, paid audience or causation |
| Friction and content demand | Store reviews and bounded FanCode video-search snapshots | Qualitative friction and relative content exploration, with sample/selection bias. No store-review prevalence as subscriber incidence or video views as Indian WTP |
| New engagement mechanics | ATP Collect, ATP Fantasy via Deltatre, FanCode Watch Along, streaming CRM cases | Treat existing mechanics as prior art. Distinctiveness must come from targeting, timing, offer rules and measurement. No unsupported retention lift |

## Why several promising alternatives were rejected

The Thai page requested as an RSS feed returned HTML without the targeted ATP social-growth item. The LTA unfiltered page no longer contained the guide shown in search results, so a targeted publisher query was required. Both bodies are preserved and marked discovery-only or excluded. A successful HTTP status is not evidence recovery.

Earlier recovered FanCode Shop affiliate, conversion and COD-return cases concern merchandise. They cannot supply streaming subscriber CAC. SonyLIV affiliate listings were paused and internally inconsistent. Historical social posts cannot settle today's ATP checkout. These exclusions are substantive findings and remain in the fourth-pass report.

## Every failed source has a disposition

The machine-readable register is `data/manifests/failure_disposition.json`. It covers every currently failed HTTP source, including failed routes that were subsequently recovered elsewhere. “Replacement” can mean a narrower usable field or a scenario fallback. It never means exact equivalence by default.

| Failed source ID | Replacement IDs | Final treatment |
|---|---|---|
| atp_calendar_2026_article | v5_atp_media_guide_lta, atp_calendar_distribution_pdf | Recovered primary annual reference. Reconcile newer event dates before using guide calendar. |
| atp_current_calendar | v5_atp_media_guide_lta, atp_calendar_distribution_pdf | Recovered primary annual reference. Reconcile newer event dates before using guide calendar. |
| atp_calendar_announcement | v5_atp_media_guide_lta, atp_calendar_distribution_pdf | Recovered primary annual reference. Reconcile newer event dates before using guide calendar. |
| atp_2026_media_guide | v5_atp_media_guide_lta, atp_calendar_distribution_pdf | Recovered primary annual reference. Reconcile newer event dates before using guide calendar. |
| miami_2026_media_notes | miami_2026_official_op, miami_2026_official_mds, miami_2026_schedule_lta | Recovered schedule and draws needed for calendar. Full daily media-note narrative not recovered or necessary. |
| sonyliv_faq | sonyliv_subscription | Official pricing page replaces price requirement. Do not infer unobserved FAQ policies. |
| tennistv_countries | v3_tennistv_india_iap, tennistv_product | India App Store listing and product page are qualified alternatives. Exact web checkout and complete territory policy remain unverified. Do not equate IAP and web prices. |
| tennistv_features | v3_tennistv_india_iap, tennistv_product | India App Store listing and product page are qualified alternatives. Exact web checkout and complete territory policy remain unverified. Do not equate IAP and web prices. |
| f1_fancode_rights | f1_rights_rendered | Official rendered rights announcement replaces blocked HTTP body. |
| atp_aces_announcement | atp_collect_rendered_v2, v4_deltatre_fantasy | Related engagement prior art replaces need for general examples. ACES-specific details not verified and excluded. |
| ey_influencer_2024 | kofluence_2025_preview, kofluence_2025_report | Alternative India influencer report. Different publisher/year, not confirmation of original EY statistic. |
| cbic_gst_services | v5_gst_council_rates | Primary rate table replaces failed tax explainers. Tax-inclusive checkout still a scenario. |
| sackmann_repository | sackmann_archive_upstream_readme, sackmann_archive_license, sackmann_archive_2026, tennismylife_2026 | Archive and alternative results retained with cutoff and identifier reconciliation. No actual-start timestamps inferred. |
| sackmann_readme | sackmann_archive_upstream_readme, sackmann_archive_license, sackmann_archive_2026, tennismylife_2026 | Archive and alternative results retained with cutoff and identifier reconciliation. No actual-start timestamps inferred. |
| brisbane_2026_orders_play | brisbane_oop_20260104, brisbane_oop_20260111 | All eight daily primary order-of-play PDFs saved. Planned/not-before times, not actual starts. |
| halle_2026_final_schedule | halle_2026_official_op, halle_final_rendered | Official order of play and rendered final schedule replace failed route. |
| indian_wells_2026_final_schedule | indian_wells_2026_official_op, indian_wells_20260306_oop, indian_wells_20260307_oop | Selected official daily schedules, including final. Not complete tournament census. |
| rome_2026_programme_flipbook | rome_2026_official_op, rome_2026_official_mds, rome_final_broadcaster | Primary final order of play and draw plus broadcaster schedule replace required timing fields. |
| winston_2026_official_op | winston_oop_pdf, winston_semifinal_oop | Alternative official daily PDFs. Session sample, not all dates. |
| atp_collect_launch | atp_collect_rendered_v2 | Rendered official page recovered prior-art evidence. |
| google_trends_five_terms_explore | google_trends_daily_table_v2, google_trends_football_table_v5 | Four-term daily table plus separate football/FanCode daily table. Different scales cannot be concatenated as one five-term export. |
| cbic_gst_services_english | v5_gst_council_rates | Primary rate table replaces failed tax explainers. Tax-inclusive checkout still a scenario. |
| v3_wimbledon_creator_campaign | v5_wearisma_wimbledon | Alternative vendor campaign documentation. Use execution precedent, not causal efficacy or estimated paid CAC. |
| v3_cleartax_telecom_gst | v5_gst_council_rates | Primary rate table replaces failed tax explainers. Tax-inclusive checkout still a scenario. |
| v3_fancode_f1_july_interview | v3_mint_fancode_f1 | Different dated cofounder interview. Do not attribute January figures to July or call engaged fans paying subscribers. |
| v4_itd_price_mirror | fancode_monthly_final_v5, fancode_japan_entitlement_v5 | Price rechecked through public official routes. Current ATP price and monthly inclusion remain unknown. Use brief price for case model and two entitlement branches, not historical social price. |
| v4_atp_social_2026 | fancode_youtube_tennis_search, fancode_youtube_atp_search | Narrow FanCode public-video metadata supports engagement proxy only. Global ATP August claim not recovered. Omit that claim rather than substitute views for Indian payer demand. |
| v4_atp_fantasy | v4_deltatre_fantasy | Official implementation partner confirms ATP fantasy mechanics. No retention effect inferred. |
| v4_mototiming_schedule | v4_motogp_report_ned_rac, v4_assen_timetable | Official MotoGP session API and 29 combined reports replace aggregator. Offset errors and restart deduplication documented in v4 report. |
| v4_atp_fantasy_site | v4_deltatre_fantasy | Official implementation partner confirms ATP fantasy mechanics. No retention effect inferred. |
| v4_trends_football_pair | google_trends_football_table_v5 | Complete 255-row browser table recovered and checksum matched. Rounded relative interest, not zero-search proof. |
| v5_atp_media_index | v5_atp_media_guide_lta, atp_calendar_distribution_pdf | Recovered primary annual reference. Reconcile newer event dates before using guide calendar. |

## Reproducibility

Run `python3 scripts/verify_release.py` for locked-file integrity. `scripts/validate_recovery_v5.py` checks the full football table, document identity and complete failed-source mapping. The full raw validator also checks original body hashes, sizes, format parsing and orphan files. Source records preserve dates, URLs, methods and scope. Downloaded copyrighted sources and public review metadata remain local research material until redistribution is reviewed.

## New HTTP source audit

| ID and URL | HTTP | Local body | Scope review |
|---|---|---|---|
| [v5_gst_council_rates](https://www.gstcouncil.gov.in/sites/default/files/2024-02/gstservicerates.pdf) | 200 | `data/raw/pricing/v5_gst_council_rates__f1d4414623a4.pdf` | GST Council PDF, page 33 visually checked: heading 9984(ii) shows 9 + 9 / 18 for telecom, broadcasting and information supply excluding e-books. URL dated 2024-02. Supports 18% model scenario, not a FanCode tax invoice or proof of tax inclusion. Not a complete 2026 amendment audit. |
| [v5_wearisma_wimbledon](https://www.wearisma.com/all-resources/top-influencers/the-top-influencers-at-wimbledon-2026/) | 200 | `data/raw/engagement/v5_wearisma_wimbledon__8d74838636b1.html` | Vendor report identifies Star Sports India and JioHotstar Wimbledon creator campaign, including Vijay Kumar and Faisal Shaikh. Prior art only. Vendor Media Value and engagement ratios are not fees, paid conversions, audience deduplication or revenue. |
| [v5_atp_media_index](https://www.atptour.com/en/media/mediaguide/) | 403 | `data/raw/_failed_requests/company/v5_atp_media_index__c1b0ebfa4c32.html` | 403. Recovered full guide through LTA publisher search and PDF, source v5_atp_media_guide_lta. |
| [v5_lta_media_index](https://www.lta.org.uk/search-results/?p=3) | 200 | `data/raw/company/v5_lta_media_index__352eef5894ea.html` | Live search pagination changed from indexed snapshot. Does not itself contain the wanted media-guide link. Superseded by targeted publisher search. |
| [v5_atp_social_feed](https://thestandard.co/category/life/feed/) | 200 | `data/raw/audience_reports/v5_atp_social_feed__f8cd21d3a01d.xml` | HTTP200 returned HTML, not requested RSS XML. No matching ATP social-growth item recovered. Exclude from numerical evidence. |
| [v5_lta_media_search](https://www.lta.org.uk/search-results/?q=2026-atp-media-guide) | 200 | `data/raw/company/v5_lta_media_search__4d434e7d8475.html` | Publisher search result provides direct link to 2026 ATP media guide hosted by LTA. Discovery provenance, not independent audience evidence. |
| [v5_atp_media_guide_lta](https://www.lta.org.uk/siteassets/events/birmingham/media/2026-atp-media-guide-full-updated.pdf) | 200 | `data/raw/company/v5_atp_media_guide_lta__9e42011f5ec7.pdf` | 160-page ATP 2026 guide hosted by LTA. Welcome on PDF page3, contents5, calendar15-16, tournament directory17 onwards. Annual edition, not live schedule. Some fonts produce extraction warnings. Player records are publication-time facts, not September rankings. Global attendance is not Indian TV audience. |
