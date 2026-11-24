# Plan: mean temperature as a V in M4

Step 4 of the [plan](../03_planning.md). The model it leads to is described in
[spec/models.md](../spec/models.md).

## Why

The supervisor's comment: the scatter of minimum demand against temperature is a V, so a linear
model that uses weather should be piecewise linear, not one straight line.

The first training window (2015 to 2018) bears this out. With the calendar and PV already in the
model, the error left on the daytime low is +121 MW at a mean temperature of 9 to 12 degrees C,
-94 MW at 18 to 21 and +242 MW at 27 to 30.

## What changes

| Item | From | To |
|---|---|---|
| M4's temperature terms | `tmax` and `tmin`, one straight slope each | `below_knot` and `above_knot`: degrees of mean temperature below and above the knot |
| M5's temperature columns | `tmax` and `tmin` | `tmean` |
| Config | | `models.temperature_knot_c: 19` |
| M1, M2, M3, M6 | | Unchanged |
| M4's label in Table I | "PV + weather, linear" | Unchanged |

M4 stays one linear model with the same number of terms: two columns replace two.

## The knot

19 degrees C: the whole-degree value with the lowest error on the daytime low over 2015 to
2018. No test year takes part.

| Knot (degrees C) | 17 | 18 | 19 | 20 | 21 |
|---|---|---|---|---|---|
| Daytime low, RMSE (MW) | 142.0 | 140.5 | 140.2 | 141.0 | 143.4 |
| Overnight low, RMSE (MW) | 79.7 | 78.5 | 77.8 | 77.6 | 78.2 |

For comparison, the straight terms give 175.1 MW on the daytime low and 90.9 MW on the
overnight low over the same days. These are in-sample fits, not forecast scores.

These numbers come from a look made outside the repository. This step makes them reproducible:
a short section in notebook 05 writes them to `results/checks/check_temperature_knot.csv`.

## Work

1. **Config.** Add the knot, with a comment on how it was chosen.
2. **`models.py`.** `add_weather` takes the knot and adds `tmean`, `below_knot` and
   `above_knot`. The column lists of M4, M5 and the variant "M4 without PV x solar" change.
   `tmax` and `tmin` stay among the predictors, unused, so the set of usable days is unchanged.
3. **`poe.py`, `evaluate.py`.** The knot is passed to the two places that build weather columns.
   The table of M4's coefficients reports the two new slopes in place of the two old ones.
4. **Test.** The two columns on a few hand-worked days: below, at and above the knot.
5. **Rerun** notebooks 05 to 08. Notebooks 01 to 04 do not depend on the models.
6. **Check.** Every number of M1, M2, M3 and M6 is identical to the archive. Only M4, M5 and the
   comparisons that involve them move.
7. **Documents.** Record D37 in `analysis_plan.md`. Update `results_summary.md`, the model
   descriptions in the READMEs and in notebook 05, and remove the "not yet true" notes from the
   spec.

## What will change in the results

Every number of M4 and of M5: their rows in Table II and Table III, their panels in Fig. 4,
three of the four comparisons (H2, model form, and M5 against M6), and the checks on M4's terms.

Which way they move is not known. Nothing has been run on the test years, so that no choice
here was made by looking at a score. A before-and-after table is shown to the author before the
commit.

One expectation, to be tested: the daily test (Table II) should improve for M4, but its
one-year-ahead scores may move little, because the earlier diagnosis traced M4's miss to the
PV x solar term and not to temperature.

## The decision record

D37 will state: the change, that it was made after the scores of all six models were seen, on
the supervisor's advice; that the knot was chosen on 2015 to 2018 only; and that the earlier
results are kept in `archive/v1_straight_line_m4`.

## Not in this step

- No second model, no second knot, no knot fitted again at each origin.
- No change to M6, to XGBoost's settings or to any target or score.
- No new figure. The old straight-line M4 is not kept as a live variant; the archive holds it.
