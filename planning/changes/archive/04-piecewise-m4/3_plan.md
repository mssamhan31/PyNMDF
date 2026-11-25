# Plan: Temperature as a V in M4

## Tasks

What was done:

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

## Outcome

### What it did to the results

Only M4 and the comparisons that involve it moved.

| Measure (MW) | Before | After |
|---|---|---|
| Daily test, MAE over all days | 227.1 | 186.1 |
| Daily test, MAE over the lowest 10% of days | 169.2 | 152.6 |
| One year ahead, pinball loss, annual daytime low | 63.5 | 67.5 |
| One year ahead, pinball loss, monthly daytime low | 51.8 | 46.2 |

H2 (M4 against M3) on the monthly daytime low changed sign, from +4.5% to -6.9%. On both annual
targets M4 still scores worse than M3.

### 24 November 2026: M4 revised

The log entry of the old status page.

- M4 now takes maximum and minimum temperature each as a V, with knots of 21 and 18 degrees
  C chosen on 2015 to 2018 only (D37). M5 is as it was first built.
- A first form, with one V on mean temperature in M4 and mean temperature in M5, was run and
  set aside after its scores were seen (D38). The form is now settled.
- New: the knot check (`check_temperature_knot.csv`) and two tests. 12 tests pass.
- Notebooks 05 to 08 were rerun and written back. In all five score tables only M4's rows
  moved; M1, M2, M3, M5 and M6 are identical to the archive.
- Effect on M4: better in the daily test (MAE 227.1 to 186.1 MW over all days); one year
  ahead, slightly worse on the annual daytime low (63.5 to 67.5 MW) and better on the monthly
  (51.8 to 46.2 MW). H2 on the monthly daytime low changed sign.
- The results summary, the READMEs, notebook 05 and the spec describe the revised M4.
