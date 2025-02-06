import types

import click

from . import config, filelib
from .display import display_json, display_paste, display_text
from .pastebin_api import PastebinAPI, parse_paste_list


@click.group()
@click.pass_context
@click.version_option()
def main(ctx: click.Context):
    """Access the pastebin.com data.

    Configuration file is at ~/.config/pastebin.toml
    """
    ctx.ensure_object(types.SimpleNamespace)

    try:
        settings = config.load()
    except config.ConfigError as error:
        click.echo(error, err=True)
        ctx.exit(1)

    ctx.obj.api = PastebinAPI(
        api_dev_key=settings["api_dev_key"],
        api_user_key=settings["api_user_key"],
    )


@main.command()
@click.pass_context
@click.option("-j", "--json-output", is_flag=True)
def ls(ctx: click.Context, json_output: bool):
    """List my pastes"""
    resp = ctx.obj.api.ls()
    if not resp.ok:
        click.echo(f"{resp.status_code} {resp.reason}", err=True)
        click.echo(resp.text)
        ctx.exit(1)

    pastes = parse_paste_list(resp.text)
    if json_output:
        display_json(pastes)
    else:
        for paste in pastes:
            display_paste(paste)


@main.command()
@click.pass_context
@click.argument("key")
def get(ctx: click.Context, key: str):
    """Get the raw content of a paste"""
    resp = ctx.obj.api.get(key)
    if not resp.ok:
        click.echo(f"{resp.status_code} {resp.reason}", err=True)
        click.echo(resp.text)
        ctx.exit(1)

    display_text(resp.text)


@main.command()
@click.argument("filename", required=False)
@click.option("-n", "--name", help="The name (title)")
@click.option(
    "-x", "--syntax", type=str.lower, help="The syntax, e.g. python, bash, make..."
)
@click.option(
    "-p",
    "--privacy",
    type=click.IntRange(0, 2),
    help="0=public, 1=unlisted, 2=private",
    default=2,
)
@click.option(
    "-e",
    "--expiry",
    type=click.Choice(["N", "10M", "1H", "1D", "1W", "2W", "1M", "6M", "1Y"]),
    help="N=Never, 10M=10 minutes, 1H=1 hour, 1D=1 day, 1W=1 week, 2W=2 weeks, 1Y=Year",
)
@click.option("-f", "--folder", help="Folder key")
@click.pass_context
def put(ctx: click.Context, filename, name, syntax, privacy, expiry, folder):
    """
    Create a new paste

    If FILENAME is -, stdin will be used

    If FILENAME is omitted, and editor will be launched to allow
    adding content
    """
    content = filelib.get_content(filename)
    if content is None:
        click.echo("Paste will not be created as there is no content.", err=True)
        ctx.exit(1)

    resp = ctx.obj.api.put(
        content=content,
        name=name,
        syntax=syntax,
        privacy=privacy,
        expiry=expiry,
        folder=folder,
    )

    if not resp.ok:
        click.echo(resp.text, err=True)
        ctx.exit(1)
    click.echo(resp.text)
