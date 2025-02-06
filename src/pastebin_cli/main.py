import types

import click

from . import config
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
@click.option("-c", "--content", required=True, prompt=True)
@click.option("-n", "--name")
@click.option("-f", "--fmt")
@click.option("-s", "--scope")
@click.option("-e", "--expiry")
@click.option("-F", "--folder")
@click.pass_context
def put(ctx: click.Context, content, name, fmt, scope, expiry, folder):
    """Create a new paste"""
    resp = ctx.obj.api.put(
        content=content,
        name=name,
        fmt=fmt,
        scope=scope,
        expiry=expiry,
        folder=folder,
    )
    print(resp)
    print(resp.text)
    resp.raise_for_status()
