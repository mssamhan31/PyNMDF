"""Turn a model into POE10, POE50 and POE90 forecasts.

POE is probability of exceedance. POE90 is the low side (a 90% chance of being exceeded) and
POE10 the high side, so POE10, POE50 and POE90 are the 0.90, 0.50 and 0.10 quantiles. Errors are
always actual minus forecast.

Two recipes:

- M1 (naive): last year's value plus a quantile of its own past year-on-year changes.
- M2 to M6: a replay. The target year is simulated many times. Each simulation takes the
  model's prediction for every day under one historical weather year and adds residuals borrowed
  from one left-out training year. The spread of the simulated lows gives the POE levels. M2, M3
  and M6 ignore the weather, so for them every weather year gives the same prediction and all of
  the spread comes from the residuals.
"""

import calendar
from collections.abc import Callable

import numpy as np
import pandas as pd

from pynmdf.models import TROUGHS, add_weather

POE_QUANTILES = {"poe10": 0.90, "poe50": 0.50, "poe90": 0.10}
DAYTIME = TROUGHS.index("daytime")


def poe_levels(values: np.ndarray) -> dict:
    """Return POE10, POE50 and POE90 of a set of values."""
    return {name: float(np.quantile(values, quantile)) for name, quantile in POE_QUANTILES.items()}


# --------------------------------------------------------------------------------------------
# M1
# --------------------------------------------------------------------------------------------


def naive_forecasts(actuals: pd.DataFrame, test_years: list[int]) -> pd.DataFrame:
    """Forecast every target with M1: next year equals this year.

    A month takes the same month of the year before, or the last valid one if that month does
    not count. The error pool at each origin is every past change between a value and the value
    it would have been forecast from; monthly pools combine the twelve calendar months.

    Args:
        actuals: The output of ``targets.period_targets``.
        test_years: The years to forecast, each from the year before.

    Returns:
        One row per target, level, test year and month: ``central``, the three POE levels and
        ``n_pool`` (the number of past errors behind them).
    """
    rows = []
    valid = actuals[actuals["valid"]]
    for (target, level), group in valid.groupby(["target", "level"]):
        years = range(actuals["year"].min(), actuals["year"].max() + 1)
        table = group.pivot(index="year", columns="month", values="actual").reindex(years)
        # What each period would have been forecast from: the last valid value before it.
        forecast = table.ffill().shift(1)
        errors = table - forecast
        for year in test_years:
            pool = errors.loc[: year - 1].to_numpy().ravel()
            pool = pool[~np.isnan(pool)]
            for month, central in forecast.loc[year].items():
                levels = {name: central + value for name, value in poe_levels(pool).items()}
                rows.append(
                    {"target": target, "level": level, "year": year, "month": month}
                    | {"central": central, **levels, "n_pool": len(pool)}
                )
    return pd.DataFrame(rows).assign(model="M1", origin=lambda frame: frame["year"] - 1)


# --------------------------------------------------------------------------------------------
# M2 to M6: the replay
# --------------------------------------------------------------------------------------------


def replayed_weather(weather: pd.DataFrame, dates: pd.DatetimeIndex, year: int) -> pd.DataFrame:
    """Lay the weather of ``year`` over the target dates, matching month and day.

    A target 29 February takes 28 February when ``year`` is not a leap year. A 29 February in
    ``year`` is simply not used when the target year has none.
    """
    day = np.where(
        (dates.month == 2) & (dates.day == 29) & (not calendar.isleap(year)), 28, dates.day
    )
    source = pd.to_datetime({"year": year, "month": dates.month, "day": day})
    return weather.reindex(source).set_axis(dates)


def draw_residuals(
    residuals: pd.DataFrame, dates: pd.DatetimeIndex, n_simulations: int, rng: np.random.Generator
) -> np.ndarray:
    """Draw a residual for every trough of every day of every simulation.

    Each simulation picks one left-out year, so a year's own offset stays together. Each
    simulated day then takes one day of that year from the same calendar month, so a spring day
    never receives a winter residual. The day's two trough residuals are used together. Where
    the chosen year has no residual in a month (a month with no valid data), that month is
    drawn from the same month of all years.

    Args:
        residuals: Out-of-fold residuals, one row per training day and one column per trough.
        dates: The days of the target year.
        n_simulations: Number of simulated years.
        rng: Random generator.

    Returns:
        An array of shape (simulations, days, troughs).
    """
    years = np.unique(residuals.index.year)
    by_month = [residuals[residuals.index.month == month] for month in range(1, 13)]
    width = max(len(month) for month in by_month)

    # pools[y, m] holds the residual days of year y in month m, padded to a common width.
    pools = np.zeros((len(years), 12, width, residuals.shape[1]))
    counts = np.zeros((len(years), 12), dtype=int)
    for y, year in enumerate(years):
        for m, month in enumerate(by_month):
            own = month[month.index.year == year]
            chosen = own if len(own) else month
            pools[y, m, : len(chosen)] = chosen.to_numpy()
            counts[y, m] = len(chosen)

    month_of_day = dates.month.to_numpy() - 1
    left_out = rng.integers(len(years), size=n_simulations)
    available = counts[left_out][:, month_of_day]
    picked = (rng.random((n_simulations, len(dates))) * available).astype(int)
    return pools[left_out[:, None], month_of_day[None, :], picked]


def period_lows(simulated: np.ndarray, dates: pd.DatetimeIndex, robust_days: dict) -> pd.DataFrame:
    """Reduce simulated daily troughs to the three targets, for the year and for each month.

    Args:
        simulated: Daily troughs of shape (simulations, days, troughs).
        dates: The days of the target year.
        robust_days: Days averaged by the robust target, for ``annual`` and for ``monthly``.

    Returns:
        One row per simulation; columns are (target, month) pairs, month 0 being the year.
    """
    lower_trough = simulated.min(axis=2)
    daytime = simulated[:, :, DAYTIME]
    lows = {}
    for month in range(13):
        days = slice(None) if month == 0 else dates.month == month
        n_days = robust_days["annual" if month == 0 else "monthly"]
        lows["minimum", month] = lower_trough[:, days].min(axis=1)
        lows["daytime_low", month] = daytime[:, days].min(axis=1)
        lows["robust", month] = np.sort(lower_trough[:, days], axis=1)[:, :n_days].mean(axis=1)
    return pd.DataFrame(lows).rename_axis(columns=["target", "month"])


def replay(
    predict: Callable[[pd.DataFrame], pd.DataFrame],
    target_calendar: pd.DataFrame,
    weather: pd.DataFrame,
    replay_years: list[int],
    residuals: pd.DataFrame | None,
    n_draws: int,
    robust_days: dict,
    rng: np.random.Generator,
    knots: dict,
) -> pd.DataFrame:
    """Simulate the target year under every replay weather year and reduce it to the targets.

    Args:
        predict: Maps a frame of predictors to the overnight and daytime low of each day.
        target_calendar: Calendar, time and PV predictors for each day of the target year.
        weather: Daily ``tmax``, ``tmin`` and ``solar``, covering every replay year.
        replay_years: The historical weather years to run the target year through.
        residuals: Out-of-fold residuals to draw from, or None to add nothing.
        n_draws: Simulations per replay year.
        robust_days: Days averaged by the robust target.
        rng: Random generator.
        knots: The knots of the two temperature Vs (degrees C), as given to ``add_weather``.

    Returns:
        The output of ``period_lows``: one row per simulation, ``len(replay_years) * n_draws``
        in all.
    """
    dates = target_calendar.index
    predicted = np.stack(
        [
            predict(add_weather(target_calendar, replayed_weather(weather, dates, year), knots))[
                TROUGHS
            ].to_numpy()
            for year in replay_years
        ]
    )
    simulated = np.repeat(predicted, n_draws, axis=0)
    if residuals is not None:
        simulated = simulated + draw_residuals(residuals[TROUGHS], dates, len(simulated), rng)
    return period_lows(simulated, dates, robust_days)
