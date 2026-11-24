# Plan: archive, then restructure

Steps 2 and 3 of the [plan](../03_planning.md). Neither changes any logic or any number.

## Step 2: archive the current version

**Goal.** Keep the results of the straight-line M4, and the code that made them, where they can
be found without digging through git history.

**What is done.**

1. Tag today's commit on `main` (`71c3cb3`) as `conference-v1-straight-line-m4`.
2. Create `publication/01_conference/archive/v1_straight_line_m4/` and copy into it, as they
   stand on disk and with no rerun:

| Into | From | Size |
|---|---|---|
| `results/` | `outputs/` (figures, tables, checks, and the folder of superseded figures) | 3.3 MB |
| `code/src/pynmdf/` | `src/pynmdf/` | 0.3 MB |
| `code/notebooks/` | `notebooks/`, the two archive notebooks included | 1.1 MB |
| `code/config.example.yaml` | `config.example.yaml` | |
| `results_summary.md` | `docs/results_summary.md` | |

3. Add a `README.md` there: what the folder is, the tag and commit it came from, why it was
   superseded, and that it is a record that is not rerun or tidied.
4. Exclude the folder from the linter and the formatter in `pyproject.toml`, so the frozen code
   is never reformatted.

**Done when.** The folder and the tag exist, and the copied files match their sources.

## Step 3: restructure

**Goal.** The layout in the [spec](../02_spec.md), with every number unchanged.

**Moves.**

| From | To |
|---|---|
| `notebooks/01_*.ipynb` to `08_*.ipynb` | `publication/01_conference/notebooks/` |
| `notebooks/archive/A1_*.ipynb`, `A2_*.ipynb` | `exploration/01_conference/` |
| `docs/analysis_plan.md`, `docs/results_summary.md` | `publication/01_conference/` |
| `docs/decision_log.md`, `docs/substation_set_decisions.md`, `docs/public_cross_check.md` | `publication/01_conference/notes/` |
| `outputs/figures`, `outputs/tables`, `outputs/checks` | `publication/01_conference/results/` |
| `outputs/archive` | `exploration/01_conference/outputs/` |
| `data/interim` | `publication/01_conference/data/interim/` |

**Edits that follow from the moves.**

- The five output paths in `config.example.yaml` and in the local `config.local.yaml`.
- The config key `archive` is renamed `exploration`, so that "archive" means one thing only:
  the version snapshot. This touches one line in `config.py` and the two exploration notebooks.
- Paths written in the moved documents, in notebook text and in docstrings.
- `.gitignore`: results are no longer ignored; `data/` and exploration outputs still are.
- A short `exploration/README.md` stating the rules in the spec.

The root README is rewritten in step 5, not here. In this step only its paths are corrected.

**Check.** Run notebooks 01 to 08 once (about 10 minutes, unattended). Every CSV under
`results/tables` and `results/checks` must be identical to its copy in the archive. Figures are
compared through their data files. The exploration notebooks are not rerun.

**Done when.** The check passes, the tests and the linter pass, and the status page says so.

## Not in these steps

- No change to any function's behaviour.
- No renaming of notebooks, modules or result files.
