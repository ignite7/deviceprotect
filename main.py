"""
CLI
"""

# Click
import click

# Modules
from services.encrypt import EncryptService


@click.group(help='What do you want to do?')
def cli():
    """
    Manage the main cli.
    """

    pass


@cli.command(help='File options.')
@click.option(
    '--file',
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
def encrypt(file, device):
    """
    Manage encrypt files and devices.
    """

    EncryptService(
        file=file,
        device=device
    )


@cli.command(help='Device options.')
@click.option(
    '--file',
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
def decrypt(file, device, key):
    """
    Manage decrypt fiiles and devices.
    """

    pass


if __name__ == '__main__':
    cli()
