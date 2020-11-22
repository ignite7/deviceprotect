"""
Utils service.
"""

# Utilities
from pathlib import Path
from os import path, mkdir
import uuid


def user_dir(save_path=None):
    """
    Handle the creation
    of the main directory
    of the app.
    """

    dir_home = str(Path.home())

    if save_path:
        app_user_dir = path.join(save_path, 'deviceprotect')
    else:
        app_user_dir = path.join(dir_home, 'deviceprotect')

    try:
        mkdir(app_user_dir)
    except OSError:
        app_user_dir += '-{}'.format(uuid.uuid4())
        mkdir(app_user_dir)

    return app_user_dir


def output(service, db_manager):
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
        return print('Decrypting ends up successfully.')
