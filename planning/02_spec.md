# Spec index

What the repository holds and the rules it follows. This page is the index; each capability
has a short page under [specs/](specs/), to be read only when needed.

## System overview

- One shared Python package, `pynmdf`, which holds the logic.
- One folder per publication, with that paper's notebooks, results and decision record.
- One folder for exploration: work that no paper relies on.

### Layout

```
AGENTS.md  LICENSE  README.md  pyproject.toml  requirements.txt
config.example.yaml              raw-data paths and every decision parameter (committed)
config.local.yaml                the real local paths (git-ignored)
src/pynmdf/                      the shared package: all logic lives here
tests/                           pytest tests on synthetic data
planning/                        status, intent, spec and the record of each change
  specs/                         one page per capability
  changes/                       one folder per change; the finished ones under archive/
publication/01_conference/       everything that belongs to the conference paper
  README.md                      how to reproduce the paper, and what each file is
  analysis_plan.md               the design and the decision record (D and F numbers)
  results_summary.md             every number the paper relies on, with its file
  notes/                         the author's notes behind three decisions
  notebooks/                     notebooks 01 to 08
  results/                       figures, tables and checks (committed)
  data/interim/                  cache passed between notebooks (git-ignored)
  archive/v1_straight_line_m4/   the results and code as they stood before M4 was revised
exploration/                     work that no paper relies on
  01_conference/                 the first looks and superseded figures of the conference study
```

`docs/` is left free for a website.

### What a publication folder holds

Each `publication/NN_name/` is self-describing:

- a `README.md` that says how to reproduce the paper;
- its notebooks, which only call the package, show results and save outputs;
- its `results/`, committed, rebuilt only by running the notebooks;
- its decision record;
- an `archive/` for any earlier version of the results that a later revision replaced.

A submitted paper is marked by a git tag. The tag is the guarantee that its results can be
rebuilt after the shared package has moved on; the package is not copied per paper.

### Exploration

`exploration/` holds first looks, superseded figures and experiments. It is not held to the
standard of a publication: its notebooks are a record, are not rerun when the package changes,
and their outputs are git-ignored. Nothing in a publication folder may depend on it. Work moves
from exploration into a publication only by being rebuilt there.

### Configuration

One file at the repository root. `config.example.yaml` is committed and holds every parameter
that is a decision, each with a comment. `config.local.yaml` is a git-ignored copy with the real
raw-data paths. Notebooks find the root by walking up to the nearest config file, so they run
from any depth. A second config is added only when a second publication needs other settings.

## Capabilities

| Capability | Code | What it does | File |
|---|---|---|---|
| Data sources | `io_demand.py`, `io_pv.py`, `io_weather.py` | Read each public source into one standard shape | [specs/data_sources.md](specs/data_sources.md) |
| Network total | `clean.py` | Clean the substation files and sum them into one half-hourly series | [specs/network_total.md](specs/network_total.md) |
| Targets | `targets.py` | Turn the series into the three scored targets and the daily lows | [specs/targets.md](specs/targets.md) |
| Models | `models.py` | The daily models M2 to M6 (M1 needs no fit) | [specs/models.md](specs/models.md) |
| POE and evaluation | `poe.py`, `evaluate.py` | Turn a model into POE10, POE50 and POE90; backtest and score | [specs/poe_and_evaluation.md](specs/poe_and_evaluation.md) |
| Outputs | `plots.py`, `config.py`, notebooks | Figures, tables and checks, and where each is written | [specs/outputs.md](specs/outputs.md) |

Data flows in that order: sources, network total, targets, models, POE, scores, outputs.

## Cross-cutting constraints

Rules that hold everywhere:

- **No private or confidential data.** Every input is public. Nothing private or confidential
  is committed: no customer data, no internal network data, no credentials, no local paths.
- **Results are never edited by hand.** A result file changes only because a notebook was rerun.
- **Reruns are exact.** Every random draw is seeded from the config seed, the model's position
  in the model list and the forecast origin; XGBoost runs on one thread.
- **Models are only ever added at the end of the list**, so that adding one never changes the
  draws of another.
- **A change of method is a decision.** A change to a model, target, score, split, parameter or
  cleaning rule is recorded in the publication's decision record, with its date and whether it
  came before or after the results were seen.
- **New logic comes with a test**, on synthetic data.

## Extending

| To add | Do this | Detail |
|---|---|---|
| A data source or another network | Write a reader that returns the standard shapes | [specs/data_sources.md](specs/data_sources.md) |
| A model | Add one entry at the end of the model list | [specs/models.md](specs/models.md) |
| A publication | Add `publication/NN_name/` with the contents listed above | this page |
| An experiment | Add a folder under `exploration/` | this page |
