"""Test 10: straight-line fits report the slope, the fit and its error correctly.

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
    # Each column is fitted on its own, so the second line does not depend on the first.
    assert np.isclose(
        fits.loc["other", "slope"], targets.line_fits(table, "noisy", ["other"])["slope"]
    )
