"""Load the analysis configuration.

Every parameter that is a decision lives in a YAML file at the repository root, not in the code.
``config.local.yaml`` (git-ignored, holds the real raw-data paths) is used when present;
otherwise ``config.example.yaml``.
"""

from pathlib import Path

import yaml

CONFIG_NAMES = ("config.local.yaml", "config.example.yaml")
# Where results go. ``figures`` and ``tables`` hold the paper's artifacts, ``checks`` what its
# limitation and robustness statements rely on, and ``exploration`` first looks and superseded
# figures. ``interim`` is cached data passed between notebooks.
OUTPUT_FOLDERS = ("interim", "figures", "tables", "checks", "exploration")


def find_root(start: Path | None = None) -> Path:
    """Return the repository root: the nearest folder at or above ``start`` holding a config file.

    Args:
        start: Folder to search from. Defaults to the current working directory, which is
            the notebook's own folder when a notebook runs.
    """
    here = (start or Path.cwd()).resolve()
    for folder in (here, *here.parents):
        if any((folder / name).exists() for name in CONFIG_NAMES):
            return folder
    raise FileNotFoundError(f"No {' or '.join(CONFIG_NAMES)} found at or above {here}")


def load_config(start: Path | None = None) -> dict:
    """Read the configuration and prepare the output folders.

    Args:
        start: Folder to search from; see ``find_root``.

    Returns:
        The configuration as a dictionary, with two additions: ``root`` (repository root) and
        ``dirs`` (absolute paths of the interim, figures, tables, checks and exploration
        folders, created if absent).
    """
    root = find_root(start)
    name = next(name for name in CONFIG_NAMES if (root / name).exists())
    config = yaml.safe_load((root / name).read_text(encoding="utf-8"))

    config["root"] = root
    config["dirs"] = {key: root / config["paths"][key] for key in OUTPUT_FOLDERS}
    for folder in config["dirs"].values():
        folder.mkdir(parents=True, exist_ok=True)
    return config
