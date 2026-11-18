# PyNMDF analysis plan

Written 11 November 2026 after exploring the raw data. On approval, the first build step copies this
file to `docs/analysis_plan.md` in the repository.

## 1. Context

A four-page IEEE conference paper asks one question: once rooftop PV capacity is in the model, does
weather improve one-year-ahead probabilistic forecasts of annual minimum demand? This repository
builds the complete, reproducible analysis behind it, from public Ausgrid and BOM files to six
figures and three tables. Samhan writes the paper; the code produces numbers, figures and tables
only, never paper prose.

The source prompt (`PyNMDF_claude_code_prompt_20261111.md`) fixes the scope, the locked decisions and
the repository shape. This plan records what the data showed, the decisions taken on 11 November
2026 where the data pushed on the prompt, and the build order.

Working folder: the repository root (empty, and not yet a git repository, when this was written).

## 2. What the data showed

**Confirmed.** PV capacity reproduces the section 6 table exactly (ten workbooks plus the FY24 PDF).
BOM files are as described. Per-file diagnostic minima reproduce the stress-test table: ten of twelve
exactly; FY2023 (1,294) and FY2024 (1,372 against 1,364) only when long gaps are part-filled the way
pandas `interpolate(limit=8)` does. Annual maxima are 4,226 to 5,269 MW.

**Time convention.** Ausgrid's notes (PDF inside the FY2015 zip) state local clock time: AEST in
winter, AEDT in summer. Labels are interval-ending. Continuity tests confirm that FY2024's final
`00:00` is 24:00 of the same day and that FY2025-26 columns are correct once sorted by label. On the
October change day the non-existent hour is blank for about half the substations up to FY2023 (the
2-hour fill covers it) and filled from FY2024.

**Formats beyond the prompt's list.** A fourth date format (`1-May-14`, Argenton FY2015);
`24:00:00` as the last label (all of FY2022); literal `NaN` strings (FY2025); days absent as rows
(FY2022, FY2024-26); Crows Nest FY2017 holds 61 dates twice, as two complementary halves.

**First look at the network total** (candidate rule, provisional until notebook 01):

| Year | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Minimum (MW) | 1,368 | 1,433 | 1,474 | 1,495 | 1,473 | 1,429 | 1,357 | 1,428 | 1,080 | 1,019 | 880 |
| Trough | night | night | night | night | night | night | day | night | day | day | day |
| Half hours kept | 98% | 99% | 99% | 100% | 98% | 95% | 91% | 97% | 96% | 88% | 99% |

Annual minima are identical at reporting thresholds from 80% to 98%. (That was the candidate
rule. On the final series two whole-day minima move slightly with the threshold; see F8.)

**Findings that changed a decision.**

| Finding | Evidence | Decision (section 3) |
|---|---|---|
| Unit rule incomplete | 110 kW values below 1,000 stay uncorrected in the FY2023 blocks (up to +1,240 MW in about 140 half hours); Mitchells Flat is an eighth case (29-30 April 2016) | D1 |
| Morisset, FY2022 | Reads about 15 times too high (19-341 MW, normal 9 MW), 30 Nov 2021 to 21 Jan 2022; lifts the Dec 2021 and Jan 2022 monthly minima by about 100 and 74 MW | D2 |
| 84 monthly test points do not exist | April 2021 has no valid half hour; January 2024 6%; November 2020 57%; five more test months at 77-90% | D4 |
| Reverse flow unsigned before May 2023 | Ausgrid's notes: many sites are amps-only. The 25 substations negative at FY2024's lowest daytime intervals sum to +70, +60, +43, +47 MW in FY2020-23, then -50, -78, -90 MW in FY2024-26 | D5 |
| City Central reads zero for 8 months | Sep 2020 to Apr 2021; neighbouring CBD substations do not pick up its 33 MW, so it is a data hole | D3 |
| Daily models cannot forecast an interval-level statistic | The lowest 0.5% is about 88 half hours from 12 to 29 different days | D6 |

**Findings reported, not acted on.**

- The 20% rule loses load outright: a dropped substation is not scaled up, so 0% to 2.4% of network
  load disappears depending on the file. Inherent in the locked rule; shown per file in the
  data-quality table.
- In FY2015-20, 5-7% of values sit in runs of 2 hours or more (coarse meter resolution, not faults);
  about 1% sit in runs of a day or more. A short stuck-run threshold would drop about 14 more
  substations per file and cut annual energy by 1.6%.
- The switch from overnight to midday is not clean: 2021 is a midday minimum, 2022 overnight.
- The daytime-trough annual minimum rises over 2015-2018 (1,833, 1,892, 1,891, 1,905) before
  falling to 880; the overnight trough stays within 1,357-1,511.

## 3. Decisions

Locked decisions in sections 5 to 7 of the prompt stand unless listed here.

**Agreed on 11 November 2026 (answers to the five questions).**

| ID | Decision |
|---|---|
| D1 | **Unit fix by block.** For each substation, every value between its first and last value above 1,000 MW (absolute) is divided by 1,000. Replaces the per-value rule |
| D2 | **Outlier rule.** A substation-day is invalid when its median absolute value exceeds 5 times that substation's 75th percentile (absolute) for the file. Removes Morisset's 53 days; also flags up to 25 days a year at two standby substations under 10 MW (Wamberal, Blackwattle Bay) |
| D3 | **Stuck run.** One value repeated for at least 96 intervals (24 hours), zero included, is invalid |
| D4 | **Monthly validity.** A monthly minimum counts for fitting and scoring only when at least 90% of the month's half hours are kept. 76 of 84 test months are scored; excluded months are listed in the data-quality table |
| D5 | **Signs stay as published.** No correction. Notebook 01 adds one check table quantifying the swing, for the limitation |
| D6 | **Superseded by D18 on 18 November.** Robustness target. Actuals use the locked definition (mean of the lowest 0.5% of half hours). The daily models forecast it as the mean of the 15 lowest simulated daily minima (2 lowest in a month); the year-by-year gap between the two definitions is reported beside the table. After D9 the daily models are M2 to M5, and M1 forecasts the locked definition directly |
| D7 | **Out-of-fold residuals.** Errors resampled in the replay come from out-of-fold residuals (leave one year out within each training window). After D9 this covers M2 to M5 |
| D8 | **Tests.** About six pytest tests on synthetic data (section 8) |

**Agreed on 12 November 2026 (plan approved with one design change).**

| ID | Decision |
|---|---|
| D9 | **Nested daily ladder.** M2 to M5 are all fitted on daily minima, share one daily PV series and share one POE recipe (the replay, with out-of-fold residuals drawn by held-out year). Each rung adds one thing: M2 calendar plus time; M3 calendar plus PV; M4 adds weather; M5 is M4's predictors in XGBoost. The annual and monthly straight-line fits are dropped. M1 is unchanged and alone keeps the error-pool recipe. Targets and scoring are unchanged. This replaces the earlier M2 and M3 design and withdraws P1 |
| P2 | **Approved.** Replay residuals are drawn by held-out year: each draw picks one left-out year, then resamples days within it. Now applies to M2 to M5 |
| P3 | **Approved.** A day enters the daily models only when both trough windows are complete |
| P4 | Approved, but no longer applies: there are no monthly lines after D9 |
| P5 | **Approved.** The forecasts table keeps `central` and `n_pool` beside the three POE columns |

**How the replay works for M2 and M3 (answer to the 12 November question).**

Nothing special is coded. The same replay function runs for M2 to M5. M2 and M3 have no weather
columns, so every replay year gives the same daily prediction path and all of the spread comes from
the residual draws. For these two models the out-of-fold residuals carry the whole weather effect,
so the left-out training years play the part that the weather years play for M4 and M5. They run
the same number of simulations as M4 and M5 (replay years times 100), so the quantiles are equally
precise.

Two consequences, both part of what the comparison measures rather than flaws:

- M2 and M3 see weather variability only through the 4 to 10 left-out training years; M4 and M5 also
  use the 17 to 23 replay years. A model with no weather input cannot use the long weather record.
- Residuals are in MW and do not scale with PV. A sunny-day residual from a low-PV year understates
  the same day's effect at the target year's PV. M4's PV x solar term does scale. This is the
  mechanism H2 tests.

**Fig. 5 stays as M2, M3, M4** (three panels, shared y-axis). After D9 the panels differ only in
predictors. M5 appears in Table III and Fig. 6.

**Agreed on 18 November 2026.**

| ID | Decision |
|---|---|
| P6 | **Approved.** Residual days are drawn from the same calendar month of the left-out year, for M2 to M5. Residual spread differs by season, and for M2 and M3 the residuals hold all of the weather; drawing across the whole year would hand a spring day a winter residual and bias the M3 against M4 comparison |
| D10 | **Confirmed.** Scrambled days are put back in time order (step 0 of the cleaning) |
| F1 | **Not corrected.** The level steps where reporting years join are stated as a data limitation |
| F2 | **Not corrected.** The substations that appear to be on standard time from FY2024 are stated as a data limitation |
| D11 | **H2 is tested by M4 against M3 only.** M5 against M4 is a separate comparison of model form (XGBoost against linear), not part of H2 |
| D12 | **Rescaled series in notebook 07.** F1 stays uncorrected in the main series. Notebook 07 adds a second network total in which each reporting-year file is rescaled so the 1 May joins meet, and shows Table III and the annual minima under both series side by side. The rescaling method is proposed in two lines when notebook 07 is reached; nothing before notebook 07 changes |
| F2 check | **Added to notebook 01**, so the limitation carries a reproducible number (`check_clock.csv`) |
| Simulated days | Left as is: M2 to M5 simulate every day of the target year, including days whose actual data is missing |
| M5 on M4's residuals | To be decided after the first run in notebook 05, as the prompt requires |
| Stops | Notebooks 02 to 04 are built in one run with one stop |

**Agreed on 18 November 2026, second round. Recorded before any model was fitted or any forecast
existed.**

| ID | Decision |
|---|---|
| D13 | **The daytime low is a second scored target.** It is the lowest half hour between 09:00 and 17:00 in the year or month. Every model's daytime-low forecast is kept (annual and monthly, POE10, POE50, POE90) beside its whole-day minimum, with actuals defined the same way. M1 forecasts it as last year's daytime low. A monthly daytime low counts only when at least 90% of that month's daytime-window half hours are kept. Notebook 06 writes Table III, Fig. 5 and Fig. 6 once per target, as separate files |
| D14 | **H1 and H2 are judged on the daytime low, annual and monthly.** H1 is M3 against M2; H2 is M4 against M3 (D11). The whole-day minimum stays the headline forecast target and is reported alongside, with the same comparisons shown as secondary |
| D15 | **Fig. 1** draws the annual overnight low and the annual daytime low as two lines in place of the single minimum, keeping maximum demand and the energy bars. The bars are grey so the third line can take green |
| D16 | **Fig. 4**, left panel: the daily daytime low against solar exposure, with the trend lines and their three slopes reported. Right panel unchanged (daily minimum against mean temperature). Each panel has its own y-axis label |
| D17 | **Table II** gains two columns: each year's overnight low and daytime low |
| D18 | **Robustness target redefined; replaces D6.** It is the mean of the 15 lowest daily minima of the year (2 lowest in a month), for the actuals and for all five models; M1 forecasts it directly. Only complete days count, and the number of complete days per year is reported beside it. The stand-in and its gap report are gone, and Fig. 3 loses its "lowest 0.5%" line. The robustness check covers the whole-day minimum only |
| D12 | Amended: the rescaled series in notebook 07 shows both targets, the whole-day minimum and the daytime low |
| Limitation text | `docs/results_summary.md` must name the daytime low explicitly where it states the sign limitation: unsigned reverse flow before May 2023 overstates daytime lows by roughly 20 to 70 MW and then steps down, for all models alike |

One rule added while building (to confirm at the notebook 05 stop): when the left-out year chosen
for a simulation has no residual day in some calendar month (April 2021, for example, has no valid
data), that month's residuals are drawn from the same month of all left-out years together.

**Found on the first run of notebook 05 (18 November 2026). Both settled in the third round below
(D19, D20); the evidence column is from that first run, with the two separate flags.**

| ID | Finding | Evidence | Status |
|---|---|---|---|
| F3 | **In the linear models (M2 to M4), the weekend and public-holiday effects add up on days that are both.** Each is worth about -430 to -545 MW on the daytime low, so a holiday falling on a weekend is predicted about 1,000 MW below a working day | For M3, the lowest predicted day of the target year is such a day in six of seven test years, and the prediction sits below what that day did: 1,865 against 2,147 (2019), 1,542 against 1,710 (2020), 1,325 against 1,795 (2021), 1,133 against 1,688 (2022), 1,170 against 1,293 (2023), 924 against 1,159 (2025). The lowest prediction on any other kind of day is 100 to 320 MW higher. Mean error of POE50 on the annual daytime low (actual minus forecast): M1 -126, M2 +64, M3 +185, M4 +257, M5 -22 MW. M5 is not affected: a tree model finds the interaction itself | **Settled by D19:** one non-working-day flag in all four models |
| M5 | **Plain XGBoost beyond its training range.** Its forecast with no borrowed miss sits 100 to 460 MW above the actual daytime low in every test year, as a model that cannot extrapolate PV should. With the left-out-year misses added, its POE50 errors are -67, +38, -72, +140, -237, +27, +14 MW | `check_m5_pv_range.csv` | **Settled by D20:** M5 stays plain |

No score (Table III) had been computed when these two were decided.

**Agreed on 18 November 2026, third round (after the first run of notebook 05, before any score).**

| ID | Decision |
|---|---|
| D19 | **One "non-working day" flag replaces the weekend and public-holiday flags**, for M2, M3, M4 and M5 alike. A day is non-working when it is a Saturday, a Sunday or a NSW public holiday. Reason (F3): the two separate flags added up on holidays falling on a weekend, and the day-level evidence suggests such a day behaves like an ordinary weekend day; one flag is also steadier than a term estimated from a few days a year. Notebook 05 keeps a check of the average miss on public holidays against ordinary weekend days, to show whether the single flag hides a real holiday effect |
| D20 | **M5 stays plain XGBoost.** No hybrid on M4's residuals |
| Fallback rule | Confirmed: a left-out year with no data in a calendar month borrows that month's residuals from all left-out years |
| Tests | Seven is accepted |

**Found on the rerun of notebook 05 with the single flag (18 November 2026). Not acted on.**

Table III was computed in the same run, so any change made in response to these two would be made
after the scores were seen, and should be labelled as such.

| ID | Finding | Evidence | Status |
|---|---|---|---|
| F4 | **The single flag hides a holiday effect, much smaller than the one F3 removed.** Given each day's own weather, the models miss public holidays on the low side by more than they miss ordinary weekend days | `check_holiday_miss.csv`, test years 2019 to 2025, 76 holidays against 667 ordinary weekend days. Mean miss (actual minus predicted) on holidays less that on weekend days, daytime low: M2 -159, M3 -150, M4 -123, M5 -126 MW. Overnight low: -45, -44, -42, -49 MW. The gap is about the same for all four models. With the single flag, M3's lowest predicted day is no longer a holiday in any test year (`check_lowest_predicted_day_m3.csv`) | **Settled by D21:** D19 stays; stated as a limitation |
| F5 | **M5 against M4 cannot be split into weather and model form.** M5 differs from M3 in two ways at once (weather and a tree model), and there is no tree model without weather | The ladder as specified (D9, D11): H2 is M4 against M3 only; M5 against M4 is model form with the same information | **Closed by D23:** M6 added |

**Agreed on 18 November 2026, fourth round. The scores of M1 to M5 (Table III, notebook 06) had
been seen when these were decided.**

| ID | Decision |
|---|---|
| D21 | **F4 is left as it is.** D19 (one non-working-day flag) stands and the holiday effect is stated as a limitation. The check stays in notebook 05 (`check_holiday_miss.csv`) |
| D22 | **Rescaling method for D12, approved as a bounding case.** Each join's step is taken as measured in notebook 01 (the change across midnight on 1 May less the usual midnight change). Every reporting-year file is multiplied by one constant so that each measured step closes: the latest file keeps its level, and each earlier file takes the factor of the file after it times one plus the step between them. The 2021 and 2025 joins cannot be measured and get no adjustment. The steps chain, so the first file is lifted by about 17% relative to the latest; the rescaled series is a bounding case, not a better estimate. Notebook 07 shows both targets under both series |
| D23 | **M6 added after the scores were seen, to close F5.** M6 is XGBoost with M3's predictors only (month, non-working day, PV capacity), with the same settings and the same POE recipe as M5. M5 against M6 is reported as a supplementary comparison of weather in tree form. It is not a pre-set test: H2 stays M4 against M3 (D11), and H1 stays M3 against M2. Adding M6 does not change any forecast of M1 to M5 (their random draws are seeded by model and origin; checked row for row) |
| D24 | **M4 is diagnosed, not changed** (F6 below) |
| Notes | `docs/decision_log.md`, `docs/substation_set_decisions.md` and `docs/public_cross_check.md` are Samhan's own notes and are not edited by the build |

**Found on 18 November 2026 when M4 was diagnosed (D24). M4 is unchanged.**

| ID | Finding | Evidence | Status |
|---|---|---|---|
| F6 | **The PV x solar term, not the temperature terms, pulls M4's forecasts down.** M4's POE50 of the annual daytime low sits below M3's in every test year and below the actual in most years from 2022 | `check_m4_terms.csv` (notebook 05): M4 refitted and replayed with one group of weather terms switched off. Mean pinball loss on the annual daytime low: M3 43.3, M4 63.5, M4 without temperature 62.6, M4 without PV x solar 45.7 MW. Mean error of POE50 (actual minus forecast): +77, +180, +150, +122 MW. From 2023 the variant holding only PV x solar is as low as M4 itself (871, 760, 707 against M4's 921, 757, 683 and M3's 1,016, 875, 839). In 2022 M3 is already about 350 MW below the actual (1,110 against 1,458) and each weather group takes off about another 55 MW. The temperature terms are a smaller, second contribution | **Recorded.** No change to M4. The two variants are a diagnostic and are not scored with the models |

**Found in notebook 07 (18 November 2026).**

| ID | Finding | Evidence | Status |
|---|---|---|---|
| F7 | **On the rescaled series (D22) the linear PV models do much worse, and the one score that favoured H1 reverses.** Rescaling lifts the early years by up to 17% and leaves 2024 and 2025 as published, so the series falls more steeply; M3 and M4 extrapolate that fall and sit below every annual actual | `sensitivity_rescaled_comparisons.csv`, `table3_daytime_low_rescaled.csv`. Mean pinball loss on the daytime low, published then rescaled, annual and monthly: M2 34.6 to 29.2 and 53.5 to 38.4; M3 43.3 to 87.0 and 49.6 to 53.6; M4 63.5 to 120.7 and 51.8 to 64.2; M5 28.5 to 20.8 and 42.8 to 41.3; M6 36.6 to 26.2 and 75.1 to 73.2 MW. H1 (M3 against M2) on the monthly daytime low goes from -7.4% to +39.6%. The other 15 of the 16 comparisons (four pairs, two targets, two levels) keep their direction; H2 stays positive (M4 worse than M3) everywhere, and M5 beats both M4 and M6 everywhere | **Recorded.** The rescaled series is a bounding case (D22); the published series stays the main one |
| F8 | **The reporting threshold barely moves the annual lows.** | `sensitivity_thresholds.csv`: between 90%, 95% and 98%, no annual daytime low moves; two whole-day minima move (2016 is 6 MW lower at 90%; 2018 is 16 MW higher at 98%) | **Recorded** |

**Agreed on 18 November 2026, fifth round. The first scores (Table III, notebooks 06 and 07) had
been seen when this was decided.**

| ID | Decision |
|---|---|
| D25 | **A daily out-of-sample comparison is added, in notebook 08.** It was added after the first scores were seen, because seven annual points cannot settle the comparison. For each test year 2019 to 2025 and each of M2 to M6, the model fitted at that origin predicts the daytime low of every day of the target year from that day's own calendar, PV capacity and weather, with no simulation and no borrowed misses. Nothing is refitted differently: these are the fits behind the forecasts of notebook 05. Reported per model: mean absolute error and mean error (actual minus predicted) over all valid days, and over the lowest 10% of actual days in each year, in total and by year; then three pairs, M3 against M2, M4 against M3 and M5 against M6. **What the pairs measure:** M4 and M5 see the actual weather here, so M4 against M3 and M5 against M6 measure how much weather explains, not how much it helps a year ahead. M3 against M2 uses no weather, so that pair is a fair one-year-ahead test |
| D25, as built | A day is valid when its actual daytime low exists under the rule the models are fitted with (P3: both trough windows complete), which gives 2,414 test days; scoring every day with a complete daytime window would add 6. The lowest 10% are taken year by year by actual value (240 days). The share is `evaluation.lowest_days_share` in the configuration |

**Found in notebook 08 (18 November 2026). The choices in "D25, as built" were accepted.**

All figures are for the daytime low over test years 2019 to 2025: 2,414 valid days, of which 240
are lowest days. MAE is mean absolute error; mean error is actual minus predicted. Source:
`daily_skill.csv`, `daily_pairs.csv` and their by-year versions.

| ID | Finding | Evidence | Status |
|---|---|---|---|
| F9 | **Day by day, PV capacity predicts the low days better than a time trend (M3 against M2, the one-year-ahead pair).** | Lowest days: MAE 211.7 against 292.4 MW (-27.6%), and M3 misses by less in all seven test years. All days: 260.3 against 274.1 MW (-5.0%), M3 better in four of seven years | **Recorded** |
| F10 | **Given the day's actual weather, both weather models miss by less than their no-weather counterparts.** These two pairs measure how much weather explains, not how much it helps a year ahead (D25) | M4 against M3: all days 227.1 against 260.3 MW (-12.8%, seven of seven years); lowest days 169.2 against 211.7 MW (-20.1%, six of seven; 2022 is the exception at +16.1%). M5 against M6: all days 157.4 against 262.3 MW (-40.0%, seven of seven); lowest days 173.1 against 339.5 MW (-49.0%, seven of seven) | **Recorded** |
| F11 | **Two cautions on reading notebook 08.** (a) On the lowest days the mean error is negative for every model partly by construction: the days are chosen for a low actual, so it compares models but does not measure bias. (b) The tree models cannot follow PV growth: M6's lowest-day errors are almost all one-sided (MAE 339.5, mean error -336.8 MW), as are M5's in 2023 (352.9, -352.9), so part of the M5 against M6 gap is that handicap and not weather | Mean error on the lowest days: M2 -286, M3 -169, M4 -91, M5 -157, M6 -337 MW | **Recorded** |

**Agreed on 18 November 2026, sixth round: the repository is sorted by what each result is for.**

The paper's four points, as set by Samhan, are the test of what is a paper artifact:

1. The minimum has shifted from the overnight low to the daytime low.
2. PV capacity tracks the daytime low over the decade and predicts the low days better than a
   time trend.
3. Weather explains which days are low.
4. One year ahead, the tree model with PV and weather forecasts best, and weather helps only in
   that form.

| ID | Decision |
|---|---|
| D26 | **Three output folders.** `outputs/figures` and `outputs/tables` hold the paper artifacts, named by their number in the paper. `outputs/checks` holds everything the limitation and robustness statements rely on. `outputs/archive` holds superseded versions and exploration, written by notebooks under `notebooks/archive` so that they stay reproducible. Main notebooks write only paper artifacts and checks. Files kept their names when they moved; nothing was dropped |
| D27 | **Fig. 5 has four panels (M2, M3, M4, M5) on the daytime low, and Fig. 6 is on the daytime low.** The three-panel Fig. 5 and the whole-day-minimum versions of both figures are archived. Fig. 3 and Fig. 6 are optional candidates for the paper |
| D28 | **Table III is one table** (`table3.csv`): six models, the daytime low and the whole-day minimum, annual and monthly, with coverage. It replaces the two per-target files, whose numbers it holds unchanged |
| D29 | **Table IV is the daily out-of-sample test** (`table4.csv`, notebook 08): a row per model and a row per pair, over all valid days and over the lowest 10%. The by-year versions are checks |
| D30 | **A straight-line fit supports point 2** (`table_pv_fit.csv`, notebook 04; no paper number): the eleven annual daytime lows of 2015 to 2025 fitted on PV capacity (the published capacity at 30 June, in MW) and, separately, on the year, with slope, intercept, R-squared and RMSE (root mean squared residual, no adjustment for the fitted parameters) |
| D31 | **Kept beside the paper artifacts, although not numbered:** the figure data files (`fig1_data`, `fig2_data`, `fig4_fits`, `fig6_data`) and `headline_numbers.csv`, on which point 4 rests |
| D32 | **Three looks first made outside the repository are now reproducible, placed by use.** M4's coefficients and the reach of PV x solar beyond its training range (`check_m4_coefficients.csv`, notebook 05) and the bias of POE50, which carries M6's monthly bias (`check_poe50_bias.csv`, notebook 06), are checks, because the paper's cautions rely on them. The holiday miss by holiday is in the archive (`A1_model_exploration`) |
| D33 | **Left where they were:** the stress-test reproduction stays in notebook 01, shown but not saved; `check_annual_summary.csv` and `check_m5_pv_range.csv` are checks |

**My reading of D9. Confirmed on 18 November 2026.**

| Point | Reading |
|---|---|
| Two troughs | Kept for M2 to M5, as locked in section 7 of the prompt: one fit per trough, lower one taken each day |
| M2's time variable | Years since 1 January 2015 as a daily value, so that M3 is M2 with one column swapped (time for daily PV) |
| "Effect allowed to differ by month" | Twelve month intercepts and twelve month-specific slopes on time (M2) or PV (M3, M4), plus the non-working-day flag (D19; first built with separate weekend and holiday flags). M4 adds one coefficient each for PV x solar, maximum temperature and minimum temperature |
| M5 columns | Month, non-working day (D19), PV, PV x solar, maximum temperature, minimum temperature |
| Robustness target | Superseded by D18: every model forecasts the mean of the 15 lowest daily minima (2 in a month) |
| Paper documents | Table I rows for M2 and M3 change (fitted on daily minima; POE from the replay), and two Method bullets in the prewriting plan no longer hold. Yours to edit |

**Found while building notebook 01 (12 November 2026). None of these is in the stress test.**

| ID | Finding | Evidence | Status |
|---|---|---|---|
| D10 | **Scrambled days in the FY2023 file.** From 1 to 30 April 2023, 104 substations (about 69% of load) have each day's 96 values in alphabetical order of interval number (1, 10, 11 ... 19, 2, 20 ...) under a time-ordered header | A day is re-ordered only when that cuts its roughness by more than half. The test finds 2,834 substation-days in FY2023 and none in the other eleven files. April 2023's mean profile returns to the shape of April 2022 and 2024. The April 2023 monthly minimum moves by 1 MW; no annual minimum moves | **Repair applied as step 0 of the cleaning. Confirmed 18 November.** To revert, set `scrambled_roughness_ratio` to 0 |
| F1 | **Level steps where reporting years join.** The files do not meet at the same level at midnight on 1 May | Step against the usual midnight change, 2015 to 2024 joins: +3.0%, +4.8%, +2.3%, +1.6%, -0.5%, -1.1%, (2021 not measurable), +7.2%, -4.1%, +3.2%. Four of the nine rank in the top 31 of 3,827 nights. The steps are in the published substation values (84% of substations above 5 MW step up at the 2022 join); substations entering and leaving the kept set explain roughly a third to a half. The FY2023 file sits 4% to 7% above both neighbours | **Not corrected; a stated data limitation (decided 18 November).** Measured in notebook 01 (`check_join_steps.csv`) |
| F2 | **Some substations are on standard time from FY2024.** During daylight saving their profiles sit one hour early | When daylight saving starts, the morning rise moves 45 minutes or more earlier for substations carrying about 22% of load in FY2024, 13% in FY2025 and 10% in FY2026, against 0% to 1% in FY2015 to FY2023; in FY2024 the same share moves back when it ends. All three annual minima from 2023 fall in daylight-saving months | **Not corrected; a stated data limitation (decided 18 November).** Measured in notebook 01 (`check_clock.csv`) |

One day (21 April 2016) reads about 350 MW high across the CBD substations; it was seen and not
pursued, because an upward block cannot create a false minimum and the day is not a maximum.

**Defaults accepted on 11 November 2026.**

| Area | Default |
|---|---|
| Time | Labels as published: local clock time, interval-ending; no time-zone conversion. Series are indexed by interval start; times in tables are interval end |
| Repeated dates in a file | First non-blank value per interval across the copies |
| Annual minimum | Lowest kept half hour of the calendar year; no coverage cut |
| Trough windows | Overnight: the 12 half hours from 00:00 to 06:00. Daytime: the 16 half hours from 09:00 to 17:00. None of the 131 monthly minima falls outside both |
| Valid trough-day | Every half hour in the window kept (see P3) |
| M1 | Last year's actual minimum; a month takes the same month last year, or the last valid same month |
| M2 to M5 | Superseded by D9 on 12 November: see the ladder in section 6 |
| PV input | One daily series (MW) for M2 to M5; target-year actuals. M1 uses none |
| Weather gaps | Gaps of up to 3 days interpolated linearly |
| Replay years | 1990 to the origin, keeping years with no longer gap: 17 at the first origin, 23 at the last |
| 29 February | The replay uses 28 February weather when the replayed year has none; a replayed 29 February is dropped when the target year has none |
| Error draws | 100 per replay year; residuals paired across the two troughs by day |
| XGBoost | 300 trees, depth 3, learning rate 0.05, subsample 0.8, seed 42 |
| Fig. 3 and Fig. 4 years | 2015, 2020, 2025 |
| Environment | Python 3.11 venv and pip, pinned requirements; NSW holidays from the `holidays` package (0.90); a minimal `pyproject.toml` so notebooks can `import pynmdf` |

## 4. Repository

As section 8 of the prompt, plus four items: `pyproject.toml` (editable install and ruff/black
settings only; no release metadata), `requirements.txt` (pinned), `tests/` (D8), and
`docs/results_summary.md` at the end. Nothing under `data/` or `outputs/` is committed.

`config.example.yaml` holds every parameter that is a decision: paths; the file name for each
reporting year and each LGA year (names are irregular, so they are mapped explicitly); the FY2024 PV
constant and its source; 1,000 MW unit threshold; outlier ratio 5 and quantile 0.75; stuck run 96;
20% missing; 8-interval gap; 95% reporting share and the 90/95/98 sensitivity set; 90% monthly
validity; trough hours; 0.5% and 1% shares; 15 and 2 stand-in days; POE levels; first test year;
replay start year and 3-day weather gap; 100 draws; seed; XGBoost settings; figure years; the
expected PV table used by the assertion.

## 5. Design by module

### `io_demand.py`

`read_reporting_year(source, fy)` returns one wide frame: index is the 15-minute interval start over
the full 1 May to 30 April calendar, one column per substation, MW. It handles a zip or a folder,
nested paths, header case and padding, four date formats, labels converted to minutes (`00:00` and
`24:00:00` both read as 24:00) and sorted, `NaN` strings, absent days (left blank), and repeated
dates (first non-blank value).

### `clean.py`

One small function per step, composed by `clean_reporting_year` in the locked order:

0. `restore_scrambled_days` (D10; added 12 November)
1. `unit_error_blocks` (D1)
2. `outlier_days` (D2) and `stuck_runs` (D3)
3. `drop_sparse_substations` (20% rule)
4. `fill_short_gaps` (interior gaps of up to 8 intervals only; longer gaps are not part-filled)
5. `network_total` (scale-up; returns the total and the reporting share at 15 minutes)
6. threshold, 7. `to_half_hour` (both inside `half_hourly_total`)

`build_network_total` joins the twelve files, asserts no duplicate or missing timestamps, and cuts
to 2015-2025. The 15-minute total and reporting share are cached so notebook 07 can re-threshold at
90%, 95% and 98% without re-reading raw files. Each file also yields one row of the data-quality
table.

### `io_pv.py`, `io_weather.py`

`pv_capacity_series` locates "Generation capacity (kWp)" and the row whose first cell is "Total" by
text, sums Res and Non-Res where both exist, adds the FY2024 constant, and asserts against the
expected table. `daily_pv` interpolates between 30 June values and extrapolates each edge with the
adjacent segment's slope. `read_weather` joins the three BOM files by date (solar exposure kept in
MJ/m2), adds the daily mean temperature, and reports missing days and the quality-flag share.

### `targets.py`, `models.py`, `poe.py`, `evaluate.py`

Detailed in section 6.

### `plots.py`

`set_style` (8 pt serif, 3.5 in and 7.16 in widths, palette from `#2a78d6`, `#eb6834`, `#1baf7a`,
no titles), one function per figure, and `save_figure` writing PNG at 600 dpi and PDF. The
placeholder figures in the skeleton are viewed before each figure is built.

## 6. Modelling and evaluation

### Targets (`targets.py`)

- `daily_troughs(total, windows)`: per date, the overnight and daytime minimum; blank unless both
  windows are complete (P3).
- `period_targets(total, ...)`: one tidy frame of annual and monthly actuals for the three scored
  targets, each with a `valid` flag: `minimum` (lowest kept half hour; D4), `daytime_low` (lowest
  kept half hour between 09:00 and 17:00; D13) and `robust` (mean of the 15 lowest daily minima,
  2 in a month, over complete days; D18).
- `lowest_intervals(total, share)`: the lowest 1% of each year's half hours, for Fig. 2 and Fig. 3.

The whole-day minimum is always taken over all kept half hours of the year or month. H1 and H2 are
judged on the daytime low (D14).

### Models (`models.py`)

M1 needs no fit: next year equals this year, and a month equals the same month last year (or the
last valid one).

M2 to M5 are a nested ladder (D9). Each is fitted on daily minima, one fit per trough, and the
lower trough is taken each day.

| ID | Form | Predictors |
|---|---|---|
| M2 Time trend | Linear regression | Month intercepts, non-working day (D19), time with a slope per month |
| M3 PV only | Linear regression | As M2, with daily PV capacity in place of time |
| M4 PV + weather | Linear regression | M3's predictors plus PV x solar exposure, maximum temperature, minimum temperature |
| M5 PV + weather | XGBoost | Month, non-working day, PV, PV x solar exposure, maximum temperature, minimum temperature |
| M6 PV only (supplementary; D23) | XGBoost | Month, non-working day, PV |

`calendar_features` and `add_weather` build every column from the PV series, weather and calendar.
`MODELS` maps each ID to its estimator and its column list, so the models are data, not code.
`M4_VARIANTS` holds the two diagnostic variants of M4 (F6), which are never scored with the models.
`fit_daily` and `predict_daily` serve all of them. `out_of_fold_residuals` refits with each training year left out in
turn and returns that year's daily residuals for both troughs (D7). `MODEL_INFO` holds the short
labels that become Table I.

### POE (`poe.py`)

Error sign throughout: actual minus forecast. POE10, POE50 and POE90 are the 0.90, 0.50 and 0.10
quantiles.

**M1.** POE = last year's value plus a quantile of an error pool. The pool is M1's past
year-on-year changes up to the origin, which are genuine one-year-ahead errors throughout (three at
the first origin, nine at the last). Monthly pools combine the twelve calendar months. POE50 is the
central forecast plus the median error, so it need not equal the central forecast.

**M2 to M5.** `replay_lows` sets PV and the calendar to the target year, then for each replay
weather year predicts every day for both troughs and adds out-of-fold residuals. Each draw picks
one left-out year (P2), then for each simulated day one day of that year from the same calendar
month (P6), using that day's two trough residuals together. It takes the lower trough
each day and keeps the lowest day of the year and of each month. One hundred draws per replay year;
POE levels are quantiles across all simulated years. `central` is the lowest day with no residual
added, averaged over replay years; it sits above POE50 by construction and is descriptive only. The
same simulations give all three targets: the lowest day (whole-day minimum), the lowest daytime
trough (daytime low) and the mean of the 15 lowest days, 2 in a month (robustness target).

M2 and M3 pass through the same function unchanged. Their columns ignore the weather, so the
prediction path is identical in every replay year and only the residual draws differ.

Error pools, out-of-fold residuals and replay years are all rebuilt at each origin from data up to
that origin only.

### Evaluation (`evaluate.py`)

`rolling_origin(total, pv, weather, cfg)` makes every forecast of the study. It loops origins 2018
to 2024 and the six models and returns one table that everything downstream reads, one row per
forecast:

`target` (minimum, daytime_low, robust) · `level` (annual, monthly) · `model` · `origin` · `year` · `month`
(0 for annual) · `central` · `poe10` · `poe50` · `poe90` · `actual` · `valid` · `n_pool`

`n_pool` is the number of errors (M1) or simulated years (M2 to M5) behind the quantiles.

`pinball_loss(actual, forecast, q)` and `score(forecasts)` give Table III: pinball loss at each of
the three quantiles and their mean, and coverage (share of actuals between POE90 and POE10), by
model, for annual and monthly targets, over valid test points only. `COMPARISONS` names the four
comparisons reported as headline numbers (H1, H2, model form, and the supplementary M5 against M6)
and `compare` computes them.

Seeds are derived from the config seed, the model and the origin, and XGBoost runs single-threaded,
so reruns reproduce exactly.

## 7. Notebooks and stop points

Each notebook opens with a markdown cell giving the paper section it serves, what it produces, its
inputs, its outputs and a numbered outline; each section has a heading and a short explanation; each
closes with its result as numbers. Work stops for review after every notebook.

The table is the repository as it stands after the tidy of the sixth round (D26). Paper artifacts
are in `outputs/figures` and `outputs/tables`; checks are in `outputs/checks`.

| Notebook | Paper artifacts | Supporting checks |
|---|---|---|
| 01 | - | `check_data_quality` (what the cleaning did; load lost to the 20% rule; scrambled days restored, D10); `check_annual_summary`; `check_kept_by_month`; `check_join_steps` (F1); `check_clock` (F2); `check_sign` (D5). Shown, not saved: the reader against the stress-test minima |
| 02 | - | `check_pv_capacity`; `check_weather_missing`; `check_weather_quality` |
| 03 | Fig. 1 (maximum, overnight low, daytime low, energy; D15) and `fig1_data` | - |
| 04 | Fig. 2 and `fig2_data`; Fig. 3; Table II (D17); Fig. 4 and `fig4_fits` (D16); `table_pv_fit` (D30) | `check_trough_windows` |
| 05 | Table I (six models) | `check_complete_days`; `check_m5_pv_range` (D20); `check_holiday_miss` (D19, F4); `check_m4_terms` and `check_m4_coefficients` (F6) |
| 06 | Table III (D28); Fig. 5 (D27); Fig. 6 and `fig6_data`; `headline_numbers` (H1, H2, model form, and the supplementary M5 against M6) | `check_poe50_bias` |
| 07 | - | `table3_robust` and `sensitivity_robust` (D18); `sensitivity_thresholds` (F8); `sensitivity_rescale_factors`, `sensitivity_rescaled_lows`, `table3_daytime_low_rescaled`, `table3_minimum_rescaled`, `sensitivity_rescaled_comparisons` (D12, D22, F7) |
| 08 | Table IV (D25, D29) | `daily_skill_by_year`; `daily_pairs_by_year` |

| Archive notebook | Writes to `outputs/archive` |
|---|---|
| `A1_model_exploration` | The first look at POE50 against the actuals; the day M3 predicts as lowest (F3); the holiday miss by holiday and around Christmas (F4) |
| `A2_superseded_figures` | Fig. 5 with three panels, on the daytime low and on the whole-day minimum; Fig. 6 on the whole-day minimum, with its data |

Notebooks 05 to 08 and the archive notebooks cover six models. The data passed between notebooks
are in `data/interim`.

**Status at 18 November 2026: complete.** All eight main notebooks and the two archive notebooks
were run twice after the tidy and all 69 files they write (outputs and `data/interim`) were
identical between the runs. The 47 output files that the tidy only moved or renamed are identical,
byte for byte, to their versions before it. `docs/results_summary.md` holds the numbers behind the
paper by type of evidence, and the README maps every paper artifact and check to its notebook.

## 8. Tests

Ten pytest tests (six planned, four added while building; see the end of this section), all on
small synthetic data built in the test (no raw files):

1. **Reader.** One substation written in each date format, header case, label order and final-label
   variant, with a repeated date and an absent day, reads to the same frame.
2. **Invalid values.** A unit block containing a value below 1,000 is corrected in full and values
   outside it are untouched; a 96-interval run is marked and a 95-interval run is not; a run of
   zeros is marked; an inflated day is marked and a normal day is not.
3. **Network total.** An 8-interval gap is filled linearly while a 9-interval gap and the edges stay
   blank; with one substation of known share blank the scaled total equals the true total; the
   interval is dropped below the threshold; a half hour is valid only when both quarters are.
4. **Scoring.** Pinball loss and coverage match hand-computed values; POE10 maps to the 0.90
   quantile; POE10 is never below POE50, nor POE50 below POE90.
5. **No look-ahead.** Scrambling demand and weather after year k leaves every forecast for origins
   up to k unchanged.
6. **Replay.** With zero residuals and a stub model that returns the maximum temperature, each
   replay returns that year's lowest value per month and year; a stub that ignores the weather
   returns the same path in every replay year; 29 February takes 28 February weather; the same
   seed gives the same output.

Tests 1 to 3 arrive with notebook 01; tests 4 to 6 with notebook 05. A seventh was added with
notebook 05: residual draws never leave their calendar month, stay within one left-out year per
simulation, and borrow from the other years when that year has no data for a month (P2, P6). An
eighth came with notebook 07, for its new logic: rescaling closes the joins between reporting
years, the latest file keeps its level, and a join that cannot be measured gets no adjustment (D22).
A ninth came with notebook 08: the daily skill tables and pairs match a hand calculation, days
with no actual are not scored, and the lowest days are picked year by year (D25). A tenth came
with the tidy: the straight-line fits behind `table_pv_fit.csv` return the right slope, R-squared
and RMSE (D30). The scoring test also covers the mean error of POE50, and the daily test Table IV.

## 9. What could go wrong

- **What D9 fixed.** M2 to M5 now share the data, the fitting level, the PV series and the POE
  recipe, so each rung of the ladder changes predictors only. The earlier caveats about three
  things changing at once and about unequal PV foresight no longer apply. M1 alone still uses a
  different recipe.
- **Slopes at the first origins.** With four training years each month's slope on time or PV rests
  on four levels, and both troughs rose over 2015-2018 (overnight 1,368 to 1,495; daytime 1,833 to
  1,905). M2 and M3 will forecast a rise for 2019. That is the model as specified, and a result.
- **M2 and M3 may be hard to tell apart.** PV capacity is a smooth function of time, so over short
  windows the two regressors carry nearly the same information. H1 may be weakly identified at the
  early origins.
- **M4's temperature terms are linear across the whole year**, although demand rises on both cold
  and hot days. They may add little for that reason alone. M5 is the check on it.
- **One year carries much of the annual ranking.** The 2022 to 2023 fall (1,428 to 1,080 MW) is by
  far the largest annual error for every model. Seven annual points cannot settle H2; the monthly
  table carries more weight.
- **POE from few years.** At the first origin M1 has three errors, and M2 to M5 draw residuals from
  four left-out years. Coverage is descriptive only.
- **Out-of-fold residuals when the held-out year is the last.** XGBoost cannot extrapolate PV, so
  those residuals are large and one-sided. They widen M5's bands, as intended by D7.
- **Residual spread may grow with PV.** If it does, residuals from early years understate
  target-year noise in the daytime trough. Left as specified; for M2 and M3 it is the effect under
  test.
- **Level steps from the 20% rule** (0% to 2.4% of load, by file) and **the sign step at May 2023**
  (roughly 20 to 70 MW on daytime minima before it) add errors common to all models.
- **Fewer monthly points.** 76 test months; calendar months in Fig. 6 have five to seven points.
- **Actuals come from kept half hours only.** In 2024 (88% kept, January almost absent) a simulated
  year covers every day while the actual does not. The review suggested dropping simulated days
  that are missing in the target year; I have not adopted it, because a forecast should not know
  the target year's data holes, and the threshold check in notebook 07 shows the annual lows
  barely move (F8). Say so if you want the mask.
- **The daytime low is the series the two uncorrected limitations hit.** Unsigned reverse flow
  before May 2023 and the standard-time substations from FY2024 both act on the midday dip. The
  whole-day minimum was shielded in 2019, 2020 and 2022, when it fell overnight. The daytime
  target's 2023 score carries the sign step, for all models alike (D14).
- **Robustness target.** After D18 every model forecasts the same day-based quantity, so no
  stand-in is involved. In 2024 only 309 of 366 days are complete.
- **Cleaning uses whole-file statistics** (shares, the 75th percentile), so training data are
  cleaned with knowledge of later months in the same file. Standard practice; noted.
- **Practical.** Reading raw files takes about four minutes (cached to parquet afterwards);
  notebook execution needs `ipykernel` and `nbconvert` installed in the venv; raw folders are on
  OneDrive and in Downloads and are only ever read.

**Alternatives considered and set aside.** A per-value outlier rule (misses 8% of Morisset's
block); hand-listed bad blocks (no automatic rule); a short stuck-run threshold (drops coarse but
valid meters); relaxing the 95% threshold for thin months (two thresholds in one series);
redefining the robustness target at daily level (departs from the locked definition); annual and
monthly straight-line fits for M2 and M3 with an error-pool POE (replaced by D9, because the step
to M4 then changed data, fitting level and POE recipe at once).

## 10. Build order

1. **Scaffold.** `git init` (no commit), venv, `pyproject.toml`, `requirements.txt`, `.gitignore`,
   both config files, `docs/analysis_plan.md` (this plan), README skeleton.
2. `io_demand.py`, `clean.py`, tests 1 to 3, notebook 01. **Stop for review.**
3. `io_pv.py`, `io_weather.py`, notebook 02. **Stop.**
4. `targets.py`, `plots.py` (style and Fig. 1), notebook 03. **Stop.**
5. Notebook 04 (Fig. 2, Fig. 3, Table II, Fig. 4). **Stop.**
6. `models.py`, `poe.py`, `evaluate.py`, tests 4 to 6, notebook 05 with plain M5. **Stop and ask**
   about refitting M5 on M4's residuals.
7. Notebook 06. **Stop.**
8. Notebook 07, `docs/results_summary.md`, final README.

No commit, push or pull request unless asked.

## 11. Verification

- `ruff check .`, `black --check .` and `pytest` pass before each stop.
- Each notebook runs top to bottom with `jupyter nbconvert --to notebook --execute --inplace`.
- Notebook 01 reproduces the stress-test diagnostic minima (using the same part-fill as the stress
  test, for that check only) and shows every section 11 check from the prompt.
- Notebook 02's assertion on the PV table passes.
- Each notebook is run twice and its saved parquet and CSV outputs compared, to confirm fixed seeds
  reproduce the same numbers.
- At the end: six figures (PNG and PDF) and four tables (CSV) in `outputs/figures` and
  `outputs/tables`, named by their number in the paper, with `table_pv_fit.csv`, the figure data
  and `headline_numbers.csv` beside them; the supporting checks in `outputs/checks`; the archive
  in `outputs/archive`. All eight main notebooks and the two archive notebooks run from raw data
  after changing only the paths in `config.local.yaml`.
