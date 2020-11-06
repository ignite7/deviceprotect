"""CLI"""

# Click
import click
from click.exceptions import UsageError

# Modules
from app.service import Services
from app.database import DataBase

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
    help='Generate key by [PATH].'
)
@click.option(
    '--save-path',
    '-s',
    type=(str),
    help='Custom save [PATH].'
)
def encrypt(files, device, multiple_keys, save_path):
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
        save_path=save_path,
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

    if files and device:
        raise UsageError(
            message='Choose only one option between (`files`, `device`).'
        )

    if key and backup or not key and not backup:
        raise UsageError(
            message='Choose only one option between (`key`, `backup`).'
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
        backup=backup,
        service='decrypt'
    )


@cli.command(help='Recovery options.')
@click.option(
    '--db-path',
    '-d',
    type=(str),
    help='Safe encryptation. backup [PATH].'
)
def recovery(db_path):
    """
    Manage the recovery of
    the encryptation state
    of the files or folders.
    """

    db_manager = DataBase()
    query = db_manager.recovery(db_path=db_path)

    #TODO Make testing of this operation
    for data in query:
        if data[4] and not data[3]:
            Services(
                files_path=data[0],
                device_path=data[0],
                multiple_keys=None,
                save_path=data[2],
                service='encrypt'
            )
        elif not data[4] and data[3]:
            Services(
                files_path=data[0],
                device_path=data[0],
                key=data[1],
                backup=None,
                service='decrypt'
            )


if __name__ == '__main__':
    cli()
