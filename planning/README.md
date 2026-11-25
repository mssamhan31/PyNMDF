# Planning template

A spec-driven planning structure for building with AI agents. Copy the `planning/` folder into the root of a repository.

The idea: decide **why** and **what** in writing before any code, build in small reviewed steps, and make every change through these files first and the code second.

## Folder map

```
planning/
  00_status.md       read first: active change, state, Later list
  01_intent.md       project why
  02_spec.md         index of capabilities + cross-cutting constraints
  specs/             current truth, one file per capability
    _template.md
  changes/
    _template/       copy this for each new change
      1_intent.md    why this change + decisions (you own)
      2_spec-delta.md  target: added / changed / removed
      3_plan.md      tasks (agent owns)
    archive/         finished changes, frozen
```

Numbers mark reading order. Files in `specs/` have no order, so they are not numbered.

## What each file is for

| File | Answers | Written by | Changes |
|---|---|---|---|
| `00_status.md` | Where are we now? | Agent, at Finish | Every change |
| `01_intent.md` | Why does this project exist? | You | Rarely |
| `02_spec.md` | What capabilities exist, and what rules apply to all? | Agent drafts, you correct | When a capability is added |
| `specs/<capability>.md` | What does this part do today? | Agent, by merging deltas | At Finish only |
| `1_intent.md` | Why this change? | You | Until approved |
| `2_spec-delta.md` | What will be different? | Agent drafts, you approve | Until approved |
| `3_plan.md` | How, in what order? | Agent drafts, you approve | During build |

`specs/` describes what is built and verified **today**. The target is `specs/` plus the active delta. They become equal at the end of every change.

## Workflow: project start

1. Write `01_intent.md`: problem, goal, stakeholders, success measures, out of scope.
2. Have the agent draft `02_spec.md` with the capability list. Correct it. `specs/` stays empty because nothing is built yet.
3. Copy `changes/_template/` to `changes/01-skeleton/`: the thinnest version that runs end to end.
4. Write `1_intent.md` and approve it. The agent drafts `2_spec-delta.md`; approve it. The agent drafts `3_plan.md`; approve it.
5. Build: the agent does one task at a time, writes the test first, runs all tests and ticks the task. Review each diff and commit.
6. Finish: the agent merges the delta into `specs/`, moves the folder to `changes/archive/` and updates `00_status.md`. Review that diff.

## Workflow: adding a change mid-project

1. Triage. If it changes the project's why, update `01_intent.md` first. If another change is active, add this one to **Later** in `00_status.md` and finish the active one first.
2. Copy `changes/_template/` to `changes/NN-name/` and follow steps 4 to 6 above. The delta must name the capability files it touches.
3. If the request alters the change you are in the middle of, edit that change's `1_intent.md` and `2_spec-delta.md` first, then have the agent re-plan the remaining tasks.

Fixes that take under an hour skip all of this and get a commit message only.

## Rules

- `00_status.md` stays under one screen. It holds pointers, not content.
- Each file has one job and one owner.
- Delete any header that has nothing to say.
- Acceptance criteria live in the spec and the delta, not in intent. Each one becomes a test, and the test name carries the requirement ID, for example `test_R3_flags_outliers`.
- A decision that outlives its change is copied into the relevant spec file as a constraint with its reason, so nobody needs the archive to build correctly.

## Rules for the agent

Paste these into `CLAUDE.md` or `AGENTS.md`:

```markdown
## Planning
- Read planning/00_status.md first, then the active change folder, then only the specs/ files the delta names.
- Never build anything that is not in the active change's 2_spec-delta.md.
- During build, edit only the Tasks section of 3_plan.md. Do not edit 1_intent.md.
- Update specs/ only at Finish, by merging the delta.
- Do not modify an existing test without approval.
- If a task conflicts with a constraint in specs/ or 02_spec.md, stop and flag it.
```

## Examples

All examples are illustrative. They follow one made-up change: adding a rolling outlier filter to a substation data cleansing pipeline.

### 00_status.md

```markdown
# Status

Updated: 2026-11-26

## Active change
changes/03-rolling-outlier-filter, stage: build (4 of 7 tasks done)

## State
Ingestion and gap-filling run daily in dev. Outlier filter still uses fixed 3 sigma.

## Open issues
New substations have under 28 days of history; behaviour not yet decided.

## Later
- Weather-adjusted threshold
- Power BI data quality page
```

### 01_intent.md

```markdown
# Intent: Substation data cleansing pipeline

## Problem
Cleansing is done by hand each month and takes about two days.

## Goal
Clean interval data arrives in one table every day with no manual steps.

## Stakeholders
Users: demand forecasters. Decides: forecasting team lead. Affected: network planning.

## Success measures
- Daily run finishes before 07:00.
- Fewer than 1% of genuine readings are flagged as outliers.

## Out of scope
Forecast models. Customer-level meter data.

## Constraints
Dev workspace only until sign-off.
```

### specs/cleansing.md (extract)

```markdown
## Requirements
- R3: Flag an interval reading as an outlier when it is more than 4 standard
  deviations from its 28-day rolling mean.
  Acceptance: on the 2025 labelled sample, false-flag rate is below 1%.
  Test: test_R3_flags_outliers

## Constraints
- All timestamps are stored in UTC. Reason: local time duplicated intervals at
  the daylight-saving change. Source: change 01.
```

### changes/03-rolling-outlier-filter/1_intent.md

```markdown
# Change 03: Rolling outlier filter

Status: Active

## Why
Fixed 3 sigma flags about 6% of summer intervals, and most are real heatwave peaks.

## Goal
Cut false flags without missing meter faults.

## Done when
False-flag rate is below 1% on the 2025 labelled sample.

## Out of scope
Weather-adjusted thresholds.

## Decisions
- Chosen: 28-day rolling mean with a 4 sigma threshold.
- Rejected: fixed 3 sigma. Fails the false-flag measure.
- Rejected: isolation forest. More accurate, but hard to explain to network planning.
```

### 2_spec-delta.md

```markdown
# Spec delta: Rolling outlier filter

## Capabilities touched
specs/cleansing.md

## Added
- R3a: Substations with under 28 days of history are not filtered and are
  marked `insufficient_history`.
  Acceptance: a 10-day-old substation produces zero flags and the marker.

## Changed
- R3: fixed 3 sigma on the full history -> 4 sigma on a 28-day rolling mean.

## Removed
None.

## At risk
Gap-filling reads the outlier flag, so its output may change for past dates.
```

### 3_plan.md

```markdown
# Plan: Rolling outlier filter

## Approach
Replace the threshold function with a window function over 28 days per
substation. Keep the output schema unchanged apart from one new column.

## Files touched
src/cleansing/outliers.py, tests/test_outliers.py

## Tasks
- [x] T1: Write test_R3_flags_outliers against the labelled sample (R3)
- [x] T2: Implement the rolling mean and standard deviation (R3)
- [ ] T3: Write test_R3a_insufficient_history (R3a)
- [ ] T4: Add the insufficient_history marker (R3a)
- [ ] T5: Run all tests, including gap-filling (At risk)

## Open questions
Should the window be 28 calendar days or 28 days with data?
```
