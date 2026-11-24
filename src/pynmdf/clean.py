"""Clean the zone substation data and build the network total.

The steps below are applied to each reporting-year file, in this order
(``publication/01_conference/analysis_plan.md``, sections 3 and 5):

0. Column order. Days published with their 96 values in alphabetical order of interval number
   are put back in time order (most substations in April 2023).
1. Unit error. Every value between a substation's first and last value above 1,000 MW is divided
   by 1,000: those blocks were published in kW.
2. Invalid values. Outlier days and stuck runs are blanked.
3. 20% rule. A substation with more than 20% of its intervals blank or invalid is dropped.
4. Short gaps. Interior gaps of up to 2 hours are filled linearly within a substation.
5. Scale-up. Network total = sum of the reporting substations / their usual share of load.
6. Threshold. An interval is dropped when the reporting share is below 95%.
7. Half hours. Pairs of 15-minute totals are averaged; both must be valid.
8. The files are joined and cut to the study window.

The approach follows Haghdadi et al. (2018), who treat outliers and stuck constant values as
invalid and exclude substations with more than 20% missing or invalid data.

Throughout, ``x`` is a frame of 15-minute MW with one row per interval start and one column per
substation, as returned by ``io_demand.read_reporting_year``.
"""

from pathlib import Path
from typing import NamedTuple

import numpy as np
import pandas as pd

from pynmdf.io_demand import INTERVALS_PER_DAY, read_reporting_year

# --------------------------------------------------------------------------------------------
# Step 0: days published out of time order
# --------------------------------------------------------------------------------------------

# In a scrambled day the values sit in alphabetical order of interval number: 1, 10, 11 ... 19,
# 2, 20 ... 96. Position p therefore holds interval ALPHABETICAL_ORDER[p], and indexing a day
# with TIME_ORDER puts it back in time order.
ALPHABETICAL_ORDER = np.array(sorted(range(1, INTERVALS_PER_DAY + 1), key=str))
TIME_ORDER = np.argsort(ALPHABETICAL_ORDER)


def _roughness(days: np.ndarray) -> np.ndarray:
    """Return the mean absolute second difference along each day (axis 1); NaN if any blank."""
    return np.abs(np.diff(days, 2, axis=1)).mean(axis=1)


def restore_scrambled_days(x: pd.DataFrame, max_ratio: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Put back in time order the days published in alphabetical order of interval number.

    A load profile is smooth in time order and jagged in any other. Each complete substation-day
    is therefore tried both ways, and is taken to be scrambled when re-ordering it cuts its
    roughness to below ``max_ratio`` of the published value. Days with any blank are left alone.

    Returns:
        restored: ``x`` with the scrambled days re-ordered.
        scrambled: A True/False frame marking every cell of a re-ordered substation-day.
    """
    days = x.to_numpy().reshape(-1, INTERVALS_PER_DAY, x.shape[1])
    reordered = days[:, TIME_ORDER, :]
    # A comparison with NaN is False, so a day holding a blank is never flagged.
    scrambled = _roughness(reordered) < max_ratio * _roughness(days)
    restored = np.where(scrambled[:, None, :], reordered, days).reshape(x.shape)
    flags = np.repeat(scrambled, INTERVALS_PER_DAY, axis=0)
    return (
        pd.DataFrame(restored, index=x.index, columns=x.columns),
        pd.DataFrame(flags, index=x.index, columns=x.columns),
    )


# --------------------------------------------------------------------------------------------
# Steps 1 and 2: each function returns a True/False frame marking the cells it is about.
# --------------------------------------------------------------------------------------------


def unit_error_blocks(x: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """Flag every cell between a substation's first and last value above ``threshold``.

    Inside such a block the whole record is in kW, including values below the threshold (loads
    under 1 MW), so the block is corrected as one piece rather than value by value.
    """
    above = x.abs() > threshold
    seen_before = above.cummax()
    seen_after = above[::-1].cummax()[::-1]
    return seen_before & seen_after


def outlier_days(x: pd.DataFrame, ratio: float, quantile: float) -> pd.DataFrame:
    """Flag whole substation-days whose median sits far above that substation's usual level.

    A day is flagged when its median absolute value exceeds ``ratio`` times the substation's
    ``quantile`` of absolute values over the file. This catches sustained scale errors (Morisset
    in FY2022 reads about 15 times too high for seven weeks) while leaving ordinary peaks alone.
    """
    size = x.abs()
    usual = size.quantile(quantile)
    day_of = x.index.normalize()
    daily_median = size.groupby(day_of).median()
    flagged = daily_median.gt(ratio * usual, axis=1) & (usual > 0)
    return flagged.reindex(day_of).set_axis(x.index)


def _run_lengths(values: np.ndarray) -> np.ndarray:
    """Return, for each element, the length of the run of equal consecutive values it sits in.

    NaN never equals NaN, so each blank counts as a run of one.
    """
    starts = np.ones(len(values), dtype=bool)
    starts[1:] = values[1:] != values[:-1]
    run_id = np.cumsum(starts) - 1
    return np.bincount(run_id)[run_id]


def _by_column(x: pd.DataFrame, function) -> pd.DataFrame:
    """Apply a NumPy function to each column and keep the frame's labels."""
    return pd.DataFrame({name: function(x[name].to_numpy()) for name in x.columns}, index=x.index)


def stuck_runs(x: pd.DataFrame, min_run: int) -> pd.DataFrame:
    """Flag values sitting in a run of one repeated value at least ``min_run`` intervals long.

    Zero counts as a value: City Central reads exactly zero for eight months of FY2021 while its
    neighbours carry no extra load, so a long run of zeros is a data hole, not an outage.
    """
    return _by_column(x, lambda column: _run_lengths(column) >= min_run)


# --------------------------------------------------------------------------------------------
# Steps 3 to 7
# --------------------------------------------------------------------------------------------


def drop_sparse_substations(x: pd.DataFrame, max_missing: float) -> pd.DataFrame:
    """Keep the substations whose share of blank intervals is at most ``max_missing``."""
    return x.loc[:, x.isna().mean() <= max_missing]


def fill_short_gaps(x: pd.DataFrame, max_gap: int) -> pd.DataFrame:
    """Fill interior gaps of up to ``max_gap`` intervals by linear interpolation.

    Longer gaps stay wholly blank (they are not part-filled), as do blanks at either end.
    """
    gap = x.isna()
    gap_length = _by_column(gap, _run_lengths)
    return x.interpolate(limit_area="inside").where(~gap | (gap_length <= max_gap))


def network_total(x: pd.DataFrame) -> pd.DataFrame:
    """Sum the reporting substations and scale up by their usual share of network load.

    A substation's usual share is its mean load over the file divided by the sum of the mean
    loads of all substations in ``x``.

    Returns:
        A frame with ``total_mw`` (the scaled-up total) and ``reporting_share`` (the share of
        usual load that reported in that interval, between 0 and 1).
    """
    usual_share = x.mean() / x.mean().sum()
    reporting_share = x.notna().mul(usual_share).sum(axis=1)
    return pd.DataFrame(
        {"total_mw": x.sum(axis=1) / reporting_share, "reporting_share": reporting_share}
    )


def to_half_hour(quarter_hourly: pd.Series) -> pd.Series:
    """Average pairs of 15-minute values; a half hour is valid only when both parts are."""
    pairs = quarter_hourly.resample("30min")
    return pairs.mean().where(pairs.count() == 2)


# --------------------------------------------------------------------------------------------
# One reporting-year file
# --------------------------------------------------------------------------------------------


def clean_reporting_year(
    raw: pd.DataFrame, cleaning: dict
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Apply steps 0 to 5 to one reporting-year file.

    Args:
        raw: 15-minute MW by substation, as read from the file.
        cleaning: The ``cleaning`` section of the configuration.

    Returns:
        substations: The kept substations, invalid values blanked and short gaps filled.
        network: ``total_mw`` and ``reporting_share`` every 15 minutes (see ``network_total``).
        quality: What each step did, as one row of the data-quality table.
    """
    # Step 0: days published out of time order.
    ordered, scrambled = restore_scrambled_days(raw, cleaning["scrambled_roughness_ratio"])

    # Step 1: kW blocks back to MW.
    blocks = unit_error_blocks(ordered, cleaning["unit_threshold_mw"])
    fixed = ordered.where(~blocks, ordered / 1000)

    # Step 2: blank what cannot be real load.
    outliers = outlier_days(fixed, cleaning["outlier_ratio"], cleaning["outlier_quantile"])
    stuck = stuck_runs(fixed, cleaning["stuck_run_intervals"])
    valid = fixed.mask(outliers | stuck)

    # Steps 3 to 5.
    kept = drop_sparse_substations(valid, cleaning["max_missing_share"])
    dropped = valid.drop(columns=kept.columns)
    substations = fill_short_gaps(kept, cleaning["max_gap_intervals"])
    network = network_total(substations)

    # A dropped substation is not scaled up, so its load leaves the total. Report how much:
    # its mean load with blanks counted as zero, against the mean load of the kept set.
    dropped_load = dropped.fillna(0).mean().sum()
    quality = {
        "substations_read": raw.shape[1],
        "scrambled_days_restored": int(scrambled.sum().sum() // INTERVALS_PER_DAY),
        "unit_values_corrected": int((blocks & ordered.notna()).sum().sum()),
        "unit_substations": int(blocks.any().sum()),
        "outlier_substation_days": int(outliers.sum().sum() // INTERVALS_PER_DAY),
        "stuck_values": int(stuck.sum().sum()),
        "substations_dropped": dropped.shape[1],
        "dropped_wholly_blank": int(raw[dropped.columns].isna().all().sum()),
        "dropped_load_mw": dropped_load,
        "dropped_load_pct": 100 * dropped_load / substations.mean().sum(),
        "substations_kept": kept.shape[1],
        "substations_with_negatives": int((fixed < 0).any().sum()),
        "all_reporting_pct": 100 * substations.notna().all(axis=1).mean(),
        "kept_pct": 100 * (network["reporting_share"] >= cleaning["min_reporting_share"]).mean(),
    }
    return substations, network, quality


def diagnostic_minimum(raw: pd.DataFrame, cleaning: dict) -> float:
    """Reproduce the stress-test minimum for one file. A check on the reader, not the final rule.

    The stress test used the unit fix, the 20% rule, a 2-hour fill and only the intervals where
    every kept substation reports. Its fill was pandas' limit-based interpolation, which also
    fills the first 2 hours of longer gaps; that behaviour is copied here, and only here, so the
    numbers are comparable.
    """
    blocks = unit_error_blocks(raw, cleaning["unit_threshold_mw"])
    kept = drop_sparse_substations(raw.where(~blocks, raw / 1000), cleaning["max_missing_share"])
    filled = kept.interpolate(limit=cleaning["max_gap_intervals"])
    complete = filled.sum(axis=1).where(filled.notna().all(axis=1))
    return to_half_hour(complete).min()


def daytime_low_means(
    substations: pd.DataFrame,
    network: pd.DataFrame,
    daytime_hours: list[int],
    n_lowest: int,
    min_share: float,
) -> pd.Series:
    """Return each substation's mean over the network's lowest daytime intervals.

    Used only by the sign check: a substation exporting at the network's midday lows shows a
    negative mean where reverse flow is signed, and a small positive one where it is not.
    """
    start, end = daytime_hours
    hour = network.index.hour
    eligible = (hour >= start) & (hour < end) & (network["reporting_share"] >= min_share)
    lowest = network.loc[eligible, "total_mw"].nsmallest(n_lowest).index
    return substations.loc[lowest].mean()


# --------------------------------------------------------------------------------------------
# All reporting years
# --------------------------------------------------------------------------------------------


def _first_sunday(year: int, month: int) -> pd.Timestamp:
    """Return the first Sunday of a month: when NSW clocks change, in October and in April."""
    first = pd.Timestamp(year, month, 1)
    return first + pd.Timedelta(days=(6 - first.dayofweek) % 7)


def _morning_rise_slot(x: pd.DataFrame, hours: list[float]) -> pd.Series:
    """Return, per substation, the 15-minute slot at which weekday load rises fastest.

    The slot is counted from midnight and searched for between ``hours[0]`` and ``hours[1]``.
    Substations with a blank anywhere in that part of their mean profile are left out.
    """
    weekdays = x[x.index.dayofweek < 5]
    slot = weekdays.index.hour * 4 + weekdays.index.minute // 15
    profile = weekdays.groupby(slot).mean().reindex(range(INTERVALS_PER_DAY))
    rise = profile.shift(-2) - profile.shift(2)  # change over the hour centred on each slot
    morning = rise.iloc[int(hours[0] * 4) : int(hours[1] * 4)]
    return morning.loc[:, morning.notna().all()].idxmax()


def clock_check(substations: pd.DataFrame, fy: int, checks: dict) -> dict:
    """Measure how much load appears to keep standard time through daylight saving.

    People follow the clock, so the morning rise in demand should sit at the same clock time
    before and after a clock change. A substation whose rise moves about an hour EARLIER when
    daylight saving starts in October (and back LATER when it ends in April) is being published
    in standard time. The test is indirect: ordinary seasonal drift is one or two slots.

    Args:
        substations: Cleaned 15-minute MW by substation for one reporting year.
        fy: The reporting year, which holds one October and one April clock change.
        checks: The ``checks`` section of the configuration.

    Returns:
        For each clock change, the share of load (per cent, among substations large enough to
        test) whose morning rise moves earlier, and later, by at least the configured shift.
    """
    window = pd.Timedelta(days=checks["clock_check_days"])
    one_day, one_interval = pd.Timedelta(days=1), pd.Timedelta(minutes=15)
    load = substations.mean()
    shares = {}
    for name, change in (("october", _first_sunday(fy - 1, 10)), ("april", _first_sunday(fy, 4))):
        # The change day itself is skipped: it has a missing or a repeated hour.
        before = substations[change - window : change - one_interval]
        after = substations[change + one_day : change + one_day + window - one_interval]
        hours = checks["clock_check_hours"]
        shift = (_morning_rise_slot(after, hours) - _morning_rise_slot(before, hours)).dropna()
        shift = shift[load[shift.index] > checks["clock_check_min_mw"]]
        weight = load[shift.index] / load[shift.index].sum()
        shares[f"{name}_earlier_pct"] = (
            100 * weight[shift <= -checks["clock_check_min_shift"]].sum()
        )
        shares[f"{name}_later_pct"] = 100 * weight[shift >= checks["clock_check_min_shift"]].sum()
    return shares


class NetworkBuild(NamedTuple):
    """Everything notebook 01 needs from one pass over the raw files."""

    network: pd.DataFrame  # total_mw and reporting_share, every 15 minutes, all reporting years
    quality: pd.DataFrame  # one row per reporting-year file
    daytime_lows: pd.DataFrame  # substation by reporting year: mean MW at the daytime lows
    clocks: pd.DataFrame  # one row per reporting-year file: load whose morning rise moves


def build_network_total(cfg: dict) -> NetworkBuild:
    """Read and clean every reporting year and join them into one 15-minute network series.

    Args:
        cfg: The configuration from ``config.load_config``.

    Returns:
        A ``NetworkBuild``. The network series runs unbroken from the first interval of the first
        reporting year to the last interval of the last; the threshold, the half-hour averaging
        and the cut to the study window are applied afterwards by ``half_hourly_total``.
    """
    cleaning, checks = cfg["cleaning"], cfg["checks"]
    networks, quality, lows, clocks = [], {}, {}, {}
    for fy, entry in cfg["paths"]["demand_files"].items():
        raw = read_reporting_year(Path(cfg["paths"]["demand_dir"]) / entry, fy)
        substations, network, quality[fy] = clean_reporting_year(raw, cleaning)
        quality[fy]["diagnostic_min_mw"] = diagnostic_minimum(raw, cleaning)
        clocks[fy] = clock_check(substations, fy, checks)
        lows[fy] = daytime_low_means(
            substations,
            network,
            cfg["targets"]["troughs"]["daytime"],
            checks["sign_check_intervals"],
            cleaning["min_reporting_share"],
        )
        networks.append(network)

    # Step 8: the files must join with no repeated or missing interval at the 1 May boundaries.
    network = pd.concat(networks)
    unbroken = pd.date_range(network.index[0], network.index[-1], freq="15min")
    if not network.index.equals(unbroken):
        raise ValueError("reporting years do not join into one unbroken 15-minute series")

    quality = pd.DataFrame.from_dict(quality, orient="index").rename_axis("reporting_year")
    quality["stress_test_min_mw"] = pd.Series(checks["stress_test_minima_mw"])
    return NetworkBuild(
        network=network,
        quality=quality,
        daytime_lows=pd.DataFrame(lows).rename_axis("substation"),
        clocks=pd.DataFrame.from_dict(clocks, orient="index").rename_axis("reporting_year"),
    )


def half_hourly_total(
    network: pd.DataFrame, min_share: float, first_year: int, last_year: int
) -> pd.Series:
    """Apply steps 6 to 8: reporting threshold, half-hour averages, cut to the study window.

    Args:
        network: 15-minute ``total_mw`` and ``reporting_share`` from ``build_network_total``.
        min_share: Lowest reporting share at which an interval is kept.
        first_year: First calendar year of the study window.
        last_year: Last calendar year of the study window.

    Returns:
        The 30-minute network total in MW, indexed by interval start, blank where invalid.
    """
    kept = network["total_mw"].where(network["reporting_share"] >= min_share)
    return to_half_hour(kept).loc[str(first_year) : str(last_year)].rename("total_mw")


def join_steps(total: pd.Series, nights: int = 7) -> pd.DataFrame:
    """Measure the level step at each 1 May join between reporting-year files.

    For every night, the change across midnight is the mean of the first hour of the new day
    minus the mean of the last hour of the old day. Its usual value is the median over the
    ``nights`` nights either side. What is left over at a join is the step between the two files.

    Args:
        total: The 30-minute network total.
        nights: Nights either side of each night used for the usual change.

    Returns:
        One row per join, named by the year of its 1 May: the change at the join, the usual
        change, the step (MW, and as a percentage of the level before midnight), and the step's
        rank among all nights of the series (1 is the largest upward step).
    """
    pairs = total.resample("h")
    hourly = pairs.mean().where(pairs.count() == 2)
    last_hour = hourly[hourly.index.hour == 23]
    first_hour = hourly[hourly.index.hour == 0]
    # Label both by the midnight between them so they align.
    last_hour = last_hour.set_axis(last_hour.index + pd.Timedelta(hours=1))
    change = (first_hour - last_hour).dropna()
    change = change.reindex(pd.date_range(change.index[0], change.index[-1], freq="D"))
    usual = change.rolling(2 * nights + 1, center=True, min_periods=nights + 1).median()
    step = change - usual

    steps = pd.DataFrame(
        {
            "change_mw": change,
            "usual_change_mw": usual,
            "step_mw": step,
            "step_pct": 100 * step / last_hour,
            "rank": step.rank(ascending=False),
            "nights_ranked": step.notna().sum(),
        }
    )
    joins = steps[(steps.index.month == 5) & (steps.index.day == 1)]
    return joins.set_axis(joins.index.year).rename_axis("join_at_1_may")


def reporting_year(index: pd.DatetimeIndex) -> np.ndarray:
    """Return the reporting year each timestamp falls in: 1 May to 30 April, named by its end."""
    return (index.year + (index.month >= 5)).to_numpy()


def join_factors(steps: pd.DataFrame) -> pd.Series:
    """Return the constant each reporting-year file is multiplied by so that its joins meet.

    The latest file keeps its level. Working back from it, each earlier file takes the factor
    of the file after it, times one plus the step measured at the join between them: that lifts
    or lowers the earlier file to meet the later one. A join whose step could not be measured
    gets no adjustment.

    The steps chain, so the factors compound from the latest file back to the first. The result
    is a bounding case, which treats every step as an error of level in the earlier file; it is
    not a better estimate of the network total.

    Args:
        steps: The output of ``join_steps``.

    Returns:
        The factor for each reporting year, from the first file to the latest.
    """
    ratio = 1 + steps["step_pct"].fillna(0) / 100
    # The join at 1 May of year y closes reporting year y, so the product of the ratios from
    # that join onwards is the factor of file y.
    factors = ratio[::-1].cumprod()[::-1]
    factors.loc[factors.index.max() + 1] = 1.0
    return factors.rename_axis("reporting_year").rename("factor")


def rescale_reporting_years(total: pd.Series, factors: pd.Series) -> pd.Series:
    """Multiply every value by the factor of the reporting-year file it came from.

    Args:
        total: The 30-minute network total.
        factors: The output of ``join_factors``.

    Returns:
        The rescaled network total, on the same index.
    """
    return total * factors.reindex(reporting_year(total.index)).to_numpy()


def sign_check(build: NetworkBuild, reference_year: int) -> pd.DataFrame:
    """Quantify the change in sign convention across files. No correction is made.

    Takes the substations whose mean is negative at the reference year's lowest daytime
    intervals and follows the same substations through every file. Where reverse flow is
    recorded unsigned, their sum is positive instead of negative.

    Returns:
        One row per reporting year: substations holding any negative value, how many of the
        reference substations the file contains, their summed mean (MW), and the summed mean of
        all substations that are negative at that file's own lowest daytime intervals (MW).
    """
    lows = build.daytime_lows
    reference = lows.index[lows[reference_year] < 0]
    return pd.DataFrame(
        {
            "substations_with_negatives": build.quality["substations_with_negatives"],
            "reference_substations_found": lows.loc[reference].notna().sum(),
            "reference_substations_mw": lows.loc[reference].sum(),
            "all_negative_mw": lows.where(lows < 0).sum(),
        }
    ).rename_axis("reporting_year")
