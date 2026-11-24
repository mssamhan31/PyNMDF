# Exploration

First looks, superseded figures and experiments: work that no paper relies on.

## Rules

- **A record, not a product.** Notebooks here are not held to the standard of a publication and
  are not rerun when the package changes. A notebook's stored outputs show the code of its time.
- **Nothing in `publication/` may depend on this folder.** Work moves from here into a
  publication only by being rebuilt there.
- **Outputs are git-ignored.** Each subfolder writes to its own `outputs/`.
- **Files are named for what they show**, never by a figure or table number, so none can be
  mistaken for a paper's figure.

## What is here

| Folder | Holds |
|---|---|
| `01_conference/` | Two notebooks from the conference study. `A1_model_exploration`: the first look at each model's POE50 (the middle probability of exceedance level) against the actuals, the day M3 predicts as lowest, and the miss on public holidays. `A2_superseded_figures`: figures the paper no longer uses |

Both notebooks read the cache of the conference study, so they run after its notebook 05. Their
stored outputs are from the first version of the models, tagged `conference-v1-straight-line-m4`.

## Adding an experiment

Add a folder, named for what it explores, with a short note of its question at the top of its
first notebook.
