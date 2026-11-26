# Release and citation

Back to the [spec index](../02_spec.md).

## Purpose

Say how the repository is cited, and how a frozen copy of it is released on GitHub and archived
on Zenodo with a DOI.

**Files.** `CITATION.cff`, `.zenodo.json` and `CHANGELOG.md` at the repository root, and the
section "How to cite" of the root README. The test is `tests/test_release_metadata.py`.

## Outputs

| File | Read by | Holds |
|---|---|---|
| `CITATION.cff` | GitHub, for its "Cite this repository" box | Title, authors with affiliations, licence, address of the repository and abstract; the version, date and DOI of the latest release |
| `.zenodo.json` | The author, when filling in Zenodo's form | The same title, authors, licence and description, with the upload type, the keywords, and the version and date of the latest release |
| `CHANGELOG.md` | People | What each release holds |

The releases:

| Tag | Date | DOI | For |
|---|---|---|---|
| `v1.0.0` | 27 November 2026 | [10.5281/zenodo.24571169](https://doi.org/10.5281/zenodo.24571169) | The conference paper |

## Process

The release checklist. Steps 1, 2, 5 and 7 are the author's; the rest can be done by an agent
on the author's word.

1. The author says the results are final and the paper is ready to submit.
2. The author starts a new upload on Zenodo, reserves its DOI with "Get a DOI now!", saves the
   draft and passes the DOI on. For a later release, the upload is started with "New version"
   on the record of the release before.
3. The version, the date and the DOI are written into `CITATION.cff`, `CHANGELOG.md` and the
   README, and the version and the date into `.zenodo.json`. The tests and the red-flag scan are
   run. Commit on `main` and push.
4. Tag that commit, `v1.0.0` for the first release, push the tag and publish the GitHub
   release, with the changelog entry as its notes.
5. The author downloads the zip of the tag from GitHub, adds it to the Zenodo draft, fills in
   the form from `.zenodo.json`, changes the licence from Zenodo's default to MIT, and
   publishes.
6. Check that the DOI leads to the record, with the right authors and licence.
7. The author writes the DOI into the paper, and submits the paper.

## Requirements

- R1: `CITATION.cff` at the repository root, in Citation File Format 1.2.0. It holds the title,
  the five authors with their affiliations, the licence, the address of the repository and a
  short abstract.
  Acceptance: the file loads as YAML and holds those fields. On GitHub the repository page shows
  "Cite this repository".
  Test: `test_R1_citation_file_is_complete`
- R2: `.zenodo.json` at the repository root. It holds the same title, authors, affiliations,
  licence and description, with the upload type "software" and the keywords.
  Acceptance: the file loads as JSON, and its title, licence, description and list of authors
  equal those of `CITATION.cff`.
  Test: `test_R2_zenodo_file_agrees_with_citation_file`
- R3: `CHANGELOG.md` at the repository root, with one entry, for 1.0.0, that says what the
  release holds.
  Acceptance: read by eye. No test.
- R4: A section "How to cite" in the root README. It gives the DOI of the latest release and
  points to the citation file.
  Acceptance: read by eye. No test.
- R5: The release checklist, as the Process above.
  Acceptance: read by eye. No test.

## Constraints

- **A release is made only on the author's word, just before a paper is submitted**, once its
  results are final. The files of a published Zenodo record are treated as final: Zenodo's own
  pages disagree on whether the owner can still change them, so a correction is a new version
  with a new DOI. (Change 08, and the next item.)
- **The release comes before the submission, because the paper cites its DOI.** The paper cites
  the DOI of the version, not the one for all versions, which is what Zenodo recommends for a
  citation. Decided by the author on 27 November 2026; change 08 had the release follow the
  submission.
- **The archive is made by a manual upload to Zenodo**: the zip of the tag, as GitHub serves
  it. Change 08 chose Zenodo's GitHub integration. On 27 November 2026 Zenodo's GitHub page
  listed no repository for the author's account, and the cause was not found, so the author
  chose the manual upload. The integration stays switched off for this repository: with it on,
  each GitHub release would make a second record.
- **The DOI is reserved before the release and written into the released files**, so the
  archived copy carries its own DOI. Between releases, the files carry the version, date and DOI
  of the latest release. No version or date is written for a release that has not been made.
- **The two metadata files say the same.** GitHub reads only `CITATION.cff`. `.zenodo.json` is
  what the author types into Zenodo's form. The test of R2 catches a difference. (Change 08.)
- **The licence is written `MIT` in `CITATION.cff` and `mit` in `.zenodo.json`.** Each format
  has its own list of identifiers: the first takes the SPDX spelling, and Zenodo's list holds
  only the lower-case one. The test compares them without case. In Zenodo's form the licence is
  changed by hand, because the default there is Creative Commons Attribution 4.0. (Change 08.)
- **The authors are the five contributors of the root README, in its order.** The author's
  affiliation is both UNSW and Ausgrid. A change of contributors is made in the README and in
  both files together. (Change 08.)
- **No ORCID iD is shown** unless its owner supplies it. None has been given. (Change 08.)
- **The first release is tagged `v1.0.0`.** Rejected: a name in the style of the first tag,
  such as `conference-v2-submitted`. A tag is never moved. (Change 08.)
- **A release freezes whatever is tracked at the tag.** Anything private that is committed
  before then is published for good, which is why step 3 runs the red-flag scan. (Change 08.)

## Known limits

- Nothing checks that the zip uploaded to Zenodo is the zip of the tag. That rests on step 5.
- `.zenodo.json` is not read by a manual upload, and has never been tried against Zenodo's
  GitHub integration. Its keys were checked against Zenodo's deposit metadata documentation on
  26 November 2026. `CITATION.cff` is valid against the Citation File Format 1.2.0 schema.
- The two tests of this page read the two metadata files, not synthetic data. They need no raw
  data.
- The citation is of the repository, not of the paper. A reference to the paper is added when
  the paper has one.
