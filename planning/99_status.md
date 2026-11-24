# 99 Status

Where the repository stands. The first two sections are rewritten whenever the state changes.
The log gains one entry per finished step, newest first.

## Now (25 November 2026)

- **Step in hand:** none. All six steps of the [plan](03_planning.md) are done; what is left
  is in its backlog.
- **Public:** <https://github.com/mssamhan31/PyNMDF>, since 24 November 2026.
- **Done:** step 1 (planning documents and `AGENTS.md`), step 2 (archive of the first
  version), step 3 (restructure), step 4 (M4 revised), step 5 (tidy and review gate) and
  step 6 (public).
- **Review gate:** publishable, with no blocker. Its questions are answered and its findings
  are fixed, except the continuous integration workflow, which stays in the backlog.
- **Branch:** `main`, pushed to `origin`. The work of 24 November 2026 was done on
  `piecewise-m4-and-restructure` and merged; that of 25 November 2026 on
  `heatmap-and-temperature-figures`, also merged.
- **Tag:** `conference-v1-straight-line-m4` on `71c3cb3`, the commit the first results came
  from. Pushed.
- **Results:** in `publication/01_conference/results`, committed, with M4 taking maximum and
  minimum temperature each as a V. Every number of M1, M2, M3, M5 and M6 is identical to the
  archived copy. The paper set is four figures and three tables, as revised by D39 and D40.

### Where the repository differs from the spec

Nowhere.

## Open items

None.

Decided on 24 November 2026, after the review:

- `planning/` is published in full, the plan and status pages included.
- The repository goes public now. Whether the paper's review is blind is not a concern.
- The submitted state of the paper is tagged on the day it is submitted. A release is
  archived on Zenodo later.
- The wording "on the supervisor's advice" is published as it stands.
- The three notes and the analysis plan are published as they stand. The root README carries
  a statement on the use of AI.
- The name is "Python for Network Minimum Demand Forecasting".

## Log

### 25 November 2026: what the paper shows

- Fig. 1 has three panels on one year axis (D39): the two annual lows, the heat map of the
  lowest half hours, which had been archived, and PV capacity. Fig. 3 has two panels on one
  y-axis: the daily daytime low against solar exposure and against maximum temperature. The
  set stays at four figures and three tables, with the same numbers.
- A five-figure set, with the heat map as a figure of its own, was drawn first and set aside
  the same day, before anything was committed.
- Table I loses "Fitted on" and "POE from". Table II has the shape of the paper's table: the
  mean absolute error of each model, and the change in per cent for three pairs named "Impact
  of ... (Mx against My)". The mean error and the number of days are kept as a new check,
  `daily_skill.csv` (D40).
- In the four figures a low is labelled "minimum demand". The text, the tables and the checks
  keep "low".
- Not a step of the plan, and not a change of method. In the package: `plots` has
  `annual_lows_hours_and_pv` and `daytime_low_against_solar_and_temperature` in place of the
  two functions that drew the old Fig. 1 and Fig. 3; `evaluate.daily_table` builds the new
  Table II, with its test. 12 tests pass.
- Notebooks 03, 04, 05, 06 and 08 were rerun and written back. Checked: no number changed.
  `fig1_hours.csv` is identical to the archived heat map data; `fig1_data.csv`,
  `fig2_data.csv` and `fig3_fits.csv` did not change; the numbers of Table II and of the
  pairs by year are those of before; every other table and check is byte-identical.
- Done on the branch `heatmap-and-temperature-figures`, merged into `main` and pushed.

### 24 November 2026: public

- The red-flag scan was run again on `main` before the push: no secret, no local path, no
  private data.
- Created the public repository <https://github.com/mssamhan31/PyNMDF> and pushed `main` and
  the tag `conference-v1-straight-line-m4`.
- Next, from the backlog: a tag on the submitted state of the paper, and a release archived
  on Zenodo.

### 24 November 2026: review follow-ups

- The root README has a section on the use of AI: what the assistants did, and that the
  intent, the judgement, the taste and the accountability are the author's.
- Abbreviations are expanded on first use in the eight notebooks, the two exploration
  notebooks, the conference README, the results summary and four module headers. The one left,
  NSW in the root README, sits inside the sponsor acknowledgement, which is kept verbatim.
- The first cell of each of the eight notebooks states its approximate runtime, as measured on
  24 November 2026. The two exploration notebooks were not timed and have no such line.
- Text only: no code path and no result changed. 12 tests pass.

### 24 November 2026: tidied and reviewed

- Added `LICENSE` (MIT) and `publication/01_conference/README.md`, which takes the detail
  that was in the root README.
- The root README is now a front page: the problem, a quick start, the layout, the data and
  its credit lines, tests, licence, acknowledgements and contributors.
- Package description brought up to date; a local folder name removed from the decision log.
- Review gate run with the `repo-review` skill: no secret, no local path, no private data.
  Verdict: publishable, no blocker. Four should-fix findings and two questions for the
  author are carried in the open items above and in the backlog.

### 24 November 2026: M4 revised

- M4 now takes maximum and minimum temperature each as a V, with knots of 21 and 18 degrees
  C chosen on 2015 to 2018 only (D37). M5 is as it was first built.
- A first form, with one V on mean temperature in M4 and mean temperature in M5, was run and
  set aside after its scores were seen (D38). The form is now settled.
- New: the knot check (`check_temperature_knot.csv`) and two tests. 12 tests pass.
- Notebooks 05 to 08 were rerun and written back. In all five score tables only M4's rows
  moved; M1, M2, M3, M5 and M6 are identical to the archive.
- Effect on M4: better in the daily test (MAE 227.1 to 186.1 MW over all days); one year
  ahead, slightly worse on the annual daytime low (63.5 to 67.5 MW) and better on the monthly
  (51.8 to 46.2 MW). H2 on the monthly daytime low changed sign.
- The results summary, the READMEs, notebook 05 and the spec describe the revised M4.

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

### 24 November 2026: planning documents written

- Agreed with the author, question by question: the model revision, the layout, the archive,
  the order of work and what tidying covers.
- Written: `planning/` (intent, spec, plan, status, six spec pages, three plan pages) and
  `AGENTS.md`.
- Reviewed by the author, with one change: the rule on data now reads "no private or
  confidential data", since every input is public.
- No code, notebook, result or existing document was changed.

### 18 November 2026: conference analysis complete

- Commit `d6408a2`: eight notebooks, six models, results summary.
- Commit `71c3cb3`: the paper's set becomes four figures and three tables; what it replaced is
  archived.
- The full record of this period is `publication/01_conference/analysis_plan.md`: decisions D1
  to D36 and findings F1 to F11.

### 11 to 12 November 2026: plan and design

- The analysis plan was written after a first look at the raw data, and approved with one
  change of design: the daily ladder of models M2 to M5.
