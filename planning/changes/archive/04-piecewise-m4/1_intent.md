# Change 04: Temperature as a V in M4

Status: Done, 24 November 2026

Step 4 of the [first plan](../02-planning-documents/3_plan.md). The model it led to is described
in [specs/models.md](../../../specs/models.md); the decision record is D37 and D38 in
`publication/01_conference/analysis_plan.md`. Assembled on 26 November 2026 from the old
planning pages; see [change 07](../07-planning-template/1_intent.md).

## Why

The supervisor's comment: the scatter of minimum demand against temperature is a V, so a linear
model that uses weather should be piecewise linear, not one straight line.

## Out of scope

Not in this step:

- No second model, and no knot fitted again at each origin.
- No change to M5, M6, XGBoost's settings, or any target or score.
- No new figure. The first M4 is not kept as a live variant; the archive holds it.

## Decisions

- **The knots.** The whole-degree pair with the lowest error on the daytime low when M4 is
  fitted on 2015 to 2018. No test year takes part. Notebook 05 (section 3) refits M4 with 81
  pairs and writes the errors to `results/checks/check_temperature_knot.csv`: the lowest is
  129.2 MW at 21 and 18 degrees C, and 7 pairs lie within 1 MW of it.
- **The form that was set aside.** A first form was built and run before this one: one V on
  mean temperature in M4, and mean temperature in place of the two temperatures in M5. It was
  set aside because it changed M5, which the supervisor's comment did not concern, and withheld
  from it information it first had. Its scores are in D38. The form of temperature is not
  changed again in the light of a score.
