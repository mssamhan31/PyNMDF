# 99 Status

Where the repository stands. The first two sections are rewritten whenever the state changes.
The log gains one entry per finished step, newest first.

## Now (24 November 2026)

- **Step in hand:** step 2 of the [plan](03_planning.md), archive the current version.
- **Done:** step 1, the planning documents and `AGENTS.md`, reviewed by the author.
- **Branch:** `piecewise-m4-and-restructure`, cut from `main` at `71c3cb3`. There is no remote;
  nothing has been pushed.
- **Results on disk:** those of commit `71c3cb3`, with M4 using straight temperature terms.

### Where the repository differs from the spec

| Spec says | Today | Closed by |
|---|---|---|
| Layout with `publication/`, `exploration/` and `planning/` | `notebooks/`, `docs/`, `outputs/` and `data/` at the root | Step 3 |
| Results are committed | `outputs/` is git-ignored | Step 3 |
| M4 uses mean temperature as a V; M5 uses mean temperature | Both use `tmax` and `tmin` as straight terms | Step 4 |
| `LICENSE`, a front-page README and a README per publication | No licence; one long README | Step 5 |

## Open items

| Item | Needed for |
|---|---|
| The contributors list for the README | Step 5 |
| Whether the conference review is double-blind | Step 6 |
| Whether the plan and status pages are published with the rest of `planning/` | Step 6 |

## Log

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
- The full record of this period is `docs/analysis_plan.md`: decisions D1 to D36 and findings
  F1 to F11.

### 11 to 12 November 2026: plan and design

- The analysis plan was written after a first look at the raw data, and approved with one
  change of design: the daily ladder of models M2 to M5.
