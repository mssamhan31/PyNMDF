# Plan: Tidy, review and go public

## Tasks

### Step 5: tidy for publication

Only what a public reader needs. Nothing here changes a number.

| Item | What is done |
|---|---|
| `LICENSE` | MIT, in the form used by PyNRPF |
| Root `README.md` | Cut to a front page, in PyNRPF's order where it applies: what PyNMDF is, the problem, install, repository layout, data, reproducing a paper, tests, licence, acknowledgements, contributors |
| `publication/01_conference/README.md` | Takes the detail now in the root README: how to run the notebooks, the map from notebook to result file, the checks, the targets, the models, how the network total is built |
| Acknowledgements | The paragraph used in PyNRPF, word for word |
| Data attribution | Ausgrid as the source of the demand and PV files. The Bureau of Meteorology's preferred credit line, and its acknowledgement of the satellite operators for solar exposure |
| `pyproject.toml` | Description brought up to date |
| `.gitignore` | Checked against the new layout |
| `decision_log.md` | The name of a local folder removed |

### The review gate

Run the `repo-review` skill: a check for secrets, local paths, private or confidential data and
anything that should not be published, then the wider audit. Only what it marks as blocking is
fixed here. Anything else it raises goes to the backlog or is dropped.

### Step 6: go public

The author's decision, given on 24 November 2026.

- [x] The review gate has passed: publishable, no blocker.
- [x] The contributors list for the README is supplied.
- [x] `planning/` is published in full, and the open items on the status page are cleared.
- [x] The work branch is merged into `main`.
- [x] The repository is created on GitHub and `main` and the tag are pushed:
      <https://github.com/mssamhan31/PyNMDF>.

After going public, both in the backlog: a tag on the submitted state of the paper, on the
day it is submitted; and a release archived on Zenodo.

## Outcome

The log entries of the old status page, newest first.

### 24 November 2026: public

- The red-flag scan was run again on `main` before the push: no secret, no local path, no
  private data.
- Created the public repository <https://github.com/mssamhan31/PyNMDF> and pushed `main` and
  the tag `conference-v1-straight-line-m4`.
- Next, from the backlog: a tag on the submitted state of the paper, and a release archived
  on Zenodo.

### 24 November 2026: review follow-ups

- The root README has a section on the use of AI: what the assistants did, and that the
  intent, the judgement, the taste and the accountability are the author's.
- Abbreviations are expanded on first use in the eight notebooks, the two exploration
  notebooks, the conference README, the results summary and four module headers. The one left,
  NSW in the root README, sits inside the sponsor acknowledgement, which is kept verbatim.
- The first cell of each of the eight notebooks states its approximate runtime, as measured on
  24 November 2026. The two exploration notebooks were not timed and have no such line.
- Text only: no code path and no result changed. 12 tests pass.

### 24 November 2026: tidied and reviewed

- Added `LICENSE` (MIT) and `publication/01_conference/README.md`, which takes the detail
  that was in the root README.
- The root README is now a front page: the problem, a quick start, the layout, the data and
  its credit lines, tests, licence, acknowledgements and contributors.
- Package description brought up to date; a local folder name removed from the decision log.
- Review gate run with the `repo-review` skill: no secret, no local path, no private data.
  Verdict: publishable, no blocker. Four should-fix findings and two questions for the
  author are carried in the open items above and in the backlog.
