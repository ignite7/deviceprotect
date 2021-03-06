"""CLI"""

# Click
import click
from click.exceptions import UsageError

# Fernet
from cryptography.fernet import Fernet

# Modules
from app.service import Services

# Utilities
from os import path, geteuid


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
    help='Generate key by [PATH].'
)
@click.option(
    '--output-path',
    '-s',
    type=(str),
    help='Custom save [PATH].'
)
def encrypt(files, device, multiple_keys, output_path):
    """
    Manage encrypt files and
    devices.
    """

    if geteuid() != 0:
        raise UsageError(
            message='You need root/admin permissions to do this operation.'
        )

    if files and device or not files and not device:
        raise UsageError(
            message='Choose only one option between (`files`, `device`).'
        )

    if output_path:
        if not path.isdir(path.abspath(output_path)):
            raise UsageError(message='The path is not a `dir`.')

    if files:
        if multiple_keys and len(files) <= 1:
            raise UsageError(
                'Multiple keys is only allow for several files or devices.'
            )

        for is_file in files:
            if not path.isfile(path.abspath(is_file)):
                raise UsageError(message='The path is not a `file`.')
    elif device:
        if multiple_keys and len(device) <= 1:
            raise UsageError(
                'Multiple keys is only allow for several files or devices.'
            )

        for is_dir in device:
            if not path.isdir(path.abspath(is_dir)):
                raise UsageError(message='The path is not a `dir` or `mount`.')

    print('Starting encryption...')
    Services(
        files_path=files,
        device_path=device,
        multiple_keys=multiple_keys,
        output_path=output_path,
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
    help='[PATH] key.'
)
@click.option(
    '--backup',
    '-b',
    type=(str),
    help='[PATH] database backup.'
)
def decrypt(files, device, key, backup):
    """
    Manage decrypt fiiles and
    devices.
    """

    if geteuid() != 0:
        raise UsageError(
            message='You need root/admin permissions to do this operation.'
        )

    if files and device:
        raise UsageError(
            message='Choose only one option between (`files`, `device`).'
        )

    if not files and not device and not backup:
        raise UsageError(message=(
            'Choose only one option between (`files`, `device`, `backup`).'
        ))

    if key and backup or not key and not backup:
        raise UsageError(
            message='Choose only one option between (`key`, `backup`).'
        )

    if key:
        try:
            Fernet(key)
        except (TypeError, ValueError):
            raise UsageError(message='Invalid key.')

    if files:
        for is_file in files:
            if not path.isfile(path.abspath(is_file)):
                raise UsageError(message='The path is not a `file`.')
    elif device:
        for is_dir in device:
            if not path.isdir(path.abspath(is_dir)):
                raise UsageError(message='The path is not a `dir` or `mount`.')

    print('Starting decryption...')
    Services(
        files_path=files,
        device_path=device,
        key=key,
        backup_path=backup,
        service='decrypt'
    )


if __name__ == '__main__':
    cli()
