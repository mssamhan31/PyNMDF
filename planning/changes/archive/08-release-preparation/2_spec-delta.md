# Spec delta: Release preparation

Drafted on 26 November 2026 and approved by the author the same day.

## Capabilities touched

- `specs/release.md`: new, for a capability "Release and citation".
- `02_spec.md`: one row under Capabilities and three lines in the layout.

## Added

- R1: `CITATION.cff` at the repository root, in Citation File Format 1.2.0. It holds the title,
  the five authors with their affiliations, the licence, the address of the repository and a
  short abstract.
  Acceptance: the file loads as YAML and holds those fields. On GitHub the repository page shows
  "Cite this repository".
  Test: `test_R1_citation_file_is_complete`
- R2: `.zenodo.json` at the repository root. It holds the same title, authors, affiliations,
  licence and description, with the upload type "software" and the keywords.
  Acceptance: the file loads as JSON, and its title, licence and list of authors equal those of
  `CITATION.cff`.
  Test: `test_R2_zenodo_file_agrees_with_citation_file`
- R3: `CHANGELOG.md` at the repository root, with one entry, for 1.0.0, that says what the
  release holds.
  Acceptance: read by eye. No test.
- R4: A section "How to cite" in the root README. It points to the citation file and has a
  place for the DOI, which is written in after the first release because it does not exist
  before.
  Acceptance: read by eye. No test.
- R5: The release checklist, as the Process of `specs/release.md`:
  1. The author says the paper is submitted.
  2. First release only: the author switches the repository on in Zenodo.
  3. The version and the date are written into `CITATION.cff`, `.zenodo.json` and
     `CHANGELOG.md`. The tests and the red-flag scan are run. Commit on `main` and push.
  4. Tag that commit `v1.0.0`, push the tag and publish the GitHub release, with the changelog
     entry as its notes.
  5. Check that the Zenodo record has appeared, with the right authors and licence.
  6. Write the DOI into the README and the citation file. Commit and push. The tag is not
     moved.

  Acceptance: read by eye. No test.

### The metadata, for the author to correct

| Field | Value |
|---|---|
| Title | PyNMDF: Python for Network Minimum Demand Forecasting |
| Description | The first paragraph of the root README: "PyNMDF is the reproducible analysis code behind research on forecasting minimum demand in distribution networks as rooftop photovoltaic (PV) capacity grows. It holds one shared package and one folder per publication. Every input is public." |
| Type | Software |
| Licence | MIT |
| Version | 1.0.0 |
| Keywords | minimum demand; rooftop photovoltaics; distribution network; probabilistic forecasting; probability of exceedance |
| Repository | <https://github.com/mssamhan31/PyNMDF> |

Authors, in this order:

| # | Name | Affiliation |
|---|---|---|
| 1 | Samhan Samhan | School of Photovoltaic and Renewable Energy Engineering, UNSW; Demand Forecasting, Ausgrid |
| 2 | Navid Haghdadi | Demand Forecasting, Ausgrid |
| 3 | Daniel Sim | Demand Forecasting, Ausgrid |
| 4 | Anna Bruce | School of Photovoltaic and Renewable Energy Engineering, UNSW |
| 5 | Baran Yildiz | School of Photovoltaic and Renewable Energy Engineering, UNSW |

## Changed

- `00_status.md`, Later: "A citation file" and "A changelog" are done and go. "A tag on the
  submitted state of the paper" and "A release archived on Zenodo" become one line that points
  to the checklist.

## Removed

None.

## At risk

- The 12 tests become 14. The two new ones read two files at the repository root, not synthetic
  data. They still need no raw data.
- `CITATION.cff` and `.zenodo.json` can drift apart. The test of R2 is there to catch it.
- A release freezes whatever is tracked at the tag. Anything private that is committed before
  then is published for good.
