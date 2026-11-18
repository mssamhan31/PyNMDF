"""The daily models M2 to M6.

Each model predicts two numbers for every day: the overnight low and the daytime low. The day's
minimum is the lower of the two. All are fitted on the same days and differ only in what they are
given. M2 to M5 are a nested ladder, each step changing one thing:

- M2 Time trend: calendar (month, non-working day) and time, with a slope per month.
- M3 PV only: as M2, with PV capacity in place of time.
- M4 PV + weather: M3 plus PV x solar exposure, maximum temperature and minimum temperature.
- M5 PV + weather (XGBoost): the same information as M4, in a tree model.

M6 PV only (XGBoost) is M3's information in a tree model. It was added after the scores of M1 to
M5 had been seen, so that M5 against M6 shows what weather adds in tree form; it is supplementary
and takes no part in the two pre-set comparisons (M3 against M2, M4 against M3).

A non-working day is a Saturday, a Sunday or a public holiday. It is one flag, not two: with
separate weekend and holiday flags the linear models added the two effects on a holiday that fell
on a weekend and predicted it about 1,000 MW below a working day, far below what such days do.

M1 (naive) needs no fit and lives in ``poe.naive_forecasts``.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor

from pynmdf.targets import public_holidays

TROUGHS = ["overnight", "daytime"]
TEMPERATURE = ["tmax", "tmin"]
WEATHER = ["pv_solar", *TEMPERATURE]
CALENDAR_AND_PV = ["month", "non_working", "pv"]

# The models are data, not code: each is an estimator and the columns it may use.
MODELS = {
    "M2": {"estimator": "linear", "trend": "time", "weather": []},
    "M3": {"estimator": "linear", "trend": "pv", "weather": []},
    "M4": {"estimator": "linear", "trend": "pv", "weather": WEATHER},
    "M5": {"estimator": "xgboost", "columns": [*CALENDAR_AND_PV, *WEATHER]},
    "M6": {"estimator": "xgboost", "columns": CALENDAR_AND_PV},
}

# M4 with one group of weather terms switched off. These are a diagnostic, used to see which
# terms pull M4's forecasts down; they are not models of the study and are never scored with it.
M4_VARIANTS = {
    "M4 without temperature": {"estimator": "linear", "trend": "pv", "weather": ["pv_solar"]},
    "M4 without PV x solar": {"estimator": "linear", "trend": "pv", "weather": TEMPERATURE},
}

# Everything that can be fitted. A model's position here seeds its random draws, so entries are
# only ever added at the end: adding one must not change the draws of another.
SPECS = MODELS | M4_VARIANTS

# Short labels for Table I.
MODEL_INFO = pd.DataFrame(
    [
        ("M1", "Naive", "Annual or monthly values", "No", "No", "Past errors"),
        ("M2", "Time trend", "Daily lows", "No", "No", "Replay of past residuals"),
        ("M3", "PV only", "Daily lows", "Yes", "No", "Replay of past residuals"),
        ("M4", "PV + weather, linear", "Daily lows", "Yes", "Yes", "Weather replay and residuals"),
        ("M5", "PV + weather, XGBoost", "Daily lows", "Yes", "Yes", "Weather replay and residuals"),
        ("M6", "PV only, XGBoost", "Daily lows", "Yes", "No", "Replay of past residuals"),
    ],
    columns=["ID", "Model", "Fitted on", "PV", "Weather", "POE from"],
)


def calendar_features(
    dates: pd.DatetimeIndex, pv: pd.Series, subdivision: str, time_zero: pd.Timestamp
) -> pd.DataFrame:
    """Return the predictors that depend only on the date: calendar, time and PV capacity.

    Args:
        dates: The days to describe.
        pv: Daily PV capacity in MW, indexed by date.
        subdivision: State code for the public holiday calendar.
        time_zero: The date at which ``time`` is zero.

    Returns:
        One row per date: ``month`` (1 to 12), ``non_working`` (1 on a Saturday, a Sunday or a
        public holiday, otherwise 0), ``time`` (years since ``time_zero``) and ``pv`` (MW).
    """
    weekend = dates.dayofweek >= 5
    holiday = (public_holidays(dates, subdivision) != "").to_numpy()
    return pd.DataFrame(
        {
            "month": dates.month,
            "non_working": (weekend | holiday).astype(float),
            "time": (dates - time_zero).days / 365.25,
            "pv": pv.reindex(dates).to_numpy(),
        },
        index=dates,
    )


def add_weather(calendar: pd.DataFrame, weather: pd.DataFrame) -> pd.DataFrame:
    """Add the weather predictors to the calendar predictors, row for row.

    The rows of ``weather`` are taken in order, whatever their dates, so that the weather replay
    can lay another year's weather over the target year's calendar.

    Args:
        calendar: The output of ``calendar_features``.
        weather: ``tmax``, ``tmin`` (degrees C) and ``solar`` (MJ/m2), one row per calendar row.

    Returns:
        ``calendar`` with ``tmax``, ``tmin`` and ``pv_solar`` (PV capacity times solar exposure).
    """
    return calendar.assign(
        tmax=weather["tmax"].to_numpy(),
        tmin=weather["tmin"].to_numpy(),
        pv_solar=calendar["pv"].to_numpy() * weather["solar"].to_numpy(),
    )


def _design(features: pd.DataFrame, model: str) -> pd.DataFrame:
    """Return the columns a model is fitted on.

    For the linear models that is twelve month intercepts, twelve month-specific slopes on the
    trend (time or PV), the non-working-day flag and any weather columns. XGBoost takes its raw
    columns and finds the interactions itself.
    """
    spec = SPECS[model]
    if spec["estimator"] == "xgboost":
        return features[spec["columns"]]
    months = pd.get_dummies(features["month"], dtype=float).reindex(
        columns=range(1, 13), fill_value=0.0
    )
    slopes = months.mul(features[spec["trend"]], axis=0)
    return pd.concat(
        [
            months.add_prefix("month_"),
            slopes.add_prefix(f"{spec['trend']}_in_month_"),
            features[["non_working", *spec["weather"]]],
        ],
        axis=1,
    )


def fit_daily(features: pd.DataFrame, troughs: pd.DataFrame, model: str, xgboost: dict) -> dict:
    """Fit one model: a separate fit for the overnight low and for the daytime low.

    Args:
        features: Predictors, one row per training day.
        troughs: The overnight and daytime low of the same days.
        model: A name in ``SPECS``: "M2" to "M6", or a diagnostic variant of M4.
        xgboost: Settings for the XGBoost estimator (used by M5 and M6 only).

    Returns:
        The fitted estimator for each trough.
    """
    design = _design(features, model)

    def new_estimator():
        if SPECS[model]["estimator"] == "xgboost":
            return XGBRegressor(**xgboost)
        # The month columns already carry the intercepts.
        return LinearRegression(fit_intercept=False)

    return {trough: new_estimator().fit(design, troughs[trough]) for trough in TROUGHS}


def linear_coefficients(fitted: dict, features: pd.DataFrame, model: str) -> pd.DataFrame:
    """Return the coefficients of a fitted linear model, one row per term and column per trough.

    Args:
        fitted: The output of ``fit_daily`` for a linear model.
        features: Any rows of the predictors it was fitted on; only the column names are used.
        model: The model's name in ``SPECS``.
    """
    terms = _design(features.iloc[:1], model).columns
    return pd.DataFrame({trough: fitted[trough].coef_ for trough in TROUGHS}, index=terms)


def predict_daily(fitted: dict, features: pd.DataFrame, model: str) -> pd.DataFrame:
    """Predict the overnight and daytime low for each row of ``features``."""
    design = _design(features, model)
    return pd.DataFrame(
        {trough: fitted[trough].predict(design) for trough in TROUGHS}, index=features.index
    )


def out_of_fold_residuals(
    features: pd.DataFrame, troughs: pd.DataFrame, model: str, xgboost: dict
) -> pd.DataFrame:
    """Return each training day's residual from a fit that never saw that day's year.

    A model's errors on days it was fitted on are too small. So each calendar year is left out
    in turn, the model is refitted on the rest, and its errors on the left-out year are kept.

    Returns:
        Actual minus predicted for both troughs, one row per training day.
    """
    year = features.index.year
    residuals = []
    for left_out in np.unique(year):
        rest, held = year != left_out, year == left_out
        fitted = fit_daily(features[rest], troughs[rest], model, xgboost)
        residuals.append(troughs.loc[held, TROUGHS] - predict_daily(fitted, features[held], model))
    return pd.concat(residuals)
