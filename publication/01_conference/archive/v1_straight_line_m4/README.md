# Archive: v1, straight-line M4

The results of the conference analysis as they stood before M4 and M5 were revised, with the
code that made them. Kept so that the earlier numbers can be read without going through git
history.

| | |
|---|---|
| Git tag | `conference-v1-straight-line-m4` |
| Commit | `71c3cb366910af5579696b40536429124d35310e` |
| Archived | 24 November 2026 |

## Why it was superseded

In this version M4 used maximum and minimum temperature as two straight terms, and M5 was given
the same two columns. Minimum demand rises on both cold and hot days, so one straight slope is
the wrong shape. On the supervisor's advice M4 was revised to use mean temperature as a V, and
M5 to use mean temperature. The revision is decision D37 in `analysis_plan.md`, and was made
after the scores of all six models had been seen.

Only M4, M5 and the comparisons that involve them differ between this version and the current
one. M1, M2, M3 and M6 are the same in both.

## What is here

| Path | Holds |
|---|---|
| `results/figures`, `results/tables` | The paper's four figures and three tables, with the data behind the figures |
| `results/checks` | What the paper's limitation and robustness statements rely on |
| `results/archive` | Superseded figures and first looks, written by the two archive notebooks |
| `results_summary.md` | Every number the paper relied on, with the file it came from |
| `code/src/pynmdf` | The package |
| `code/notebooks` | The eight main notebooks and the two archive notebooks |
| `code/config.example.yaml` | Every decision parameter |

The code is exactly that of the commit above. The results are a copy of the output folder as
it stood on disk on the day of archiving; they were not rebuilt for the archive.

Paths written inside these files are those of the layout at the time: `outputs/`, `notebooks/`
and `docs/` at the repository root.

## This folder is a record

It is not rerun, refactored, linted or tidied. To rebuild these results, check out the tag and
follow the README of that commit.
