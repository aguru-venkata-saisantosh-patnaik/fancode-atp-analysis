# FanCode ATP Analysis

Analysis behind a growth strategy for **ATP Tennis on FanCode in India**: who can be converted into paying viewers, on which viewing occasions, at what price, whether that price repays the cost of acquisition, and the order in which budget should be released.

Every figure used in the final recommendation is reproducible from this repository. Each claim is tagged with the kind of evidence behind it, and each source is logged with its URL, fetch time and checksum.

---

## The problem

ATP Tennis is a portfolio sport with no home crowd and no fixed season. Its calendar runs most of the year, across time zones India does not control, and its biggest moments belong to other broadcasters. Three findings shaped the answer.

| Finding | Figure | Where it comes from |
| --- | --- | --- |
| India's attention peaks on tournaments FanCode does not hold | Search runs at **1.74x** an ordinary week during the Grand Slams, against **1.01x** during the Masters events FanCode does hold | `05_search_attention` |
| Most of the tour is watchable in India, but not all of it | **31 of 55** events land in an Indian evening. Of twelve verified finals, **six** hold prime time under every delay test | `01_viewing_calendar` |
| A single cheap pass cannot repay acquisition | An ₹89 pass keeps **₹43.32** after tax, fees and delivery, against a ₹150 to 200 target cost per subscriber | `07_contribution_and_pricing` |

The conclusion the analysis supports: grow through users FanCode already reaches who show tennis interest, sell the cheapest access that covers the occasion they came for, and treat outside acquisition as something to be earned by measurement rather than assumed.

---

## Repository layout

| Path | Contents |
| --- | --- |
| `notebooks/source/` | 11 analysis notebooks, unexecuted, one per question |
| `notebooks/executed/` | The same notebooks with all outputs, exactly as run |
| `models/` | `year1_model` and `audit_v2`, the corrected model that supersedes it |
| `data/processed/` | Cleaned inputs the notebooks read |
| `data/manifests/` | Collection logs, source inventory, checksums, validation records |
| `outputs/tables/` | 79 result tables |
| `outputs/figures/` | 42 figures in PNG and SVG |
| `outputs/reports/` | Rendered notebook reports and per-question findings |
| `outputs/validation/` | Checks run against the results |
| `config/` | Source registry, external evidence registry, collection protocol, environment lock |
| `scripts/` | Collection, validation and release tooling |
| `src/` | Shared helpers used across notebooks |
| `docs/` | Data availability, source catalogues, recovery notes |

---

## The notebooks

| Notebook | What it establishes |
| --- | --- |
| `00_evidence_and_case` | Case facts, operating assumptions, and the claim register every later notebook writes into |
| `01_viewing_calendar` | Real start times for all 55 regular 2026 events, converted to IST, with twelve finals verified against official orders of play |
| `02_portfolio_clashes` | Overlap in minutes between ATP finals and F1, football and MotoGP, so tennis is never sold into a fan's own match |
| `03_offers_and_baskets` | Live FanCode pricing, pass formats and basket comparisons against the monthly and annual plans |
| `04_review_friction` | 15,229 app reviews, of which 4,903 are low rated, classified for payment and access complaints |
| `05_search_attention` | 53 weeks of India search interest for tennis, each week tagged by what was on court |
| `06_player_and_video_risk` | Player availability and the risk of building a pass around individual names |
| `07_contribution_and_pricing` | Unit contribution per pass and per season after GST, gateway fees and delivery cost |
| `08_channel_economics` | Cost per acquired payer by channel, and the allocation that follows from it |
| `09_retention_and_experiments` | Retention behaviour, KPI definitions with fixed denominators, and experiment design |
| `10_strategy_and_claims` | Final claims, each tied back to the notebook and source that produced it |

---

## The models

Two models sit in `models/`, and the difference between them matters.

**`year1_model`** was the first pass: persona targets, channel budget and a year-one P&L.

**`audit_v2`** is the corrected model and the one the final recommendation uses. It fixes five errors found when the first pass was audited:

1. **No subtraction across different population bases.** The earlier version subtracted a weekly viewing estimate from a survey-derived follower estimate. Populations are now anchored on one reported company figure, 21M engaged F1 fans, with survey shares used only as relative weights between sports.
2. **Repeat purchase read correctly.** The case states that match-pass buyers return at 60 to 65%. Read as "ever repurchases", a buyer makes about **1.6** purchases, not the four implied by treating that rate as a per-event hazard.
3. **Audience pools demoted to a capacity check.** The pools test whether the year-one target is a reachable share of the audience, **0.47% to 1.5%**, rather than forecasting demand.
4. **Seasonality-aware payback, across three scenarios.** Year-two contribution is earned over the eight busy months of the tour, not spread evenly. Payback lands at **12.0, 13.4 and 20.9 months** in the high, base and low cases. The low case does not repay inside two years.
5. **Purchase CAC and incremental CAC kept apart.** A blended **₹175** purchase CAC is **₹291** if only 60% of payers are genuinely new. The pilot is therefore sized on the lift that pays for itself, a **0.496pp** break-even, and not on the smallest detectable lift.

Both are kept so the correction is auditable rather than quietly overwritten.

---

## Evidence convention

Every claim in the analysis carries one of four tags, used consistently across notebooks, tables and the claim register in `outputs/reports/claim_register.json`.

| Tag | Meaning |
| --- | --- |
| **C** | Case input, taken from the brief as given |
| **O** | Observed, collected from a named public source and recorded in the manifests |
| **D** | Derived, computed in these notebooks from C or O inputs |
| **A** | Assumption, chosen by us and stated as such |

---

## Sources

| Source | What it contributed |
| --- | --- |
| Case brief | Every **C** figure: illustrative audience scale, the ₹79 to 99 pass range, the ₹399 season, the 60 to 65% repeat rate, 90% season renewal, the ₹150 to 200 CAC target |
| [Google Trends India](https://trends.google.com) | Weekly interest for tennis and comparison sports across 2025 and 2026, tagged by what was on court, producing 1.74x against 1.01x |
| IBM Sports Fan Survey 2025 | n = 2,209. Used only as a relative weight between sports, never as a population count |
| [Play Store](https://play.google.com) and [App Store](https://apps.apple.com) | 15,229 FanCode reviews collected, 4,903 of them low rated, classified for payment and access friction |
| [FanCode](https://www.fancode.com) | Offer, plan and checkout pages captured 13 September 2026 for live pricing |
| [ATP](https://www.atptour.com) | Tour calendar and official orders of play for start-time verification |
| [Formula 1](https://www.formula1.com), [La Liga](https://www.laliga.com), [MotoGP](https://www.motogp.com) | Competing fixture calendars, converted to IST for clash analysis |
| [Razorpay](https://razorpay.com), [Cloudflare Stream](https://www.cloudflare.com), GST schedule | Gateway fees, delivery cost and tax treatment behind unit contribution |
| Meta rate card, Nurdd CPC benchmarks, Kofluence creator report | Message and media costs behind channel CAC |
| [Tennis TV](https://www.tennistv.com), SonyLIV, JioHotstar | Competitor pricing for the per-event comparison |
| Public reporting on FanCode's F1 engagement | The 21M engaged F1 fans figure that anchors every audience pool |

Every capture is logged in `data/manifests/` with its URL, timestamp, validation result and SHA-256 checksum.

---

## Reproducing the analysis

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install jupyter pandas numpy matplotlib
jupyter lab
```

Run `notebooks/source/` in order, 00 through 10. Each reads from `data/processed/` and writes to `outputs/`. The models run standalone:

```bash
python models/audit_v2.py      # writes audit_v2.json
python models/year1_model.py   # writes year1_model.json
```

`config/collection_environment.lock.txt` records the environment the collection scripts ran in.

---

## On the raw captures

The raw HTML captures are not committed. They are saved copies of third-party pages, and republishing them is not ours to do.

What is committed is the full provenance trail. `config/sources.json` and `data/manifests/` record every source URL, when it was fetched, whether validation passed, and the checksum of what was retrieved, so any figure can be traced to its origin and re-collected with the scripts in `scripts/`.

---

## Limits

- **The audience pools are not counts of buyers.** The 7.8M, 14.0M and 1.6M sport pools are anchored on one reported company figure and weighted by a survey ratio. They rank the segments and test that the target is reachable. They are not FanCode subscriber numbers.
- **Some case figures are illustrative.** The 36M, 21.6M and 14.4M audience figures are the brief's own and are labelled illustrative there. They are used as scale only, and no revenue is built on them.
- **App review counts say nothing about awareness.** Review mentions measure what people write about, not what they know. They are used only to size payment and access friction.
- **The low case loses money.** If owned prompts convert at half the estimate, blended purchase CAC rises to about ₹228 and payback passes 20 months. That case is kept visible in the model rather than excluded.

---

## Not included

The competition case brief is not in this repository. It is copyrighted by its authors and marked not for reproduction.
