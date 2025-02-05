# display.py


import rich.console
import rich.json
import rich.theme

TITLE = "paste_title"
KEY = "paste_key"
URL = "paste_url"

MY_THEME = rich.theme.Theme(
    {
        "title": "light_goldenrod1",
        "meta": "bright_black",
        "content": "white",
        "error": "red",
    }
)


def _get_console():
    return rich.console.Console(theme=MY_THEME)


def display_paste(paste: dict):
    console = _get_console()
    console.print(paste[TITLE], style="title")
    console.print(f"Key: {paste[KEY]}")
    console.print(f"URL: {paste[URL]}")
    console.print()


def display_json(data: dict):
    console = _get_console()
    console.print(rich.json.JSON.from_data(data, indent=2))
