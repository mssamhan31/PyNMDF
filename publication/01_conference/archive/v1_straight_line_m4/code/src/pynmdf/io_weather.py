"""Read daily weather from Bureau of Meteorology Climate Data Online files.

Three daily files for one station (066037, Sydney Airport AMO): maximum temperature, minimum
temperature and global solar exposure. Conventions, from the note file that comes with each:

- The minimum temperature is the lowest in the 24 hours to 9 am and is recorded against that
  day, so it describes the early morning of its date.
- The maximum temperature is the highest in the 24 hours from 9 am and is recorded against the
  day the period starts, so it describes the afternoon of its date.
- Solar exposure is derived from satellite images, not measured at the station, and is in
  MJ/m2 (the folder name says kWh; the file header is right).
- Temperature quality flag Y means quality control is complete; N means it is not yet complete
  or the date is uncertain. Values flagged N are used.
"""

from pathlib import Path

import pandas as pd

from pynmdf.clean import fill_short_gaps

VALUE_COLUMNS = {
    "tmax": "Maximum temperature (Degree C)",
    "tmin": "Minimum temperature (Degree C)",
    "solar": "Daily global solar exposure (MJ/m*m)",
}


def _read_file(path: Path) -> pd.DataFrame:
    """Read one BOM daily file, indexed by date."""
    table = pd.read_csv(path)
    dates = pd.to_datetime(table[["Year", "Month", "Day"]].rename(columns=str.lower))
    return table.set_index(dates.rename("date"))


def read_weather(cfg: dict) -> pd.DataFrame:
    """Return daily weather exactly as published, with gaps left blank.

    Args:
        cfg: The configuration from ``config.load_config``.

    Returns:
        One row per calendar day from 1 January of ``weather.first_year`` to 31 December of the
        last study year, with columns ``tmax`` and ``tmin`` (degrees C) and ``solar`` (MJ/m2).
    """
    folder = Path(cfg["paths"]["weather_dir"])
    files = cfg["paths"]["weather_files"]
    published = {
        key: _read_file(folder / files[key])[column] for key, column in VALUE_COLUMNS.items()
    }
    days = pd.date_range(
        f"{cfg['weather']['first_year']}-01-01", f"{cfg['study']['last_year']}-12-31", name="date"
    )
    return pd.DataFrame(published).reindex(days)


def temperature_quality(cfg: dict) -> pd.DataFrame:
    """Count the BOM quality flags on the two temperature series over the study window.

    Returns:
        Days by flag (Y, N, or missing) for ``tmax`` and ``tmin``. Solar exposure has no flag.
    """
    folder = Path(cfg["paths"]["weather_dir"])
    window = slice(str(cfg["study"]["first_year"]), str(cfg["study"]["last_year"]))
    flags = {
        key: _read_file(folder / cfg["paths"]["weather_files"][key]).loc[window, "Quality"]
        for key in ("tmax", "tmin")
    }
    return pd.DataFrame(flags).fillna("missing").apply(pd.Series.value_counts).fillna(0).astype(int)


def fill_weather(weather: pd.DataFrame, max_gap_days: int) -> pd.DataFrame:
    """Fill short gaps and add the daily mean temperature.

    Gaps of up to ``max_gap_days`` are filled linearly; longer gaps stay blank. ``tmean`` is the
    mean of the daily maximum and minimum.
    """
    filled = fill_short_gaps(weather, max_gap_days)
    return filled.assign(tmean=filled[["tmax", "tmin"]].mean(axis=1, skipna=False))


def missing_days(weather: pd.DataFrame) -> pd.DataFrame:
    """Count missing days per calendar year, by variable and for any variable."""
    blank = weather.isna()
    blank = blank.assign(any_variable=blank.any(axis=1))
    return blank.groupby(weather.index.year).sum().rename_axis("year")


def complete_years(weather: pd.DataFrame) -> list[int]:
    """Return the calendar years in which no variable has a blank day."""
    blank_days = weather.isna().any(axis=1).groupby(weather.index.year).sum()
    return blank_days[blank_days == 0].index.tolist()
