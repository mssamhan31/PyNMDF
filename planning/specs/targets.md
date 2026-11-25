# Targets

Back to the [spec index](../02_spec.md).

## Purpose

Turn the half-hourly network total into what is forecast and scored, and into the daily lows
the models are fitted on.

**Code.** `src/pynmdf/targets.py`.

## Outputs

### The three scored targets

Each exists for every calendar year and every month.

| Target | Definition | Role |
|---|---|---|
| `minimum` | The lowest kept half hour of the whole day | The headline forecast |
| `daytime_low` | The lowest kept half hour starting between 09:00 and 17:00 | The target the two hypotheses are judged on |
| `robust` | The mean of the 15 lowest daily minima of a year (the 2 lowest of a month), over complete days | A check that one extreme half hour does not drive a result |

### The daily lows

The daily models are fitted on two numbers per day: the overnight low (00:00 to 06:00) and the
daytime low (09:00 to 17:00). The day's minimum is the lower of the two.

## Constraints

- A monthly value counts only when at least 90% of the month's half hours are kept.
- A day enters the daily models only when both of its windows are complete.
- The windows and the thresholds are parameters under `targets` in the config.
- That the hypotheses are judged on the daytime low was fixed before any model was run.

**Decision record.** `publication/01_conference/analysis_plan.md`: D4, D13, D14 and D18.
