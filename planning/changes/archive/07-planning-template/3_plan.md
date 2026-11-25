# Plan: Planning template

## Approach

Copy the template's own files in. Write each new page from the old ones by moving whole
sections under the template's headings, without rewording them. Then check by script that
every sentence of the old pages is in the new ones, and only then remove the old pages.

## Files touched

`planning/` (every page), `AGENTS.md` and the root `README.md`. No code, notebook or result.

## Tasks

- [x] T1: Copy `README.md`, `specs/_template.md` and `changes/_template/` from the template.
- [x] T2: Write `00_status.md`, `01_intent.md` and `02_spec.md` under the template's headings.
- [x] T3: Write the six pages of `specs/` from those of `spec/`.
- [x] T4: Write the archived changes 01 to 06 from the first plan, its three plan pages and the
      log of the old status page.
- [x] T5: Check that nothing is lost (see Outcome), then remove `03_planning.md`,
      `99_status.md`, `plan/` and `spec/`.
- [x] T6: Add the template's rules to `AGENTS.md`; correct its links and those of the root
      `README.md`.
- [x] T7: Check that every link under `planning/`, in `AGENTS.md` and in the root `README.md`
      leads to a file.

## Outcome

- **Nothing lost.** The old pages were cut into 768 units: headings, table cells, and the
  sentences of paragraphs and list items. Of these, 695 are in the new pages word for word. The
  other 73 were each accounted for by hand:
  - 23 headings, renamed to the template's or made a sub-heading;
  - 19 link texts and layout lines that named `spec/`, `plan/` or a component;
  - 12 lines that pointed from one page to another ("Back to the spec", "Step 4 of the plan"),
    reworded for the new pages;
  - 10 lines, eight of them from the old status page, reworded from steps and backlog to
    changes and Later;
  - 4 sentences that opened with the label "Goal." or "Done when.", which is now a heading;
  - 5 sentences that said how the old pages worked, dropped. They are named in the
    [spec delta](2_spec-delta.md).
- **Links.** Every link under `planning/`, in `AGENTS.md` and in the root `README.md` leads to
  a file.
- No code, notebook or result changed. 12 tests pass.
