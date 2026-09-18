# FanCode ATP Analysis

The analysis behind a growth strategy for **ATP Tennis on FanCode in India**. It covers who can be converted into paying viewers, on which viewing occasions, at what price, whether that price repays acquisition, and the order in which budget should be released.

Every economic figure in the recommendation comes from one model, `models/atp_economics.py`, whose inputs sit in one tagged file, `models/model_inputs.json`. Every claim carries an evidence tag. Every public source is logged with its URL, fetch time and checksum.

---

## The recommendation this supports

**Turn one match into a season.** Launch an owned-led season-conversion engine now, and release acquisition scale capital only when a holdout proves it pays.

| Finding | Figure | Where |
| --- | --- | --- |
| India's attention peaks on tournaments FanCode does not hold | Search runs at **1.74x** an ordinary week in Slam fortnights, against **1.01x** in the Masters weeks FanCode holds | `05_search_attention` |
| Only part of the tour lands in Indian prime time | Of **165** event windows across **55** events, **19** hold 18:00–23:00 IST under every timing test. **8** of those are still ahead this season | `10_campaign_ready_windows` |
| No acquisition channel repays its cost on pass purchases alone | An acquired payer contributes **₹98.56** over 24 months. Owned messaging (₹99 CAC) comes closest. Paid media (₹333) loses **₹235** per payer | `08_economics_model` |
| The return depends on converting existing pass buyers to a season | With a 10% control upgrade rate, 24-month break-even needs a **13.9–15.7%** treatment upgrade rate, and 15-month payback needs **16.9–19.0%** | `08_economics_model` |

The upgrade lift is the central hypothesis, not an established result. The plan funds a ₹1 lakh first gate. Scale money moves only if the holdouts prove incremental acquisition and incremental season conversion.

---

## The economics model

`models/atp_economics.py` holds two mutually exclusive cohorts, each measured against its own holdout.

**1. Acquisition: new ATP pass buyers.**
- **Channels that stay funded.** Owned, native, contests and publisher clear the brief's ₹150–200 target on attributed CAC and keep their envelope.
- **Paid media.** At ₹333 it is capped to a ₹25 lakh test for audiences not already on FanCode.
- **Performance reserve (₹0.77 Cr).** The freed money is not moved into owned messaging, because owned reach is finite. It is released only to a channel whose measured marginal incremental CAC is at or below ₹200.
- **Result.** The committed ₹2.27 Cr, including brand and measurement, buys **151.2k** attributed payers at **₹150** blended attributed CAC. That meets ₹200 incremental CAC only if at least **75%** of those payers are genuinely incremental.

**2. Upgrade: existing ATP pass buyers moved to a season pass.**
- **Eligible cohort: 864k.** That is 24M ordinary-week viewers × 90% core (case, illustrative) × 20% reached (assumption) × 20% active pass buyers (assumption).
- **Counting.** Only upgrades above the 10% control rate are credited. Each is worth the season contribution less the passes that buyer would have bought anyway.
- **Credit cost.** The ₹44.50 credit costs ₹36.66 of contribution and is charged to every treated upgrader, including those who would have upgraded anyway.
- **New payers.** Later upgrades by newly acquired payers are not counted. They are upside.

| Scenario | Treatment upgrade rate | Acquired payers incremental | Net at 24 months | Payback |
| --- | --- | --- | --- | --- |
| No upgrade campaign | n/a | 100% / 87.5% / 60% | −₹0.99 / −₹1.18 / −₹1.59 Cr | Not inside 24 months |
| Low | 12% | 60% | −₹1.24 Cr | Not inside 24 months |
| Reference | 16% | 87.5% | +₹0.50 Cr | 17.1 months, fails the 15-month gate |
| High | 20% | 100% | +₹2.02 Cr | 12.3 months |

**Sensitivity to the active pass-buyer share.** At a 10% share instead of 20%, break-even rises to **16.9–20.5%**. Gate 1 therefore has to count the real share before any upgrade assumption is used.

**Gate sizing.** Each gate is sized to prove the economics, not merely to detect an effect.
- **Gate 1.** 46,928 users. It proves the owned lift's 95% lower bound clears the 0.496pp at which incremental CAC equals ₹200.
- **Gate 2.** Between 316 and 101,227 eligible pass buyers per arm, depending on how far the true rate sits above the threshold. It proves the upgrade rate's lower bound clears the break-even or payback threshold.
- **If the true rate sits close to a threshold, it cannot be proved at a sensible cost.** The decision is then continue or reallocate, never scale.

Campaign economics exclude the undisclosed rights fee. This is an incremental campaign P&L, not a claim about total rights ROI.

---

## Campaign-ready windows

`models/campaign_windows.py` scores every 2026 ATP event in FanCode's package as India viewing windows: day session, night session and final.

- **The timing test.** A window is **campaign-ready** only if its start sits inside all three viewing windows (18–23, 19–24 and 17–24 IST) under every start delay from 0 to 120 minutes. That is 12 of 12 tests.
- **What each window carries:**
  - its sport-clash check (F1 races, La Liga fixtures)
  - its player-story trigger (post-Slam follow-through, race to Turin, season finale)
  - the offer to sell
  - a timing-confidence label
- **Ranking.** Windows are ranked by a 100-point score: 40% timing robustness, 30% tier, 15% continuity and 15% clash-free. The weights are settings, not estimates.

The full list is `outputs/tables/10_campaign_ready_windows.csv`. The windows still ahead this season are in `10_campaign_ready_upcoming.csv`.

---

## Repository layout

| Path | Contents |
| --- | --- |
| `models/` | `atp_economics.py` and `campaign_windows.py`, the tagged `model_inputs.json`, and `atp_economics.json` output |
| `notebooks/source/` | 11 analysis notebooks, unexecuted |
| `notebooks/executed/` | The same notebooks with all outputs, exactly as run |
| `data/processed/` | Cleaned inputs the notebooks and models read |
| `data/manifests/` | Collection logs, source inventory, checksums, validation records |
| `outputs/tables/` | Result tables, prefixed by notebook number |
| `outputs/figures/` | Figures in PNG and SVG |
| `outputs/reports/` | Rendered notebooks, per-notebook findings and `index.html` |
| `outputs/validation/` | Checks run against the results |
| `config/`, `analysis_config/` | Source registry, evidence registry, collection protocol, analysis settings |
| `scripts/` | Collection, validation, notebook build and packaging tooling |
| `src/` | Shared helpers used across notebooks |
| `docs/` | Data availability, source catalogues, recovery notes |

---

## The notebooks

| Notebook | What it establishes |
| --- | --- |
| `00_evidence_and_case` | Case facts, operating assumptions and requirement coverage |
| `01_viewing_calendar` | Start times for the 2026 calendar in IST, with twelve finals verified against official orders of play |
| `02_portfolio_clashes` | Overlap between ATP finals and F1, football and MotoGP, so tennis is never sold into a fan's own match |
| `03_offers_and_baskets` | FanCode pricing, pass formats and basket comparisons against monthly and annual plans |
| `04_review_friction` | 15,229 app reviews, 4,903 low rated, classified for payment and access complaints |
| `05_search_attention` | 53 weeks of India search interest for tennis, each week tagged by what was on court |
| `06_player_and_video_risk` | Player availability and the risk of building a pass around individual names |
| `07_contribution_and_pricing` | Unit contribution per pass and per season, credit and discount hurdles, usage-cost stress |
| `08_economics_model` | The two-cohort model: channel CAC and net per payer, allocation by gate, P&L scenarios, break-even and payback upgrade rates, gate sizing |
| `09_retention_and_experiments` | Retention journeys, KPI definitions with fixed denominators, general power grids |
| `10_campaign_ready_windows` | The scored 2026 window list and the windows still ahead this season |

---

## Evidence convention

| Tag | Meaning |
| --- | --- |
| **C** | Case input, taken from the brief as given |
| **O** | Observed, collected from a named public source and recorded in the manifests |
| **D** | Derived, computed here from C or O inputs |
| **A** | Assumption, chosen by us and stated as such |

Every model input carries one of these tags in `models/model_inputs.json`, and `outputs/tables/08_model_inputs.csv` lists them.

---

## Sources

| Source | What it contributed |
| --- | --- |
| Case brief | Every **C** figure: illustrative audience scale, the ₹79–99 pass range, the ₹399 season, the 60–65% repeat rate, 90% season renewal, the 7.8% contest conversion, the ₹150–200 CAC target |
| [Google Trends India](https://trends.google.com) | Weekly interest for tennis and comparison sports across 2025 and 2026 |
| IBM Sports Fan Survey 2025 | n = 2,209. Used only as a relative weight between sports, never as a population count |
| [Play Store](https://play.google.com) and [App Store](https://apps.apple.com) | 15,229 FanCode reviews, classified for payment and access friction |
| [FanCode](https://www.fancode.com) | Offer, plan and checkout pages captured 13 September 2026 |
| [ATP](https://www.atptour.com) | Tour calendar and official orders of play |
| [Formula 1](https://www.formula1.com), [La Liga](https://www.laliga.com), [MotoGP](https://www.motogp.com) | Competing fixture calendars, converted to IST |
| [Razorpay](https://razorpay.com), [Cloudflare Stream](https://www.cloudflare.com), GST schedule | Gateway fees, delivery cost and tax behind unit contribution |
| Meta rate card, Nurdd CPC benchmarks, Kofluence creator report | Message and media costs behind channel CAC |
| [Tennis TV](https://www.tennistv.com), SonyLIV, JioHotstar | Competitor pricing |
| Public reporting on FanCode's F1 engagement | The 21M engaged F1 fans that anchor the sport pools |

---

## Reproducing the analysis

The two models and notebooks 08 and 10 run from committed files only:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install jupyter pandas numpy matplotlib scipy statsmodels pypdf beautifulsoup4 pillow
python models/atp_economics.py      # writes models/atp_economics.json
python models/campaign_windows.py   # writes outputs/tables/10_campaign_ready_windows.csv
```

To change an assumption, edit `models/model_inputs.json` and rerun. `scripts/analysis/build_notebooks.py` regenerates the notebook sources. `scripts/analysis/run_notebooks.py` executes them. `scripts/analysis/package_analysis.py` validates the package and rebuilds `outputs/reports/index.html`.

Notebooks 00–07 and 09 read the raw captures, which are not committed. Their executed versions, tables and figures are committed as run.

---

## On the raw captures

The raw HTML and PDF captures are saved copies of third-party pages, and republishing them is not ours to do.

What is committed is the full provenance trail. `config/sources.json` and `data/manifests/` record every source URL, when it was fetched, whether validation passed, and the checksum of what was retrieved.

---

## Limits

- **The upgrade lift is a hypothesis.** The 20% active pass-buyer share, the 10% control rate and the treatment rate are assumptions to be tested in Gates 1 and 2, not measured FanCode behaviour.
- **The core audience is the brief's illustration.** 21.6M = 24M ordinary-week viewers × 90%, both labelled illustrative in the brief. The upgrade cohort is built on it and says so.
- **Audience pools are not counts of buyers.** The F1, football and MotoGP pools are anchored on one reported company figure and weighted by a survey ratio. They split in-app payers between personas and test reachability. They are not subscriber numbers.
- **Test-ceiling CACs are purchasing rules.** Native personalities (₹150) and publisher takeovers (₹180) have no public cost basis. They are ceilings a purchase must meet, not estimates.
- **Session times are modelled** except for the twelve verified finals. Each week's order of play must be confirmed before a send.
- **Football clashes after 8 September 2026 are not checked**, because 2026-27 fixtures were not captured. MotoGP session clocks are quarantined in `02_portfolio_clashes`.
- **App review counts measure visibility, not awareness.**

---

## Not included

The competition case brief is not in this repository. It is copyrighted by its authors and marked not for reproduction.
