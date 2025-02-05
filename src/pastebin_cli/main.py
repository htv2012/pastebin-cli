import types

import click

from . import config
from .display import display_paste
from .pastebin_api import PastebinAPI, parse_paste_list


@click.group()
@click.pass_context
@click.option("-j", "--json-output", is_flag=True)
def main(ctx: click.Context, json_output: bool):
    ctx.ensure_object(types.SimpleNamespace)
    ctx.json_output = json_output

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
def ls(ctx: click.Context):
    resp = ctx.obj.api.ls()
    if not resp.ok:
        click.echo(f"{resp.status_code} {resp.reason}", err=True)
        click.echo(resp.text)
        ctx.exit(1)

    pastes = parse_paste_list(resp.text)
    for paste in pastes:
        display_paste(paste)
