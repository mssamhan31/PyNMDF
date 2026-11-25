# Plan: What the paper shows

## Outcome

The log entry of the old status page.

### 25 November 2026: what the paper shows

- Fig. 1 has three panels on one year axis (D39): the two annual lows, the heat map of the
  lowest half hours, which had been archived, and PV capacity. Fig. 3 has two panels on one
  y-axis: the daily daytime low against solar exposure and against maximum temperature. The
  set stays at four figures and three tables, with the same numbers.
- A five-figure set, with the heat map as a figure of its own, was drawn first and set aside
  the same day, before anything was committed.
- Table I loses "Fitted on" and "POE from". Table II has the shape of the paper's table: the
  mean absolute error of each model, and the change in per cent for three pairs named "Impact
  of ... (Mx against My)". The mean error and the number of days are kept as a new check,
  `daily_skill.csv` (D40).
- In the four figures a low is labelled "minimum demand". The text, the tables and the checks
  keep "low".
- Not a step of the plan, and not a change of method. In the package: `plots` has
  `annual_lows_hours_and_pv` and `daytime_low_against_solar_and_temperature` in place of the
  two functions that drew the old Fig. 1 and Fig. 3; `evaluate.daily_table` builds the new
  Table II, with its test. 12 tests pass.
- Notebooks 03, 04, 05, 06 and 08 were rerun and written back. Checked: no number changed.
  `fig1_hours.csv` is identical to the archived heat map data; `fig1_data.csv`,
  `fig2_data.csv` and `fig3_fits.csv` did not change; the numbers of Table II and of the
  pairs by year are those of before; every other table and check is byte-identical.
- Done on the branch `heatmap-and-temperature-figures`, merged into `main` and pushed.
- After that push (D41): Table I names the type of each model (naive, linear or XGBoost) in
  place of a model name, and the panels of Fig. 4 are titled by ID only. Notebooks 05 and 06
  were rerun; no number changed. Committed on the same branch on 26 November 2026 and merged
  into `main`.
