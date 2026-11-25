# Intent: PyNMDF

Why this repository exists. The [spec](02_spec.md) says what the repository holds, the
[status](00_status.md) says where it stands today, and [changes/](changes/) holds the record of
each change made to it.

## Problem

Minimum demand is falling as rooftop PV capacity rises, and it has moved from the early morning
to the middle of the day. The research asks which inputs and model forms forecast it well a year
ahead, and reports the answer as probability of exceedance (POE) levels.

## Goal

PyNMDF is Python for Network Minimum Demand Forecasting: the reproducible analysis code behind a
line of PhD research on forecasting minimum demand in distribution networks as rooftop PV grows.

## Stakeholders

- A reader of a paper who wants to see how a number was produced, or to reproduce it.
- The author, when adding a publication, a data source or a method.

## Publications

| Folder | Paper | Question | State |
|---|---|---|---|
| `publication/01_conference` | Four-page conference paper | Once rooftop PV capacity is in the model, does weather improve one-year-ahead probabilistic forecasts of annual minimum demand? | Analysis complete; M4 revised on 24 November 2026 |

## Out of scope

Possible later, none committed to. Each is an entry under Later on the [status](00_status.md)
page.

- A website for the repository.
- An installable library with a public interface.
- A journal paper (`publication/02_journal`).
- Another network's data, for example German data.
- More methods and experiments.

## Constraints

What must stay true:

1. **Reproducible from public data.** Every published number can be rebuilt from public files by
   running the notebooks, and reruns give the same numbers.
2. **No private or confidential data.** Every input is a public file from a public source.
   Nothing private or confidential, such as customer data or internal network data, enters the
   repository.
3. **Decisions are on record.** Each decision has an ID, a date and its evidence, and is marked
   as set before the results were seen or added after.
4. **The least that meets the need.** Code is added when a publication needs it, not before.
