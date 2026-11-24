# AGENTS.md

Guidance for coding agents working in this repository.

PyNMDF (Python for Network Minimum Demand Forecasting) is the reproducible analysis code behind
research on forecasting minimum demand in distribution networks as rooftop PV grows. It holds
one shared package and one folder per publication.

## Start here

1. [planning/99_status.md](planning/99_status.md): where the work stands, and where the
   repository still differs from its spec.
2. [planning/01_intent.md](planning/01_intent.md), [02_spec.md](planning/02_spec.md) and
   [03_planning.md](planning/03_planning.md): why, what and how. The spec and the plan link to
   detail pages; read a detail page only when the task needs it.

## The red lines

- **Results belong to the papers.** Files under `publication/*/results/` change only because a
  notebook was rerun. Never edit a result value by hand.
- **A change of method is a decision, not an edit.** Changing a model, target, score, split,
  parameter or cleaning rule is methodology: propose it, and record it in the publication's
  decision record with its date and whether it came before or after the results were seen. If
  a fix needs such a change to be correct, stop and say so.
- **No private or confidential data.** Every input is a public file from a public source.
  Never commit private or confidential data (customer data, internal network data), credentials
  or local paths.

## Things that look wrong but are deliberate

- `publication/*/archive/` holds a frozen copy of earlier results and of the code that made
  them. The duplication is the point. Do not rerun, refactor, lint or tidy it.
- New models go at the **end** of `SPECS` in `src/pynmdf/models.py`. A model's position seeds
  its random draws, so inserting one changes the numbers of every model after it.
- `exploration/` is a record of first looks. Its notebooks are not rerun when the package
  changes, and nothing in a publication folder may depend on it.
- Three faults in the published demand files are measured and reported but not corrected. That
  is a recorded decision, not an oversight.

## Commands

Windows, Python 3.11, PowerShell.

```powershell
py -3.11 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt

.venv\Scripts\python -m pytest                 # tests, on synthetic data
.venv\Scripts\ruff check .
.venv\Scripts\black --check src tests

# run one notebook in place
.venv\Scripts\jupyter nbconvert --to notebook --execute --inplace "publication\01_conference\notebooks\05_backtest_models.ipynb"
```

Notebooks need the raw files and a `config.local.yaml`; see the README. Tests need neither.

## Architecture

The package is read in the order of the analysis: `io_demand`, `io_pv`, `io_weather` (read the
public files), `clean` (the network total), `targets` (what is forecast), `models` (M2 to M6),
`poe` (POE levels), `evaluate` (backtest and scores), `plots` (figures). `config` loads the one
YAML file that holds every decision parameter. Notebooks only call the package, show results
and save outputs.

## Conventions

- Australian spelling in all prose: README, docstrings, comments, notebook markdown. American
  spelling stays in code identifiers and library interfaces.
- Plain, short sentences. Comments say what a block is for and why.
- Every module opens with its purpose; every public function documents arguments, returns and
  units.
- Every notebook opens with a cell giving its purpose, inputs, outputs and numbered steps.
- New logic comes with a test. Run the tests before calling work done.
- Line length 100, `black` and `ruff`.

## Keeping the documents true

A change that makes a page under `planning/` untrue updates that page in the same change.
`planning/99_status.md` gains a log entry when a step of the plan is finished. A README is
updated in the same change that makes it out of date.

## Git

Work on a branch. Do not commit, push, tag or open a pull request unless asked. A tag marks the
submitted state of a paper and is never moved.
