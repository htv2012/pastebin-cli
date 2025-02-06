import click


def get_content(filename: str):
    """
    Get the content of a file

    If `filename` is "-", get content from stdin.

    If `Filename` is None, open an editor so the user can create
    the content.

    Return the content of the file, or editor. In case of editor,
    a None return value means the user did not create the content.
    """
    if filename is None:
        content = click.edit("(Edit the content of the paste here)", require_save=True)
    else:
        with click.open_file(filename) as stream:
            content = stream.read()

    return content
