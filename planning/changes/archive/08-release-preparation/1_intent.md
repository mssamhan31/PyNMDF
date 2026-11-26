# Change 08: Release preparation

Status: Done

Drafted on 26 November 2026 from the author's answers of that day, and approved by the author
the same day.

## Why

The paper needs a copy of the repository that is frozen and can be cited: a GitHub release,
archived on Zenodo with a DOI. The files of a published Zenodo record cannot be changed, and the
paper is not submitted yet, so the release itself has to wait. What can be done now is to make
it a short job on the day.

## Goal

On the day the paper is submitted, cutting the release is a checklist of a few steps, with
nothing left to decide.

## Done when

- The repository says how to cite it, and GitHub shows its "Cite this repository" box.
- The title, authors, licence and description of the Zenodo record that a release will create
  are set in advance, in a file.
- The steps of a release are written down, with who does each.

## Out of scope

- Cutting the tag `v1.0.0` and the release. That is done on the author's word, on submission
  day.
- Switching the repository on in Zenodo. Only the author can log in.
- A continuous integration workflow. It stays under Later.
- A trial release in Zenodo's sandbox.
- A reference to the paper itself. It is added when the paper has one.

## Decisions

- **Prepare now, release on submission day.** The figures and tables changed twice in the week
  of 23 November 2026, and a release freezes them. Decided on 24 November 2026 and confirmed on
  26 November 2026. Rejected: releasing now.
- **The tag is `v1.0.0`.** Rejected: a name in the style of the first tag, such as
  `conference-v2-submitted`.
- **Zenodo's GitHub integration** makes the archive: it copies the repository each time a
  GitHub release is published.
- **The record lists the five contributors of the root README, in its order.** The author's
  affiliation is both UNSW and Ausgrid.
- **No ORCID iD is shown** unless the author supplies one. None has been given.
- **Two metadata files.** `.zenodo.json` is for Zenodo and `CITATION.cff` is for GitHub's
  citation box. Zenodo reads only the first when both exist, so the two must say the same.
