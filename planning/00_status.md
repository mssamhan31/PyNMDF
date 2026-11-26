# Status

Updated: 2026-11-27

## Active change

None. Changes 01 to 08 are finished and sit under [changes/archive](changes/archive/); what is
left is under Later.

## State

- **Public:** <https://github.com/mssamhan31/PyNMDF>, since 24 November 2026.
- **Done:** the conference analysis (01), the planning documents and `AGENTS.md` (02), the
  archive of the first version and the restructure (03), M4 revised (04), the tidy, the review
  gate and going public (05), what the paper shows (06), this folder's move to the planning
  template (07), the preparation of the first release (08) and the release itself.
- **Review gate:** publishable, with no blocker. Its questions are answered and its findings
  are fixed, except the continuous integration workflow, which stays under Later.
- **Release:** `v1.0.0`, of 27 November 2026, the state the conference paper is submitted from.
  Its copy on Zenodo has the DOI
  [10.5281/zenodo.24571169](https://doi.org/10.5281/zenodo.24571169); the author uploads the zip
  of the tag there by hand. The steps of a release are in [specs/release.md](specs/release.md).
- **Branch:** `main`, pushed to `origin`. The work of 24 November 2026 was done on
  `piecewise-m4-and-restructure` and merged; that of 25 November 2026 on
  `heatmap-and-temperature-figures`, also merged; that of 26 November 2026 on
  `planning-template`, also merged; change 08, the method explainer deck and the release on
  `release-preparation`, also merged.
- **Tags:** `v1.0.0` on the commit of the release. `conference-v1-straight-line-m4` on
  `71c3cb3`, the commit the first results came from. Both pushed.
- **Results:** in `publication/01_conference/results`, committed, with M4 taking maximum and
  minimum temperature each as a V. Every number of M1, M2, M3, M5 and M6 is identical to the
  archived copy. The paper set is four figures and three tables, as revised by D39 to D41.
- **Spec:** the repository differs from it nowhere.

## Open issues

None.

## Later

Not planned in detail and not started. Each is taken up only when it is needed.

- A website for the repository. Pages in `docs/`, as in PyNRPF.
- A continuous integration workflow. Tests and linter on every push. Raised by the review of
  24 November 2026.
- An installable library with a public interface. Only if others need to call the code.
- A journal paper. `publication/02_journal`.
- Another network's data, for example German data. See
  [specs/data_sources.md](specs/data_sources.md) for where it plugs in.
- More methods and experiments. Start in `exploration/`.
