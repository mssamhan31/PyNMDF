# Spec: data sources

Back to the [spec](../02_spec.md).

## Purpose

Read each public source into one standard shape. Nothing else in the package knows how a
source's files are laid out.

## The three sources

| Source | Module | Reads | Returns |
|---|---|---|---|
| Demand | `io_demand.py` | Ausgrid distribution zone substation data: one archive per reporting year (1 May to 30 April), one CSV per substation, one row per day, 96 columns of 15-minute MW | `read_reporting_year`: one wide frame per reporting year, 15-minute MW, one row per interval start, one column per substation |
| PV capacity | `io_pv.py` | Ausgrid "average electricity use" workbooks by local government area: network solar capacity (kWp) at 30 June of each year | `pv_capacity_series`: capacity at each 30 June. `daily_pv`: daily capacity in MW, interpolated between those dates |
| Weather | `io_weather.py` | Bureau of Meteorology Climate Data Online, station 066037 (Sydney Airport AMO): daily maximum temperature, minimum temperature and global solar exposure | `read_weather`, `fill_weather`: daily `tmax`, `tmin`, `tmean` (degrees C) and `solar` (MJ/m2), gaps of up to 3 days filled |

## Rules

- **Time.** Local clock time, as published. Series are indexed by interval start; tables report
  the time an interval ends, to match Ausgrid's column labels.
- **Layouts drift.** The demand reader absorbs every file layout found in FY2015 to FY2026. The
  PV reader finds its value by header text and row label, never by position.
- **Checked on read.** The PV series must match the table of expected values in the config.
  The one year published as PDF only (FY2024) is entered in the config with its source.
- **Public only.** Every source is a public file from a public website. No private or
  confidential data is read.
- **Paths.** The files are downloaded from their sources and read from the paths in
  `config.local.yaml`.

## Where a new source plugs in

The rest of the package needs three series and nothing else from a source:

1. a half-hourly demand total in MW, indexed by interval start in local time, blank where too
   little data reports;
2. daily PV capacity in MW;
3. daily weather with `tmax`, `tmin` and `solar`.

Another network, for example German data, needs its own reader modules that return these
shapes and its own entries in the config. Two parts of the package are specific to the current
sources and would need a counterpart: `clean.py` repairs faults of the Ausgrid files, and the
public holiday calendar is Australian (`targets.public_holidays`).

Nothing has been built for a second source. This section records where it would go.

## Decision record

`publication/01_conference/analysis_plan.md`, sections 2 and 5.
