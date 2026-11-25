# Change 07: Planning template

Status: Done, 26 November 2026

## Why

The author wants `planning/` in the format of the planning template, so that the same format
can be used in other repositories.

## Goal

The folder follows the template and no information that was in it is lost: a change of format,
not of content.

## Done when

Every section of the old pages has a place in the new ones. The [spec delta](2_spec-delta.md)
lists where each went, for the author to check before the commit.

## Out of scope

- `publication/01_conference/analysis_plan.md`, the decision record (D1 to D41). It stays where
  it is, untouched. A change points to its D numbers.
- Requirement numbers (R1, R2 and so on) and tests named after them. Numbering means writing
  acceptance criteria that do not exist yet and renaming tests, which is content and code, not
  format. It starts with the first new change that touches a spec page.
- The frozen `archive/` folders of a publication, and `exploration/`.

## Decisions

Agreed with the author on 26 November 2026.

- **Past work becomes archived changes.** Six of them, 01 to 06, built only from text that
  already existed: the steps table and the three plan pages of the first plan, and the log of
  the old status page. Where that text has nothing for one of a change's three files, the file
  is left out, not invented. Rejected: keeping the log on the status page, which breaks the
  template's rule that the status page stays under one screen.
- **Extra headings, as few as possible.** Where existing text has no heading in the template,
  it gets one of its own. Each is listed in the [spec delta](2_spec-delta.md).
- **A template heading with nothing to say is deleted**, as the template allows. Nothing is
  written to fill one.
- **The template's rules for the agent go into `AGENTS.md`**, so that the format has force.
  Rejected: correcting only the paths in `AGENTS.md`.
- **The template's `README.md` and `_template` files are copied in as they are.** Its
  `.gitkeep` is left out, since `changes/archive/` is not empty.
