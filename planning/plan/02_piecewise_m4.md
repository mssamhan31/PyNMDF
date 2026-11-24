# Plan: temperature as a V in M4

Step 4 of the [plan](../03_planning.md). Done on 24 November 2026. The model it led to is
described in [spec/models.md](../spec/models.md); the decision record is D37 and D38 in
`publication/01_conference/analysis_plan.md`.

## Why

The supervisor's comment: the scatter of minimum demand against temperature is a V, so a linear
model that uses weather should be piecewise linear, not one straight line.

## What changed

| Item | From | To |
|---|---|---|
| M4's temperature terms | `tmax` and `tmin`, one straight slope each | For each temperature, the degrees below a knot and the degrees above it: `tmax_below`, `tmax_above`, `tmin_below`, `tmin_above` |
| Config | | `models.temperature_knots_c`: 21 for `tmax`, 18 for `tmin` |
| M1, M2, M3, M5, M6 | | Unchanged; their numbers are identical to the archive |
| M4's label in Table I | "PV + weather, linear" | Unchanged |

M4 stays one linear model, with four temperature terms in place of two.

## The knots

The whole-degree pair with the lowest error on the daytime low when M4 is fitted on 2015 to
2018. No test year takes part. Notebook 05 (section 3) refits M4 with 81 pairs and writes the
errors to `results/checks/check_temperature_knot.csv`: the lowest is 129.2 MW at 21 and 18
degrees C, and 7 pairs lie within 1 MW of it.

## What was done

1. **Config.** The two knots, and the candidates for the knot check.
2. **`models.py`.** `add_weather` takes the knots and adds the four columns. M4's column list and
   that of the variant "M4 without PV x solar" follow.
3. **`poe.py`, `evaluate.py`.** The knots are passed to the two places that build weather
   columns. The table of M4's coefficients reports the four new slopes. A new function,
   `temperature_knot_fit`, is the knot check.
4. **Tests.** Two new tests: the four columns on hand-worked days, with M4 recovering a different
   slope on every arm; and the knot check finding the knots of two planted Vs. 12 tests pass.
5. **Rerun** of notebooks 05 to 08, written back in place.
6. **Check.** In all five score tables, only M4's rows moved.
7. **Documents.** D37 and D38, the results summary, the READMEs, notebook 05 and the spec.

## What it did to the results

Only M4 and the comparisons that involve it moved.

| Measure (MW) | Before | After |
|---|---|---|
| Daily test, MAE over all days | 227.1 | 186.1 |
| Daily test, MAE over the lowest 10% of days | 169.2 | 152.6 |
| One year ahead, pinball loss, annual daytime low | 63.5 | 67.5 |
| One year ahead, pinball loss, monthly daytime low | 51.8 | 46.2 |

H2 (M4 against M3) on the monthly daytime low changed sign, from +4.5% to -6.9%. On both annual
targets M4 still scores worse than M3.

## The form that was set aside

A first form was built and run before this one: one V on mean temperature in M4, and mean
temperature in place of the two temperatures in M5. It was set aside because it changed M5,
which the supervisor's comment did not concern, and withheld from it information it first had.
Its scores are in D38. The form of temperature is not changed again in the light of a score.

## Not in this step

- No second model, and no knot fitted again at each origin.
- No change to M5, M6, XGBoost's settings, or any target or score.
- No new figure. The first M4 is not kept as a live variant; the archive holds it.
