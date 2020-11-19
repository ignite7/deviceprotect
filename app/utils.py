"""
Utils service.
"""

# Fernet
from cryptography.fernet import Fernet

# Utilities
from pathlib import Path
from os import path, mkdir, remove
import uuid


def user_dir(save_path):
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
        app_dir += '-{}'.format(uuid.uuid4())
        mkdir(app_dir)

    return app_dir


def create_key():
    """
    Create and returns the master
    key.
    """

    return Fernet.generate_key()


def output(service, db_manager, backup_path):
    """Shows the encrypt output."""

    if service == 'encrypt':
        query = db_manager.get()
        message = 'SUMMARY ENCRYPTATION INFO.\n'

        for data in query:
            save_path = path.join(data[0], 'summary.txt')
            message += (
                '|  MASTER PATH: {} | KEY: {} | ACTION: {} '
                '| CHILD PATH: {} | IS_ENCRYPTED: {} | CREATED AT: {} |\n'
            ).format(data[1], data[2], data[3], data[4], data[5], data[6])

        with open(save_path, 'w') as f:
            f.write(message)

        db_manager.conn.close()

        return print(
            'Encrypting ends up successfully\n',
            'The info can be found: "{}".'.format(save_path)
        )
    else:
        if path.exists(backup_path):
            remove(backup_path)
            print('Backup deleted successfully.')

        return print('Decrypting ends up successfully.')
