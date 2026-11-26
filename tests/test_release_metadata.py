"""Tests of the release metadata: the two files at the repository root that say how the
repository is cited and archived.

`CITATION.cff` feeds GitHub's "Cite this repository" box. `.zenodo.json` sets the record that
Zenodo makes from a GitHub release; when both files exist Zenodo reads only that one, so the
two must say the same.

These tests read those two files, not synthetic data. They need no raw data.
"""

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _citation() -> dict:
    """Load `CITATION.cff`, which is a YAML file."""
    return yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))


def test_R1_citation_file_is_complete():
    citation = _citation()

    # --- The four keys that Citation File Format 1.2.0 requires.
    assert citation["cff-version"] == "1.2.0"
    for key in ("message", "title", "authors"):
        assert citation[key], f"{key} is empty"

    # --- What this repository adds: the abstract, the licence and where the code is.
    assert citation["abstract"].strip()
    assert citation["license"] == "MIT"
    assert citation["repository-code"].startswith("https://github.com/")

    # --- The five authors, each with both parts of the name and an affiliation.
    assert len(citation["authors"]) == 5
    for author in citation["authors"]:
        for key in ("family-names", "given-names", "affiliation"):
            assert author[key].strip(), f"{key} is empty for {author}"


def test_R2_zenodo_file_agrees_with_citation_file():
    citation = _citation()
    zenodo = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))

    # --- What only the Zenodo record holds.
    assert zenodo["upload_type"] == "software"
    assert zenodo["keywords"], "keywords is empty"

    # --- What both files hold must be the same. The licence is compared without case, because
    #     each format spells the identifier its own way: `MIT` in the citation file and `mit` in
    #     Zenodo's list of licences.
    assert zenodo["title"] == citation["title"]
    assert zenodo["description"] == citation["abstract"]
    assert zenodo["license"].lower() == citation["license"].lower()

    # --- The same authors in the same order. Zenodo writes a name as "Family name, Given names".
    from_citation = [
        (f"{author['family-names']}, {author['given-names']}", author["affiliation"])
        for author in citation["authors"]
    ]
    from_zenodo = [(creator["name"], creator["affiliation"]) for creator in zenodo["creators"]]
    assert from_zenodo == from_citation
