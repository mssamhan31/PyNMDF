"""Test 1: the reader absorbs every file layout Ausgrid has used.

All data are synthetic. One substation is written four ways (date format, header case and
padding, label style and order, how blanks are written); each must read to the same series.
"""

import zipfile

import numpy as np
import pandas as pd

from pynmdf.io_demand import read_reporting_year, read_substation

DAYS = pd.date_range("2014-05-01", periods=3, freq="D")
END_MINUTES = list(range(15, 1441, 15))


def _label(end_minute: int, zero_padded: bool, last: str) -> str:
    """Write an interval label the way a given year's file does."""
    if end_minute == 1440:
        return last
    hours, minutes = divmod(end_minute, 60)
    return f"{hours:02d}:{minutes:02d}" if zero_padded else f"{hours}:{minutes:02d}"


def _write_csv(values, date_text, header, zero_padded, last, shuffle, blank) -> bytes:
    """Render three days of one substation as CSV text.

    Day 2 is left out of the file. Day 3 is written twice: the first copy holds the morning and
    the second the afternoon, like Crows Nest in FY2017.
    """
    labels = [_label(minute, zero_padded, last) for minute in END_MINUTES]
    order = np.random.default_rng(0).permutation(96) if shuffle else np.arange(96)

    def row(day, cells):
        text = [blank if np.isnan(cell) else f"{cell:.5f}" for cell in cells[order]]
        return ",".join(["2015", "Testville 33_11kV", date_text(DAYS[day]), "MW", *text])

    morning, afternoon = values[2].copy(), values[2].copy()
    morning[48:] = np.nan
    afternoon[:48] = np.nan
    lines = [
        ",".join([*header, *(labels[i] for i in order)]),
        row(0, values[0]),
        row(2, morning),
        row(2, afternoon),
    ]
    return "\n".join(lines).encode()


def test_reader_absorbs_every_file_layout(tmp_path):
    values = np.random.default_rng(1).uniform(1, 9, size=(3, 96)).round(5)
    expected = values.copy()
    expected[1] = np.nan  # the day absent from the file
    expected = pd.Series(
        expected.ravel(),
        index=pd.date_range("2014-05-01", periods=3 * 96, freq="15min"),
        name="Testville 33_11kV",
    )

    lower = ["year", "Zone Substation", "Date", "unit"]
    title = ["Year", "Zone Substation", "Date", "Unit"]
    padded = [" year ", "Zone Substation ", " Date", " Unit "]
    layouts = {
        "FY2015 style": (lambda d: d.strftime("%d%b%Y").upper(), lower, False, "24:00", False, ""),
        "FY2024 style": (lambda d: d.strftime("%d/%m/%Y"), title, True, "00:00", False, ""),
        "FY2025 style": (lambda d: d.strftime("%Y-%m-%d"), padded, True, "24:00", True, "NaN"),
        "odd FY2015 file": (
            lambda d: f"{d.day}-{d:%b}-{d:%y}",
            lower,
            False,
            "24:00:00",
            False,
            "",
        ),
    }
    for name, layout in layouts.items():
        series = read_substation(_write_csv(values, *layout), DAYS)
        pd.testing.assert_series_equal(series, expected, obj=name, check_freq=False)

    # A reporting year reads the same from a folder and from a zip with a nested folder.
    raw = _write_csv(values, *layouts["FY2015 style"])
    folder = tmp_path / "FY2015" / "nested"
    folder.mkdir(parents=True)
    (folder / "Testville 33_11kV FY2015.csv").write_bytes(raw)
    with zipfile.ZipFile(tmp_path / "FY2015.zip", "w") as archive:
        archive.writestr("FY 2015/Testville 33_11kV FY2015.csv", raw)
        archive.writestr("FY 2015/Information.pdf", b"not a csv")

    from_folder = read_reporting_year(tmp_path / "FY2015", 2015)
    from_zip = read_reporting_year(tmp_path / "FY2015.zip", 2015)
    pd.testing.assert_frame_equal(from_folder, from_zip)
    assert from_zip.shape == (365 * 96, 1)
    assert from_zip.index[0] == pd.Timestamp("2014-05-01 00:00")
    assert from_zip.index[-1] == pd.Timestamp("2015-04-30 23:45")
    pd.testing.assert_series_equal(
        from_zip["Testville 33_11kV"].iloc[: 3 * 96], expected, check_freq=False
    )
