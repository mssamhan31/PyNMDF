# Substation set: insights and why the decisions stand

Written 18 November 2026 from a discussion between Samhan and Claude (chat). It explains two
decisions already recorded in `analysis_plan.md` and does not change them. Exact per-file counts
are in the data-quality table produced by notebook 01; the counts below are from the data stress
test of 11 November 2026, which counted missing data only.

## The two decisions

| Decision | In one line |
|---|---|
| Sum all substations that pass the cleaning rule in each reporting year; no fixed set | Load moves between substations, and a fixed set turns those moves into false changes in demand |
| Drop a substation with more than 20% of its data missing or invalid in that year | The alternative is to invent months of values; dropping costs at most 2.4% of load and invents nothing |

## What the numbers look like

| Reporting year | Files published | Kept (stress test) | Removed |
|---|---|---|---|
| FY2015 | 176 | 166 | 10 |
| FY2016 | 176 | 168 | 8 |
| FY2017 | 220 | 178 | 42 |
| FY2018 | 223 | 181 | 42 |
| FY2019 | 223 | 176 | 47 |
| FY2020 | 223 | 177 | 46 |
| FY2021 | 199 | 176 | 23 |
| FY2022 | 178 | 172 | 6 |
| FY2023 | 194 | 178 | 16 |
| FY2024 | 176 | 174 | 2 |
| FY2025 | 175 | 174 | 1 |
| FY2026 | 175 | 175 | 0 |

With the full cleaning rules (flagged values also count as invalid), 163 to 179 remain per year.

## Layer 1: what Ausgrid publishes (not our choice)

- The file count runs from 175 to 223, but the published set is steadier than that suggests.
- FY2017 to FY2020 include 36 to 42 empty placeholder files a year. Without them, about 175 to 185
  real substations are published every year.
- About 200 distinct substation names appear across the period and 154 are present in every file
  checked (FY2023 not counted), so roughly 45 come or go over twelve years: built, retired or
  renamed. Example: Engadine 33 kV became Engadine 132 kV.

## Layer 2: what the cleaning removes (our choice)

- Rule: drop a substation with more than 20% of its intervals missing or invalid in that file.
  Invalid includes a value stuck for 24 hours or more and a day reading many times too high.
- In FY2017 to FY2020 nearly all removals are the empty placeholders, which hold no data.
- Real substations removed for poor data: mostly under ten a year, more in FY2021 and FY2023,
  almost none from FY2024.
- Load lost: 0% to 2.4% of network load, depending on the file. A dropped substation is not
  scaled up.
- Not a removal: a kept substation that is blank for a few hours stays in, and the scale-up rule
  covers the gap.
- Precedent: Haghdadi, Bruce, MacGill and Passey (2018) used the same 20% threshold and kept 138
  of 176 substations.

## Why not a fixed set of substations

Illustration (invented numbers): a new substation B opens in 2019 and takes 30 MW of customers
from its neighbour A.

| Year | A | B | Sum of all | Fixed set (A only, because B is not in every year) |
|---|---|---|---|---|
| 2018 | 80 MW | not built | 80 MW | 80 MW |
| 2019 | 50 MW | 30 MW | 80 MW | 50 MW |

- Real demand did not change. Summing everything shows that; the fixed set shows a 30 MW fall
  that never happened, and nothing in the data flags it.
- A fixed set swaps steps at known dates (1 May, measurable) for hidden steps scattered through
  the series that look like real demand changes. For a study of how the minimum falls, the hidden
  kind is worse.
- A fixed set also shrinks: any substation with one bad year drops out for all twelve (City
  Central reads zero for eight months in FY2021), leaving well under 154.
- It would not fix F1 (below), and it would mean rebuilding notebook 01.

## Link to F1 (level steps where reporting years join)

- The steps at the 1 May joins have two causes: (1) different substations in the sum on each side,
  and (2) the same substation reading differently in the new file on the same night.
- Cause 1 explains roughly a third to a half. Cause 2 is the rest: at the 2022 join, 84% of
  substations above 5 MW step up on the same night. That is in the published values.
- A fixed set removes only cause 1, so it would leave the larger part.
- Size, for scale: the steps over the 2015 to 2018 joins add up to about +12%, against a rise of
  about 9% in the annual minimum over the same years. The early rise may be an artefact.
- All five models are scored against the same target, so they carry the same steps. The model
  comparisons (M3 against M2, M4 against M3) are less exposed than the absolute numbers.

## What was decided on 18 November 2026

- Keep both decisions above. F1 stays uncorrected in the main series and is stated as a data
  limitation.
- Proposed check for notebook 07 (to be sent to Claude Code): a second network total with each
  reporting-year file rescaled so the 1 May joins meet, then Table III and the annual minima
  under both series, side by side. If the model rankings hold, the limitation is stated with
  evidence; if they change, that is known before writing.
