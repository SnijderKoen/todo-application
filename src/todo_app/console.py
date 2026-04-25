"""Project-wide Rich Console.

Import this `console` in any module that needs to render user-facing output.
Defining it once here ensures every command shares the same terminal
detection, theme, and configuration.
"""

from __future__ import annotations

from rich.console import Console

console: Console = Console()
