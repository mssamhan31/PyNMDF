# Plan: Release preparation

Drafted on 26 November 2026 and approved by the author the same day.

## Approach

Write the two metadata files from the table in the [spec delta](2_spec-delta.md), each after its
test. Neither carries a version or a date yet: step 3 of the checklist writes them on release
day, so that nothing on `main` claims a release that does not exist. Then the changelog and the
README section. The field names are checked against the Citation File Format 1.2.0 schema and
Zenodo's help page before the files are written, not taken from memory.

## Files touched

- New: `CITATION.cff`, `.zenodo.json`, `CHANGELOG.md`, `tests/test_release_metadata.py`.
- Edited: the root `README.md`.
- At Finish: `planning/specs/release.md` (new), `planning/02_spec.md`, `planning/00_status.md`.

## Tasks

- [x] T1: Write `test_R1_citation_file_is_complete` in `tests/test_release_metadata.py`. It
      fails, as there is no file yet. (R1)
      Done: it failed with `FileNotFoundError`.
- [x] T2: Write `CITATION.cff`. The test of T1 passes. (R1)
      Done: the test passes, and the file is valid against the Citation File Format 1.2.0
      schema, downloaded from the format's repository.
- [x] T3: Write `test_R2_zenodo_file_agrees_with_citation_file`. It fails. (R2)
      Done: it failed with `FileNotFoundError`. It also compares the description, which R2
      names but its acceptance line does not.
- [x] T4: Write `.zenodo.json`. The test of T3 passes. (R2)
      Done. The licence is written `mit` here and `MIT` in `CITATION.cff`: Zenodo's list of
      licences holds `mit` and returns nothing for `MIT`, and the schema of the citation format
      holds only `MIT`. The test compares the two without case.
- [x] T5: Write `CHANGELOG.md`, with the entry for 1.0.0 undated. (R3)
- [x] T6: Add the section "How to cite" to the root README, with the place for the DOI. Add the
      three new files to its layout, and correct its line on the tests, which says twelve. (R4)
      Done. The expected output under Quick start said 12 passed and now says 14.
- [x] T7: Run all the tests, `ruff` and `black`. (At risk)
      Done: 14 tests pass; `ruff` and `black` find nothing.
- [x] T8: Finish. Write `specs/release.md` with R1 to R5 and the checklist as its Process, add
      its row and the three files to `02_spec.md`, update Later, and archive this folder. (R5)

One check cannot be made before the push to `main`: that the repository page on GitHub shows
"Cite this repository" (R1). It is made after the push and reported.

## Open questions

- The author's name in the two files. Both formats want a family name and a given name. Is it
  family name "Samhan" and given name "Samhan"? Answered by the author on 26 November 2026:
  yes.
