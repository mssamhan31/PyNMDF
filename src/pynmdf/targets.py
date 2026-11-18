"""Targets and summaries derived from the 30-minute network total.

Throughout, ``total`` is the 30-minute network total in MW, indexed by interval start in local
clock time and blank where the cleaning rule found too little data. Times reported here are
interval END times, to match Ausgrid's column labels.
"""

import holidays
import numpy as np
import pandas as pd

HALF_HOUR = pd.Timedelta(minutes=30)
HALF_HOURS_PER_DAY = 48


# --------------------------------------------------------------------------------------------
# Years and months
# --------------------------------------------------------------------------------------------


def annual_summary(total: pd.Series) -> pd.DataFrame:
    """Summarise each calendar year of the network total.

    Returns:
        One row per year: minimum and maximum (MW) with the time each interval ended, the share
        of half hours kept, and energy (GWh). Energy allows for gaps: mean valid MW times the
        hours in the year.
    """
    by_year = total.groupby(total.index.year)
    hours_in_year = by_year.size() / 2
    return pd.DataFrame(
        {
            "min_mw": by_year.min(),
            "min_time": by_year.idxmin() + HALF_HOUR,
            "max_mw": by_year.max(),
            "max_time": by_year.idxmax() + HALF_HOUR,
            "kept_share": by_year.count() / by_year.size(),
            "energy_gwh": by_year.mean() * hours_in_year / 1000,
        }
    ).rename_axis("year")


def kept_share_by_month(total: pd.Series) -> pd.DataFrame:
    """Return the share of half hours kept, as a table of years (rows) by months (columns)."""
    kept = total.notna().groupby([total.index.year, total.index.month]).mean()
    return kept.unstack().rename_axis(index="year", columns="month")


def public_holidays(dates: pd.DatetimeIndex, subdivision: str) -> pd.Series:
    """Return the public holiday falling on each date, or an empty string.

    Args:
        dates: The dates to look up.
        subdivision: Australian state or territory code, for example "NSW".
    """
    calendar = holidays.Australia(subdiv=subdivision, years=sorted(set(dates.year)))
    return pd.Series([calendar.get(day, "") for day in dates], index=dates, name="public_holiday")


def in_window(total: pd.Series, window: list[int]) -> pd.Series:
    """Return the half hours that start inside ``[start hour, end hour)``."""
    start, end = window
    hour = total.index.hour
    return total[(hour >= start) & (hour < end)]


def annual_window_lows(total: pd.Series, windows: dict) -> pd.DataFrame:
    """Return each calendar year's lowest kept half hour inside each trough window.

    Args:
        total: The 30-minute network total.
        windows: Window name to ``[start hour, end hour)`` of the interval start.

    Returns:
        One row per year and one column per window, named ``<window>_low_mw``.
    """
    lows = {}
    for name, window in windows.items():
        inside = in_window(total, window)
        lows[f"{name}_low_mw"] = inside.groupby(inside.index.year).min()
    return pd.DataFrame(lows).rename_axis("year")


def annual_minimum_table(
    total: pd.Series, weather: pd.DataFrame, subdivision: str, windows: dict
) -> pd.DataFrame:
    """Describe each year's minimum: when it fell and what the day was like (Table II).

    Args:
        total: The 30-minute network total.
        weather: Daily weather with ``solar`` (MJ/m2) and ``tmax`` (degrees C), indexed by date.
        subdivision: State code for the public holiday calendar.
        windows: The trough windows, for the year's overnight and daytime lows.

    Returns:
        One row per year: the minimum (MW), its date, the time its half hour ended, the day of
        the week, the public holiday if any, that day's solar exposure and maximum temperature,
        and the year's lowest half hour inside each trough window (MW).
    """
    summary = annual_summary(total)
    day = pd.DatetimeIndex((summary["min_time"] - HALF_HOUR).dt.normalize())
    table = pd.DataFrame(
        {
            "min_mw": summary["min_mw"].to_numpy(),
            "date": day.strftime("%Y-%m-%d"),
            "time": summary["min_time"].dt.strftime("%H:%M").to_numpy(),
            "day": day.day_name().str[:3],
            "public_holiday": public_holidays(day, subdivision).to_numpy(),
            "solar_mj_m2": weather["solar"].reindex(day).to_numpy(),
            "tmax_c": weather["tmax"].reindex(day).to_numpy(),
        },
        index=summary.index,
    )
    return table.join(annual_window_lows(total, windows))


def period_targets(
    total: pd.Series, windows: dict, month_min_kept: float, robust_days: dict
) -> pd.DataFrame:
    """Return the annual and monthly actuals of the three scored targets.

    - ``minimum``: the lowest kept half hour of the period.
    - ``daytime_low``: the lowest kept half hour inside the daytime window.
    - ``robust``: the mean of the lowest daily minima of the period (15 in a year, 2 in a
      month), taken over complete days only.

    A year always counts. A month counts only when enough of it is kept: at least
    ``month_min_kept`` of the month's half hours, or of its daytime-window half hours for the
    daytime low. The robust target also needs as many complete days as it averages.

    Args:
        total: The 30-minute network total.
        windows: The trough windows; only ``daytime`` is used here.
        month_min_kept: Smallest kept share at which a monthly value counts.
        robust_days: Days averaged by the robust target, for ``annual`` and for ``monthly``.

    Returns:
        One row per target, level (``annual`` or ``monthly``), year and month (0 for a year):
        ``actual``, ``valid``, ``kept_share`` and ``complete_days``.
    """
    series = {
        "minimum": total,
        "daytime_low": in_window(total, windows["daytime"]),
        "robust": daily_minimum(total).dropna(),
    }
    frames = []
    for level in ("annual", "monthly"):

        def by_period(values: pd.Series, monthly: bool = level == "monthly"):
            keys = [values.index.year, values.index.month] if monthly else [values.index.year]
            return values.groupby(keys)

        days = robust_days[level]
        actual = {
            "minimum": by_period(series["minimum"]).min(),
            "daytime_low": by_period(series["daytime_low"]).min(),
            "robust": by_period(series["robust"]).apply(lambda low: low.nsmallest(days).mean()),
        }
        complete_days = by_period(series["robust"]).size()
        for target in actual:
            # The robust target is built from whole days, so its coverage is the whole period's.
            coverage = by_period(series["minimum" if target == "robust" else target])
            frame = pd.DataFrame({"actual": actual[target]}).reindex(actual["minimum"].index)
            frame["kept_share"] = coverage.count() / coverage.size()
            frame["complete_days"] = complete_days.reindex(frame.index, fill_value=0)
            enough = frame["kept_share"] >= (month_min_kept if level == "monthly" else 0)
            if target == "robust":
                enough &= frame["complete_days"] >= days
            frame["valid"] = frame["actual"].notna() & enough
            frame = frame.reset_index(names=["year", "month"][: frame.index.nlevels])
            frames.append(frame.assign(target=target, level=level))
    columns = ["target", "level", "year", "month", "actual", "valid", "kept_share", "complete_days"]
    return pd.concat(frames, ignore_index=True).fillna({"month": 0}).astype({"month": int})[columns]


# --------------------------------------------------------------------------------------------
# Days
# --------------------------------------------------------------------------------------------


def daily_minimum(total: pd.Series) -> pd.Series:
    """Return each day's lowest half hour, blank unless all 48 half hours of the day are kept."""
    by_day = total.groupby(total.index.normalize())
    lowest = by_day.min().where(by_day.count() == HALF_HOURS_PER_DAY)
    return lowest.rename("min_mw").rename_axis("date")


def daily_troughs(total: pd.Series, windows: dict) -> pd.DataFrame:
    """Return each day's minimum inside each trough window.

    The minimum sits overnight in the early years and at midday in the later ones, so the daily
    models fit the two troughs separately and take the lower.

    Args:
        total: The 30-minute network total.
        windows: Window name to ``[start hour, end hour)`` of the interval start.

    Returns:
        One row per date and one column per window. A day is blank in every column unless every
        half hour of every window is kept.
    """
    troughs = {}
    for name, (start, end) in windows.items():
        inside = in_window(total, [start, end])
        by_day = inside.groupby(inside.index.normalize())
        troughs[name] = by_day.min().where(by_day.count() == 2 * (end - start))
    troughs = pd.DataFrame(troughs).rename_axis("date")
    return troughs.where(troughs.notna().all(axis=1))


def yearly_line_fits(daily: pd.DataFrame, x: str, y: str, years: list[int]) -> pd.DataFrame:
    """Fit a least-squares straight line of ``y`` on ``x`` within each of the given years.

    Args:
        daily: One row per date, holding columns ``x`` and ``y``.
        x: Name of the explanatory column.
        y: Name of the response column.
        years: The calendar years to fit, one line each.

    Returns:
        One row per year: ``slope``, ``intercept``, the range of ``x`` fitted (``x_min``,
        ``x_max``) and the number of days used.
    """
    fits = {}
    for year in years:
        days = daily.loc[daily.index.year == year, [x, y]].dropna()
        slope, intercept = np.polyfit(days[x], days[y], 1)
        fits[year] = {
            "slope": slope,
            "intercept": intercept,
            "x_min": days[x].min(),
            "x_max": days[x].max(),
            "days": len(days),
        }
    return pd.DataFrame.from_dict(fits, orient="index").rename_axis("year")


def line_fits(table: pd.DataFrame, y: str, xs: list[str]) -> pd.DataFrame:
    """Fit a least-squares straight line of ``y`` on each of several explanatory columns.

    Each line is fitted on its own, so the fits can be compared: which single column tracks
    ``y`` more closely.

    Args:
        table: One row per observation, holding ``y`` and every column in ``xs``.
        y: Name of the response column.
        xs: Names of the explanatory columns, one line each.

    Returns:
        One row per explanatory column: ``slope``, ``intercept``, ``r_squared``, ``rmse`` (the
        root mean squared residual, in the units of ``y``) and ``points``.
    """
    fits = {}
    for x in xs:
        rows = table[[x, y]].dropna()
        slope, intercept = np.polyfit(rows[x], rows[y], 1)
        residual = rows[y] - (intercept + slope * rows[x])
        fits[x] = {
            "slope": slope,
            "intercept": intercept,
            "r_squared": 1 - (residual**2).sum() / ((rows[y] - rows[y].mean()) ** 2).sum(),
            "rmse": np.sqrt((residual**2).mean()),
            "points": len(rows),
        }
    return pd.DataFrame.from_dict(fits, orient="index").rename_axis("fitted_on")


# --------------------------------------------------------------------------------------------
# The low end of each year
# --------------------------------------------------------------------------------------------


def lowest_intervals(total: pd.Series, share: float) -> pd.DataFrame:
    """Return the lowest ``share`` of each calendar year's kept half hours, lowest first.

    Returns:
        One row per selected half hour, indexed by its start time: ``year``, ``mw``, ``hour``
        (clock hour in which it starts) and ``position_pct``, its place in the year's sorted
        half hours as a percentage (0 is the minimum).
    """
    kept = total.dropna()
    year = kept.index.year
    lowest = kept.groupby(year, group_keys=False).apply(
        lambda values: values.nsmallest(round(share * len(values)))
    )
    frame = pd.DataFrame({"year": lowest.index.year, "mw": lowest, "hour": lowest.index.hour})
    half_hours_in_year = kept.groupby(year).size()
    rank = frame.groupby("year").cumcount()
    frame["position_pct"] = 100 * rank / frame["year"].map(half_hours_in_year)
    return frame


def low_hour_shares(lowest: pd.DataFrame) -> pd.DataFrame:
    """Return the share (per cent) of each year's lowest half hours that start in each hour.

    Args:
        lowest: The output of ``lowest_intervals``.

    Returns:
        A table of clock hours 0 to 23 (rows) by years (columns); each column sums to 100.
    """
    shares = pd.crosstab(lowest["hour"], lowest["year"], normalize="columns")
    return 100 * shares.reindex(range(24), fill_value=0.0)
