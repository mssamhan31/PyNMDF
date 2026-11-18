"""Tests 2, 3 and 8: invalid values are marked; the network total fills, scales and thresholds;
and the rescaling used by the robustness check closes the joins between reporting years.

All data are synthetic and small enough to check by hand.
"""

import numpy as np
import pandas as pd

from pynmdf import clean


def _frame(columns: dict, start="2022-08-01") -> pd.DataFrame:
    """Build a 15-minute frame from equal-length arrays."""
    length = len(next(iter(columns.values())))
    index = pd.date_range(start, periods=length, freq="15min")
    return pd.DataFrame(columns, index=index, dtype=float)


def test_invalid_values_are_marked():
    # --- Scrambled days: day 2 of three is written in alphabetical order of interval number
    #     (1, 10, 11 ... 19, 2, 20 ...). It is put back; smooth days and days with a blank are not.
    smooth = 10 + 5 * np.sin(np.linspace(0, 2 * np.pi, 96))
    published = np.concatenate([smooth, smooth[clean.ALPHABETICAL_ORDER - 1], smooth])
    with_blank = published.copy()
    with_blank[100] = np.nan
    restored, scrambled = clean.restore_scrambled_days(
        _frame({"a": published, "b": with_blank}), max_ratio=0.5
    )
    assert np.allclose(restored["a"], np.tile(smooth, 3))
    assert scrambled["a"].to_numpy().nonzero()[0].tolist() == list(range(96, 192))
    assert not scrambled["b"].any()

    # --- Unit block: a kW block that contains a value below the threshold (a load under 1 MW).
    load = np.full(40, 5.0)
    load[10:20] = [5000, 4800, 800, 5200, np.nan, 5100, 950, 4900, 5000, 5300]
    blocks = clean.unit_error_blocks(_frame({"a": load, "b": np.full(40, 7.0)}), threshold=1000)
    assert blocks["a"].to_numpy().nonzero()[0].tolist() == list(range(10, 20))
    assert not blocks["b"].any()

    # --- Stuck runs: 96 equal values are stuck, 95 are not; zero counts as a value.
    rng = np.random.default_rng(0)
    varying = rng.uniform(1, 2, 400)
    stuck_96, stuck_95, zeros = varying.copy(), varying.copy(), varying.copy()
    stuck_96[100:196] = 3.3
    stuck_95[100:195] = 3.3
    zeros[100:196] = 0.0
    stuck = clean.stuck_runs(_frame({"s96": stuck_96, "s95": stuck_95, "zero": zeros}), 96)
    assert stuck["s96"].to_numpy().nonzero()[0].tolist() == list(range(100, 196))
    assert not stuck["s95"].any()
    assert stuck["zero"].sum() == 96

    # --- Outlier days: ten days of ordinary load, with day 4 reading fifteen times too high.
    ordinary = np.tile(np.linspace(5, 10, 96), 10)
    inflated = ordinary.copy()
    inflated[3 * 96 : 4 * 96] *= 15
    outliers = clean.outlier_days(_frame({"ok": ordinary, "bad": inflated}), 5, 0.75)
    assert not outliers["ok"].any()
    assert outliers["bad"].to_numpy().nonzero()[0].tolist() == list(range(3 * 96, 4 * 96))


def test_network_total_fills_scales_and_thresholds():
    # --- Gap fill: an 8-interval gap is filled linearly; a 9-interval gap and the edges are not.
    ramp = np.arange(60, dtype=float)
    gappy = ramp.copy()
    gappy[[0, 59]] = np.nan  # edges
    gappy[10:18] = np.nan  # 8 intervals
    gappy[30:39] = np.nan  # 9 intervals
    filled = clean.fill_short_gaps(_frame({"a": gappy}), max_gap=8)["a"].to_numpy()
    assert np.allclose(filled[10:18], ramp[10:18])
    assert np.isnan(filled[30:39]).all()
    assert np.isnan(filled[[0, 59]]).all()

    # --- Scale-up: A carries 75% of load and B 25%. With B blank, A alone scales to the true 40.
    a, b = np.full(16, 30.0), np.full(16, 10.0)
    b[5] = np.nan
    network = clean.network_total(_frame({"a": a, "b": b}))
    assert network.dtypes.eq("float64").all()
    assert np.allclose(network["total_mw"], 40.0)
    assert np.isclose(network["reporting_share"].iloc[5], 0.75)
    assert np.allclose(network["reporting_share"].drop(network.index[5]), 1.0)

    # --- Threshold and half hours: the 75% interval falls below 95%, so its half hour is
    #     dropped; every other half hour is the mean of two valid quarters.
    half_hourly = clean.half_hourly_total(network, min_share=0.95, first_year=2022, last_year=2022)
    assert half_hourly.isna().to_numpy().nonzero()[0].tolist() == [2]
    assert np.allclose(half_hourly.dropna(), 40.0)
    assert len(half_hourly) == 8


def test_rescaling_closes_the_joins_between_reporting_years():
    # --- A flat load published at a different level in each reporting-year file. The file that
    #     starts on 1 May 2020 reads 10% above the one before it; the next reads 20% below that;
    #     the last starts level with it.
    index = pd.date_range("2020-01-01", "2022-12-31 23:30", freq="30min")
    published = {2020: 1000.0, 2021: 1100.0, 2022: 880.0, 2023: 880.0}
    total = pd.Series(clean.reporting_year(index), index=index).map(published)

    # 30 April belongs to the file that ends on it, 1 May to the next.
    assert total["2021-04-30 23:30"] == 1100.0 and total["2021-05-01 00:00"] == 880.0

    steps = clean.join_steps(total)
    assert np.allclose(steps["step_pct"], [10.0, -20.0, 0.0])

    # The latest file keeps its level and the earlier ones are brought to it, one join at a time.
    factors = clean.join_factors(steps)
    assert factors.index.tolist() == [2020, 2021, 2022, 2023]
    assert np.allclose(factors, [0.8 * 1.1, 0.8, 1.0, 1.0])
    rescaled = clean.rescale_reporting_years(total, factors)
    assert np.allclose(rescaled, 880.0)
    assert np.allclose(clean.join_steps(rescaled)["step_mw"], 0.0)

    # --- A join that cannot be measured (no data in the hour before it) gets no adjustment.
    blank = total.copy()
    blank["2021-04-30 23:00":"2021-04-30 23:30"] = np.nan
    unmeasured = clean.join_factors(clean.join_steps(blank))
    assert np.allclose(unmeasured, [1.1, 1.0, 1.0, 1.0])
