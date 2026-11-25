# Spec delta: Planning template

## Capabilities touched

None. The six pages under `specs/` say what they said under `spec/`; only their headings and
their place changed. The layout in [02_spec.md](../../../02_spec.md) names the new folders.

## Added

- `planning/README.md`, `specs/_template.md` and `changes/_template/`: the template's own files.
- A section "Planning" in `AGENTS.md`, with the template's six rules for the agent.

## Changed

Where each section of the old pages went. Paths are relative to `planning/`; "archive" stands
for `changes/archive`.

### 01_intent.md

| Old section | Now in |
|---|---|
| Opening line | `01_intent.md`, opening line, reworded: it pointed to the plan and the old status page |
| What PyNMDF is, first paragraph | `01_intent.md`, Goal |
| What PyNMDF is, second paragraph | `01_intent.md`, Problem |
| Who it is for | `01_intent.md`, Stakeholders |
| What it holds | `02_spec.md`, System overview |
| What must stay true | `01_intent.md`, Constraints |
| Publications | `01_intent.md`, Publications (extra heading) |
| Not now | `01_intent.md`, Out of scope. "The backlog of the plan" now reads "Later on the status page" |

### 02_spec.md

| Old section | Now in |
|---|---|
| Opening lines | `02_spec.md`, opening lines. "Component" now reads "capability", `spec/` reads `specs/` |
| Layout | `02_spec.md`, System overview, Layout (extra sub-heading). The three lines for `planning/` describe the new folders |
| Components | `02_spec.md`, Capabilities. The links point to `specs/` |
| What a publication folder holds | `02_spec.md`, System overview, same sub-heading (extra) |
| Exploration | `02_spec.md`, System overview, Exploration (extra sub-heading) |
| Configuration | `02_spec.md`, System overview, Configuration (extra sub-heading) |
| Rules that hold everywhere | `02_spec.md`, Cross-cutting constraints |
| Extending | `02_spec.md`, Extending (extra heading) |

### 03_planning.md

| Old section | Now in |
|---|---|
| Opening lines | `archive/02-planning-documents/3_plan.md`, opening lines. Two sentences on how the old page worked are dropped |
| Steps | `archive/02-planning-documents/3_plan.md`, Steps (extra heading). The Detail column points to the archived changes |
| Why this order | `archive/02-planning-documents/3_plan.md`, Approach |
| How the steps are worked | `archive/02-planning-documents/3_plan.md`, Approach |
| Backlog | `00_status.md`, Later, one line for each row |

### 99_status.md

| Old section | Now in |
|---|---|
| Opening lines, on how the old page worked | Dropped. `README.md` says how the new page works |
| Now: Step in hand | `00_status.md`, Active change |
| Now: Public, Review gate, Branch, Tag, Results | `00_status.md`, State |
| Now: Done | `00_status.md`, State, reworded: it lists changes in place of steps |
| Where the repository differs from the spec | `00_status.md`, State, the line "Spec" |
| Open items | `00_status.md`, Open issues |
| Decided on 24 November 2026, after the review | `archive/05-tidy-and-go-public/1_intent.md`, Decisions |
| Log, 25 November 2026: what the paper shows | `archive/06-what-the-paper-shows/3_plan.md`, Outcome |
| Log, 24 November 2026: public | `archive/05-tidy-and-go-public/3_plan.md`, Outcome |
| Log, 24 November 2026: review follow-ups | `archive/05-tidy-and-go-public/3_plan.md`, Outcome |
| Log, 24 November 2026: tidied and reviewed | `archive/05-tidy-and-go-public/3_plan.md`, Outcome |
| Log, 24 November 2026: M4 revised | `archive/04-piecewise-m4/3_plan.md`, Outcome |
| Log, 24 November 2026: repository restructured | `archive/03-archive-and-restructure/3_plan.md`, Outcome |
| Log, 24 November 2026: current version archived | `archive/03-archive-and-restructure/3_plan.md`, Outcome |
| Log, 24 November 2026: planning documents written | `archive/02-planning-documents/3_plan.md`, Outcome |
| Log, 18 November 2026: conference analysis complete | `archive/01-conference-analysis/3_plan.md`, Outcome |
| Log, 11 to 12 November 2026: plan and design | `archive/01-conference-analysis/3_plan.md`, Outcome |

### plan/01_archive_and_restructure.md

| Old section | Now in |
|---|---|
| Opening lines | `archive/03-archive-and-restructure/1_intent.md`, opening lines |
| Step 2: Goal; Step 3: Goal | `archive/03-archive-and-restructure/1_intent.md`, Goal |
| Step 2: What is done | `archive/03-archive-and-restructure/3_plan.md`, Tasks |
| Step 2: Done when; Step 3: Done when | `archive/03-archive-and-restructure/1_intent.md`, Done when |
| Step 3: Moves | `archive/03-archive-and-restructure/2_spec-delta.md`, Changed |
| Step 3: Edits that follow from the moves; Check | `archive/03-archive-and-restructure/3_plan.md`, Tasks |
| Not in these steps | `archive/03-archive-and-restructure/1_intent.md`, Out of scope |

### plan/02_piecewise_m4.md

| Old section | Now in |
|---|---|
| Opening lines | `archive/04-piecewise-m4/1_intent.md`, opening lines and the Status line |
| Why | `archive/04-piecewise-m4/1_intent.md`, Why |
| What changed | `archive/04-piecewise-m4/2_spec-delta.md`, Changed |
| The knots | `archive/04-piecewise-m4/1_intent.md`, Decisions |
| What was done | `archive/04-piecewise-m4/3_plan.md`, Tasks |
| What it did to the results | `archive/04-piecewise-m4/3_plan.md`, Outcome |
| The form that was set aside | `archive/04-piecewise-m4/1_intent.md`, Decisions |
| Not in this step | `archive/04-piecewise-m4/1_intent.md`, Out of scope |

### plan/03_tidy_and_go_public.md

| Old section | Now in |
|---|---|
| Opening line | `archive/05-tidy-and-go-public/1_intent.md`, opening lines |
| Step 5: tidy for publication | `archive/05-tidy-and-go-public/3_plan.md`, Tasks. Its last paragraph, "Not in this step", is in `1_intent.md`, Out of scope |
| The review gate | `archive/05-tidy-and-go-public/3_plan.md`, Tasks |
| Step 6: go public | `archive/05-tidy-and-go-public/3_plan.md`, Tasks |
| Done when | `archive/05-tidy-and-go-public/1_intent.md`, Done when |

### spec/, now specs/

On every page the title loses "Spec:", "Back to the spec" reads "Back to the spec index", and
the section "Decision record" is a paragraph at the end of Constraints.

| Old section | Now in |
|---|---|
| Purpose, on all six pages | Purpose |
| Code, on five pages | Purpose, as a paragraph that starts "Code." |
| `data_sources.md`: The three sources | Inputs (the columns Source, Module and Reads) and Outputs (Source, Module and Returns) |
| `data_sources.md`: Rules | Constraints |
| `data_sources.md`: Where a new source plugs in | Same heading (extra) |
| `network_total.md`: Steps | Process |
| `network_total.md`: Outputs | Outputs |
| `network_total.md`: Rules | Constraints |
| `targets.md`: The three scored targets; The daily lows | Outputs, each as a sub-heading (extra) |
| `targets.md`: Rules | Constraints |
| `models.md`: The models; How they are fitted; Temperature as a V in M4; Adding a model | Process, each as a sub-heading (extra) |
| `models.md`: Rules | Constraints |
| `poe_and_evaluation.md`: POE levels; Two recipes; The backtest; Scores | Process, each as a sub-heading (extra) |
| `poe_and_evaluation.md`: Rules | Constraints |
| `outputs.md`: Where things go | Outputs |
| `outputs.md`: Rules | Constraints |
| `outputs.md`: Earlier versions | Constraints, as the item that starts "Earlier versions." |

### Outside planning/

| File | Change |
|---|---|
| `AGENTS.md` | "Start here" points to the new pages. "Keeping the documents true" says when the spec and status pages are updated. One line on the archive of changes is added to the deliberate oddities |
| `README.md` | The layout line and the section on the planning documents describe the new folder |

## Removed

- `03_planning.md`, `99_status.md`, `plan/` and `spec/`, once their content was in place.
- Template headings with nothing to say: Success measures in the intent; Tech stack in the spec
  index; Requirements and Known limits on all six spec pages; Inputs on five of them, Process
  on three and Outputs on two.
- Five sentences that said how the old pages worked: three at the top of the old status page
  and two at the top of the old plan.

## At risk

Links into the old pages from outside `planning/`. Two files had any: `AGENTS.md` and the root
`README.md`. Both are corrected.
