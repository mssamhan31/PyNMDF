# 99 Status

Where the repository stands. The first two sections are rewritten whenever the state changes.
The log gains one entry per finished step, newest first.

## Now (24 November 2026)

- **Step in hand:** step 4 of the [plan](03_planning.md), revise M4 and M5.
- **Done:** step 1 (planning documents and `AGENTS.md`), step 2 (archive of the current
  version) and step 3 (restructure).
- **Branch:** `piecewise-m4-and-restructure`, cut from `main` at `71c3cb3`. There is no remote;
  nothing has been pushed.
- **Tag:** `conference-v1-straight-line-m4` on `71c3cb3`, the commit the current results came
  from.
- **Results:** in `publication/01_conference/results`, committed, with M4 using straight
  temperature terms. They are identical to the archived copy.

### Where the repository differs from the spec

| Spec says | Today | Closed by |
|---|---|---|
| M4 uses mean temperature as a V; M5 uses mean temperature | Both use `tmax` and `tmin` as straight terms | Step 4 |
| `LICENSE`, a front-page README and a README per publication | No licence; one long README | Step 5 |

## Open items

| Item | Needed for |
|---|---|
| The contributors list for the README | Step 5 |
| Whether the conference review is double-blind | Step 6 |
| Whether the plan and status pages are published with the rest of `planning/` | Step 6 |

## Log

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
