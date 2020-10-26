"""
CLI
"""

# Click
import click
from click.exceptions import UsageError

# Modules
from services.service import Services


@click.group(help='What do you want to do?')
def cli():
    """
    Manage the main cli.
    """

    pass


@cli.command(help='File options.')
@click.option(
    '--files',
    '-f',
    type=(str),
    help='[PATH] file.'
)
@click.option(
    '--device',
    '-d',
    type=(str),
    help='[PATH] device.'
)
def encrypt(files, device):
    """
    Manage encrypt files and devices.
    """

    if files and device:
        raise UsageError(
            message='Choose only one option between (`files`, `device`)'
        )

    Services(
        file_path=files,
        device_path=device,
        service='encrypt'
    )


@cli.command(help='Device options.')
@click.option(
    '--files',
    '-f',
    type=(str),
    help='[PATH] file.'
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
    Manage decrypt fiiles and devices.
    """

    if files and device:
        raise UsageError(
            message='Choose only one option between (`files`, `device`)'
        )

    Services(
        file_path=files,
        device_path=device,
        key=key,
        service='decrypt'
    )


if __name__ == '__main__':
    cli()
