# Spec: models

Back to the [spec](../02_spec.md).

> **Not yet true.** M4 and M5 are described as they will be after step 4 of the
> [plan](../03_planning.md). Today both use maximum and minimum temperature as two straight
> terms. See [plan/02_piecewise_m4.md](../plan/02_piecewise_m4.md).

## Purpose

Six models that differ only in what they are given, so that a difference in score can be
credited to one thing.

## Code

`src/pynmdf/models.py`. M1 needs no fit and lives in `poe.naive_forecasts`.

## The models

| ID | Form | Given |
|---|---|---|
| M1 Naive | No fit | Last year's value |
| M2 Time trend | Linear regression | Month, non-working day, time with a slope per month |
| M3 PV only | Linear regression | As M2, with PV capacity in place of time |
| M4 PV + weather, linear | Linear regression | As M3, plus PV x solar exposure and mean temperature as a V |
| M5 PV + weather, XGBoost | XGBoost | Month, non-working day, PV, PV x solar exposure, mean temperature |
| M6 PV only, XGBoost | XGBoost | Month, non-working day, PV |

M2 to M5 are a ladder: each step changes one thing. M6 is M3's information in a tree model.

## How they are fitted

- Each model is fitted twice, once on the overnight low and once on the daytime low. The lower
  prediction is the day's minimum.
- A linear model has twelve month intercepts, twelve month slopes on its trend (time or PV),
  one non-working-day flag and its weather columns. There is no separate intercept.
- A non-working day is a Saturday, a Sunday or a public holiday: one flag, not two.
- XGBoost runs with fixed settings from the config. Nothing is tuned.

## Mean temperature as a V in M4

Demand rises on both cold and hot days, so one straight slope on temperature is the wrong
shape. M4 uses two columns in its place, built from the day's mean temperature and one knot:

- `below_knot`: degrees below the knot, zero on a warmer day;
- `above_knot`: degrees above the knot, zero on a cooler day.

Each gets its own slope. The result is two straight lines that meet at the knot, which is
piecewise linear regression with one breakpoint. M4 stays one linear model.

The knot is `models.temperature_knot_c` in the config: 19 degrees C, the whole-degree value
with the lowest error on the daytime low over 2015 to 2018, the first training window. No test
year takes part in the choice. M5 is given raw mean temperature, since a tree needs no knot.

## Rules

- **The model list is data.** `SPECS` maps each model to its estimator and its columns.
- **Entries are only added at the end of `SPECS`.** A model's position seeds its random draws.
- **Diagnostic variants** (`M4_VARIANTS`) switch off one group of M4's weather terms. They are
  never scored with the six models.
- **What was set when.** M3 against M2 and M4 against M3 were set before any model was run. M6
  was added after the scores of M1 to M5 were seen. The form of temperature in M4 and M5 was
  revised after the first scores, on the supervisor's advice.

## Adding a model

1. Add one entry at the end of `SPECS`, and a row to `MODEL_INFO` if it is one of the study's
   models.
2. Add or extend a test.
3. Record the decision, with whether it came before or after the results were seen.

## Decision record

`publication/01_conference/analysis_plan.md`: D9, D19, D20, D23 and D37.
