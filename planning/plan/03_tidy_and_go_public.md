# Plan: tidy, review and go public

Steps 5 and 6 of the [plan](../03_planning.md).

## Step 5: tidy for publication

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

Not in this step: the website, a continuous integration workflow, a citation file and a
changelog. All four are in the backlog.

## The review gate

Run the `repo-review` skill: a check for secrets, local paths, private or confidential data and
anything that should not be published, then the wider audit. Only what it marks as blocking is
fixed here. Anything else it raises goes to the backlog or is dropped.

## Step 6: go public

The author's decision, given on 24 November 2026.

- [x] The review gate has passed: publishable, no blocker.
- [x] The contributors list for the README is supplied.
- [x] `planning/` is published in full, and the open items on the status page are cleared.
- [x] The work branch is merged into `main`.
- [x] The repository is created on GitHub and `main` and the tag are pushed:
      <https://github.com/mssamhan31/PyNMDF>.

After going public, both in the backlog: a tag on the submitted state of the paper, on the
day it is submitted; and a release archived on Zenodo.

## Done when

The status page records the gate result and the date the repository went public.
