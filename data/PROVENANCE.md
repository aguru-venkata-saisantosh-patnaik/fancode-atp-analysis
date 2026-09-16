# Raw collection guide

**Current release: raw-v5-2026-09-14.** See the [final recovery and gap treatment](../../docs/RAW_V5_CLOSURE.md). This update supersedes earlier status summaries below. Football Trends and the full primary ATP guide are now recovered. Every failed HTTP source has an explicit disposition. Remaining private or ambiguous facts use the documented scenario treatments.

Author: Competition team

Provider files are immutable snapshots. Their names normally contain a stable source ID and the first 12 characters of the full SHA-256 stored in the manifest. Corrections belong in the source-validation notes or later processing code, never inside a downloaded body.

| Folder | Contents | Interpretation |
|---|---|---|
| `case_inputs/case_brief/` | Original competition problem statement | Supplied commercial assumptions and submission requirements |
| `case_inputs/reference_cases/` | Six supplied reference presentations | Analytical and visual references, not FanCode measurements |
| `schedules/` | ATP programmes/orders, F1 calendar, 177 official MotoGP session records, 29 race reports, 421 La Liga records and source documentation | Mixture of event dates, scheduled starts, not-before times and discovery pages |
| `player_results/` | Official completed draws for 12 editions, secondary 2025/2026 CSVs, ongoing snapshot and source documentation | Mixed coverage, incompatible identifiers and unresolved date semantics. Reconcile before joining |
| `offers/` | FanCode/competitor product pages, terms and official price announcement | Product evidence at retrieval date, with eligibility limits |
| `reviews/google_play/` | Original public mobile and TV review RPC response bodies | All accessible ratings retained, no sentiment filtering |
| `reviews/` | iOS RSS pages and store listings | Store metadata and bounded most-recent review sample |
| `company/` | Rights announcement and company context | Public rights scope, not internal costs or subscriber economics |
| `channel_costs/` | Indian vendor rate listings, creator report pages and separately limited international benchmark | Ad unit costs and reference material, not observed FanCode CAC |
| `methodology/` | Primary Google Trends and conversion-lift documentation | Measurement definitions, not observations from an experiment |
| `browser_captures/` | Selected verbatim text transcribed from rendered public pages | Field notes with explicit selection scope, not full HTML or screenshots |
| `search_interest/` | Four-term 255-day 2026 browser table, original two-term 53-week 2025 API response, request metadata and failed requests | Relative India search interest. 2025 and 2026 requests have different frequency and normalization |
| `public_video/` | Two official FanCode channel keyword-search HTML pages | 53 distinct video IDs in an incomplete ranked sample. No media files downloaded |
| `audience_reports/` | Public research reports and publisher summaries | Distinct dates, populations and methods, not interchangeable payer counts |
| `pricing/` | Additional public product listings and terms | Listed prices and terms, not completed transactions |
| `cost_benchmarks/` | Supplier prices, rate-card mirror and vendor comparison dataset | External cost inputs, some low-confidence proxies |
| `engagement/` | Existing creator campaign and product-feature evidence | Prior art and feasibility, not measured incremental lift |
| `measurement/` | Additional published research design | Methodology only, no purchased tracker results |
| `_failed_requests/` | Preserved error, challenge and rate-limit response bodies | Excluded from substantive analysis |

The location of a file does not certify usability. Check `../manifests/source_validation.json`. Some HTTP 200 pages contain only placeholders or a different year's schedule. Some `.html` filenames contain valid JSON because the source response header was inconsistent. Use format detection, not filename alone.

A repeated hash indicates duplicate content, for example the same final draw reached through two source IDs. It is one source document, not two independent observations. The initial empty iOS page-2 response remains alongside the later successful response, with both attempts retained in the log.

Do not count gates opening as match starts, ticket sessions as ATP-only minutes, “not before” as actual starts, a final draw as information known before the event, app installs as payers or vendor rate cards as causal acquisition costs. Future tables and notebook transformations belong outside this folder.

The current release is raw-v5. All previous raw bodies remain intact. Archived v1, v2, v3 and v4 metadata is under `data/releases/`. See [the recovery report](../../docs/RAW_V4_RECOVERY.md) for expanded evidence and surviving gaps.

Fourth-pass sources and semantic defects are documented in [RAW_V4_RECOVERY.md](../../docs/RAW_V4_RECOVERY.md). MotoGP API offset labels conflict with checked local schedules. The 2025 Trends series has boundary-crossing weekly bins. Neither issue is repaired inside raw provider files.
