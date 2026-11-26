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
| `CITATION.cff` | GitHub, for its "Cite this repository" box | Title, authors with affiliations, licence, address of the repository, abstract |
| `.zenodo.json` | Zenodo, when it archives a GitHub release | The same title, authors, licence and description, with the upload type and the keywords |
| `CHANGELOG.md` | People | What each release holds |

No release has been made yet. The first, `v1.0.0`, is made just before the conference paper is
submitted, so that the paper can cite its DOI.

## Process

The release checklist. Steps 1, 2 and 6 are the author's; the rest can be done by an agent on
the author's word.

1. The author says the results are final and the paper is ready to submit.
2. First release only: the author switches the repository on in Zenodo.
3. The version and the date are written into `CITATION.cff`, `.zenodo.json` and `CHANGELOG.md`.
   The tests and the red-flag scan are run. Commit on `main` and push.
4. Tag that commit `v1.0.0`, push the tag and publish the GitHub release, with the changelog
   entry as its notes.
5. Check that the Zenodo record has appeared, with the right authors and licence.
6. The author writes the DOI of that version into the paper, and submits the paper.
7. Write the same DOI into the README and the citation file. Commit and push. The tag is not
   moved.

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
- R4: A section "How to cite" in the root README. It points to the citation file and has a
  place for the DOI, which is written in after the first release because it does not exist
  before.
  Acceptance: read by eye. No test.
- R5: The release checklist, as the Process above.
  Acceptance: read by eye. No test.

## Constraints

- **A release is made only on the author's word, just before a paper is submitted**, once its
  results are final. The files of a published Zenodo record cannot be changed: a correction is a
  new version with a new DOI. (Change 08, and the next item.)
- **The release comes before the submission, because the paper cites its DOI.** Zenodo cannot
  reserve a DOI ahead of a GitHub release, so the DOI exists only once the release is made. The
  paper cites the DOI of the version, not the one for all versions, which is what Zenodo
  recommends for a citation. Decided by the author on 27 November 2026; change 08 had the
  release follow the submission.
- **No version, date or DOI is written before the release exists.** Steps 3 and 7 write them,
  so that nothing on `main` claims a release that has not been made. (Change 08.)
- **The two metadata files say the same.** GitHub reads only `CITATION.cff`. Zenodo reads only
  `.zenodo.json` when both exist. The test of R2 catches a difference. (Change 08.)
- **The licence is written `MIT` in `CITATION.cff` and `mit` in `.zenodo.json`.** Each format
  has its own list of identifiers: the first takes the SPDX spelling, and Zenodo's list holds
  only the lower-case one. The test compares them without case. (Change 08.)
- **The authors are the five contributors of the root README, in its order.** The author's
  affiliation is both UNSW and Ausgrid. A change of contributors is made in the README and in
  both files together. (Change 08.)
- **No ORCID iD is shown** unless its owner supplies it. None has been given. (Change 08.)
- **The first release is tagged `v1.0.0`.** Rejected: a name in the style of the first tag,
  such as `conference-v2-submitted`. A tag is never moved. (Change 08.)
- **Zenodo's GitHub integration makes the archive.** It copies the repository each time a
  GitHub release is published. (Change 08.)
- **A release freezes whatever is tracked at the tag.** Anything private that is committed
  before then is published for good, which is why step 3 runs the red-flag scan. (Change 08.)

## Known limits

- `.zenodo.json` has not been tried against Zenodo. Its keys were checked against Zenodo's
  deposit metadata documentation on 26 November 2026, and `CITATION.cff` was validated against
  the Citation File Format 1.2.0 schema the same day. A trial release in Zenodo's sandbox was
  left out of change 08, so step 5 is the first place a fault would show.
- Zenodo's documentation does not say what version and date a record takes when the file gives
  none. Step 3 writes both, so the question does not arise.
- The two tests of this page read the two metadata files, not synthetic data. They need no raw
  data.
- The citation is of the repository, not of the paper. A reference to the paper is added when
  the paper has one.
