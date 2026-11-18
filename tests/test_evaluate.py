"""Tests 4, 5 and 9: scoring is right, no forecast can see past its origin, and the daily
skill tables match a hand calculation.

All data are synthetic.
"""

import numpy as np
import pandas as pd

from pynmdf import evaluate, poe


def test_scoring_matches_hand_calculation():
    # --- Pinball loss: too low costs q per MW, too high costs (1 - q) per MW.
    assert np.isclose(evaluate.pinball_loss(100, 90, 0.9), 9.0)
    assert np.isclose(evaluate.pinball_loss(100, 90, 0.1), 1.0)
    assert np.isclose(evaluate.pinball_loss(100, 110, 0.9), 1.0)
    assert np.isclose(evaluate.pinball_loss(100, 110, 0.1), 9.0)

    # --- POE10 is the high side (0.90 quantile) and POE90 the low side (0.10 quantile).
    levels = poe.poe_levels(np.arange(101.0))
    assert levels == {"poe10": 90.0, "poe50": 50.0, "poe90": 10.0}
    assert levels["poe10"] >= levels["poe50"] >= levels["poe90"]

    # --- Table: two valid points and one invalid, which must not be scored.
    forecasts = pd.DataFrame(
        {
            "model": "M9",
            "actual": [100.0, 100.0, 500.0],
            "poe10": [120.0, 95.0, 0.0],
            "poe50": [110.0, 90.0, 0.0],
            "poe90": [90.0, 80.0, 0.0],
            "valid": [True, True, False],
        }
    )
    table = evaluate.score(forecasts, ["model"]).loc["M9"]
    assert table["points"] == 2
    assert np.isclose(table["pinball_poe10"], (0.1 * 20 + 0.9 * 5) / 2)
    assert np.isclose(table["pinball_poe50"], (0.5 * 10 + 0.5 * 10) / 2)
    assert np.isclose(table["pinball_poe90"], (0.1 * 10 + 0.1 * 20) / 2)
    assert np.isclose(table["pinball_mean"], (3.25 + 5.0 + 1.5) / 3)
    assert np.isclose(table["coverage"], 0.5)  # the first actual is inside its band, the second not
    # Mean error of POE50 over the two valid points: (100 - 110) and (100 - 90).
    assert np.isclose(evaluate.poe50_bias(forecasts, ["model"])["M9"], 0.0)


def test_daily_skill_matches_hand_calculation():
    # --- Two years of ten valid days. The actual low falls by 10 MW a day within each year, so
    #     with a share of 0.2 the lowest days of a year are its last two.
    dates = pd.date_range("2020-12-22", "2021-01-10", freq="D")
    actual = np.tile(np.arange(190.0, 90.0, -10.0), 2)
    in_lowest = np.tile(np.arange(10) >= 8, 2)
    # Model A is 5 MW too high every day. Model B is exact, except 20 MW too low on the lowest days.
    predicted = {"A": actual + 5, "B": actual - 20 * in_lowest}
    frames = [
        pd.DataFrame({"date": dates, "model": model, "low": "daytime", "predicted": values})
        for model, values in predicted.items()
    ]
    daily = pd.concat(frames, ignore_index=True).assign(actual=np.tile(actual, 2))
    # Rows that must not be scored: a day with no actual, and the other low.
    extra = daily.iloc[[0]].assign(date=pd.Timestamp("2020-12-21"), actual=np.nan)
    daily = pd.concat([daily, extra, daily.assign(low="overnight", predicted=0.0)])

    errors = evaluate.daily_errors(daily, "daytime", lowest_share=0.2)
    assert len(errors) == 40
    assert errors.loc[errors["lowest"], "date"].dt.day.isin([30, 31, 9, 10]).all()

    skill = evaluate.daily_skill(errors, ["model"])
    assert skill.loc[("all days", "A")].tolist() == [5.0, -5.0, 20]
    assert skill.loc[("lowest days", "A")].tolist() == [5.0, -5.0, 4]
    assert skill.loc[("all days", "B")].tolist() == [4.0, 4.0, 20]  # 20 MW on 4 of 20 days
    assert skill.loc[("lowest days", "B")].tolist() == [20.0, 20.0, 4]

    # --- The pair: B misses by less than A over all days, and by more on the lowest days.
    pairs = evaluate.compare_daily(errors, {"B against A": ("B", "A")})
    assert np.isclose(pairs.loc[("B against A", "all days"), "change_pct"], -20.0)
    assert np.isclose(pairs.loc[("B against A", "lowest days"), "change_pct"], 300.0)
    by_year = evaluate.compare_daily(errors, {"B against A": ("B", "A")}, by=("year",))
    assert np.allclose(by_year.xs("all days", level="day_set")["difference_mw"], -1.0)
    assert by_year.index.get_level_values("year").unique().tolist() == [2020, 2021]

    # --- The table of the daily test holds the same numbers: the models first, then the pair.
    table = evaluate.daily_table(errors, {"B against A": ("B", "A")})
    assert table.index.tolist() == ["A", "B", "B against A"]
    assert table.loc["B", ["all_days_n", "all_days_mae_mw", "lowest_days_mae_mw"]].tolist() == [
        20,
        4.0,
        20.0,
    ]
    assert np.isclose(table.loc["B against A", "all_days_mae_change_pct"], -20.0)
    assert np.isclose(table.loc["B against A", "lowest_days_mae_difference_mw"], 15.0)
    assert table.loc["B against A", ["all_days_mae_mw", "lowest_days_n"]].isna().all()


def _synthetic_world(seed: int) -> tuple[pd.Series, pd.Series, pd.DataFrame]:
    """Build seven years of half-hourly demand with an overnight dip and a PV-driven midday dip."""
    rng = np.random.default_rng(seed)
    weather_days = pd.date_range("2010-01-01", "2021-12-31", freq="D")
    season = np.cos(2 * np.pi * (weather_days.dayofyear - 15) / 365)
    weather = pd.DataFrame(
        {
            "tmax": 22 + 6 * season + rng.normal(0, 3, len(weather_days)),
            "tmin": 13 + 5 * season + rng.normal(0, 2, len(weather_days)),
            "solar": np.clip(16 + 8 * season + rng.normal(0, 4, len(weather_days)), 1, None),
        },
        index=weather_days,
    )
    days = pd.date_range("2015-01-01", "2021-12-31", freq="D")
    pv = pd.Series(np.linspace(200, 900, len(days)), index=days)

    half_hours = pd.date_range(days[0], periods=len(days) * 48, freq="30min")
    hour = half_hours.hour + half_hours.minute / 60
    day = np.repeat(np.arange(len(days)), 48)
    sunshine = weather["solar"].reindex(days).to_numpy()[day]
    midday_dip = 0.02 * pv.to_numpy()[day] * sunshine * np.exp(-(((hour - 13) / 2.5) ** 2))
    overnight_dip = 400 * np.exp(-(((hour - 4) / 2.5) ** 2))
    noise = rng.normal(0, 10, len(half_hours))
    total = pd.Series(2000 - overnight_dip - midday_dip + noise, index=half_hours, name="total_mw")
    return total, pv, weather


CFG = {
    "study": {"first_year": 2015, "last_year": 2021},
    "evaluation": {"first_test_year": 2019},
    "calendar": {"holiday_subdivision": "NSW"},
    "targets": {
        "month_min_kept_share": 0.9,
        "troughs": {"overnight": [0, 6], "daytime": [9, 17]},
        "robust_days": {"annual": 15, "monthly": 2},
    },
    "models": {
        "seed": 1,
        "n_draws": 3,
        "xgboost": {"n_estimators": 10, "max_depth": 2, "learning_rate": 0.3, "subsample": 0.8},
    },
}


def test_no_forecast_sees_past_its_origin():
    total, pv, weather = _synthetic_world(seed=0)
    before = evaluate.rolling_origin(total, pv, weather, CFG)

    # Scramble demand and weather after 2019. PV is left alone: the target year's capacity is
    # taken as known by design.
    last_origin = 2019
    rng = np.random.default_rng(99)
    later = total.index.year > last_origin
    total = total.where(~later, rng.permutation(total[later].to_numpy()).mean() + 500)
    weather.loc[weather.index.year > last_origin] = rng.normal(0, 50, (366 + 365, 3))
    after = evaluate.rolling_origin(total, pv, weather, CFG)

    made_by_then = before["origin"] <= last_origin
    assert made_by_then.sum() > 0 and (~made_by_then).sum() > 0
    forecast_columns = ["central", "poe10", "poe50", "poe90", "n_pool"]
    pd.testing.assert_frame_equal(
        before.loc[made_by_then, forecast_columns], after.loc[made_by_then, forecast_columns]
    )
    # The scrambling did reach the later forecasts, so the test is not passing by default.
    changed = before.loc[~made_by_then, "poe50"] != after.loc[~made_by_then, "poe50"]
    assert changed.any()
