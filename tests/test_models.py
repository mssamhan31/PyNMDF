"""Test 11: each temperature enters M4 as a V, and each arm of each V gets its own slope.

All data are synthetic.
"""

import numpy as np
import pandas as pd

from pynmdf import models

KNOTS = {"tmax": 21.0, "tmin": 18.0}


def _features(tmax, tmin, dates: pd.DatetimeIndex, pv=500.0, solar=20.0) -> pd.DataFrame:
    """Predictors for days with the given maximum and minimum temperature."""
    calendar = models.calendar_features(dates, pd.Series(pv, index=dates), "NSW", dates[0])
    weather = pd.DataFrame({"tmax": tmax, "tmin": tmin, "solar": solar}, index=dates)
    return models.add_weather(calendar, weather, KNOTS)


def test_each_temperature_enters_m4_as_a_v():
    # --- Three hand-worked days. Maximum: 7 below its knot, on it, 10 above. Minimum: 8 below
    #     its knot, on it, 4 above.
    dates = pd.date_range("2020-03-02", periods=3, freq="D")
    features = _features(np.array([14.0, 21.0, 31.0]), np.array([10.0, 18.0, 22.0]), dates)
    assert features["tmax_below"].tolist() == [7.0, 0.0, 0.0]
    assert features["tmax_above"].tolist() == [0.0, 0.0, 10.0]
    assert features["tmin_below"].tolist() == [8.0, 0.0, 0.0]
    assert features["tmin_above"].tolist() == [0.0, 0.0, 4.0]
    assert features["pv_solar"].tolist() == [10000.0, 10000.0, 10000.0]

    # --- A day with no maximum temperature has no V on it either, so it cannot be fitted on.
    gap = _features(np.array([14.0, np.nan, 31.0]), np.array([10.0, 18.0, 22.0]), dates)
    assert gap[["tmax", "tmax_below", "tmax_above"]].iloc[1].isna().all()

    # --- M4 is given the four arms; M5 is given the two temperatures as they are.
    assert list(models._design(features, "M4").columns[-5:]) == [
        "pv_solar",
        "tmax_below",
        "tmax_above",
        "tmin_below",
        "tmin_above",
    ]
    assert list(models._design(features, "M5").columns[-3:]) == ["pv_solar", "tmax", "tmin"]

    # --- Lows built from two Vs with a different slope on every arm: M4 recovers all four.
    days = pd.date_range("2019-01-01", "2020-12-31", freq="D")
    rng = np.random.default_rng(0)
    world = _features(
        rng.uniform(12, 38, len(days)),
        rng.uniform(4, 26, len(days)),
        days,
        pv=np.linspace(400, 600, len(days)),
        solar=rng.uniform(5, 30, len(days)),
    )
    arms = {"tmax_below": 30.0, "tmax_above": 50.0, "tmin_below": 20.0, "tmin_above": 40.0}
    low = 1000 + sum(slope * world[arm] for arm, slope in arms.items())
    troughs = pd.DataFrame({"overnight": low, "daytime": low + 200})
    fitted = models.fit_daily(world, troughs, "M4", xgboost={})
    slopes = models.linear_coefficients(fitted, world, "M4")
    for arm, slope in arms.items():
        assert np.allclose(slopes.loc[arm], slope)
