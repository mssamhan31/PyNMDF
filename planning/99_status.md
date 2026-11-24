# 99 Status

Where the repository stands. The first two sections are rewritten whenever the state changes.
The log gains one entry per finished step, newest first.

## Now (24 November 2026)

- **Step in hand:** step 6 of the [plan](03_planning.md), go public. It is the author's
  decision and the author's action.
- **Done:** step 1 (planning documents and `AGENTS.md`), step 2 (archive of the first
  version), step 3 (restructure), step 4 (M4 revised) and step 5 (tidy and review gate).
- **Review gate:** publishable, with no blocker. The findings are in the open items below.
- **Branch:** `piecewise-m4-and-restructure`, cut from `main` at `71c3cb3`. There is no remote;
  nothing has been pushed.
- **Tag:** `conference-v1-straight-line-m4` on `71c3cb3`, the commit the first results came
  from.
- **Results:** in `publication/01_conference/results`, committed, with M4 taking maximum and
  minimum temperature each as a V. Every number of M1, M2, M3, M5 and M6 is identical to the
  archived copy.

### Where the repository differs from the spec

Nowhere.

## Open items

| Item | Needed for |
|---|---|
| Whether the conference review is double-blind | Step 6 |
| Whether the plan and status pages are published with the rest of `planning/` | Step 6 |
| Whether the wording "on the supervisor's advice" (D37 and four other places) is to be published | Step 6 |
| Whether the three notes and the analysis plan, which record working discussions, are published as they stand | Step 6 |
| The name: "Forecasting" here, "Forecast" in the author's register of repositories | Step 6 |
| Review, should fix: abbreviations not expanded on first use (mainly PV and POE) in the notebooks, the results summary and three module headers | Backlog |
| Review, should fix: no approximate runtime in the first cell of nine notebooks | Backlog |

## Log

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
