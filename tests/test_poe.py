"""Test 6: the weather replay lays each historical year over the target year correctly.

All data are synthetic. Stub models stand in for the fitted ones, so the expected answer can be
read straight from the weather.
"""

import numpy as np
import pandas as pd

from pynmdf import models, poe

ROBUST_DAYS = {"annual": 15, "monthly": 2}
KNOTS = {"tmax": 21.0, "tmin": 18.0}  # the stub models below ignore them


def test_replay_runs_the_target_year_through_each_weather_year():
    rng = np.random.default_rng(0)
    weather_days = pd.date_range("2010-01-01", "2012-12-31", freq="D")  # 2012 is a leap year
    weather = pd.DataFrame(
        rng.uniform(5, 40, (len(weather_days), 3)),
        index=weather_days,
        columns=["tmax", "tmin", "solar"],
    )
    dates = pd.date_range("2020-01-01", "2020-12-31", freq="D")  # a leap target year
    pv = pd.Series(1000.0, index=dates)
    calendar = models.calendar_features(dates, pv, "NSW", dates[0])
    replay_years = [2010, 2011, 2012]

    # --- 29 February: a year without one lends its 28 February; a leap year lends its own.
    assert (
        poe.replayed_weather(weather, dates, 2011)
        .loc["2020-02-29"]
        .equals(weather.loc["2011-02-28"])
    )
    assert (
        poe.replayed_weather(weather, dates, 2012)
        .loc["2020-02-29"]
        .equals(weather.loc["2012-02-29"])
    )

    # --- A stub that returns the maximum temperature, with no residual: each simulation's lows
    #     are that weather year's lowest maximum temperature, for the year and for each month.
    def follows_weather(features):
        return pd.DataFrame(
            {"overnight": features["tmax"], "daytime": features["tmax"] + 100}, index=features.index
        )

    lows = poe.replay(
        follows_weather, calendar, weather, replay_years, None, 1, ROBUST_DAYS, rng, KNOTS
    )
    assert len(lows) == len(replay_years)
    for row, year in enumerate(replay_years):
        tmax = weather.loc[str(year), "tmax"]
        assert np.isclose(lows.loc[row, ("minimum", 0)], tmax.min())
        assert np.isclose(lows.loc[row, ("daytime_low", 0)], tmax.min() + 100)
        assert np.isclose(lows.loc[row, ("minimum", 7)], tmax[tmax.index.month == 7].min())
        assert np.isclose(
            lows.loc[row, ("robust", 7)], tmax[tmax.index.month == 7].nsmallest(2).mean()
        )

    # --- A stub that ignores the weather gives the same path in every replay year.
    def ignores_weather(features):
        return pd.DataFrame(
            {"overnight": features["month"] * 10.0, "daytime": features["pv"]}, index=features.index
        )

    same = poe.replay(
        ignores_weather, calendar, weather, replay_years, None, 1, ROBUST_DAYS, rng, KNOTS
    )
    assert (same.nunique() == 1).all()

    # --- With residuals: one simulation per draw, and the same seed gives the same output.
    residual_days = pd.date_range("2015-01-01", "2018-12-31", freq="D")
    residuals = pd.DataFrame(
        rng.normal(0, 30, (len(residual_days), 2)), index=residual_days, columns=models.TROUGHS
    )

    def run(seed):
        generator = np.random.default_rng(seed)
        return poe.replay(
            follows_weather,
            calendar,
            weather,
            replay_years,
            residuals,
            4,
            ROBUST_DAYS,
            generator,
            KNOTS,
        )

    assert len(run(7)) == len(replay_years) * 4
    pd.testing.assert_frame_equal(run(7), run(7))
    assert not run(7).equals(run(8))


def test_residuals_stay_in_their_month_and_year():
    # Each residual is tagged with its own year and month, so a draw reveals where it came from.
    days = pd.date_range("2015-01-01", "2017-12-31", freq="D")
    tag = days.year * 100.0 + days.month
    residuals = pd.DataFrame({"overnight": tag, "daytime": tag}, index=days)
    residuals = residuals[~((days.year == 2016) & (days.month == 4))]  # 2016 has no April at all
    dates = pd.date_range("2020-01-01", "2020-12-31", freq="D")

    drawn = poe.draw_residuals(residuals, dates, 50, np.random.default_rng(3))[:, :, 0]
    month_drawn, year_drawn = drawn % 100, drawn // 100
    assert (month_drawn == dates.month.to_numpy()).all()  # never a residual from another month

    april = dates.month.to_numpy() == 4
    one_year_per_simulation = np.ptp(year_drawn[:, ~april], axis=1) == 0
    assert one_year_per_simulation.all()
    # A simulation that picked 2016 has to borrow its April from the other years.
    picked_2016 = year_drawn[:, 0] == 2016
    assert picked_2016.any() and (year_drawn[picked_2016][:, april] != 2016).all()
