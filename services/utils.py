"""
Utils service.
"""

# Fernet
from cryptography.fernet import Fernet

# Utilities
from datetime import date
from pathlib import Path
from os import path, mkdir
import sys


def handler_dir_app(save_path):
    """
    Handle the creation
    of the main directory
    of the app.
    """

    dir_home = str(Path.home())

    if save_path:
        app_dir = path.join(save_path, 'deviceprotect')
    else:
        app_dir = path.join(dir_home, 'deviceprotect')

    try:
        mkdir(app_dir)
    except OSError:
        now = date.today()
        app_dir += now.strftime('%m-%d-%y_%H:%M:%S')
        mkdir(app_dir)

    return app_dir


def create_key():
    """
    Create and returns the master
    key.
    """

    return Fernet.generate_key()


def output(db_manager, service, dir_home):
    """
    Shows the output to the
    user.
    """

    if not dir_home:
        return print('Decrypting ends up successfully.')

    sum_path = path.join(dir_home, 'summary.txt')

    if service == 'encrypt':
        fields = db_manager.get(table='keys')
        message = 'SUMMARY INFO.\n'

        for field in fields:
            message += (
                'ID: {} | KEY: {} | '
                'PATH: {} | CRETATED AT: {}\n'
            ).format(field[0], field[1], field[2], field[3])

        with open(sum_path, 'w') as raw_file:
            raw_file.write(message)

        return print(
            'Encrypting ends up successfully\n',
            'The info can be found: "{}".'.format(sum_path)
        )
