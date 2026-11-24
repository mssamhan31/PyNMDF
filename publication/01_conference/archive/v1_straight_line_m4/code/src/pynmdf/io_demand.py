"""Read Ausgrid distribution zone substation files.

Ausgrid publishes one archive per reporting year (1 May to 30 April). Each archive holds one CSV
per zone substation, with one row per day and 96 columns of 15-minute MW. The layout drifts from
year to year; this module absorbs every variant found in FY2015 to FY2026 and returns one wide
frame per reporting year.

Time convention (Ausgrid's notes in the FY2015 archive): local clock time, and each column label
marks the END of its interval ("0:15" ... "24:00"). Frames returned here are indexed by interval
START, so all 96 intervals of a day carry that day's date.
"""

import io
import zipfile
from collections.abc import Iterator
from pathlib import Path

import pandas as pd

INTERVALS_PER_DAY = 96
META_COLUMNS = ("year", "zone substation", "date", "unit")
# Formats seen so far: 01MAY2014, 2024-05-01, 01/05/2023 (day first), 1-May-14.
DATE_FORMATS = ("%d%b%Y", "%Y-%m-%d", "%d/%m/%Y", "%d-%b-%y")
END_MINUTES = list(range(15, 24 * 60 + 1, 15))


def reporting_year_days(fy: int) -> pd.DatetimeIndex:
    """Return every calendar day of reporting year ``fy``: 1 May of the year before to 30 April."""
    return pd.date_range(f"{fy - 1}-05-01", f"{fy}-04-30", freq="D")


def _csv_payloads(source: Path) -> Iterator[tuple[str, bytes]]:
    """Yield (file name, raw bytes) for every CSV in a zip archive or a folder, at any depth."""
    if source.is_dir():
        for path in sorted(source.rglob("*.csv")):
            yield path.name, path.read_bytes()
    else:
        with zipfile.ZipFile(source) as archive:
            for name in sorted(archive.namelist()):
                if name.lower().endswith(".csv"):
                    yield Path(name).name, archive.read(name)


def _parse_dates(text: pd.Series) -> pd.Series:
    """Parse a date column written in any one of the formats Ausgrid has used."""
    for date_format in DATE_FORMATS:
        dates = pd.to_datetime(text, format=date_format, errors="coerce")
        if dates.notna().all():
            return dates
    raise ValueError(f"unrecognised date format, for example {text.iloc[0]!r}")


def _end_minute(label: str) -> int:
    """Return the minutes after midnight at which the interval named by a column label ends.

    "0:15" gives 15; "24:00" and "24:00:00" give 1440. FY2024 labels its last interval "00:00";
    continuity with the 23:45 column shows it is 24:00 of the same day, so 0 also gives 1440.
    """
    hours, minutes = label.split(":")[:2]
    return (int(hours) * 60 + int(minutes)) or 24 * 60


def read_substation(raw: bytes, days: pd.DatetimeIndex) -> pd.Series:
    """Read one substation CSV as a 15-minute MW series covering every interval of ``days``.

    Args:
        raw: Contents of the CSV file.
        days: Calendar days of the reporting year, in order.

    Returns:
        A series named after the substation and indexed by interval start. Days absent from the
        file are blank. A date that appears more than once keeps, for each interval, the first
        value that is not blank.
    """
    table = pd.read_csv(io.BytesIO(raw), dtype=str, encoding="utf-8-sig")
    table.columns = table.columns.str.strip()
    meta = {name.lower(): name for name in table.columns if name.lower() in META_COLUMNS}
    if set(meta) != set(META_COLUMNS):
        raise ValueError(f"expected the columns {META_COLUMNS}, found {list(table.columns[:4])}")
    units = set(table[meta["unit"]].str.strip().str.upper())
    if units != {"MW"}:
        raise ValueError(f"expected MW throughout, found units {units}")

    # Interval columns are ordered by the time their label names, not by position in the file:
    # recent files are out of order.
    labels = [name for name in table.columns if name not in meta.values()]
    end_minutes = [_end_minute(label) for label in labels]
    if sorted(end_minutes) != END_MINUTES:
        raise ValueError("interval labels do not cover 00:15 to 24:00 exactly once")
    # float() rejects anything that is not a number or blank, so a new oddity fails loudly.
    values = table[labels].astype(float).set_axis(end_minutes, axis=1).sort_index(axis=1)

    # One row per calendar day of the reporting year.
    values.index = _parse_dates(table[meta["date"]].str.strip())
    if not values.index.isin(days).all():
        raise ValueError("dates fall outside the reporting year")
    by_day = values.groupby(level=0).first().reindex(days)

    interval_starts = pd.date_range(days[0], periods=len(days) * INTERVALS_PER_DAY, freq="15min")
    name = table[meta["zone substation"]].iloc[0].strip()
    return pd.Series(by_day.to_numpy().ravel(), index=interval_starts, name=name)


def read_reporting_year(source: str | Path, fy: int) -> pd.DataFrame:
    """Read every substation of one reporting year.

    Args:
        source: The year's zip archive, or a folder holding its CSV files (nesting is ignored).
        fy: Reporting year, named by the year in which it ends (FY2015 is May 2014 to April 2015).

    Returns:
        A frame of 15-minute MW: one row per interval start from 1 May to 30 April, one column
        per substation. Blank where Ausgrid published nothing.
    """
    days = reporting_year_days(fy)
    substations = []
    for file_name, raw in _csv_payloads(Path(source)):
        try:
            substations.append(read_substation(raw, days))
        except ValueError as error:
            raise ValueError(f"FY{fy}, {file_name}: {error}") from error
    frame = pd.concat(substations, axis=1)
    if frame.columns.duplicated().any():
        repeated = sorted(frame.columns[frame.columns.duplicated()])
        raise ValueError(f"FY{fy}: substation names appear in more than one file: {repeated}")
    return frame
