"""Read rooftop photovoltaic (PV) capacity from Ausgrid's "average electricity use" workbooks.

Ausgrid publishes one workbook per financial year with a row per local government area and a
network "Total" row. Among its columns is the solar generation capacity (kWp) recorded as
connected at 30 June. Sheet names and column positions change from year to year, so the value is
found by its header text and the label of the Total row, never by position.

FY2015 and FY2016 give one capacity column. From FY2017 there are two, residential and
non-residential, and network capacity is their sum. The single early column is taken to cover
both (a decision recorded in ``publication/01_conference/analysis_plan.md``).
"""

from pathlib import Path

import numpy as np
import pandas as pd

CAPACITY_HEADER = "generation capacity (kwp)"


def read_total_kwp(path: str | Path) -> float:
    """Return network PV capacity (kWp) at 30 June from one workbook.

    Args:
        path: The local government area workbook for one financial year.
    """
    cells = pd.read_excel(path, sheet_name=0, header=None)
    # Compare text without case, padding or line breaks.
    text = cells.astype(str).apply(
        lambda column: column.str.replace(r"\s+", " ", regex=True).str.strip().str.lower()
    )

    # The capacity header; in later years it spans two sub-columns named on the row below.
    headers = np.argwhere((text == CAPACITY_HEADER).to_numpy())
    if len(headers) == 0:
        raise ValueError(f"no 'Generation capacity (kWp)' header found in {path}")
    header_row, first_column = headers[0]
    below = text.iloc[header_row + 1, first_column : first_column + 2]
    columns = [first_column + offset for offset, label in enumerate(below) if "(kwp)" in label]
    columns = columns or [first_column]

    # The network row is labelled exactly "Total"; the "Sub-total" rows are not wanted.
    total_row = (text[0] == "total").to_numpy().nonzero()[0][0]
    return float(cells.iloc[total_row, columns].sum())


def pv_capacity_series(cfg: dict) -> pd.Series:
    """Return network PV capacity (kWp) at 30 June of each year, checked against the config.

    Args:
        cfg: The configuration from ``config.load_config``.

    Returns:
        A series indexed by year. FY2024, published as PDF only, comes from the configuration.

    Raises:
        ValueError: If any year differs from the expected table by more than 1 kWp.
    """
    folder = Path(cfg["paths"]["pv_dir"])
    capacity = {
        year: read_total_kwp(folder / name) for year, name in cfg["paths"]["pv_files"].items()
    }
    capacity[2024] = float(cfg["pv"]["kwp_2024"])
    capacity = pd.Series(capacity).sort_index().rename_axis("year").rename("kwp")

    expected = pd.Series(cfg["pv"]["expected_kwp"])
    wrong = capacity[(capacity - expected).abs() > 1]
    if not capacity.index.equals(expected.index) or len(wrong):
        raise ValueError(f"PV capacity differs from the expected table: {wrong.to_dict()}")
    return capacity


def daily_pv(capacity_kwp: pd.Series, first_year: int, last_year: int) -> pd.Series:
    """Return daily PV capacity in MW over the study window.

    Capacity follows a straight line between consecutive 30 June values. Before the first value
    and after the last, the nearest line is extended at its own slope.

    Args:
        capacity_kwp: Capacity at 30 June, indexed by year.
        first_year: First calendar year of the study window.
        last_year: Last calendar year of the study window.
    """
    knots = pd.to_datetime([f"{year}-06-30" for year in capacity_kwp.index]).to_julian_date()
    mw = capacity_kwp.to_numpy() / 1000
    days = pd.date_range(f"{first_year}-01-01", f"{last_year}-12-31", freq="D", name="date")
    position = days.to_julian_date().to_numpy()

    daily = np.interp(position, knots, mw)
    # Interpolation holds the end values flat outside the known dates; extend the end lines.
    before, after = position < knots[0], position > knots[-1]
    first_slope = (mw[1] - mw[0]) / (knots[1] - knots[0])
    last_slope = (mw[-1] - mw[-2]) / (knots[-1] - knots[-2])
    daily[before] = mw[0] + first_slope * (position[before] - knots[0])
    daily[after] = mw[-1] + last_slope * (position[after] - knots[-1])
    return pd.Series(daily, index=days, name="pv_mw")
