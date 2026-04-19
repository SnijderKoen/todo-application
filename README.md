# todo

A local, colorful CLI todo list. Built with [Typer](https://typer.tiangolo.com/) + [Rich](https://rich.readthedocs.io/).

> **Status:** M1 scaffolding only. No real task features yet — those land in the next milestones (see plan below).

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
todo            # placeholder panel
todo --help     # list commands (auto-generated)
todo --version
```

## Optional alias

You mentioned wanting a separate "edit" command. When `todo edit` lands in M5, add this to your shell rc:

```bash
alias todo-edit='todo edit'
```

## Data

Once task features land, tasks will be stored in `./tasks.json` in the working directory (git-ignored by default).

## Roadmap

- **M1** — Project skeleton, `todo` entry point, tests, lint. *(current)*
- **M2** — Core: `Task` model, JSON storage w/ atomic writes, config.
- **M3** — `todo add` + default list view (Rich table).
- **M4** — `done`, `undone`, `rm`, `show`.
- **M5** — `todo edit` via `$EDITOR`.
- **M6** — Labels & filters (`+label @ctx !!`).
- **M7** — Due-date parsing, overdue highlighting, shell completion docs.
- **M8** — Kanban `todo board`, optional Textual TUI.

## Dev

```bash
pytest        # run tests
ruff check .  # lint
ruff format . # format
```
