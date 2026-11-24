# 03 Plan

How the repository gets from where it is to what the [spec](02_spec.md) describes. This page is
the overview; each open step has a detail page under [plan/](plan/). The [status](99_status.md)
says which step is in hand.

## Steps

| # | Step | State | Detail |
|---|---|---|---|
| 0 | Build the conference analysis: eight notebooks, six models, results summary | Done, 18 November 2026 | `publication/01_conference/analysis_plan.md` (today at `docs/analysis_plan.md`) |
| 1 | Write the planning documents and `AGENTS.md` | Done, 24 November 2026 | this folder |
| 2 | Archive the current version: results and code as they stand, and a tag | To do | [plan/01_archive_and_restructure.md](plan/01_archive_and_restructure.md) |
| 3 | Restructure: move files to the layout in the spec; no change of logic | To do | [plan/01_archive_and_restructure.md](plan/01_archive_and_restructure.md) |
| 4 | Revise M4 and M5: mean temperature as a V in M4, raw mean temperature in M5 | To do | [plan/02_piecewise_m4.md](plan/02_piecewise_m4.md) |
| 5 | Tidy for publication, then the review gate | To do | [plan/03_tidy_and_go_public.md](plan/03_tidy_and_go_public.md) |
| 6 | Go public | To do, on the author's decision | [plan/03_tidy_and_go_public.md](plan/03_tidy_and_go_public.md) |

## Why this order

- **Archive first**, so the snapshot is exactly the commit the current results came from.
- **Restructure before the model change**, so that a pure move can be shown to change no number.
- **Model change after that**, so that every number that then moves is due to the model alone.

## How the steps are worked

- All work is on the branch `piecewise-m4-and-restructure`. Nothing is pushed.
- One commit per step, made only after the author has seen the result of that step.
- The status page gains a log entry when a step is finished. Any change that makes a planning
  page untrue updates that page in the same change.

## Backlog

Not planned in detail and not started. Each is taken up only when it is needed.

| Item | Note |
|---|---|
| A website for the repository | Pages in `docs/`, as in PyNRPF |
| A continuous integration workflow | Tests and linter on every push |
| A citation file | When the paper has a citation |
| A changelog | When there is a release to describe |
| An installable library with a public interface | Only if others need to call the code |
| A journal paper | `publication/02_journal` |
| Another network's data, for example German data | See [spec/data_sources.md](spec/data_sources.md) for where it plugs in |
| More methods and experiments | Start in `exploration/` |
