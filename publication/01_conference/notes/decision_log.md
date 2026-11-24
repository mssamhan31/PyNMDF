# PyNMDF decision log

One running record of exploration results, insights and key decisions, kept by Claude (chat) at
Samhan's request from 18 November 2026. Newest entries at the bottom. Claude Code's working plan is
`analysis_plan.md`; this log explains the why in plain terms and points to it for detail.

Other notes in this folder:

| File | What it holds |
|---|---|
| `analysis_plan.md` | Claude Code's plan: every decision (D), proposal (P) and finding (F) with evidence |
| `substation_set_decisions.md` | Why the substation set changes by year and why poor-data substations are dropped |
| `public_cross_check.md` | The network total against public Ausgrid figures (about 80% of the whole network) |

Paper documents (plan, scope, skeleton) are kept outside this repository.

## 11 November 2026: scope and data

| Topic | Decision | Why | Alternative set aside |
|---|---|---|---|
| Scope | One network total (sum of public zone substations), calendar 2015 to 2025, one year ahead, POE10/50/90 | Minimum publishable unit on public data | Substation-level forecasts, longer horizons, other data sources |
| Gaps in the data | Scale-up rule: total = sum of reporting substations divided by their usual share; drop an interval below 95% reporting | Keeps most of the year without inventing false lows | Complete intervals only (27 to 240 days a year); blanks as zero (380 MW instead of 880 MW) |
| Signs | Kept as published | Correcting them is a project in itself | Sign correction. Later confirmed from Ausgrid's notes: reverse flow is unsigned before May 2023, roughly 20 to 70 MW on daytime lows |
| PV capacity | 2015 and 2016 single column taken as residential plus non-residential; edges extrapolated | The 2017 residential figure is below the 2016 figure | - |
| Monthly validity | A month counts only when at least 90% of its half hours are kept | A missed minimum is always too high, never too low, so thin months bias the score | 75% or 50% (adds months most likely to have missed the true minimum) |
| Trough windows | Overnight 00:00 to 06:00, daytime 09:00 to 17:00 | No monthly minimum falls outside them; narrow windows keep more days valid and keep the daytime low a midday feature | Whole-day or 6am to 6pm split |
| Honest misses | Misses for the simulation come from a left-out year, not from days the model was trained on | In-sample misses are too small and make the range too narrow | In-sample residuals |

## 12 November 2026: model design

| Topic | Decision | Why | Alternative set aside |
|---|---|---|---|
| Ladder | M2 to M5 all fitted on daily minima with one POE recipe; each adds one thing | The first design changed data, fitting level and POE recipe at once between M3 and M4, so a win could not be credited to weather | Annual straight-line M2 and M3 |
| Time against PV | M3 swaps time for PV; it does not add PV on top of time | Time and PV rise together, so a model with both cannot split the effect and forecasts erratically | Add PV to time (answerable only with a longer record) |
| Season | Calendar terms (month, day type), with the time or PV effect allowed to differ by month | PV's effect differs a lot between months | "Typical weather" inputs (confusing); one trend for all months (too blunt) |
| Miss draws | A simulated day draws its miss from the same calendar month | A spring day must not receive a winter-sized miss | Draw from any day of the year |

## 18 November 2026: data findings

| Topic | Insight or decision | Why it matters |
|---|---|---|
| Substation set | Sum all substations that pass the rule each year; no fixed set | Load moves between substations; a fixed set turns that into false falls. See `substation_set_decisions.md` |
| Level steps at 1 May (F1) | Not corrected in the main series. Steps over the 2015 to 2018 joins add up to about +12%, against a rise of about 9% in the minimum | The early rise may be an artefact. A rescaled series is run in notebook 07 as a bounding case (closing every step lifts FY2015 by about 17% against FY2026) |
| Clock time (F2) | Substations carrying 21.7%, 12.8% and 10.0% of load sit an hour early in daylight saving in FY2024 to FY2026. Limitation only | Second-order: the midday low is fairly flat across an hour |
| Network coverage | The total is about 80% of the whole Ausgrid network | Call it the sum of published zone substations. See `public_cross_check.md` |
| Fig. 1 facts | 2015 to 2025: maximum -0.6% (no trend), energy -7.3% (gentle decline), minimum -35.7% | Headline numbers for the Introduction |

## 18 November 2026: the daytime-low insight

- From 2015 to 2025 the overnight low moves from 1,368 to 1,435 MW (+4.9%), while the daytime low
  falls from 1,833 to 880 MW (-52%). The daytime low is the lower of the two in 2021, 2023, 2024
  and 2025.
- The daytime low's slope against solar exposure is +0.6, -6.6 and -35.4 MW per MJ/m2 in 2015, 2020
  and 2025. On the whole-day minimum the same slopes were -4.8, -2.0 and -14.7, because the early
  minima were overnight and sunshine cannot affect them.
- New narrative: as PV grows, the minimum shifts from the overnight low to the daytime low, and
  the two cross.

| Decision | Why |
|---|---|
| Fig. 1 shows the two lows as separate lines; Fig. 4's left panel uses the daytime low; Table II lists both lows | Shows the crossing and the steepening directly |
| The daytime low is a second scored target | In 2019, 2020 and 2022 the whole-day minimum was overnight, so those years cannot tell the models apart |
| H1 and H2 are judged on the daytime low; the whole-day minimum stays the headline forecast | Fixed before any model result existed. PV and weather act only on the daytime low |
| Robustness measure is the mean of the 15 lowest daily minima (2 in a month) | The daily models forecast it directly; the old "lowest 0.5% of half hours" needed a stand-in |

## 18 November 2026: calendar terms

- Finding: with separate weekend and holiday flags, a holiday on a weekend received both effects
  and was predicted about 1,000 MW below a working day (Christmas Day 2022: predicted 1,133 MW,
  actual 1,688 MW). The annual forecast is the lowest of 365 simulated days, so one such day set it.
- Decision: one "non-working day" flag (weekend or public holiday) in M2 to M5. Steadier than a
  third term estimated from a few days a year.
- Check afterwards: holidays still run 120 to 160 MW below ordinary weekend days on the daytime
  low, concentrated at Easter, Christmas Day and New Year's Day; working days from 24 December to
  2 January are missed by about 300 MW (a shutdown period).
- Decision: left as a stated limitation. The gap is about the same in all four models, and changing
  it after seeing scores would be tuning.
- M5 stays plain XGBoost; no hybrid on M4's residuals, which would blur the comparison of model form.

## 18 November 2026: first results (notebook 06)

Mean pinball loss in MW (lower is better), before any sensitivity run:

| Model | Daytime low, annual | Daytime low, monthly | Minimum, annual | Minimum, monthly |
|---|---|---|---|---|
| M1 Naive | 63.1 | 50.5 | 45.2 | 43.5 |
| M2 Time trend | 34.6 | 53.5 | 31.1 | 37.5 |
| M3 PV only | 43.3 | 49.6 | 41.6 | 41.4 |
| M4 PV + weather, linear | 63.5 | 51.8 | 60.0 | 44.1 |
| M5 PV + weather, XGBoost | 28.5 | 42.8 | 26.9 | 32.5 |

| Question | Result | How solid |
|---|---|---|
| H1: does PV beat the time trend (M3 against M2)? | Annual: 25% worse. Monthly: 7% better (daytime low) | Mixed. Seven annual points; M2 wins partly through a very wide band |
| H2: does linear weather help (M4 against M3)? | Worse at both levels (47% and 5%) | Not yet trustworthy: M4's whole band sits low from 2022, cause undiagnosed |
| Model form (M5 against M4) | M5 better by 55% and 17% | Solid, but weather and model form cannot be separated |

Insights:

- Suspected cause of M4's failure: temperature enters as one straight line all year, while Fig. 4
  shows a U shape. On an extreme replay day a straight line can push the prediction far too low,
  and the lowest of 365 days sets the forecast.
- Why not make every model XGBoost: a tree only uses the order of an input. Time and PV capacity
  both only go up, so to a tree they are the same input, and M2 and M3 would give identical
  forecasts. H1 can only be tested in linear form. Weather can be tested in tree form.

Proposed on 18 November and since carried out (see the next section):

| Proposal | Why |
|---|---|
| Diagnose M4's low band (rerun the replay with the temperature terms off) | To know whether the H2 result is about weather or about a crude linear form |
| Add M6: XGBoost with PV and calendar only | M5 against M6 isolates weather in a form that can handle the U shape. The pre-set H2 test (M4 against M3) is still reported |

## 18 November 2026: M4 diagnosis, M6 and the sensitivity runs (notebook 07)

**M4 diagnosis.** The suspicion above was wrong: the temperature terms are not the cause. The
PV x solar term is. Evidence, on the annual daytime low:

| Variant | Mean pinball loss (MW) | Mean POE50 error (MW) |
|---|---|---|
| M3 | 43.3 | +77 |
| M4 | 63.5 | +180 |
| M4 without temperature | 62.6 | +150 |
| M4 without PV x solar | 45.7 | +122 |

- Each target year's sunniest days lie 8% to 29% beyond the largest PV x solar value seen in
  training, so the straight line is extended past its data on exactly the days that set the minimum.
- On the 15-lowest-days measure M4's gap to M3 shrinks from +44% to +13%, so the problem sits in
  the single most extreme day.
- Not settled: whether the real response flattens at high PV, or the simulation stacks an extreme
  weather day on top of an extreme miss. Either way it is a limit of the linear form.

**M6 added** (XGBoost with month, non-working day and PV capacity; no weather), after the scores
were seen, to separate weather from model form. Adding it changed no forecast of M1 to M5.

**Comparisons on the daytime low** (change in mean pinball loss, negative means the first model is better):

| Comparison | Annual, published | Annual, rescaled | Monthly, published | Monthly, rescaled |
|---|---|---|---|---|
| H1: M3 against M2 | +25.0% | +198.2% | -7.4% | +39.6% |
| H2: M4 against M3 | +46.7% | +38.7% | +4.5% | +19.8% |
| Model form: M5 against M4 | -55.1% | -82.8% | -17.3% | -35.6% |
| Supplementary: M5 against M6 | -22.2% | -20.8% | -43.0% | -43.6% |

**What holds up**

| Finding | Status |
|---|---|
| H1 (PV beats the time trend) | Not supported. Its one favourable score reverses on the rescaled series |
| H2, pre-set test (linear weather against linear PV) | Weather does not help in linear form; it makes the forecast worse |
| Model form | XGBoost beats the linear model on the same inputs, at both levels and on both series |
| Weather in tree form (supplementary, added after the scores) | Weather helps. Caveat: M6 cannot follow rising PV at all, so part of M5's gain is the weather inputs offsetting that handicap |

**Sensitivity**

- Rescaled series: factors from 1.171 (FY2015) to 1.000. Fifteen of 16 comparisons keep their
  direction; the exception is H1 on the monthly daytime low. It is a bounding case, not a better
  estimate. M3 and M4 collapse on it because they extend the steeper fall below every actual.
- The 2022 miss is not explained by the level steps: rescaling moves that year's daytime low only
  from 1,458 to 1,443 MW.
- The 15-lowest-days measure points the same way as the whole-day minimum for all four comparisons.
- Reporting threshold (90%, 95%, 98%): no annual daytime low moves.

**Answer to the research question, as it stands:** it depends on the model form. Weather adds
nothing in a linear model and adds skill in a tree model that can handle the PV and sunshine
interaction.

## 18 November 2026: daily out-of-sample test (notebook 08)

**Why it was run.** The first H1 test rested on seven annual numbers, each the single lowest day of
a year, so one odd year could swing it. Samhan wanted strongly backed findings, not low-evidence
ones. Each model already predicts every day of the target year, so all 2,414 valid days of 2019 to
2025 were scored, with the lowest 10% of days in each year (240 days) scored separately. Nothing was
refitted. Added after the first scores were seen, and recorded as such (D25).

Mean absolute error (MAE) on the daily daytime low, MW:

| Model | All days | Mean error, all days | Lowest 10% of days |
|---|---|---|---|
| M2 Time trend | 274 | -115 | 292 |
| M3 PV only | 260 | -13 | 212 |
| M4 PV + weather, linear | 227 | -19 | 169 |
| M5 PV + weather, XGBoost | 157 | +33 | 173 |
| M6 PV only, XGBoost | 262 | -10 | 340 |

| Pair | All days | Lowest 10% | Years the first model is better (all days / lowest 10%) |
|---|---|---|---|
| M3 against M2 (PV for time) | -5.0% | -27.6% | 4 of 7 / 7 of 7 |
| M4 against M3 (weather added, linear) | -12.8% | -20.1% | 7 of 7 / 6 of 7 |
| M5 against M6 (weather added, tree) | -40.0% | -49.0% | 7 of 7 / 7 of 7 |

**What it shows**

- H1 is supported where it matters. On the lowest tenth of days, the PV model misses by 28% less
  than the time-trend model, in every one of the seven test years. Over all days the gain is small
  (5%). The time trend also runs 115 MW too high on average (it lags the fall); the PV model is
  close to unbiased (13 MW).
- Weather explains the days: given the day's actual weather, error falls in both the linear and the
  tree form, in nearly every year.
- This does not contradict the annual POE scores; it is a different and larger body of evidence.
  The annual scores have seven points and depend on the simulated lowest day of a year.

**Cautions**

- M3 against M2 uses no weather, so it is a fair one-year-ahead test (PV capacity is still the
  actual value: perfect foresight).
- M4 and M5 are given the actual weather here, so their pairs measure how much weather explains,
  not how much it helps a year ahead.
- Mean error on the lowest days is negative partly by construction (the days are picked for a low
  actual); use it to compare models, not as a measure of bias.
- M6 cannot follow rising PV, so part of the M5 against M6 gap is that handicap.

**Where the evidence stands after this round**

| Statement | Evidence |
|---|---|
| PV capacity predicts the low days better than a time trend | Strong: 240 low days, 7 of 7 years, 28% lower error; and 96% against 88% of variation explained over the decade |
| Weather explains which days are low | Strong: 2,414 days, both model forms |
| A year ahead, a tree model with PV and weather gives the best POE forecasts | Moderate: seven annual and about 77 monthly points; holds on the rescaled series |
| A year ahead, weather inputs help a tree model and not a linear one | Moderate, with the M6 caveat; the linear failure is traced to the PV x solar term on the sunniest simulated days |

## 18 November 2026: analysis closed, paper reframed

- Repository tidied by Claude Code: `outputs/figures` and `outputs/tables` hold paper artifacts
  only, `outputs/checks` the 26 supporting checks, `outputs/archive` the superseded and exploratory
  results. `docs/results_summary.md` holds every number by type of evidence.
- Reproducible versions of two earlier quick calculations: the decade fit (`table_pv_fit.csv`:
  R-squared 0.958 on PV capacity against 0.879 on the year) and the M6 bias (`check_poe50_bias.csv`).

| Decision (Samhan) | Choice |
|---|---|
| Paper length | Four pages |
| Lead | The shift from the overnight low to the daytime low, then the forecasting comparison |
| Kept beyond the core set | Fig. 2 heat map, Table II annual minima, the monthly scores figure |
| Dropped | The load duration curve figure (repository `fig3`) |

The four points the paper makes, strongest first:

1. The minimum has shifted from the overnight low to the daytime low.
2. PV capacity tracks the daytime low over the decade and predicts the low days better than a time trend.
3. Weather explains which days are low.
4. One year ahead, the tree model with PV and weather forecasts best, and weather helps only in that form.

Paper numbering now differs from the repository names (paper Fig. 3 is `fig4`, Fig. 4 is `fig5`,
Fig. 5 is `fig6`; paper Table III is `table4.csv`, Table IV is `table3.csv`). The map is in
Appendix A14 of the prewriting plan. Paper plan v8, scope plan v6 and the skeleton
`PyNMDF_skeleton_20261118.docx` are kept outside this repository.

## 18 November 2026: figure and table set revised

**Why.** The first set showed the shift three times (Fig. 1, the heat map, the annual minima
table) and gave PV's role, the strongest new evidence, no figure. Two items carried no clear
message: the monthly scores figure and the temperature panel.

| Paper item | What it shows | Point it supports |
|---|---|---|
| Fig. 1 | Overnight and daytime lows (top) and PV capacity (bottom), 2015 to 2025 | 1: the shift |
| Fig. 2 | Annual daytime low against PV capacity, eleven years, fitted line, R-squared 0.96 | 2: PV drives it |
| Fig. 3 | Daily daytime low against solar exposure, 2015, 2020, 2025 | 2 and 3: the response to sunshine steepens |
| Fig. 4 | POE bands for four models on the annual daytime low | 4: one-year-ahead forecasts |
| Table I | The six models | Method |
| Table II | Daily out-of-sample test | 2 and 3 |
| Table III | POE scores on the daytime low | 4 |

- Fig. 1 uses two stacked panels, not two y-axes: both would be in MW on different scales, which
  invites comparing a bar's height with a line's value.
- Archived, with their code, in `outputs/archive`: the heat map, the load duration curve, the
  temperature panel, the monthly scores figure, and the earlier Fig. 1 with maximum demand and
  energy.
- Facts that moved from figures or tables into sentences keep a source file in `outputs/checks`:
  maximum and energy, the annual minima with date and day type, the daytime share of the lowest
  half hours, and the whole-day-minimum scores.
- Paper numbers now match the repository file names. First commit made locally (root commit
  amended to remove a local path); the new set is on branch `paper-set-v2`.
