# Results summary

The numbers behind the paper, organised by type of evidence. Every number comes from a file that
the notebooks rebuild; the file is named under each table. This document states numbers and what
each one measures. It does not interpret them for the paper.

Paths are relative to this folder, `publication/01_conference/`.

Conventions: demand is in MW. An error is actual minus forecast, so a positive mean error means
the forecasts sat too low. In a comparison of two models, a negative change means the first model
scores better. Test years are 2019 to 2025; each is forecast from data up to the end of the year
before, with the target year's PV capacity taken as known.

## 0. Reading guide

The paper has four figures and three tables. Fig. 1 is the two annual lows over PV capacity;
Fig. 2 the annual daytime low against PV capacity; Fig. 3 the daily daytime low against solar
exposure; Fig. 4 the POE bands on the annual daytime low. Table I lists the six models; Table II
is the daily out-of-sample test; Table III holds the one-year-ahead POE scores on the daytime
low. Numbers the paper states in a sentence, without a figure or table, come from the checks
named beside them.

### 0.1 The paper's four points and where their evidence is

| Point | Evidence | Section |
|---|---|---|
| 1. The minimum has shifted from the overnight low to the daytime low | Fig. 1; the checks on the lowest half hours and on the annual minima | 1.1 to 1.3 |
| 2. PV capacity tracks the daytime low over the decade and predicts the low days better than a time trend | Fig. 2 and `table_pv_fit.csv`; Table II, M3 against M2 | 1.4, 2.2 |
| 3. Weather explains which days are low | Fig. 3; Table II, M4 against M3 and M5 against M6 | 1.5, 2.2 |
| 4. One year ahead, the tree model with PV and weather forecasts best, and weather helps only in that form | Table III and Fig. 4; `headline_numbers.csv` | 3.1 to 3.3 |

Numbers that qualify a point are stated beside it: section 3.2 for point 2 (one year ahead, on
POE scores, M3 against M2 goes the other way on the annual targets), and section 3.4 for point 4
(part of M5's margin over M6 is a handicap of M6, not weather). Section 3.2 also bears on the
second half of point 4: on the monthly daytime low, M4 scores better than M3.

### 0.2 What was fixed before the results, and what was added after

| When | What | Record |
|---|---|---|
| Before any model was run | The three targets: whole-day minimum (headline), daytime low, and the mean of the 15 lowest daily minima | D13, D18 |
| Before any model was run | H1 is M3 against M2 and H2 is M4 against M3, both judged on the daytime low, annual and monthly | D11, D14 |
| Before any model was run | Model form is M5 against M4 | D11 |
| Before any model was run | The rolling-origin protocol, the POE recipe, pinball loss and coverage; the reporting thresholds of 90%, 95% and 98%; a check on a rescaled series | Plan, D12 |
| After the first run of the models, before any score | One non-working-day flag in place of separate weekend and holiday flags; M5 kept as plain XGBoost | D19, D20 |
| **After the scores of M1 to M5 were seen** | **M6** (XGBoost with M3's information) and the supplementary comparison M5 against M6 | D23 |
| **After the scores were seen** | **Notebook 08**, the daily out-of-sample test, and its three pairs | D25 |
| **After the scores were seen** | **The form of temperature in M4**: maximum and minimum temperature each as a V, in place of one straight term each, on the supervisor's advice. The knots were chosen on 2015 to 2018 only | D37 |
| After the scores were seen | The diagnosis of M4 (M4 itself unchanged); the method of the rescaling; the straight-line fit of section 1.4 and Fig. 2; the fourth panel (M5) of Fig. 4 | D24, D22, D30, D27, D34 |

### 0.3 Four things to keep in view

- **Seven annual points.** The annual one-year-ahead scores of section 3 rest on seven test years.
  The monthly scores rest on 77 months (daytime low) or 76 (whole-day minimum).
- **Actual weather in notebook 08.** In the daily test of section 2, M4 and M5 are given each
  day's actual weather. Their pairs measure how much weather explains, not how much it helps a year
  ahead. M3 against M2 uses no weather and is a one-year-ahead test.
- **M6 and notebook 08 are supplementary.** Neither was planned before the results.
- **H2 is judged on a revised M4.** H2 was set as M4 against M3 before any model was run. The
  form of temperature in M4 was revised after the scores were seen (D37), so every number of M4
  here is that of the revised model. The numbers of the first M4 are in
  `archive/v1_straight_line_m4`. No other model changed.

## 1. Descriptive evidence

### 1.1 The two lows and PV capacity by year (Fig. 1)

| Year | Overnight low | Daytime low | PV capacity at 30 June |
|---|---|---|---|
| 2015 | 1,368 | 1,833 | 230 |
| 2016 | 1,433 | 1,891 | 287 |
| 2017 | 1,474 | 1,888 | 346 |
| 2018 | 1,495 | 1,902 | 449 |
| 2019 | 1,473 | 1,759 | 620 |
| 2020 | 1,429 | 1,671 | 780 |
| 2021 | 1,388 | 1,357 | 1,050 |
| 2022 | 1,428 | 1,458 | 1,291 |
| 2023 | 1,393 | 1,080 | 1,563 |
| 2024 | 1,420 | 1,019 | 1,882 |
| 2025 | 1,435 | 880 | 2,084 |

The overnight low is the lowest half hour between 00:00 and 06:00; the daytime low the lowest
between 09:00 and 17:00. Over 2015 to 2025 the overnight low stays within 1,368 to 1,495 MW; the
daytime low goes from 1,833 to 880 MW, after a high of 1,902 MW in 2018. The daytime low is below
the overnight low in 2021, 2023, 2024 and 2025.

Source: `results/tables/fig1_data.csv` (notebook 03).

Annual maximum and energy, which the paper states in a sentence (check, not a figure):

| Year | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Maximum (MW) | 4,633 | 4,717 | 5,269 | 4,676 | 5,146 | 5,066 | 4,459 | 4,226 | 4,757 | 4,679 | 4,607 |
| Energy (GWh) | 21,444 | 22,013 | 22,386 | 22,291 | 21,931 | 20,927 | 19,805 | 20,175 | 19,287 | 19,685 | 19,872 |

Source: `results/checks/check_annual_summary.csv` (notebook 01).

### 1.2 When the lowest 1% of half hours occur (check)

| Year | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Starting 09:00 to 17:00 (%) | 0 | 0 | 0 | 0 | 0 | 0 | 19 | 27 | 97 | 99 | 100 |
| Starting 00:00 to 06:00 (%) | 100 | 96 | 98 | 97 | 98 | 98 | 79 | 69 | 0 | 0 | 0 |

The lowest 1% is about 170 half hours a year; the remainder start outside both windows. Share of
days on which the daytime trough is the lower of the two: 0% up to 2020, then 0.9%, 3.4%, 17.8%,
26.2% and 32.9% in 2021 to 2025.

Sources: `results/checks/check_low_hours.csv` and `check_trough_windows.csv` (notebook 04).

### 1.3 Each year's minimum (check)

| Year | Minimum | Date | Half hour ending | Day | Public holiday | Solar (MJ/m²) | Tmax (°C) |
|---|---|---|---|---|---|---|---|
| 2015 | 1,368 | 5 Apr | 04:30 | Sun | Easter Sunday | 16.2 | 23.2 |
| 2016 | 1,433 | 24 Apr | 05:00 | Sun | | 14.3 | 22.0 |
| 2017 | 1,474 | 17 Apr | 04:30 | Mon | Easter Monday | 14.2 | 23.7 |
| 2018 | 1,495 | 29 Apr | 05:00 | Sun | | 13.4 | 20.2 |
| 2019 | 1,473 | 10 Nov | 05:00 | Sun | | 28.6 | 23.9 |
| 2020 | 1,429 | 12 Apr | 05:00 | Sun | Easter Sunday | 17.1 | 20.5 |
| 2021 | 1,357 | 17 Oct | 14:30 | Sun | | 25.7 | 21.5 |
| 2022 | 1,428 | 17 Apr | 05:00 | Sun | Easter Sunday | 14.9 | 24.7 |
| 2023 | 1,080 | 29 Oct | 13:00 | Sun | | 27.4 | 26.0 |
| 2024 | 1,019 | 26 Oct | 14:00 | Sat | | 27.3 | 19.4 |
| 2025 | 880 | 27 Dec | 14:30 | Sat | | 29.9 | 21.5 |

The minimum is overnight in every year to 2020 and in 2022, and in the daytime in 2021 and from
2023. Times are local clock time.

Source: `results/checks/check_annual_minima.csv` (notebook 04), which also holds each year's
overnight and daytime lows.

### 1.4 The annual daytime low fitted on PV capacity and on the year (Fig. 2)

Two straight lines, each fitted on its own to the eleven annual daytime lows of 2015 to 2025.
Fig. 2 plots the eleven points and the first line, with its R-squared.

| Fitted on | Slope | R-squared | RMSE (MW) | Points |
|---|---|---|---|---|
| PV capacity (MW at 30 June) | -0.570 MW per MW | 0.958 | 75.1 | 11 |
| Year | -108.8 MW per year | 0.879 | 127.8 | 11 |

RMSE is the root mean squared residual of the eleven points, with no adjustment for the two
fitted parameters. These are in-sample fits to annual values, not forecasts. Added after the
scores were seen (D30).

Sources: `results/tables/table_pv_fit.csv` and `fig2_data.csv` (notebook 04, section 2).

### 1.5 The daily daytime low against solar exposure (Fig. 3)

| Year | Slope (MW per MJ/m²) | Days |
|---|---|---|
| 2015 | +0.6 | 358 |
| 2020 | -6.6 | 347 |
| 2025 | -35.4 | 360 |

A least-squares line of each day's daytime low on that day's solar exposure, within one year.

Source: `results/tables/fig3_fits.csv` (notebook 04, section 3).

## 2. Daily out-of-sample test (Table II)

Added after the first scores were seen (D25). For each test year, each of M2 to M6 is fitted on
the days up to the end of the year before (the same fits as the forecasts of section 3) and
predicts the daytime low of every day of the test year from that day's own calendar, PV capacity
and weather. Nothing is simulated. There are 2,414 valid days; the lowest days are the 10% of each
year's valid days with the lowest actual daytime low, 240 in all.

**M4 and M5 see each day's actual weather.** M2, M3 and M6 use no weather.

### 2.1 The models

| Model | MAE, all days | Mean error, all days | MAE, lowest 10% | Mean error, lowest 10% |
|---|---|---|---|---|
| M2 Time trend | 274.1 | -115.1 | 292.4 | -286.4 |
| M3 PV only | 260.3 | -13.1 | 211.7 | -168.9 |
| M4 PV + weather, linear | 186.1 | -25.1 | 152.6 | -55.7 |
| M5 PV + weather, XGBoost | 157.4 | +32.6 | 173.1 | -157.3 |
| M6 PV only, XGBoost | 262.3 | -10.3 | 339.5 | -336.8 |

MAE is the mean absolute error. On the lowest days the mean error is negative for every model
partly by construction: the days are chosen for a low actual, so it compares models but does not
measure bias.

### 2.2 The three pairs

| Pair | What it measures | Days | MAE, first | MAE, second | Change | Years first is better |
|---|---|---|---|---|---|---|
| M3 against M2 | PV against time; one year ahead | All | 260.3 | 274.1 | -5.0% | 4 of 7 |
| M3 against M2 | | Lowest 10% | 211.7 | 292.4 | -27.6% | 7 of 7 |
| M4 against M3 | What weather explains, linear | All | 186.1 | 260.3 | -28.5% | 7 of 7 |
| M4 against M3 | | Lowest 10% | 152.6 | 211.7 | -27.9% | 6 of 7 |
| M5 against M6 | What weather explains, XGBoost | All | 157.4 | 262.3 | -40.0% | 7 of 7 |
| M5 against M6 | | Lowest 10% | 173.1 | 339.5 | -49.0% | 7 of 7 |

The exception for M4 against M3 on the lowest days is 2022 (+17.9%). M6's errors on the lowest
days are almost all one-sided (MAE 339.5, mean error -336.8), as are M5's in 2023 (352.9 and
-352.9): a tree model cannot follow PV capacity beyond the range it was fitted on (section 4.5), so
part of the M5 against M6 gap is that handicap of M6 and not weather.

Sources: `results/tables/table2.csv`; by year, `results/checks/daily_skill_by_year.csv` and
`daily_pairs_by_year.csv` (notebook 08).

## 3. One-year-ahead POE scores (Table III)

Each model forecasts POE10, POE50 and POE90 of every target one year ahead. The score is pinball
loss in MW, lower being better; the value given is the mean over the three POE levels and the test
points. Coverage is the share of actuals between POE90 and POE10; a calibrated band holds about
80%. **The annual columns rest on seven test years.**

### 3.1 Scores by model

Table III: the daytime low, the target H1 and H2 are judged on.

| Model | Annual pinball | Annual coverage | Monthly pinball | Monthly coverage |
|---|---|---|---|---|
| M1 Naive | 63.1 | 3 of 7 | 50.5 | 0.61 |
| M2 Time trend | 34.6 | 7 of 7 | 53.5 | 0.70 |
| M3 PV only | 43.3 | 5 of 7 | 49.6 | 0.58 |
| M4 PV + weather, linear | 67.5 | 4 of 7 | 46.2 | 0.70 |
| M5 PV + weather, XGBoost | 28.5 | 5 of 7 | 42.8 | 0.69 |
| M6 PV only, XGBoost | 36.6 | 6 of 7 | 75.1 | 0.52 |

The same scores on the whole-day minimum, the headline target (a check, for the sentence in
which the paper mentions them):

| Model | Annual pinball | Annual coverage | Monthly pinball | Monthly coverage |
|---|---|---|---|---|
| M1 Naive | 45.2 | 1 of 7 | 43.5 | 0.42 |
| M2 Time trend | 31.1 | 7 of 7 | 37.5 | 0.66 |
| M3 PV only | 41.6 | 5 of 7 | 41.4 | 0.58 |
| M4 PV + weather, linear | 61.5 | 4 of 7 | 41.5 | 0.62 |
| M5 PV + weather, XGBoost | 26.9 | 5 of 7 | 32.5 | 0.63 |
| M6 PV only, XGBoost | 28.0 | 6 of 7 | 42.2 | 0.63 |

Monthly scores are over 77 valid months for the daytime low and 76 for the whole-day minimum, out
of 84. M5 has the lowest pinball loss in all four columns. M2's band holds all seven annual
actuals on both targets; in 2023 its band on the daytime low runs from about 620 to 1,370 MW.

Sources: `results/tables/table3.csv` for the daytime low and `results/checks/table3_minimum.csv`
for the whole-day minimum (notebook 06). Both also hold the loss at each POE level.

### 3.2 The four comparisons

Change in mean pinball loss, in per cent.

| Comparison | Set | Daytime low, annual | Daytime low, monthly | Minimum, annual | Minimum, monthly |
|---|---|---|---|---|---|
| H1: M3 against M2 (PV against time) | Before the results | +25.0 | -7.4 | +34.1 | +10.3 |
| H2: M4 against M3 (weather on top of PV, linear) | Before the results | +56.0 | -6.9 | +47.7 | +0.2 |
| Model form: M5 against M4 (XGBoost against linear) | Before the results | -57.8 | -7.2 | -56.2 | -21.6 |
| Supplementary: M5 against M6 (weather in tree form) | After the scores were seen | -22.2 | -43.0 | -4.0 | -23.0 |

On the target the hypotheses are judged on, M3 scores worse than M2 on the annual daytime low
(43.3 against 34.6 MW) and better on the monthly (49.6 against 53.5 MW). M4 scores worse than M3
on both annual targets (67.5 against 43.3 MW on the daytime low) and better on the monthly
daytime low (46.2 against 49.6 MW); on the monthly whole-day minimum the two are level (41.5
against 41.4 MW). M5 scores better than M4 and better than M6 at both levels and on both
targets.

Source: `results/tables/headline_numbers.csv` (notebook 06).

### 3.3 Annual daytime low: POE50 against the actual (Fig. 4)

| Year | Actual | M2 | M3 | M4 | M5 |
|---|---|---|---|---|---|
| 2019 | 1,759 | 1,789 | 1,782 | 1,728 | 1,810 |
| 2020 | 1,671 | 1,738 | 1,639 | 1,553 | 1,680 |
| 2021 | 1,357 | 1,584 | 1,426 | 1,295 | 1,410 |
| 2022 | 1,458 | 1,323 | 1,110 | 994 | 1,293 |
| 2023 | 1,080 | 1,251 | 1,016 | 915 | 1,332 |
| 2024 | 1,019 | 1,049 | 875 | 740 | 994 |
| 2025 | 880 | 925 | 839 | 650 | 881 |

Source: `data/interim/forecasts.parquet`; the bands are shown under the figure in notebook 06.

### 3.4 Bias of POE50

Mean error of POE50 over the valid test points (MW).

| Target, level | M1 | M2 | M3 | M4 | M5 | M6 |
|---|---|---|---|---|---|---|
| Daytime low, annual | -126 | -62 | +77 | +193 | -25 | -49 |
| Daytime low, monthly | -90 | -140 | -34 | +32 | -61 | -132 |
| Minimum, annual | -101 | -65 | +54 | +162 | 0 | -41 |
| Minimum, monthly | -75 | -86 | -34 | +16 | -8 | -34 |

M4's annual forecasts sit too low (section 4.4). M6's monthly forecasts of the daytime low sit
132 MW above the actuals on average, against 61 MW for M5: M6 has no input that moves with PV
beyond its training range, which is the handicap noted in section 2.2.

Source: `results/checks/check_poe50_bias.csv` (notebook 06).

## 4. Sensitivity

### 4.1 One extreme half hour: the mean of the 15 lowest daily minima

The whole-day minimum replaced by the mean of the 15 lowest daily minima of the year (the 2 lowest
in a month), over complete days.

| Model | Annual pinball | Annual coverage | Monthly pinball | Monthly coverage |
|---|---|---|---|---|
| M1 | 36.9 | 2 of 7 | 40.5 | 0.41 |
| M2 | 25.8 | 7 of 7 | 34.4 | 0.68 |
| M3 | 31.9 | 5 of 7 | 39.3 | 0.57 |
| M4 | 36.5 | 4 of 7 | 38.4 | 0.59 |
| M5 | 25.5 | 4 of 7 | 30.2 | 0.58 |
| M6 | 30.5 | 5 of 7 | 39.6 | 0.67 |

| Comparison | Annual, minimum | Annual, 15 lowest days | Monthly, minimum | Monthly, 15 lowest days |
|---|---|---|---|---|
| H1: M3 against M2 | +34.1 | +23.3 | +10.3 | +14.3 |
| H2: M4 against M3 | +47.7 | +14.5 | +0.2 | -2.4 |
| Model form: M5 against M4 | -56.2 | -30.2 | -21.6 | -21.2 |
| Supplementary: M5 against M6 | -4.0 | -16.6 | -23.0 | -23.7 |

Three of the four comparisons point the same way on both measures, at both levels. H2 does so at
the annual level; at the monthly level it is within 3% of zero on both measures and changes
sign between them. Complete days per year,
2015 to 2025: 357, 361, 360, 365, 353, 347, 331, 352, 342, 309, 359.

Sources: `results/checks/table3_robust.csv`, `sensitivity_robust.csv` (notebook 07);
`check_complete_days.csv` (notebook 05).

### 4.2 The reporting threshold

The network total rebuilt keeping intervals in which at least 90%, 95% (as used) or 98% of usual
load reports. No annual daytime low moves. Two whole-day minima move, both in training years: 2016
is 1,427.0 MW at 90% against 1,432.6 MW, and 2018 is 1,510.9 MW at 98% against 1,495.1 MW.

Source: `results/checks/sensitivity_thresholds.csv` (notebook 07).

### 4.3 The level steps between reporting years: a rescaled series

Each reporting-year file multiplied by one constant so that the measured steps at the 1 May joins
close, the latest file keeping its level. This is a bounding case, not a correction (D22): the
factors compound from 1.000 for FY2025 and FY2026 to 1.171 for FY2015 (FY2023: 0.990).

Mean pinball loss on the daytime low (MW), published series then rescaled:

| Model | Annual, published | Annual, rescaled | Monthly, published | Monthly, rescaled |
|---|---|---|---|---|
| M1 | 63.1 | 42.4 | 50.5 | 43.1 |
| M2 | 34.6 | 29.2 | 53.5 | 38.4 |
| M3 | 43.3 | 87.0 | 49.6 | 53.6 |
| M4 | 67.5 | 123.3 | 46.2 | 60.0 |
| M5 | 28.5 | 20.8 | 42.8 | 41.3 |
| M6 | 36.6 | 26.2 | 75.1 | 73.2 |

Change in mean pinball loss on the daytime low (%):

| Comparison | Annual, published | Annual, rescaled | Monthly, published | Monthly, rescaled |
|---|---|---|---|---|
| H1: M3 against M2 | +25.0 | +198.2 | -7.4 | +39.6 |
| H2: M4 against M3 | +56.0 | +41.7 | -6.9 | +12.0 |
| Model form: M5 against M4 | -57.8 | -83.2 | -7.2 | -31.2 |
| Supplementary: M5 against M6 | -22.2 | -20.8 | -43.0 | -43.6 |

Across both targets and both levels, 14 of the 16 comparisons keep their direction. The two that
reverse are H1 and H2 on the monthly daytime low. On the rescaled series no annual daytime low falls
inside the band of M3 or of M4. Rescaling moves the 2022 daytime low from 1,458 to 1,443 MW.

Sources: `results/checks/sensitivity_rescale_factors.csv`, `sensitivity_rescaled_lows.csv`,
`table3_daytime_low_rescaled.csv`, `table3_minimum_rescaled.csv`,
`sensitivity_rescaled_comparisons.csv` (notebook 07).

### 4.4 Why M4's forecasts sit low

M4 refitted and replayed with one group of weather terms switched off; M4 itself is unchanged.
Annual daytime low:

| | Mean pinball loss (MW) | Mean error of POE50 (MW) | POE50 in 2023, 2024, 2025 |
|---|---|---|---|
| M3 | 43.3 | +77 | 1,016, 875, 839 |
| M4 | 67.5 | +193 | 915, 740, 650 |
| M4 without temperature | 62.6 | +150 | 871, 760, 707 |
| M4 without PV × solar | 46.3 | +123 | 1,018, 833, 759 |

M4's daytime-low coefficients across the seven origins: PV × solar -15.4 to -18.3 MW per 1,000
MW × MJ/m²; each degree of maximum temperature below 21 °C +47.6 to +71.8 MW, and each degree
above it +18.2 to +19.7 MW; each degree of minimum temperature below 18 °C -12.4 to -4.6 MW, and
each degree above it +94.1 to +105.7 MW. PV × solar on the sunniest days of each target year
(its 99th percentile) lies 7.8% to 29.3% beyond the largest value in the training days.

Sources: `results/checks/check_m4_terms.csv`, `check_m4_coefficients.csv` (notebook 05).

### 4.5 A tree model beyond the PV capacity it was fitted on

M5's forecast of the annual daytime low with no borrowed miss added sits above the actual in six
of seven test years, by 135 to 484 MW (2022: 2 MW below). PV capacity at the middle of each target
year is 5% to 16% above the highest value in the training data.

Source: `results/checks/check_m5_pv_range.csv` (notebook 05).

### 4.6 The single non-working-day flag

Mean miss on public holidays less that on ordinary weekend days, given each day's own weather,
over 76 holidays and 667 weekend days in 2019 to 2025 (MW):

| Low | M2 | M3 | M4 | M5 | M6 |
|---|---|---|---|---|---|
| Daytime | -159 | -150 | -132 | -126 | -96 |
| Overnight | -45 | -44 | -45 | -49 | -43 |

Source: `results/checks/check_holiday_miss.csv` (notebook 05).

### 4.7 The knots of M4's two temperature Vs

M4 takes maximum and minimum temperature each as a V (D37): one slope for each degree below a
knot and another for each degree above it. The knots are the whole-degree pair with the lowest
error on the daytime low when M4 is fitted on the days of 2015 to 2018, the first training
window. No test year takes part. These are in-sample fits, not forecast scores.

| | Knot on maximum (°C) | Knot on minimum (°C) | Daytime low RMSE (MW) | Overnight low RMSE (MW) |
|---|---|---|---|---|
| Lowest error on the daytime low (in use) | 21 | 18 | 129.2 | 69.1 |
| Lowest error on the overnight low | 24 | 17 | 133.8 | 68.6 |

The 81 pairs tried run from 17 to 25 °C on the maximum and from 14 to 22 °C on the minimum.
Their error on the daytime low runs from 129.2 to 148.8 MW; 7 pairs lie within 1 MW of the
lowest.

Source: `results/checks/check_temperature_knot.csv` (notebook 05, section 3).

## 5. Limitations of the data, with their measures

None of these is corrected in the main series. Each acts on all models alike.

| Limitation | Measure | Source in `results/checks` |
|---|---|---|
| **Reverse flow is recorded without its sign before May 2023, which overstates the daytime low.** The daytime low before May 2023 is overstated by roughly 20 to 70 MW and then steps down | The 25 substations that read negative at FY2024's lowest daytime intervals sum to +70, +60, +41 and +46 MW in FY2020 to FY2023, and to -50, -77 and -90 MW in FY2024 to FY2026. Substations with any negative value: 0 to 3 per file to FY2023, then 43, 47 and 68 | `check_sign.csv` |
| Reporting-year files do not meet at the same level at 1 May | Step at the joins of 2015 to 2024: +3.0%, +4.8%, +2.3%, +1.6%, -0.5%, -1.1%, not measurable, +7.2%, -4.1%, +3.2%. The 2025 join is not measurable. Bounded in section 4.3 | `check_join_steps.csv` |
| From FY2024 some substations appear to stay on standard time during daylight saving | Share of load whose morning rise moves earlier when daylight saving starts: 21.7% (FY2024), 12.8% (FY2025), 10.0% (FY2026), against 0% to 1.2% in FY2015 to FY2023. The daytime lows of 2023 to 2025 fall in daylight-saving months | `check_clock.csv` |
| A substation with more than 20% of its intervals blank or invalid is dropped, and its load is not replaced | 0.0% to 2.4% of network load per file | `check_data_quality.csv` |
| Not every half hour is kept | Kept by year, 2015 to 2025: 98.4%, 98.8%, 99.3%, 100.0%, 97.7%, 94.8%, 90.9%, 96.7%, 96.3%, 87.9%, 99.3%. Eight test months are below 90% and are not scored for the whole-day minimum: May 2019, October and November 2020, April 2021 (no valid data), October 2022, September 2023, January and August 2024 | `check_annual_summary.csv`, `check_kept_by_month.csv`, `sensitivity_thresholds.csv` |
| The two trough windows do not cover the whole day | The day's minimum falls outside both windows on at most 0.6% of days in any year | `check_trough_windows.csv` |
| Weather is one station (Sydney Airport), with gaps | In 2015 to 2025 at most 7 days a year miss any variable; gaps of up to 3 days are filled. Earlier years with longer gaps are left out of the replay, which uses 17 weather years at the first origin and 23 at the last. Temperature quality flag: Y on 494 days and N on about 3,500 of the 4,018 days of 2015 to 2025 | `check_weather_missing.csv`, `check_weather_quality.csv` |
| PV capacity is the published total at 30 June of each year, interpolated to days | The capacities read match the expected table to within 1 kWp. FY2024 was published as PDF only and is entered in the configuration | `check_pv_capacity.csv` |
