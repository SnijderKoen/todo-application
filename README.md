# Todo App

A local, colorful CLI todo list. Built with [Typer](https://typer.tiangolo.com/) + [Rich](https://rich.readthedocs.io/).

## Install (development)

Requires **Python 3.11+**.

```bash
# create a venv (optional but recommended)
python -m venv .venv
source .venv/bin/activate

# runtime deps only
pip install -r requirements.txt

# or install the package in editable mode so the `todo` command is on your PATH
pip install -e .

# dev extras (pytest, ruff)
pip install -r requirements-dev.txt
```

For a global install you can also use `pipx`:

```bash
pipx install .
```

## Usage (scaffold)

```bash
todo            # show todo app info
todo --help     # list commands (auto-generated)
todo --version
```

## Dev

```bash
pytest        # run tests
ruff check .  # lint
ruff format . # format
```
