# Network total against public Ausgrid figures: a rough cross-check

Written 18 November 2026 from a discussion between Samhan and Claude (chat). A sanity check only;
no result depends on it.

## What "network total" means in this project

The sum of the public zone substation files, after cleaning. It is not the whole Ausgrid network.
It leaves out:

- customers supplied above zone-substation level (for example at subtransmission voltage),
- substations Ausgrid does not publish,
- substations dropped by the 20% rule (0% to 2.4% of load, by file; see `substation_set_decisions.md`).

So it should sit below Ausgrid's network-wide figures, and it does.

## Comparison

| Quantity | This project (zone substation sum) | Public Ausgrid figure | Ratio |
|---|---|---|---|
| Annual energy | 19,872 GWh in calendar 2025; 19,287 to 22,386 GWh over 2015 to 2025 | 24,931 GWh, Ausgrid's forecast of total energy for 2024/25 (a forecast, not an actual) | about 80% |
| Maximum demand | 4,226 to 5,269 MW over 2015 to 2025 | 5,570 MW in 2012-13 (whole network; a different year) | about 75% to 95% |

Both ratios are consistent with a total that covers most of the network but not all of it. The
years and definitions do not match exactly, so this supports the order of magnitude and nothing
finer.

## What the series shows, 2015 to 2025 (`outputs/checks/check_annual_summary.csv`)

- Maximum demand: no trend. It moves between 4,226 and 5,269 MW with the weather; -0.6% end to end.
- Annual energy: a gentle decline, -7.3% end to end, after a peak in 2017.
- Minimum demand: -35.7%.
- Caution: part of the 2015 to 2017 rise in energy and in the minimum coincides with the level
  steps at the 1 May joins (F1 in `analysis_plan.md`).

## Wording for the paper

Call it the "sum of published zone substations" or "aggregated zone substation load", not
"Ausgrid's network demand", and state that it is a subset of the network.

## Sources

- AER, Ausgrid electricity distribution network (maximum demand 2012-13):
  https://www.aer.gov.au/industry/networks/entities/assets/ausgrid-electricity-distribution-network
- Ausgrid, 2024-29 Revised Proposal, Attachment 8.9, Demand, consumption and customer number
  forecasts, 30 November 2023 (total energy forecast for 2024/25):
  https://aer.gov.au/system/files/2023-12/Ausgrid%20-%20Revised%20proposal%20-%20Att.%208.9%20-%20Demand%2C%20consumption%20and%20customer%20number%20forecasts%20-%2030%20Nov%2023%20-%20Public.pdf
