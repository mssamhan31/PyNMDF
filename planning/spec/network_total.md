# Spec: network total

Back to the [spec](../02_spec.md).

## Purpose

Clean the zone substation files and sum them into one half-hourly series: the "network total".
It is the sum of the published zone substations, not the whole Ausgrid network.

## Code

`src/pynmdf/clean.py`. One small function per step, composed by `clean_reporting_year` and
`build_network_total`.

## Steps

Applied to each reporting-year file on its own, in this order:

| Step | Rule |
|---|---|
| 0 | Days published with their 96 values out of time order are put back in order (April 2023) |
| 1 | Blocks published in kW are divided by 1,000 |
| 2 | Outlier days and values stuck for 24 hours or more are blanked |
| 3 | A substation with more than 20% of its intervals blank or invalid is dropped |
| 4 | Gaps of up to 2 hours are filled linearly |
| 5 | Network total = sum of the reporting substations divided by their usual share of load |
| 6 | An interval is dropped when less than 95% of usual load reports |
| 7 | Pairs of 15-minute totals are averaged to half hours; both must be valid |
| 8 | The files are joined and cut to the study window (calendar 2015 to 2025) |

The approach follows Haghdadi et al. (2018), <https://doi.org/10.1109/TSTE.2017.2751647>.

## Outputs

- The 15-minute total with its reporting share, and the half-hourly total (both cached).
- One row per file of the data-quality table.
- Three measures of faults in the published files that are **not corrected**: the level step
  where reporting years join at 1 May, substations that appear to stay on standard time from
  FY2024, and reverse flow recorded without its sign before May 2023.
- A rescaled series in which the 1 May steps are closed. It is a bounding case, not a
  correction, and is used only for a sensitivity check.

## Rules

- Every threshold is a parameter under `cleaning` in the config.
- Nothing is invented: a dropped substation is not replaced, and long gaps stay blank.

## Decision record

`publication/01_conference/analysis_plan.md`: decisions D1 to D5 and D10, findings F1 and F2.
`publication/01_conference/notes/substation_set_decisions.md` explains why the set of
substations is not fixed.
