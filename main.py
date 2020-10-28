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
    multiple=True,
    type=(str),
    help='[PATH] device.'
)
@click.option(
    '--multiple-keys',
    '-m',
    is_flag=True,
    help='Generate key by [PATH]'
)
def encrypt(files, device, multiple_keys):
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
        for is_dir in device:
            if not path.isdir(is_dir) and not path.ismount(is_dir):
                raise UsageError(message='The path is not a `dir` or `mount`.')


    Services(
        files_path=files,
        device_path=device,
        multiple_keys=multiple_keys,
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
    multiple=True,
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
@click.option(
    '--multiple-keys',
    '-m',
    is_flag=True,
    help='Generate key by [PATH]'
)
def decrypt(files, device, key, multiple_keys):
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
        for is_dir in device:
            if not path.isdir(is_dir) and not path.ismount(is_dir):
                raise UsageError(message='The path is not a `dir` or `mount`.')

        Services(
        files_path=files,
        device_path=device,
        key=key,
        multiple_keys=multiple_keys,
        service='decrypt'
    )


if __name__ == '__main__':
    cli()
