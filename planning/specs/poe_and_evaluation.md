# POE and evaluation

Back to the [spec index](../02_spec.md).

## Purpose

Turn each model into POE10, POE50 and POE90 forecasts one year ahead, and score them all under
one protocol.

**Code.** `src/pynmdf/poe.py` and `src/pynmdf/evaluate.py`.

## Process

### POE levels

POE is probability of exceedance. POE90 is the low side (a 90% chance of being exceeded) and
POE10 the high side, so POE10, POE50 and POE90 are the 0.90, 0.50 and 0.10 quantiles. An error
is always actual minus forecast.

### Two recipes

- **M1.** Last year's value plus a quantile of its own past year-on-year changes.
- **M2 to M6: the replay.** The target year is simulated many times. Each simulation takes the
  model's prediction for every day under one historical weather year and adds residuals borrowed
  from one left-out training year, each day drawing from the same calendar month. The spread of
  the simulated lows gives the POE levels. The same simulations give all three targets.

Residuals are out-of-fold: each training year is left out in turn, so a model is never judged
by errors on days it was fitted on.

### The backtest

- **Rolling origin.** Train to the end of 2018 and forecast 2019, then extend a year at a time
  to 2025: seven test years.
- `evaluate.rolling_origin` is the only place that makes forecasts, so nothing after an origin
  can reach a forecast made from it.
- One exception, by design: the PV capacity of the target year is taken as known.

### Scores

- **Pinball loss** in MW at each POE level, and their mean. Lower is better.
- **Coverage:** the share of actuals between POE90 and POE10. A calibrated band holds about 80%.
- **Four comparisons** on mean pinball loss:

| Comparison | Set |
|---|---|
| H1: M3 against M2 (PV against time) | Before the results |
| H2: M4 against M3 (weather on top of PV, linear) | Before the results |
| Model form: M5 against M4 | Before the results |
| Supplementary: M5 against M6 (weather in tree form) | After the scores were seen |

- **The daily out-of-sample test** scores each model day by day, given that day's own weather.
  For M4 and M5 it shows how much weather explains, not how much it helps a year ahead.

## Constraints

- Reruns are exact: each draw is seeded from the config seed, the model's position in `SPECS`
  and the origin.
- Error pools, residuals and replay weather years are rebuilt at each origin from data up to
  that origin only.
- The annual scores rest on seven test years. Any statement built on them says so.

**Decision record.** `publication/01_conference/analysis_plan.md`: D7, D9, D11, D12, D23 and
D25; section 6.
