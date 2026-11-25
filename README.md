# PyNMDF: Python for Network Minimum Demand Forecasting

PyNMDF is the reproducible analysis code behind research on forecasting minimum demand in
distribution networks as rooftop photovoltaic (PV) capacity grows. It holds one shared package
and one folder per publication. Every input is public.

## The problem

Minimum demand on a distribution network is falling as rooftop PV capacity rises, and it has
moved from the early morning to the middle of the day. In the case study here, the sum of
Ausgrid's public zone substations, the lowest daytime half hour of the year fell from 1,833 MW
in 2015 to 880 MW in 2025, while the lowest overnight half hour stayed between 1,368 and
1,495 MW.

The research asks which inputs and model forms forecast the minimum well a year ahead. Forecasts
are given as probability of exceedance (POE) levels: POE10, POE50 and POE90.

## Publications

| Folder | Paper | Question |
|---|---|---|
| [publication/01_conference](publication/01_conference/README.md) | Four-page conference paper | Once rooftop PV capacity is in the model, does weather improve one-year-ahead probabilistic forecasts of annual minimum demand? |

## Install

Windows, Python 3.11:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

## Quick start

The tests run on synthetic data, so they show the package working before any data is
downloaded:

```powershell
.venv\Scripts\python -m pytest
```

Expected output, after about 15 seconds:

```
............                                                             [100%]
12 passed
```

The results of the conference paper can be read without running anything: start with
[publication/01_conference/results_summary.md](publication/01_conference/results_summary.md).
To rebuild them, see [Reproducing a paper](#reproducing-a-paper).

## Repository layout

```
src/pynmdf/                  the shared package: all logic lives here
tests/                       pytest tests on synthetic data
publication/01_conference/   the conference paper: notebooks, results, decision record
exploration/                 first looks and superseded figures; no paper relies on it
planning/                    status, intent and spec of the repository, and the record of each change
config.example.yaml          data paths and every decision parameter
AGENTS.md                    guidance for coding agents
```

The package is read in the order of the analysis:

```
io_demand.py   read every zone substation file layout
io_pv.py       read PV capacity from the local government area workbooks
io_weather.py  read the Bureau of Meteorology daily files; fill short gaps
clean.py       the cleaning rule and the network total
targets.py     the three scored targets and the daily lows
models.py      the daily models M2 to M6
poe.py         POE10, POE50 and POE90
evaluate.py    rolling-origin backtest, scores and checks
plots.py       one function per figure
config.py      load the configuration
```

## Data

Every input is a public file from a public source. The repository holds the figures, tables
and checks built from these files, not the files themselves: download them from the sources
below and point the configuration at them.

| Variable | Source | What to download |
|---|---|---|
| Demand | [Ausgrid distribution zone substation data](https://www.ausgrid.com.au/about-us/about-ausgrid/research-data-sets/distribution-zone-substation-data) | One archive per reporting year, FY2015 to FY2026 (each runs 1 May to 30 April). Leave them zipped, or unzip into a folder |
| PV capacity | [Ausgrid average electricity use](https://www.ausgrid.com.au/about-us/about-ausgrid/research-data-sets/average-electricity-use) | The local government area workbook for each year, FY2015 to FY2025. FY2024 exists only as a PDF; its network total is entered in the configuration |
| Weather | [Bureau of Meteorology Climate Data Online](http://www.bom.gov.au/climate/data/), station 066037 (Sydney Airport AMO) | Daily maximum temperature (IDCJAC0010), daily minimum temperature (IDCJAC0011) and daily global solar exposure (IDCJAC0016), each as "all years of data" |

Then copy `config.example.yaml` to `config.local.yaml` and edit the entries under `paths`. That
is the only change needed; `config.local.yaml` is git-ignored.

Sources and credit:

- Demand and PV capacity: Ausgrid, which retains copyright in its data.
- Weather: Bureau of Meteorology, © Commonwealth of Australia. Licensed from the Commonwealth of
  Australia under a Creative Commons Attribution 4.0 International licence.
- Solar exposure data derived from satellite imagery processed by the Bureau of Meteorology from
  the Himawari series operated by Japan Meteorological Agency and from GOES-9 operated by the
  National Oceanographic & Atmospheric Administration (NOAA) for the Japan Meteorological
  Agency.

## Reproducing a paper

Each publication folder has a README with the steps. For the conference paper, install the
package, download the data, set the paths, and run its eight notebooks in order (about five
minutes): see [publication/01_conference/README.md](publication/01_conference/README.md). Its
figures, tables and checks are committed under `publication/01_conference/results`, and every
run reproduces them exactly.

## Tests

```powershell
.venv\Scripts\python -m pytest
.venv\Scripts\ruff check .
.venv\Scripts\black --check src tests
```

Twelve tests, all on synthetic data. They need no data files.

## Planning documents

[planning/](planning/00_status.md) holds the status, the intent and the spec of the repository,
and one folder for each change made to it. [planning/README.md](planning/README.md) says how
the folder works. Each publication keeps its own decision record.

## Licence

MIT. See [LICENSE](LICENSE). The licence covers the code. The data stay under the terms of
their sources.

## Acknowledgements

This project is part of Samhan's PhD study, supported by the University International
Postgraduate Award (UIPA) Scholarship from UNSW, the Industry Collaboration Project
Scholarship from Ausgrid, the RACE for 2030 Scholarship, and the NSW Decarbonisation
Innovation Hub (NSW Decarb Hub).

## Contributors

- Samhan Samhan (SPREE, UNSW; Demand Forecasting, Ausgrid)
- Navid Haghdadi (Demand Forecasting, Ausgrid)
- Daniel Sim (Demand Forecasting, Ausgrid)
- Anna Bruce (SPREE, UNSW)
- Baran Yildiz (SPREE, UNSW)

SPREE is the School of Photovoltaic and Renewable Energy Engineering.

## Use of AI

AI assistants were used throughout this repository: Claude, by Anthropic, in chat and through
Claude Code. They helped to brainstorm, to write and review the code and its tests, to run the
analysis and to draft the documentation. The notes under `publication/01_conference/notes` and
the analysis plan record that work as it happened.

The intent, the judgement, the taste and the accountability are the author's. The author set
the research question and the method, made the decisions recorded here, reviewed the
AI-generated output, and remains accountable for everything in this repository.
