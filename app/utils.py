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
import uuid

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
        app_dir += '-{}'.format(uuid.uuid4())
        mkdir(app_dir)

    return app_dir


def create_key():
    """
    Create and returns the master
    key.
    """

    return Fernet.generate_key()


def encrypt_output(db_manager):
    """Shows the encrypt output."""

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


def decrypt_output():
    """Shows the decrypt output."""

    return print('Decrypting ends up successfully.')
