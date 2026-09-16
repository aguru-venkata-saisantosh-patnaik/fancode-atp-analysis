# Second-pass raw collection recovery

Author: Competition team

Collection date: 14 September 2026. This release expands the evidence collection. It does not contain a fitted model, cleaned analysis tables or presentation outputs.

The expanded collection contains **254 raw files**, including **34 additions** to v1. It records 151 HTTP source IDs, of which 129 retrieved a body successfully and 22 remain failed. Successful retrieval does not certify suitability. There are also 13 documented browser observations and seven supplied PDFs.

## What was recovered

| Block | First release | Second-pass result | Permitted use |
|---|---|---|---|
| Official ATP singles draws | 7 of 12 selected editions | All 12. Recovered Winston-Salem, Marrakech, Madrid, Dubai and Indian Wells | Retrospective participation, rounds and results within the fixed sample |
| Official final orders | Five requests failed | Miami, Marrakech, Madrid, Dubai and Indian Wells final-day PDFs recovered | Planned timing evidence with release timestamps and walkover caveats |
| Google Trends | No values | Complete 255-day table, 1 January to 12 September 2026, India, Web Search, all categories, tennis/FanCode/Formula 1/MotoGP search terms | Exploratory relative search interest with confounding and query ambiguity disclosed |
| Secondary results | Original repository returned 404 | Sackmann archival mirror: 2,944 rows for 2025 and 1,449 for 2026. TennisMyLife: 2,944 rows for 2025, 2,132 for 2026 and 127 in the ongoing snapshot | Broader progression work after reconciling identifiers, event coverage and date definitions |
| Monthly offer | Subscription route showed ₹116 | Recurring route shows ₹199 less ₹20 coupon, payable ₹179, and one-time/recurring-payment wording | Route-specific price audit. Both observations preserved |
| Current future calendar | Distribution PDF with outdated labels/TBDs | 16 visible September-November official event windows | Update future planning after excluding events outside the relevant rights scope |
| ATP stream listing | Chengdu observation | Seven Hangzhou daily stream cards | Product-listing audit. Seven cards are not seven individual tennis matches |
| Existing engagement mechanic | Not captured | ATP Collect official 2025 announcement and FAQ excerpt | Prior-art and feasibility reference, not a measured retention effect |
| FanCode public video | Not captured | Two public channel-search snapshots. 28 tennis-query and 30 ATP-query entries, 53 distinct video IDs | Bounded metadata exploration, not a census or India-only demand estimate |

All ten official PDF retries returned HTTP 200 and parsed as PDFs. Their failed first-attempt bodies remain in the raw folder.

The Trends download button did not produce an accessible file. The complete accessible chart table was therefore transcribed as tab-separated text, preserving the provider's x/y headers. Only directional formatting characters and outer whitespace were removed. The stored text matched the live DOM on 5,587 characters, 255 data rows and FNV-1a checksum `8edf4d2d`. Its file is separately protected by SHA-256. The query mapping and related-query context are registered in `manual_captures.json`. This is a documented browser-table capture, not an original provider CSV export.

## Problems discovered during validation

1. The two results publishers use different player identifiers and overlapping matches. Their row counts cannot be added to claim unique coverage. The mirror includes the original dictionary and CC BY-NC-SA 4.0 attribution. TennisMyLife's database page declares MIT licensing and describes its collection process.
2. The mirror's 2026 snapshot is from June. Its latest tournament-week value is 25 May. It is not a September season-to-date file.
3. TennisMyLife's documentation calls `tourney_date` the tournament week. In its 2026 file, 47 event IDs instead have multiple dates. The ongoing file also varies by date. The 2025 file does not. The date basis and timezone must be reconciled separately for each file.
4. TennisMyLife's Winston-Salem final date is 30 August while the official final order says 29 August. That mismatch cannot be resolved by assuming a timezone.
5. TennisMyLife's 2025 file has 489 missing match numbers and 480 repeated tournament-ID/match-number keys. The 2026 file has two repeated keys. Do not delete these rows as duplicates without inspecting the full match identity.
6. The ongoing US Open file includes the 13 September final, outside the registered cutoff. Its presence in raw is intentional. Later processing must exclude post-cutoff observations using verified dates.
7. FanCode's monthly offers differ by public route. Neither observation settles ATP inclusion, the renewal charge or tax invoicing. The Hangzhou listing also illustrates why stream cards cannot be counted as individual matches.
8. ATP Collect already offers free match collectibles. Its reported historical participation is global, publisher-reported and unrelated to demonstrated FanCode paid retention. Reward eligibility varies by country.

## Remaining gaps and stopping decisions

| Gap | Retry result | Treatment |
|---|---|---|
| Broader Trends series including football and 2025 | Public five-term endpoint returned 429 | Preserve failure, no further endpoint retries. Four-term browser series is the available scope |
| Current ATP checkout price and monthly inclusion | Recurring monthly route and another public ATP listing inspected | Still unresolved. Use case prices as case inputs and retain both entitlement branches |
| Tennis TV India price | Get Premium and public package route reached registration | No account created. No India price claimed |
| GST source | English CBIC rate-page retry failed to connect | Tax-inclusive treatment remains a scenario, not an invoice fact |
| Complete actual match starts | Recovered orders remain scheduled/not-before evidence. Results CSVs contain no starts | No duration stacking presented as actual timing |
| Full annual calendar revisions | Current browser capture covers 16 future windows. Page's PDF link points to Challenger calendar | Keep partial update explicit and retain original calendar caveats |
| Football kickoff census | No additional exact-kickoff dataset collected | Existing date/competition context only |
| Full YouTube census, exact publication dates and geography | Only initial keyword-search pages collected | Disclose selection and publication-age limitations |
| Full creator-cost report and payer conversion | Gated report/internal outcomes unavailable | Existing public vendor unit costs plus explicitly labelled modelling assumptions later |
| Respondents, internal cohorts and rights fees | No new access supplied | No fabricated respondent, payer or cost records |

## Reproduce the checks

From the repository root:

```bash
python3 scripts/verify_release.py
python3 scripts/verify_release.py --archive raw-v1-2026-09-14
python3 scripts/validate_results_sources.py
python3 scripts/validate_video_sources.py
# With requirements-collection.txt installed:
python3 scripts/validate_raw.py
```

`release.json` locks the current raw inventory and provenance. Archived v1 metadata verifies its original 220 raw bodies in their existing locations. The archive does not duplicate the large raw directory. Live refetches can change, while the retained snapshots support reproducible offline analysis. Raw third-party material remains local and has not been published or submitted.
