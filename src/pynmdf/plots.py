"""Figures for the paper: a shared style and one function per figure.

Style follows the IEEE two-column page: 3.5 inches for one column and 7.16 inches for full
width, 8 pt serif text, no title inside a figure (captions are written in the paper), and axis
labels with units. Every series differs in colour, marker and line style at once, so a figure
still reads in greyscale.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter

ONE_COLUMN, FULL_WIDTH = 3.5, 7.16  # inches
BLUE, ORANGE, GREEN = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, GRID = "#222222", "#555555", "#dddddd"
# One (colour, marker, line style) per series, always used in this order.
SERIES = [(BLUE, "o", "-"), (ORANGE, "s", "--"), (GREEN, "^", "-.")]
# A model keeps its colour, marker and line style in every figure it appears in. M2, the
# baseline with no PV, is the neutral grey.
MODEL_STYLE = {
    "M2": (MUTED, "D", ":"),
    "M3": (BLUE, "o", "-"),
    "M4": (ORANGE, "s", "--"),
    "M5": (GREEN, "^", "-."),
}
MODEL_TITLES = {
    "M2": "M2: time trend (no PV)",
    "M3": "M3: PV only",
    "M4": "M4: PV + weather",
    "M5": "M5: PV + weather (XGBoost)",
}
MONTH_INITIALS = list("JFMAMJJASOND")
# One hue from white to dark, so more is darker in colour and in greyscale alike.
BLUES = LinearSegmentedColormap.from_list("blues", ["#ffffff", BLUE, "#0b2a5b"])
THOUSANDS = FuncFormatter(lambda value, _: f"{value:,.0f}")


def set_style() -> None:
    """Apply the shared figure style. Call once at the top of a notebook."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif"],
            "font.size": 8,
            "axes.labelsize": 8,
            "axes.labelcolor": INK,
            "axes.edgecolor": MUTED,
            "axes.linewidth": 0.6,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.grid.axis": "y",
            "axes.axisbelow": True,
            "grid.color": GRID,
            "grid.linewidth": 0.5,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "legend.fontsize": 8,
            "legend.frameon": False,
            "lines.linewidth": 1.2,
            "lines.markersize": 3.5,
            "figure.dpi": 150,
            "pdf.fonttype": 42,  # embed TrueType fonts, as IEEE requires
        }
    )


def save_figure(figure: Figure, folder: Path, name: str) -> None:
    """Save a figure as ``name.png`` (600 dpi) and ``name.pdf`` in ``folder``.

    The PDF carries no creation date, so re-running a notebook reproduces the same file.
    """
    figure.savefig(folder / f"{name}.png", dpi=600)
    figure.savefig(folder / f"{name}.pdf", metadata={"CreationDate": None})


def fig1_annual_demand(annual: pd.DataFrame) -> Figure:
    """Fig. 1: annual maximum, overnight low and daytime low (lines, MW), and energy (bars, GWh).

    The year's minimum is the lower of the two low lines. Two axes at the author's request; their
    scales are aligned so that 1,000 MW sits level with 10,000 GWh and the gridlines coincide.

    Args:
        annual: One row per year with ``max_mw``, ``overnight_low_mw``, ``daytime_low_mw`` and
            ``energy_gwh``.
    """
    figure, demand = plt.subplots(figsize=(ONE_COLUMN, 2.5), layout="constrained")
    energy = demand.twinx()
    years = annual.index

    energy.bar(years, annual["energy_gwh"], width=0.6, color=GRID, label="Energy")
    lines = {
        "max_mw": "Maximum demand",
        "overnight_low_mw": "Overnight low",
        "daytime_low_mw": "Daytime low",
    }
    for (column, label), (colour, marker, style) in zip(lines.items(), SERIES):
        demand.plot(
            years, annual[column], color=colour, marker=marker, linestyle=style, label=label
        )

    demand.set(xlabel="Year", ylabel="Demand (MW)", ylim=(0, 6000), xticks=years[::2])
    energy.set(ylabel="Annual energy (GWh)", ylim=(0, 60000))
    for axis in (demand, energy):
        axis.yaxis.set_major_formatter(THOUSANDS)
    energy.spines["right"].set_visible(True)
    energy.grid(False)
    # Draw the lines over the bars.
    demand.set_zorder(energy.get_zorder() + 1)
    demand.patch.set_visible(False)

    handles = demand.get_legend_handles_labels()[0] + energy.get_legend_handles_labels()[0]
    figure.legend(handles=handles, loc="outside upper center", ncols=2, handlelength=2.4)
    return figure


def fig2_low_hours(hour_shares: pd.DataFrame, pv_kwp: pd.Series) -> Figure:
    """Fig. 2: when the lowest half hours of each year occur, over PV capacity by year.

    Args:
        hour_shares: The output of ``targets.low_hour_shares``: hours (rows) by years (columns).
        pv_kwp: PV capacity at 30 June, indexed by year.
    """
    figure, (hours, capacity) = plt.subplots(
        2, 1, figsize=(ONE_COLUMN, 3.1), sharex=True, layout="constrained", height_ratios=[3, 1.1]
    )
    years = hour_shares.columns.to_numpy()

    mesh = hours.pcolormesh(
        np.append(years, years[-1] + 1) - 0.5, np.arange(25), hour_shares, cmap=BLUES, vmin=0
    )
    hours.set(ylabel="Hour of day", yticks=range(0, 25, 6), ylim=(0, 24))
    hours.grid(False)
    # The evening hours never hold a low, so the colour scale sits in that empty corner.
    scale = hours.inset_axes([0.05, 0.82, 0.42, 0.035])
    figure.colorbar(mesh, cax=scale, orientation="horizontal")
    scale.set_title("Share of lowest 1% of half hours (%)", fontsize=8, loc="left", pad=3)
    # Each band is named in the empty space level with it: the overnight band ends before the
    # last years, and the midday band starts after the first ones.
    hours.text(years[-2], 4.5, "overnight", ha="center", va="center")
    hours.text(years[2] + 0.5, 12.5, "midday", ha="center", va="center")

    capacity.bar(years, pv_kwp.reindex(years) / 1000, width=0.6, color=GREEN)
    capacity.set(xlabel="Year", ylabel="PV capacity (MW)", xticks=years[::2])
    capacity.yaxis.set_major_formatter(THOUSANDS)
    return figure


def fig3_low_duration(lowest: pd.DataFrame, years: list[int]) -> Figure:
    """Fig. 3: the low end of the load duration curve for selected years.

    Args:
        lowest: The output of ``targets.lowest_intervals``.
        years: The years to draw.
    """
    figure, axis = plt.subplots(figsize=(ONE_COLUMN, 2.4), layout="constrained")
    for year, (colour, marker, style) in zip(years, SERIES):
        curve = lowest[lowest["year"] == year]
        axis.plot(curve["position_pct"], curve["mw"], color=colour, linestyle=style, label=year)
        # The curve starts at the year's absolute minimum.
        axis.plot(0, curve["mw"].iloc[0], color=colour, marker=marker, markersize=5, clip_on=False)
        right_end = (curve["position_pct"].iloc[-1], curve["mw"].iloc[-1])
        axis.annotate(year, right_end, (3, 0), textcoords="offset points", va="center")

    axis.set(xlabel="Share of the year, half hours sorted from lowest (%)", ylabel="Demand (MW)")
    axis.set_xlim(left=-0.02, right=lowest["position_pct"].max() * 1.12)
    axis.yaxis.set_major_formatter(THOUSANDS)
    axis.legend(loc="lower right", handlelength=2.2, bbox_to_anchor=(0.9, 0.08))
    return figure


def fig4_weather(daily: pd.DataFrame, solar_fits: pd.DataFrame) -> Figure:
    """Fig. 4: daytime low against solar exposure (left), minimum against temperature (right).

    Sunshine acts on the midday dip, so the left panel uses the daily daytime low and adds a
    least-squares line per year to show how the slope changes. Temperature acts on the whole
    day, so the right panel uses the daily minimum. The panels have separate y-axes.

    Args:
        daily: One row per date with ``daytime`` and ``min_mw`` (MW), ``solar`` (MJ/m2) and
            ``tmean`` (degrees C).
        solar_fits: The output of ``targets.yearly_line_fits`` for ``daytime`` on ``solar``; its
            index gives the years to draw.
    """
    figure, (solar, temperature) = plt.subplots(
        1, 2, figsize=(ONE_COLUMN, 2.4), layout="constrained"
    )
    panels = ((solar, "solar", "daytime"), (temperature, "tmean", "min_mw"))
    for (year, fit), (colour, marker, style) in zip(solar_fits.iterrows(), SERIES):
        days = daily[daily.index.year == year].dropna()
        for axis, x, y in panels:
            axis.scatter(
                days[x],
                days[y],
                s=3,
                color=colour,
                marker=marker,
                alpha=0.45,
                linewidths=0,
                label=year,
            )
        ends = np.array([fit["x_min"], fit["x_max"]])
        solar.plot(ends, fit["intercept"] + fit["slope"] * ends, color=colour, linestyle=style)

    solar.set(xlabel="Solar exposure (MJ/m²)", ylabel="Daily daytime low (MW)")
    temperature.set(xlabel="Mean temperature (°C)", ylabel="Daily minimum (MW)")
    for axis in (solar, temperature):
        axis.yaxis.set_major_formatter(THOUSANDS)
    handles, labels = temperature.get_legend_handles_labels()
    legend = figure.legend(handles, labels, loc="outside upper center", ncols=3, markerscale=2.5)
    for handle in legend.legend_handles:
        handle.set_alpha(1)
    return figure


def fig5_poe_bands(annual: pd.DataFrame, models: list[str], ylabel: str) -> Figure:
    """Fig. 5: the actual annual value against each model's POE10, POE50 and POE90.

    One panel per model on a shared y-axis. The band runs from POE90 (low side) to POE10 (high
    side) and the line is POE50.

    Args:
        annual: Annual forecasts of one target: ``model``, ``year``, ``poe10``, ``poe50``,
            ``poe90`` and ``actual``.
        models: The models to draw, left to right.
        ylabel: Label of the shared y-axis, with its unit.
    """
    figure, axes = plt.subplots(
        1, len(models), figsize=(FULL_WIDTH, 2.6), sharey=True, layout="constrained"
    )
    # Every year fits under a panel only with three panels or fewer. With more, every second
    # year is labelled and the years between keep an unlabelled tick.
    label_every = 1 if len(models) <= 3 else 2
    for axis, model in zip(axes, models):
        rows = annual[annual["model"] == model].sort_values("year")
        colour = MODEL_STYLE[model][0]
        axis.fill_between(
            rows["year"], rows["poe90"], rows["poe10"], color=colour, alpha=0.25, lw=0
        )
        axis.plot(rows["year"], rows["poe50"], color=colour)
        axis.plot(rows["year"], rows["actual"], color=INK, marker="o", linestyle="none")
        axis.set_title(MODEL_TITLES[model], fontsize=8)
        axis.set_xticks(rows["year"].iloc[::label_every])
        if label_every > 1:
            axis.set_xticks(rows["year"], minor=True)
        axis.yaxis.set_major_formatter(THOUSANDS)
    axes[0].set_ylabel(ylabel)
    figure.supxlabel("Test year", fontsize=8)

    # Each panel has its own colour, so the legend uses neutral handles.
    handles = [
        Patch(color=MUTED, alpha=0.25, lw=0, label="POE90 to POE10"),
        Line2D([], [], color=MUTED, label="POE50"),
        Line2D([], [], color=INK, marker="o", linestyle="none", label="Actual"),
    ]
    figure.legend(handles=handles, loc="outside upper center", ncols=3)
    return figure


def fig6_monthly_pinball(by_month: pd.DataFrame, models: list[str]) -> Figure:
    """Fig. 6: mean pinball loss of the monthly forecasts, by calendar month.

    Args:
        by_month: ``pinball_mean`` (MW) indexed by model and calendar month, for one target.
        models: The models to draw.
    """
    figure, axis = plt.subplots(figsize=(ONE_COLUMN, 2.4), layout="constrained")
    for model in models:
        colour, marker, style = MODEL_STYLE[model]
        loss = by_month.loc[model, "pinball_mean"]
        axis.plot(loss.index, loss, color=colour, marker=marker, linestyle=style, label=model)
    axis.set(xlabel="Calendar month", ylabel="Pinball loss (MW)")
    axis.set_xticks(range(1, 13), MONTH_INITIALS)
    axis.set_ylim(bottom=0)
    axis.yaxis.set_major_formatter(THOUSANDS)
    figure.legend(loc="outside upper center", ncols=len(models), handlelength=2.4)
    return figure
