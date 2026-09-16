# FanCode ATP Analysis

Analysis behind a strategy for growing paid ATP Tennis viewership on FanCode in India: who can be converted, on which viewing occasions, at what price, whether it repays acquisition, and how the budget should be released.

Every figure used in the final recommendation is reproducible from this repository.

## Layout

| Path | Contents |
| --- | --- |
| `notebooks/source/` | 11 analysis notebooks, unexecuted, one per question |
| `notebooks/executed/` | The same notebooks with outputs, as run |
| `models/` | Year-one channel and P&L model, plus `audit_v2` which corrects and supersedes it |
| `data/processed/` | Cleaned CSVs the notebooks read: event start times, fixtures, offers, reviews, search interest |
| `data/manifests/` | Collection logs, source inventory, checksums and validation records for every raw capture |
| `outputs/tables/` | 79 result tables |
| `outputs/figures/` | 42 figures, PNG and SVG |
| `outputs/reports/` | Rendered notebook reports and per-question findings |
| `outputs/validation/` | Checks run against the results |
| `config/` | Source registry, external evidence registry, collection protocol and environment lock |
| `scripts/` | Collection, validation and release tooling |
| `src/` | Shared helpers used by the notebooks |
| `docs/` | Data availability, source catalogues and recovery notes |

## The notebooks

| Notebook | Question it answers |
| --- | --- |
| `00_evidence_and_case` | Case facts, operating assumptions and the claim register |
| `01_viewing_calendar` | When ATP events actually start in Indian time |
| `02_portfolio_clashes` | Overlaps with F1, football and MotoGP |
| `03_offers_and_baskets` | Live pricing, offers and basket comparisons |
| `04_review_friction` | What app reviews say about payment and access |
| `05_search_attention` | Weekly search interest for tennis in India |
| `06_player_and_video_risk` | Player availability and video evidence risk |
| `07_contribution_and_pricing` | Unit contribution per pass and per season |
| `08_channel_economics` | Cost per acquired payer by channel |
| `09_retention_and_experiments` | Retention behaviour and experiment design |
| `10_strategy_and_claims` | Final claims, each tied back to its source |

## Evidence convention

Claims carry one of four tags, used consistently across notebooks, tables and the claim register:

- **C** case input, taken from the brief
- **O** observed, collected from a public source and recorded in the manifests
- **D** derived, computed in these notebooks from C or O inputs
- **A** assumption, chosen by us and stated as such

## Reproducing

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install jupyter pandas numpy matplotlib
jupyter lab            # run notebooks/source in order, 00 to 10
```

`config/collection_environment.lock.txt` records the environment the collection scripts were run in. `data/manifests/RAW_SHA256SUMS.txt` holds checksums for every raw capture.

## On the raw captures

The raw HTML captures are not committed. They are saved copies of third-party pages, and republishing them is not ours to do. What is committed is the full provenance trail: `config/sources.json` and `data/manifests/` record every source URL, when it was fetched, whether validation passed and the checksum of what was retrieved, so any claim can be traced to its origin and re-collected.

## Not included

The competition case brief is not in this repository. It is copyrighted by its authors and marked not for reproduction.
