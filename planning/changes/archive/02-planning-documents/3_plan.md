# Plan: Planning documents

The first plan of the repository: how it gets from where it is to what the
[spec](../../../02_spec.md) describes. This is the page `planning/03_planning.md` as it stood on
26 November 2026. Each of its steps is now a change in this archive, and its backlog is the
Later list of the [status page](../../../00_status.md).

## Approach

**Why this order.**

- **Archive first**, so the snapshot is exactly the commit the current results came from.
- **Restructure before the model change**, so that a pure move can be shown to change no number.
- **Model change after that**, so that every number that then moves is due to the model alone.

**How the steps are worked.**

- All work is on the branch `piecewise-m4-and-restructure`. Nothing is pushed.
- One commit per step, made only after the author has seen the result of that step.
- The status page gains a log entry when a step is finished. Any change that makes a planning
  page untrue updates that page in the same change.

## Steps

| # | Step | State | Detail |
|---|---|---|---|
| 0 | Build the conference analysis: eight notebooks, six models, results summary | Done, 18 November 2026 | `publication/01_conference/analysis_plan.md`; [change 01](../01-conference-analysis/1_intent.md) |
| 1 | Write the planning documents and `AGENTS.md` | Done, 24 November 2026 | `planning/`; this change |
| 2 | Archive the current version: results and code as they stand, and a tag | Done, 24 November 2026 | [change 03](../03-archive-and-restructure/1_intent.md) |
| 3 | Restructure: move files to the layout in the spec; no change of logic | Done, 24 November 2026 | [change 03](../03-archive-and-restructure/1_intent.md) |
| 4 | Revise M4: maximum and minimum temperature each as a V | Done, 24 November 2026 | [change 04](../04-piecewise-m4/1_intent.md) |
| 5 | Tidy for publication, then the review gate | Done, 24 November 2026 | [change 05](../05-tidy-and-go-public/1_intent.md) |
| 6 | Go public | Done, 24 November 2026 | [change 05](../05-tidy-and-go-public/1_intent.md) |

## Outcome

The log entry of the old status page.

### 24 November 2026: planning documents written

- Agreed with the author, question by question: the model revision, the layout, the archive,
  the order of work and what tidying covers.
- Written: `planning/` (intent, spec, plan, status, six spec pages, three plan pages) and
  `AGENTS.md`.
- Reviewed by the author, with one change: the rule on data now reads "no private or
  confidential data", since every input is public.
- No code, notebook, result or existing document was changed.
