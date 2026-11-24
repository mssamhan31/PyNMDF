# 01 Conference paper

Everything behind a four-page conference paper on minimum demand forecasting.

**Question.** Once rooftop photovoltaic (PV) capacity is in the model, does weather improve one-year-ahead
probabilistic forecasts of annual minimum demand?

**Case study.** One Ausgrid network total (the sum of the public zone substations, at 30 minutes)
for calendar years 2015 to 2025, with five simple models compared under one rolling-origin
protocol at three probability of exceedance (POE) levels, POE10, POE50 and POE90, and a sixth added afterwards as a supplementary check. All
inputs are public.

Paths on this page are relative to this folder. Commands are run from the repository root.

## What is in this folder

| Path | Holds |
|---|---|
| [results_summary.md](results_summary.md) | The numbers behind the paper, by type of evidence, each with the file it comes from |
| [analysis_plan.md](analysis_plan.md) | The design, and the record of every decision and finding made while building (D1 to D40, F1 to F11). Its seventh round holds the key from the paper's earlier figure and table numbers to the current ones |
| `notes/` | The author's own notes behind three decisions |
| `notebooks/` | The eight notebooks. Each opens with the figures, tables and checks it produces |
| `results/` | Figures, tables and checks (committed) |
| `data/interim/` | Cached data passed between notebooks (git-ignored) |
| [archive/v1_straight_line_m4/](archive/v1_straight_line_m4/README.md) | The results and code as they stood before M4 was revised |

## Run

Install the package and download the data first; see the [README at the repository
root](../../README.md). Then run the eight notebooks in order. Each reads the cached outputs of
the ones before it.

```powershell
$notebooks = "01_demand_network_total", "02_pv_and_weather", "03_fig1_introduction",
    "04_results_data_insights", "05_backtest_models", "06_results_forecast_comparison",
    "07_robustness_and_sensitivity", "08_daily_out_of_sample"
foreach ($name in $notebooks) {
    .venv\Scripts\jupyter nbconvert --to notebook --execute --inplace "publication\01_conference\notebooks\$name.ipynb"
}
```

The eight notebooks take about five minutes on a laptop. Notebook 01 reads every raw demand file
and takes about two minutes; notebooks 05 and 07 take about a minute each.

Every run reproduces every file exactly: the random draws are seeded and XGBoost runs on one
thread. Twice while this repository was built, a notebook that saves figures stopped with an
error on one run and ran clean on the next with nothing changed. The cause was not found; if it
happens, run the notebook again.

## Reproduce the main result

After the eight notebooks have run, the one-year-ahead comparison is in
`results/tables/table3.csv` (pinball loss and coverage of the six models on the daytime low) and
`results/tables/headline_numbers.csv` (the four comparisons between models). The daily
out-of-sample test is in `results/tables/table2.csv`. `results_summary.md` lists every number the
paper relies on with its file.

## Where results go

| Folder | Holds |
|---|---|
| `results/figures`, `results/tables` | The paper's figures and tables, named by their number in the paper, with the data behind the figures |
| `results/checks` | Everything the paper's limitation and robustness statements, and its sentences without a figure, rely on |
| `data/interim` | Cached data passed between notebooks |

Figures, tables and checks are committed. The cache is git-ignored and rebuilt by the notebooks.
Figures are saved as PNG (600 dpi) and PDF, tables and checks as CSV.

## The paper's figures and tables

Four figures and three tables, under `results`. In the figures a low is labelled "minimum
demand": the daytime low reads "daytime minimum demand". The text, the tables and the checks keep
"low".

| Figure or table | File | Notebook | Drawn by |
|---|---|---|---|
| Fig. 1, three panels on one year axis: (a) the annual overnight low and daytime low, (b) when each year's lowest 1% of half hours occur, as a heat map, (c) PV capacity | `figures/fig1`, `tables/fig1_data.csv`, `tables/fig1_hours.csv` | 03 | `plots.annual_lows_hours_and_pv` |
| Fig. 2: the annual daytime low against PV capacity, with the fitted line and R-squared | `figures/fig2`, `tables/fig2_data.csv` | 04, section 2 | `plots.daytime_low_against_pv` |
| Fig. 3: the daily daytime low against solar exposure (left) and against maximum temperature (right), 2015, 2020 and 2025 | `figures/fig3`, `tables/fig3_fits.csv` | 04, section 3 | `plots.daytime_low_against_solar_and_temperature` |
| Fig. 4: POE bands on the annual daytime low, M2 to M5 | `figures/fig4` | 06, section 4 | `plots.poe_bands` |
| Table I: the six models, and whether each uses PV and weather | `tables/table1.csv` | 05, section 3 | |
| Table II: the daily out-of-sample test: the mean absolute error of each model, and the change in per cent for three pairs | `tables/table2.csv` | 08, section 6 | |
| Table III: one-year-ahead POE scores on the daytime low, six models, annual and monthly | `tables/table3.csv` | 06, section 2 | |
| Straight-line fit of the annual daytime low on PV capacity and on the year | `tables/table_pv_fit.csv` | 04, section 2 | |
| The four comparisons between models, on pinball loss | `tables/headline_numbers.csv` | 06, section 5 | |

## Supporting checks

All in `results/checks`.

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
| Each year's minimum, with its date, time and day type, and the two lows | `check_annual_minima.csv` | 04, section 4 |
| Share of the lowest 1% of half hours in the daytime and overnight windows | `check_low_hours.csv` | 04, section 5 |
| Whether the two trough windows catch the daily minimum | `check_trough_windows.csv` | 04, section 6 |
| Complete days behind the 15-lowest-days measure | `check_complete_days.csv` | 05, section 2 |
| The knots of M4's two temperature Vs: every candidate pair, on the first training window | `check_temperature_knot.csv` | 05, section 3 |
| Plain XGBoost beyond the PV capacity it was trained on | `check_m5_pv_range.csv` | 05, section 5 |
| The holiday check: public holidays against ordinary weekend days | `check_holiday_miss.csv` | 05, section 6 |
| M4 term diagnosis: one group of weather terms switched off | `check_m4_terms.csv` | 05, section 7 |
| M4's weather coefficients and the reach of PV x solar beyond training | `check_m4_coefficients.csv` | 05, section 7 |
| One-year-ahead POE scores on the whole-day minimum | `table3_minimum.csv` | 06, section 3 |
| Bias of POE50 by model, including M6's monthly bias | `check_poe50_bias.csv` | 06, section 6 |
| The 15-lowest-days measure: POE scores and the comparisons on it | `table3_robust.csv`, `sensitivity_robust.csv` | 07, section 2 |
| Reporting thresholds of 90%, 95% and 98% | `sensitivity_thresholds.csv` | 07, section 3 |
| The rescaled series: factors and annual lows | `sensitivity_rescale_factors.csv`, `sensitivity_rescaled_lows.csv` | 07, sections 4.1 and 4.2 |
| The rescaled series: POE scores and the comparisons | `table3_daytime_low_rescaled.csv`, `table3_minimum_rescaled.csv`, `sensitivity_rescaled_comparisons.csv` | 07, sections 4.3 and 4.4 |
| The mean error and the number of days of the daily test by model, which Table II leaves out | `daily_skill.csv` | 08, section 3 |
| Table II by test year | `daily_skill_by_year.csv`, `daily_pairs_by_year.csv` | 08, sections 4 and 5 |

Three checks hold numbers the paper no longer shows in a figure or table but still refers to in
a sentence: `check_annual_summary.csv` (annual maximum and energy), `check_annual_minima.csv`
(the annual minima with date, time and day type) and `daily_skill.csv` (the mean error of the
daily test). `check_low_hours.csv` counts the half hours of panel (b) of Fig. 1 by trough window.

## Exploration and the archive

Neither is used by the paper.

- [exploration/01_conference](../../exploration/README.md), at the repository root, holds two
  notebooks: the first looks at the models, and earlier figures. One of those figures, the heat
  map, is back in the paper as a panel of Fig. 1; it is drawn again in notebook 03, not taken
  from there.
- [archive/v1_straight_line_m4](archive/v1_straight_line_m4/README.md) holds the results and code
  as they stood before M4 was revised.

## What is forecast

Three targets, each for every year and every month: the whole-day minimum (the headline), the
daytime low (the lowest half hour between 09:00 and 17:00) and a robustness target (the mean of
the 15 lowest daily minima of a year, or the 2 lowest of a month). The two hypotheses, that PV
capacity beats a time trend and that weather adds little on top of PV, are judged on the daytime
low; that choice was recorded before any model was run.

## The models

M1 repeats last year's value. M2 to M5 are a ladder fitted on daily lows, each step adding one
thing: M2 knows the calendar and time; M3 swaps time for PV capacity; M4 adds weather (PV capacity
times solar exposure, and maximum and minimum temperature each as a V); M5 is given M4's
information in XGBoost. The two tests fixed in advance are M3 against M2 and M4 against M3. M6
(XGBoost with M3's information) was added after the scores of M1 to M5 had been seen, so that M5
against M6 shows what weather adds in tree form; it is reported as supplementary.

Each temperature enters M4 as a V because demand rises on both cold and hot days: one slope for
each degree below a knot and another for each degree above it, two straight lines meeting at the
knot. The knots are 21 °C for maximum temperature and 18 °C for minimum temperature, chosen on
2015 to 2018 only. M5 takes the two temperatures as they are. M4 first used them as two straight
terms; its form was revised after the scores of all six models had been seen (D37).

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

Times are local clock time (Australian Eastern Standard Time, AEST, or Australian Eastern
Daylight Time, AEDT), as Ausgrid publishes them. Series are indexed by
interval start; tables report the time an interval ends, matching Ausgrid's column labels.

Three properties of the published files are measured but not corrected; see section 3 of the
analysis plan and the limitations in the results summary. Reporting years do not always meet at
the same level on 1 May (steps of up to 7%); from FY2024 some substations appear to be on
standard time all year; and reverse flow is recorded without its sign before May 2023, which
overstates the daytime low in those years.
