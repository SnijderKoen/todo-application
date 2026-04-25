"""Todo CLI — a local, colorful command-line todo list."""

from importlib.metadata import version

# Single source of truth: the version declared in pyproject.toml.
# `importlib.metadata.version` reads it from the installed distribution's
# metadata, so bumping `pyproject.toml` is enough — no need to edit code.
__version__ = version("todo-app")
