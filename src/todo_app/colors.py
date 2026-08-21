# All labels will get a color assigned from this list
LABEL_COLORS: list[str] = [
    "orange1",
    "deep_sky_blue1",
    "spring_green1",
    "medium_purple1",
    "gold1",
    "cyan1",
    "salmon1",
    "light_steel_blue",
    "chartreuse1",
    "medium_orchid1",
    "yellow1",
    "turquoise2",
    "light_coral",
    "violet",
    "aquamarine1",
    "plum1",
    "sky_blue1",
    "gold3",
    "medium_spring_green",
    "orchid1",
    "cyan2",
    "sandy_brown",
    "light_steel_blue1",
    "khaki3",
    "pink1",
    "dark_turquoise",
    "light_salmon1",
    "cornflower_blue",
    "light_goldenrod2",
    "thistle1",
    "aquamarine3",
    "navajo_white1",
    "medium_purple2",
    "steel_blue1",
    "plum2",
    "pale_violet_red1",
]

ID_COLOR = "cyan"
TITLE_COLOR = "thistle1"
COMPLETED_COLOR = "dark_sea_green3"
MARK_COMPLETED_COLOR = "green3"
MARK_UNCOMPLETED_COLOR = "yellow"
DEADLINE_COLOR = "red1"
DEADLINE_OVERDUE_COLOR = "red"
DEADLINE_TODAY_COLOR = "yellow"
DEADLINE_SOON_COLOR = "orange1"
DEADLINE_OK_COLOR = "green"
CREATED_COLOR = "dim light_steel_blue"
ERROR_COLOR = "red"
LABEL_COLOR = "grey100"
ADDED_COLOR = "green"
DELETED_COLOR = "bright_red"
NOT_FOUND_COLOR = "orange_red1"


if __name__ == "__main__":
    from rich.console import Console

    console = Console()
    for color in LABEL_COLORS:
        console.print(f"[{color}]{color}[/{color}]")
