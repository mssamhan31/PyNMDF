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
  template (07) and the preparation of the first release (08).
- **Review gate:** publishable, with no blocker. Its questions are answered and its findings
  are fixed, except the continuous integration workflow, which stays under Later.
- **Release:** none yet. The citation file, the Zenodo file and the changelog are written. The
  release `v1.0.0` is made just before the paper is submitted, so that the paper can cite its
  DOI; its steps are in [specs/release.md](specs/release.md).
- **Branch:** `main`, pushed to `origin`. The work of 24 November 2026 was done on
  `piecewise-m4-and-restructure` and merged; that of 25 November 2026 on
  `heatmap-and-temperature-figures`, also merged; that of 26 November 2026 on
  `planning-template`, also merged; change 08 and the method explainer deck on
  `release-preparation`, also merged.
- **Tag:** `conference-v1-straight-line-m4` on `71c3cb3`, the commit the first results came
  from. Pushed.
- **Results:** in `publication/01_conference/results`, committed, with M4 taking maximum and
  minimum temperature each as a V. Every number of M1, M2, M3, M5 and M6 is identical to the
  archived copy. The paper set is four figures and three tables, as revised by D39 to D41.
- **Spec:** the repository differs from it nowhere.

## Open issues

- One check of change 08 waits for the push to `main`: that the repository's page on GitHub
  shows "Cite this repository".

## Later

Not planned in detail and not started. Each is taken up only when it is needed.

- A website for the repository. Pages in `docs/`, as in PyNRPF.
- A continuous integration workflow. Tests and linter on every push. Raised by the review of
  24 November 2026.
- The release `v1.0.0`: the tag, the GitHub release and the Zenodo archive. Just before the
  paper is submitted, by the checklist in [specs/release.md](specs/release.md).
- An installable library with a public interface. Only if others need to call the code.
- A journal paper. `publication/02_journal`.
- Another network's data, for example German data. See
  [specs/data_sources.md](specs/data_sources.md) for where it plugs in.
- More methods and experiments. Start in `exploration/`.
