# Plan: Archive, then restructure

## Tasks

### Step 2: archive the current version

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

### Step 3: restructure

**Moves.** In the [spec delta](2_spec-delta.md).

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

## Outcome

The log entries of the old status page, newest first.

### 24 November 2026: repository restructured

- Moved to the layout in the spec: notebooks, documents, results and cache under
  `publication/01_conference/`; the two exploration notebooks and their outputs under
  `exploration/01_conference/`. Git records every tracked move as a rename.
- Paths corrected in both config files, the package docstrings, the notebook text, the results
  summary, the root README and `.gitignore`. The config key `archive` is now `exploration`.
  `analysis_plan.md` is left as written, with a dated note that maps old paths to new ones.
- Results are now committed; the cache and the exploration outputs stay git-ignored.
- Checked: notebooks 01 to 08 were run from their new folder (317 seconds). All 45 result files
  (8 tables, 29 checks, 8 figures) are byte-identical to the archived copy. The tests, the
  linter and the formatter check pass.
- Not done, by design: the executed notebooks were not written back, so the stored outputs in
  the tracked notebooks are those of the earlier run; the exploration notebooks were not rerun.
- No logic and no number changed.

### 24 November 2026: current version archived

- Tagged commit `71c3cb3` as `conference-v1-straight-line-m4`.
- Copied into `publication/01_conference/archive/v1_straight_line_m4/`: the results as they
  stood on disk (70 files, no rerun), the package and the ten notebooks as in the tagged commit,
  the example config and the results summary. A README there says what the folder is.
- Checked: the copies are identical to their sources.
- `pyproject.toml` now keeps the linter and the formatter out of archive folders.
