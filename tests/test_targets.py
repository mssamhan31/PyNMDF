"""Test 10: straight-line fits report the slope, the fit and its error correctly, and the
lowest half hours are shared out between the trough windows.

All data are synthetic and small enough to check by hand.
"""

import numpy as np
import pandas as pd

from pynmdf import targets


def test_line_fits_match_hand_calculation():
    table = pd.DataFrame(
        {
            "x": [0.0, 1.0, 2.0, 3.0],
            "exact": [2.0, 5.0, 8.0, 11.0],  # 2 + 3x
            "noisy": [0.0, 1.0, 1.0, 2.0],
            "other": [3.0, 1.0, 2.0, 0.0],
        }
    )

    # --- A response that lies on a line is fitted exactly.
    exact = targets.line_fits(table, "exact", ["x"]).loc["x"]
    assert np.allclose(exact[["slope", "intercept", "r_squared", "rmse"]], [3.0, 2.0, 1.0, 0.0])
    assert exact["points"] == 4

    # --- A noisy response: the least-squares line is 0.1 + 0.6x, which leaves residuals of
    #     -0.1, 0.3, -0.3 and 0.1. Their squares sum to 0.2, against 2.0 about the mean.
    fits = targets.line_fits(table, "noisy", ["x", "other"])
    assert fits.index.tolist() == ["x", "other"]
    assert np.allclose(fits.loc["x", ["slope", "intercept"]], [0.6, 0.1])
    assert np.isclose(fits.loc["x", "r_squared"], 0.9)
    assert np.isclose(fits.loc["x", "rmse"], np.sqrt(0.2 / 4))
    # --- Shares by trough window: one year's lows all start at 04:00, the other's are split
    #     between 13:00 (inside the daytime window), 17:00 (its end, so outside) and 07:00.
    hour_shares = pd.DataFrame(0.0, index=range(24), columns=[2015, 2025])
    hour_shares.loc[4, 2015] = 100.0
    hour_shares.loc[[13, 17, 7], 2025] = [60.0, 30.0, 10.0]
    shares = targets.low_window_shares(hour_shares, {"overnight": [0, 6], "daytime": [9, 17]})
    assert shares.loc[2015].tolist() == [100.0, 0.0, 0.0]
    assert shares.loc[2025].tolist() == [0.0, 60.0, 40.0]

    # Each column is fitted on its own, so the second line does not depend on the first.
    assert np.isclose(
        fits.loc["other", "slope"], targets.line_fits(table, "noisy", ["other"])["slope"]
    )
