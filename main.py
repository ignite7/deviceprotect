"""CLI"""

# Click
import click
from click.exceptions import UsageError

# Modules
from services.service import Services

# Utilities
from os import path


@click.group(help='What do you want to do?')
def cli():
    """
    Manage the main cli.
    """

    pass


@cli.command(help='Encrypt options.')
@click.option(
    '--files',
    '-f',
    multiple=True,
    type=(str),
    help='[PATH] file or files.'
)
@click.option(
    '--device',
    '-d',
    type=(str),
    help='[PATH] device.'
)
def encrypt(files, device):
    """
    Manage encrypt files and
    devices.
    """

    if files and device:
        raise UsageError(
            message='Choose only one option between (`files`, `device`).'
        )

    if files:
        for is_file in files:
            if not path.isfile(is_file):
                raise UsageError(message='The path is not a `file`.')
    elif device:
        if not path.isdir(device) and not path.ismount(device):
            raise UsageError(message='The path is not a `dir` or `mount`.')


    Services(
        files_path=files,
        device_path=device,
        service='encrypt'
    )


@cli.command(help='Decrypt options.')
@click.option(
    '--files',
    '-f',
    multiple=True,
    type=(str),
    help='[PATH] file or files.'
)
@click.option(
    '--device',
    '-d',
    type=(str),
    help='[PATH] device.'
)
@click.option(
    '--key',
    '-k',
    type=(str),
    required=True,
    help='[PATH] key.'
)
def decrypt(files, device, key):
    """
    Manage decrypt fiiles and
    devices.
    """

    if files and device:
        raise UsageError(
            message='Choose only one option between (`files`, `device`).'
        )

    if files:
        for is_file in files:
            if not path.isfile(is_file):
                raise UsageError(message='The path is not a `file`.')

    elif device:
        if not path.isdir(device) and not path.ismount(device):
            raise UsageError(message='The path is not a `dir` or `mount`.')

    Services(
        files_path=files,
        device_path=device,
        key=key,
        service='decrypt'
    )


if __name__ == '__main__':
    cli()
