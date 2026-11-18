# PyNMDF

Reproducible analysis for a four-page conference paper on minimum demand forecasting.

**Question.** Once rooftop PV capacity is in the model, does weather improve one-year-ahead
probabilistic forecasts of annual minimum demand?

**Case study.** One Ausgrid network total (the sum of the public zone substations, at 30 minutes)
for calendar years 2015 to 2025, with five simple models compared under one rolling-origin
protocol at POE10, POE50 and POE90, and a sixth added afterwards as a supplementary check. All
inputs are public.

Two documents sit beside this one:

- [docs/results_summary.md](docs/results_summary.md): the numbers behind the paper, by type of
  evidence, each with the file it comes from.
- [docs/analysis_plan.md](docs/analysis_plan.md): the design, and the record of every decision
  and finding made while building (D1 to D33, F1 to F11).

## Install

Windows, Python 3.11:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

## Data

Nothing from Ausgrid or the Bureau of Meteorology is stored in this repository. Both keep
copyright in their files, so download them yourself and point the configuration at them.

| Variable | Source | What to download |
|---|---|---|
| Demand | [Ausgrid distribution zone substation data](https://www.ausgrid.com.au/about-us/about-ausgrid/research-data-sets/distribution-zone-substation-data) | One archive per reporting year, FY2015 to FY2026 (each runs 1 May to 30 April). Leave them zipped, or unzip into a folder |
| PV capacity | [Ausgrid average electricity use](https://www.ausgrid.com.au/about-us/about-ausgrid/research-data-sets/average-electricity-use) | The local government area workbook for each year, FY2015 to FY2025. FY2024 exists only as a PDF; its network total is entered in the configuration |
| Weather | [BOM Climate Data Online](http://www.bom.gov.au/climate/data/), station 066037 (Sydney Airport AMO) | Daily maximum temperature (IDCJAC0010), daily minimum temperature (IDCJAC0011) and daily global solar exposure (IDCJAC0016), each as "all years of data" |

Then copy `config.example.yaml` to `config.local.yaml` and edit the entries under `paths`. That
is the only change needed; `config.local.yaml` is git-ignored.

## Run

Run the eight main notebooks in order. Each reads the cached outputs of the ones before it.

```powershell
$notebooks = "01_demand_network_total", "02_pv_and_weather", "03_fig1_introduction",
    "04_results_data_insights", "05_backtest_models", "06_results_forecast_comparison",
    "07_robustness_and_sensitivity", "08_daily_out_of_sample"
foreach ($name in $notebooks) {
    .venv\Scripts\jupyter nbconvert --to notebook --execute --inplace "notebooks\$name.ipynb"
}
```

Notebook 01 reads every raw demand file and takes a few minutes; notebooks 05 and 07 take a
minute or two each; the others are quick. The two archive notebooks are optional and run the
same way, after notebook 05:

```powershell
foreach ($name in "A1_model_exploration", "A2_superseded_figures") {
    .venv\Scripts\jupyter nbconvert --to notebook --execute --inplace "notebooks\archive\$name.ipynb"
}
```

Every run reproduces every file exactly: the random draws are seeded and XGBoost runs on one
thread.

Tests, linter and formatter:

```powershell
.venv\Scripts\python -m pytest
.venv\Scripts\ruff check .
.venv\Scripts\black --check src tests
```

## Reproduce the main result

After the eight notebooks have run, the one-year-ahead comparison is in
`outputs/tables/table3.csv` (pinball loss and coverage of the six models) and
`outputs/tables/headline_numbers.csv` (the four comparisons between models). The daily
out-of-sample test is in `outputs/tables/table4.csv`. `docs/results_summary.md` lists every
number the paper relies on with its file.

## Where results go

| Folder | Holds |
|---|---|
| `outputs/figures`, `outputs/tables` | The paper's figures and tables, named by their number in the paper, with the data behind the figures |
| `outputs/checks` | Everything the paper's limitation and robustness statements rely on |
| `outputs/archive` | Superseded versions and exploration, written by `notebooks/archive` |
| `data/interim` | Cached data passed between notebooks |

All four are git-ignored and rebuilt by the notebooks. Figures are saved as PNG (600 dpi) and
PDF, tables and checks as CSV.

## Paper artifacts

| Artifact | File | Notebook |
|---|---|---|
| Fig. 1: annual maximum, overnight low, daytime low and energy | `figures/fig1`, `tables/fig1_data.csv` | 03 |
| Fig. 2: when the lowest 1% of half hours occur, with PV capacity | `figures/fig2`, `tables/fig2_data.csv` | 04, section 2 |
| Fig. 3: low end of the load duration curve (optional candidate) | `figures/fig3` | 04, section 3 |
| Fig. 4: daytime low against solar exposure; minimum against temperature | `figures/fig4`, `tables/fig4_fits.csv` | 04, section 5 |
| Fig. 5: POE bands on the annual daytime low, M2 to M5 | `figures/fig5` | 06, section 3 |
| Fig. 6: monthly pinball loss by calendar month, daytime low (optional candidate) | `figures/fig6`, `tables/fig6_data.csv` | 06, section 4 |
| Table I: the six models | `tables/table1.csv` | 05, section 3 |
| Table II: each year's minimum, with the overnight and daytime lows | `tables/table2.csv` | 04, section 4 |
| Table III: one-year-ahead POE scores, six models, both targets, annual and monthly | `tables/table3.csv` | 06, section 2 |
| Table IV: daily out-of-sample test, the models and three pairs | `tables/table4.csv` | 08, section 6 |
| Straight-line fit of the annual daytime low on PV capacity and on the year | `tables/table_pv_fit.csv` | 04, section 6 |
| The four comparisons between models, on pinball loss | `tables/headline_numbers.csv` | 06, section 5 |

## Supporting checks

All in `outputs/checks`.

| Check | File | Notebook |
|---|---|---|
| What the cleaning did to each reporting-year file | `check_data_quality.csv` | 01, section 3 |
| The reader against the stress-test minima | shown, not saved | 01, section 4 |
| Each year's minimum, maximum, share of half hours kept and energy | `check_annual_summary.csv` | 01, section 6 |
| Share of each month kept | `check_kept_by_month.csv` | 01, section 7 |
| Level steps where reporting years join at 1 May | `check_join_steps.csv` | 01, section 8 |
| Substations that appear to stay on standard time | `check_clock.csv` | 01, section 9 |
| The change in sign convention for reverse flow | `check_sign.csv` | 01, section 10 |
| PV capacity against the expected table | `check_pv_capacity.csv` | 02, section 2 |
| Weather gaps | `check_weather_missing.csv` | 02, section 4 |
| Temperature quality flags | `check_weather_quality.csv` | 02, section 5 |
| Whether the two trough windows catch the daily minimum | `check_trough_windows.csv` | 04, section 7 |
| Complete days behind the 15-lowest-days measure | `check_complete_days.csv` | 05, section 2 |
| Plain XGBoost beyond the PV capacity it was trained on | `check_m5_pv_range.csv` | 05, section 5 |
| The holiday check: public holidays against ordinary weekend days | `check_holiday_miss.csv` | 05, section 6 |
| M4 term diagnosis: one group of weather terms switched off | `check_m4_terms.csv` | 05, section 7 |
| M4's weather coefficients and the reach of PV x solar beyond training | `check_m4_coefficients.csv` | 05, section 7 |
| Bias of POE50 by model, including M6's monthly bias | `check_poe50_bias.csv` | 06, section 6 |
| The 15-lowest-days measure: Table III and the comparisons on it | `table3_robust.csv`, `sensitivity_robust.csv` | 07, section 2 |
| Reporting thresholds of 90%, 95% and 98% | `sensitivity_thresholds.csv` | 07, section 3 |
| The rescaled series: factors and annual lows | `sensitivity_rescale_factors.csv`, `sensitivity_rescaled_lows.csv` | 07, sections 4.1 and 4.2 |
| The rescaled series: Table III and the comparisons | `table3_daytime_low_rescaled.csv`, `table3_minimum_rescaled.csv`, `sensitivity_rescaled_comparisons.csv` | 07, sections 4.3 and 4.4 |
| Table IV by test year | `daily_skill_by_year.csv`, `daily_pairs_by_year.csv` | 08, sections 4 and 5 |

## The archive

`notebooks/archive` holds two notebooks that write to `outputs/archive`. Nothing in the archive
is used by the paper or by its limitation and robustness statements; it is kept so that earlier
versions and exploration stay reproducible.

| Notebook | Holds |
|---|---|
| `A1_model_exploration` | The first look at each model's POE50 against the actuals; the day M3 predicts as lowest, which led to the single non-working-day flag; the miss on public holidays, holiday by holiday and around Christmas |
| `A2_superseded_figures` | Fig. 5 with three panels (M2, M3, M4), on the daytime low and on the whole-day minimum; Fig. 6 on the whole-day minimum, with its data |

## Layout

```
config.example.yaml      raw-data paths and every decision parameter (committed)
config.local.yaml        your real paths (git-ignored)
docs/analysis_plan.md    the design and the record of every decision taken while building
docs/results_summary.md  the numbers behind the paper, by type of evidence
docs/                    the author's own notes (decision_log.md, substation_set_decisions.md,
                         public_cross_check.md)
src/pynmdf/              the logic, as a small importable package
  config.py              load the configuration and prepare the output folders
  io_demand.py           read every zone substation file layout
  io_pv.py               read PV capacity from the LGA workbooks; daily capacity series
  io_weather.py          read the BOM daily files; fill short gaps
  clean.py               cleaning rule, the network total, its checks and the rescaled series
  targets.py             the three scored targets, daily troughs, summaries and line fits
  models.py              the daily models: the nested ladder M2 to M5, and M6
  poe.py                 POE10, POE50 and POE90: past errors for M1, the replay for M2 to M6
  evaluate.py            rolling-origin backtest, scores, comparisons, checks and daily skill
  plots.py               shared figure style and one function per figure
notebooks/               the eight main notebooks: paper artifacts and supporting checks only
notebooks/archive/       two notebooks for superseded figures and exploration
tests/                   pytest tests on synthetic data
data/interim/            cached parquet (git-ignored)
outputs/                 figures, tables, checks and archive (git-ignored)
```

Every main notebook opens with the paper artifacts and the supporting checks it produces.

## What is forecast

Three targets, each for every year and every month: the whole-day minimum (the headline), the
daytime low (the lowest half hour between 09:00 and 17:00) and a robustness target (the mean of
the 15 lowest daily minima of a year, or the 2 lowest of a month). The two hypotheses, that PV
capacity beats a time trend and that weather adds little on top of PV, are judged on the daytime
low; that choice was recorded before any model was run.

## The models

M1 repeats last year's value. M2 to M5 are a ladder fitted on daily lows, each step adding one
thing: M2 knows the calendar and time; M3 swaps time for PV capacity; M4 adds weather (PV capacity
times solar exposure, maximum and minimum temperature); M5 is given M4's information in XGBoost.
The two tests fixed in advance are M3 against M2 and M4 against M3. M6 (XGBoost with M3's
information) was added after the scores of M1 to M5 had been seen, so that M5 against M6 shows
what weather adds in tree form; it is reported as supplementary.

Notebook 08 was also added after the first scores were seen. It scores the daily models day by
day, each given the day's own weather. Because M4 and M5 see the actual weather there, their
pairs show how much weather explains, not how much it helps a year ahead; M3 against M2 uses no
weather and stays a one-year-ahead test.

The annual one-year-ahead scores rest on seven test years (2019 to 2025).

## How the network total is built

Each reporting-year file is cleaned on its own, in this order: put back in time order the days
published scrambled (April 2023); correct blocks published in kW; blank outlier days and stuck
runs; drop substations with more than 20% of intervals blank or invalid; fill gaps of up to two
hours; sum the reporting substations and scale up by their usual share of network load; drop
intervals where less than 95% of usual load reports; average to half hours. The files are then
joined and cut to 2015 to 2025. The cleaning follows Haghdadi et al. (2018),
<https://doi.org/10.1109/TSTE.2017.2751647>.

Times are local clock time (AEST or AEDT), as Ausgrid publishes them. Series are indexed by
interval start; tables report the time an interval ends, matching Ausgrid's column labels.

Three properties of the published files are measured but not corrected; see section 3 of the
analysis plan and the limitations in the results summary. Reporting years do not always meet at
the same level on 1 May (steps of up to 7%); from FY2024 some substations appear to be on
standard time all year; and reverse flow is recorded without its sign before May 2023, which
overstates the daytime low in those years.
