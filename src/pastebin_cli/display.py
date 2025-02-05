# display.py
import typing

import rich.console
import rich.json
import rich.theme


class Paste(typing.TypedDict):
    paste_key: str
    paste_date: str
    paste_title: str
    paste_size: str
    paste_expire_date: str
    paste_private: str
    paste_format_long: str
    paste_format_short: str
    paste_url: str
    paste_hits: str


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


def display_paste(paste: Paste):
    """Display a paste with color"""
    console = _get_console()
    console.print(paste["paste_title"], style="title", highlight=False)
    console.print(f"Key: {paste['paste_key']}")
    console.print(f"URL: {paste['paste_url']}")
    console.print()


def display_json(data: dict):
    """Display a JSON object with syntax highlighting"""
    console = _get_console()
    console.print(rich.json.JSON.from_data(data, indent=2))


def display_text(text: str):
    """Display text, with syntax highlighting when possible"""
    console = _get_console()
    console.print(text)
