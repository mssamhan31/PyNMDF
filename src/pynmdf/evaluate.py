"""Rolling-origin backtest, scoring and model checks.

Every model forecasts each test year from data up to the end of the year before (the origin):
train 2015 to 2018 and test 2019, then extend one year at a time. ``rolling_origin`` is the only
place that makes forecasts, so nothing after an origin can reach a forecast made from it. The one
exception is by design: PV capacity of the target year is taken as known.

Errors and misses are always actual minus predicted.
"""

from functools import partial
from typing import NamedTuple

import numpy as np
import pandas as pd

from pynmdf import io_weather, models, poe, targets

KEYS = ["target", "level", "year", "month"]


class _DailyData(NamedTuple):
    """One row per day of the study window, ready for the daily models."""

    calendar: pd.DataFrame  # predictors that depend only on the date
    features: pd.DataFrame  # calendar plus that day's weather
    troughs: pd.DataFrame  # the overnight and daytime low to be explained
    usable: np.ndarray  # True where a day can be fitted on
    xgboost: dict  # settings for the XGBoost models (M5 and M6)


def _daily_data(total: pd.Series, pv: pd.Series, weather: pd.DataFrame, cfg: dict) -> _DailyData:
    """Assemble the daily predictors and lows that every daily model is fitted on."""
    study, settings = cfg["study"], cfg["models"]
    dates = pd.date_range(f"{study['first_year']}-01-01", f"{study['last_year']}-12-31", freq="D")
    calendar = models.calendar_features(dates, pv, cfg["calendar"]["holiday_subdivision"], dates[0])
    features = models.add_weather(calendar, weather.reindex(dates))
    troughs = targets.daily_troughs(total, cfg["targets"]["troughs"]).reindex(dates)
    usable = troughs.notna().all(axis=1).to_numpy() & features.notna().all(axis=1).to_numpy()
    xgboost = {**settings["xgboost"], "random_state": settings["seed"], "n_jobs": 1}
    return _DailyData(calendar, features, troughs, usable, xgboost)


def _test_years(cfg: dict) -> range:
    return range(cfg["evaluation"]["first_test_year"], cfg["study"]["last_year"] + 1)


# --------------------------------------------------------------------------------------------
# Forecasts
# --------------------------------------------------------------------------------------------


def _forecast_rows(simulated: pd.DataFrame, central: pd.Series) -> pd.DataFrame:
    """Reduce the simulated lows of one model and origin to one row per target and month."""
    levels = simulated.quantile(list(poe.POE_QUANTILES.values())).T
    levels.columns = list(poe.POE_QUANTILES)
    rows = levels.assign(central=central, n_pool=len(simulated)).reset_index()
    return rows.assign(level=np.where(rows["month"] == 0, "annual", "monthly"))


def _actuals(total: pd.Series, cfg: dict) -> pd.DataFrame:
    """Return the actual value of every target, as the forecasts are scored against."""
    wanted = cfg["targets"]
    return targets.period_targets(
        total, wanted["troughs"], wanted["month_min_kept_share"], wanted["robust_days"]
    )


def _replay_forecasts(
    data: _DailyData, weather: pd.DataFrame, cfg: dict, names: list[str]
) -> list[pd.DataFrame]:
    """Forecast every target, test year and month with the named daily models.

    Each model is fitted on the days up to the origin and run through the replay
    (``poe.replay``) with its own out-of-fold residuals.
    """
    settings, robust_days = cfg["models"], cfg["targets"]["robust_days"]
    dates = data.features.index
    weather_years = io_weather.complete_years(weather[["tmax", "tmin", "solar"]])
    # M1 is model 1; the daily models count from 2 in the order they are defined.
    number = {model: position for position, model in enumerate(models.SPECS, start=2)}

    rows = []
    for year in _test_years(cfg):
        origin = year - 1
        train = data.usable & (dates.year <= origin)
        target_calendar = data.calendar[dates.year == year]
        replay_years = [past for past in weather_years if past <= origin]
        for model in names:
            fit_on = (data.features[train], data.troughs[train], model, data.xgboost)
            fitted = models.fit_daily(*fit_on)
            residuals = models.out_of_fold_residuals(*fit_on)
            run = partial(
                poe.replay,
                partial(models.predict_daily, fitted, model=model),
                target_calendar,
                weather,
                replay_years,
                robust_days=robust_days,
                rng=np.random.default_rng([settings["seed"], number[model], origin]),
            )
            simulated = run(residuals=residuals, n_draws=settings["n_draws"])
            # The central forecast adds no residual; it is the mean over the weather years.
            central = run(residuals=None, n_draws=1).mean()
            rows.append(
                _forecast_rows(simulated, central).assign(model=model, origin=origin, year=year)
            )
    return rows


def _forecast_table(rows: list[pd.DataFrame], actuals: pd.DataFrame) -> pd.DataFrame:
    """Join forecasts to their actuals and put the columns and rows in a fixed order."""
    forecasts = pd.concat(rows, ignore_index=True).merge(
        actuals[[*KEYS, "actual", "valid"]], on=KEYS, how="left"
    )
    columns = ["target", "level", "model", "origin", "year", "month"]
    columns += ["central", *poe.POE_QUANTILES, "actual", "valid", "n_pool"]
    return forecasts[columns].sort_values(columns[:6], ignore_index=True)


def rolling_origin(
    total: pd.Series, pv: pd.Series, weather: pd.DataFrame, cfg: dict
) -> pd.DataFrame:
    """Forecast every target, test year and month with all six models.

    Args:
        total: The 30-minute network total.
        pv: Daily PV capacity in MW.
        weather: Daily ``tmax``, ``tmin`` and ``solar`` with short gaps filled, from the first
            replay year on.
        cfg: The configuration from ``config.load_config``.

    Returns:
        One row per forecast: ``target`` (minimum, daytime_low, robust), ``level`` (annual,
        monthly), ``model``, ``origin``, ``year``, ``month`` (0 for a year), ``central``,
        ``poe10``, ``poe50``, ``poe90``, ``actual``, ``valid`` and ``n_pool`` (the number of
        past errors, or of simulated years, behind the POE levels).
    """
    actuals = _actuals(total, cfg)
    data = _daily_data(total, pv, weather, cfg)
    rows = [poe.naive_forecasts(actuals, _test_years(cfg))]
    rows += _replay_forecasts(data, weather, cfg, list(models.MODELS))
    return _forecast_table(rows, actuals)


def m4_variant_forecasts(
    total: pd.Series, pv: pd.Series, weather: pd.DataFrame, cfg: dict
) -> pd.DataFrame:
    """Forecast with M4 after switching off one group of its weather terms at a time.

    A diagnostic, not part of the comparison: it shows which terms pull M4's forecasts down.
    Each variant is refitted and run through the same replay as M4 itself.

    Returns:
        The same columns as ``rolling_origin``, one row per forecast of each variant in
        ``models.M4_VARIANTS``.
    """
    data = _daily_data(total, pv, weather, cfg)
    rows = _replay_forecasts(data, weather, cfg, list(models.M4_VARIANTS))
    return _forecast_table(rows, _actuals(total, cfg))


# --------------------------------------------------------------------------------------------
# Scores
# --------------------------------------------------------------------------------------------


def pinball_loss(actual, forecast, quantile: float) -> np.ndarray:
    """Return the pinball loss of a forecast of the given quantile.

    A forecast that is too low costs ``quantile`` per MW and one that is too high costs
    ``1 - quantile`` per MW, so the loss is smallest at the true quantile.
    """
    error = np.asarray(actual, dtype=float) - np.asarray(forecast, dtype=float)
    return np.maximum(quantile * error, (quantile - 1) * error)


def score(forecasts: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    """Score forecasts by pinball loss and coverage.

    Only valid test points are scored. Coverage is the share of actuals lying between POE90 and
    POE10; with few test points it is descriptive only.

    Args:
        forecasts: The output of ``rolling_origin``.
        by: Columns to group by, for example ``["target", "level", "model"]``.

    Returns:
        One row per group: the mean pinball loss at each POE level (MW), their mean, the
        coverage and the number of test points.
    """
    scored = forecasts[forecasts["valid"] & forecasts["poe50"].notna()].copy()
    for name, quantile in poe.POE_QUANTILES.items():
        scored[f"pinball_{name}"] = pinball_loss(scored["actual"], scored[name], quantile)
    scored["coverage"] = scored["actual"].between(scored["poe90"], scored["poe10"])
    scored["points"] = 1

    losses = [f"pinball_{name}" for name in poe.POE_QUANTILES]
    table = scored.groupby(by)[[*losses, "coverage"]].mean()
    table.insert(len(losses), "pinball_mean", table[losses].mean(axis=1))
    return table.assign(points=scored.groupby(by)["points"].sum())


def poe50_bias(forecasts: pd.DataFrame, by: list[str]) -> pd.Series:
    """Return the mean error of POE50 over the valid test points of each group.

    The error is actual minus forecast, in MW: positive means the forecasts sat too low on
    average, negative too high.

    Args:
        forecasts: The output of ``rolling_origin``.
        by: Columns to group by, for example ``["target", "level", "model"]``.
    """
    scored = forecasts[forecasts["valid"] & forecasts["poe50"].notna()]
    error = (scored["actual"] - scored["poe50"]).rename("mean_error_mw")
    return error.groupby([scored[column] for column in by]).mean()


def score_table(forecasts: pd.DataFrame, target: str) -> pd.DataFrame:
    """Return Table III for one target: every model's scores, annual beside monthly.

    Returns:
        One row per model. Columns are the outputs of ``score`` prefixed by ``annual_`` and by
        ``monthly_``.
    """
    scores = score(forecasts[forecasts["target"] == target], ["model", "level"])
    levels = ("annual", "monthly")
    return pd.concat(
        [scores.xs(level, level="level").add_prefix(f"{level}_") for level in levels], axis=1
    )


# The comparisons reported as headline numbers: a name mapped to (model, reference). The first
# two were fixed before any model was run. The last came with M6, after the scores of M1 to M5
# had been seen, and is supplementary.
COMPARISONS = {
    "H1: PV against time": ("M3", "M2"),
    "H2: weather on top of PV": ("M4", "M3"),
    "Model form: XGBoost against linear": ("M5", "M4"),
    "Supplementary: weather in tree form": ("M5", "M6"),
}


def compare(forecasts: pd.DataFrame, pairs: dict) -> pd.DataFrame:
    """Compare pairs of models on mean pinball loss, for every target and level.

    Args:
        forecasts: The output of ``rolling_origin``.
        pairs: A name for each comparison, mapped to ``(model, reference)``, for example
            ``COMPARISONS``.

    Returns:
        One row per comparison, target and level: both mean pinball losses (MW), their
        difference and the change in per cent. A negative change means ``model`` scores better
        than ``reference``.
    """
    loss = score(forecasts, ["target", "level", "model"])["pinball_mean"].unstack("model")
    rows = []
    for name, (model, reference) in pairs.items():
        rows.append(
            pd.DataFrame(
                {
                    "comparison": name,
                    "model": model,
                    "reference": reference,
                    "model_pinball_mw": loss[model],
                    "reference_pinball_mw": loss[reference],
                    "difference_mw": loss[model] - loss[reference],
                    "change_pct": 100 * (loss[model] / loss[reference] - 1),
                }
            )
        )
    return pd.concat(rows).reset_index().set_index(["comparison", "target", "level"])


# --------------------------------------------------------------------------------------------
# Checks on the daily models
# --------------------------------------------------------------------------------------------


def own_weather_predictions(
    total: pd.Series, pv: pd.Series, weather: pd.DataFrame, cfg: dict
) -> pd.DataFrame:
    """Predict every day of each test year from its origin, given that day's own weather.

    A check, not a forecast: the target year's weather is not known a year ahead. It shows what
    each fitted model says about a day once its inputs are known, with no replay and no
    residual, so that a model's misses can be read day by day.

    Returns:
        One row per test day, model and low (``overnight`` or ``daytime``): ``date``, ``model``,
        ``low``, ``predicted`` and ``actual`` (blank when the day's lows are not both complete).
    """
    data = _daily_data(total, pv, weather, cfg)
    dates = data.features.index
    frames = []
    for year in _test_years(cfg):
        train, target = data.usable & (dates.year <= year - 1), dates.year == year
        for model in models.MODELS:
            fitted = models.fit_daily(
                data.features[train], data.troughs[train], model, data.xgboost
            )
            predicted = models.predict_daily(fitted, data.features[target], model)
            for low in models.TROUGHS:
                frames.append(
                    pd.DataFrame(
                        {
                            "date": dates[target],
                            "model": model,
                            "low": low,
                            "predicted": predicted[low].to_numpy(),
                            "actual": data.troughs.loc[target, low].to_numpy(),
                        }
                    )
                )
    return pd.concat(frames, ignore_index=True)


def lowest_predicted_days(
    daily: pd.DataFrame, model: str, low: str, subdivision: str
) -> pd.DataFrame:
    """Compare, for each test year, the day a model predicts as lowest with the day that was.

    Args:
        daily: The output of ``own_weather_predictions``.
        model: The model to look at.
        low: ``overnight`` or ``daytime``.
        subdivision: State code for the public holiday calendar.

    Returns:
        One row per test year: the lowest predicted day, its public holiday if any, the
        prediction and what that day did; then the day that was actually lowest, its value and
        what the model predicted for it.
    """
    days = daily[(daily["model"] == model) & (daily["low"] == low)].set_index("date")
    by_year = days.groupby(days.index.year)
    predicted_day = pd.DatetimeIndex(by_year["predicted"].idxmin())
    actual_day = pd.DatetimeIndex(by_year["actual"].idxmin())
    return pd.DataFrame(
        {
            "lowest_predicted_day": predicted_day.strftime("%a %d %b"),
            "public_holiday": targets.public_holidays(predicted_day, subdivision).to_numpy(),
            "predicted_mw": days.loc[predicted_day, "predicted"].to_numpy(),
            "actual_that_day_mw": days.loc[predicted_day, "actual"].to_numpy(),
            "lowest_actual_day": actual_day.strftime("%a %d %b"),
            "actual_low_mw": days.loc[actual_day, "actual"].to_numpy(),
            "predicted_for_it_mw": days.loc[actual_day, "predicted"].to_numpy(),
        },
        index=pd.Index(predicted_day.year, name="year"),
    )


def miss_on_holidays(daily: pd.DataFrame, subdivision: str) -> pd.DataFrame:
    """Compare the average miss on public holidays with that on ordinary weekend days.

    The models treat both as one kind of day (non-working). If public holidays were really
    lower than ordinary weekend days, the models would miss them on the low side: the actual
    would sit below the prediction and the average miss on holidays would be clearly negative
    next to that on ordinary weekend days.

    Args:
        daily: The output of ``own_weather_predictions``.
        subdivision: State code for the public holiday calendar.

    Returns:
        One row per low and model: the mean miss (actual minus predicted, MW) and the number of
        days for each kind of day, and the difference between the two means.
    """
    day = pd.DatetimeIndex(daily["date"].unique())
    holiday = pd.Series((targets.public_holidays(day, subdivision) != "").to_numpy(), index=day)
    is_holiday = daily["date"].map(holiday).to_numpy()
    is_weekend = (daily["date"].dt.dayofweek >= 5).to_numpy()
    kind = np.select([is_holiday, is_weekend], ["holiday", "weekend"], default="working")

    scored = daily.assign(miss=daily["actual"] - daily["predicted"], kind=kind).dropna()
    scored = scored[scored["kind"] != "working"]
    table = scored.groupby(["low", "model", "kind"])["miss"].agg(["mean", "size"]).unstack("kind")
    return pd.DataFrame(
        {
            "holiday_mean_miss_mw": table["mean", "holiday"],
            "holiday_days": table["size", "holiday"],
            "weekend_mean_miss_mw": table["mean", "weekend"],
            "weekend_days": table["size", "weekend"],
            "holiday_minus_weekend_mw": table["mean", "holiday"] - table["mean", "weekend"],
        }
    )


def m4_weather_terms(
    total: pd.Series, pv: pd.Series, weather: pd.DataFrame, cfg: dict
) -> pd.DataFrame:
    """Describe M4's weather terms at each origin, and how far PV x solar is extrapolated.

    M4 is fitted up to each origin, as in the backtest. Its PV x solar term is a product, so
    it grows with PV capacity: the sunniest days of a target year carry a larger product than
    any training day. This table shows the size of each coefficient and of that reach.

    Returns:
        One row per test year, all for the daytime low: the coefficient on PV x solar (MW per
        1,000 MW x MJ/m2) and on maximum and minimum temperature (MW per degree C); the largest
        PV x solar in the training days; PV x solar on the sunniest days of the target year
        under its own weather (the quantile in ``checks.pv_solar_quantile``); and how far, in
        per cent, the second lies beyond the first.
    """
    data = _daily_data(total, pv, weather, cfg)
    dates = data.features.index
    rows = {}
    for year in _test_years(cfg):
        train, target = data.usable & (dates.year <= year - 1), dates.year == year
        fitted = models.fit_daily(data.features[train], data.troughs[train], "M4", data.xgboost)
        daytime = models.linear_coefficients(fitted, data.features, "M4")["daytime"]
        seen = data.features.loc[train, "pv_solar"].max()
        reached = data.features.loc[target, "pv_solar"].quantile(cfg["checks"]["pv_solar_quantile"])
        rows[year] = {
            "pv_solar_mw_per_1000": 1000 * daytime["pv_solar"],
            "tmax_mw_per_degree": daytime["tmax"],
            "tmin_mw_per_degree": daytime["tmin"],
            "pv_solar_max_in_training": seen,
            "pv_solar_high_in_target": reached,
            "beyond_training_pct": 100 * (reached / seen - 1),
        }
    return pd.DataFrame.from_dict(rows, orient="index").rename_axis("year")


# --------------------------------------------------------------------------------------------
# Daily skill, given each day's own weather
# --------------------------------------------------------------------------------------------

# The two sets of days every daily score is given for.
DAY_SETS = ["all days", "lowest days"]


def daily_errors(daily: pd.DataFrame, low: str, lowest_share: float) -> pd.DataFrame:
    """Return the miss of every model on every valid day, for one low.

    A day is valid when its actual low exists. Each year's lowest days are marked: the
    ``lowest_share`` of that year's valid days with the lowest actual values.

    Args:
        daily: The output of ``own_weather_predictions``.
        low: ``overnight`` or ``daytime``.
        lowest_share: Share of each year's valid days that count as its lowest days.

    Returns:
        One row per valid day and model: ``date``, ``year``, ``model``, ``error`` (actual minus
        predicted, MW) and ``lowest`` (True on that year's lowest days).
    """
    days = daily[daily["low"] == low].dropna(subset=["actual", "predicted"])
    days = days.assign(year=days["date"].dt.year, error=days["actual"] - days["predicted"])
    # Ranked within a year and model; every model has the same days, so the same days are marked.
    rank = days.groupby(["year", "model"])["actual"].rank(pct=True)
    columns = ["date", "year", "model", "error", "lowest"]
    return days.assign(lowest=rank <= lowest_share)[columns].reset_index(drop=True)


def daily_skill(errors: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    """Summarise daily misses, over all valid days and over the lowest days only.

    Args:
        errors: The output of ``daily_errors``.
        by: Columns to group by, for example ``["model"]`` or ``["year", "model"]``.

    Returns:
        One row per day set (``all days``, ``lowest days``) and group: the mean absolute error
        and the mean error (MW), and the number of days behind them.
    """
    scored = errors.assign(abs_error=errors["error"].abs())
    day_sets = dict(zip(DAY_SETS, [scored, scored[scored["lowest"]]], strict=True))
    summaries = {
        name: rows.groupby(by).agg(
            mae_mw=("abs_error", "mean"), mean_error_mw=("error", "mean"), days=("error", "size")
        )
        for name, rows in day_sets.items()
    }
    return pd.concat(summaries, names=["day_set"])


def compare_daily(errors: pd.DataFrame, pairs: dict, by: tuple[str, ...] = ()) -> pd.DataFrame:
    """Compare pairs of models on the mean absolute error of their daily predictions.

    Args:
        errors: The output of ``daily_errors``.
        pairs: A name for each comparison, mapped to ``(model, reference)``.
        by: Further columns to split by, for example ``("year",)``; none gives the totals.

    Returns:
        One row per comparison, day set and group: both mean absolute errors (MW), their
        difference and the change in per cent. A negative change means ``model`` misses by less
        than ``reference``.
    """
    mae = daily_skill(errors, [*by, "model"])["mae_mw"].unstack("model")
    rows = []
    for name, (model, reference) in pairs.items():
        rows.append(
            pd.DataFrame(
                {
                    "comparison": name,
                    "model": model,
                    "reference": reference,
                    "model_mae_mw": mae[model],
                    "reference_mae_mw": mae[reference],
                    "difference_mw": mae[model] - mae[reference],
                    "change_pct": 100 * (mae[model] / mae[reference] - 1),
                }
            )
        )
    return pd.concat(rows).reset_index().set_index(["comparison", "day_set", *by])


def daily_table(errors: pd.DataFrame, pairs: dict) -> pd.DataFrame:
    """Return Table IV: the daily skill of each model, then the pairs, for both sets of days.

    Args:
        errors: The output of ``daily_errors``.
        pairs: A name for each comparison, mapped to ``(model, reference)``.

    Returns:
        One row per model and then one per comparison. Columns are ``<day set>_<measure>``,
        the day set being ``all_days`` or ``lowest_days``. Model rows hold ``n`` (days),
        ``mae_mw`` and ``mean_error_mw``; comparison rows hold ``mae_difference_mw`` and
        ``mae_change_pct`` (negative when the first model misses by less).
    """
    by_model = daily_skill(errors, ["model"]).rename(columns={"days": "n"})
    by_pair = compare_daily(errors, pairs)[["difference_mw", "change_pct"]].add_prefix("mae_")
    table = pd.concat([part.unstack("day_set") for part in (by_model, by_pair)])
    # Put the two day sets side by side, each with its measures in the order built above.
    table = table.swaplevel(axis=1)[DAY_SETS]
    table.columns = [f"{day_set.replace(' ', '_')}_{name}" for day_set, name in table.columns]
    counts = [name for name in table.columns if name.endswith("_n")]
    return table.astype(dict.fromkeys(counts, "Int64")).rename_axis("row")
