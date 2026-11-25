# Spec: outputs

Back to the [spec](../02_spec.md).

## Purpose

Say what the notebooks write, where it goes and what is committed.

## Code

`src/pynmdf/plots.py` (figures), `src/pynmdf/config.py` (folders) and the notebooks.

## Where things go

Folders are entries under `paths` in the config, relative to the repository root.

| Folder | Holds | Committed |
|---|---|---|
| `publication/01_conference/results/figures` | The paper's figures, as PNG (600 dpi) and PDF | Yes |
| `publication/01_conference/results/tables` | The paper's tables and the data behind its figures, as CSV | Yes |
| `publication/01_conference/results/checks` | What the paper's limitation and robustness statements, and its sentences without a figure, rely on | Yes |
| `publication/01_conference/data/interim` | Cached data passed between notebooks | No |
| `exploration/01_conference/outputs` | First looks and superseded figures | No |

The map from each notebook to the files it writes is in
`publication/01_conference/README.md`. Every number the paper relies on is listed with its file
in `publication/01_conference/results_summary.md`.

## Rules

- **Notebooks do no logic.** They call the package, show results and save outputs.
- **Results are never edited by hand.** They change only when a notebook is rerun.
- **Names.** The paper's figures and tables are named by their number in the paper. Anything
  else is named for what it shows, so it cannot be mistaken for a current figure.
- **Figures** follow one shared style (`plots.set_style`): sized for a two-column page, no title
  inside the figure, and readable in greyscale. One function per figure, named for what it
  draws.
- **Every result file is a small summary.** No result file holds a half-hourly series or a
  value for a single substation.

## Earlier versions

When a revision replaces published-quality results, the old results and the code that made them
are copied once into the publication's `archive/` folder, with a README naming the commit they
came from. An archive is a record: it is not rerun, refactored, linted or tidied.

## Decision record

`publication/01_conference/analysis_plan.md`: D31 to D36, and D39 to D41.
