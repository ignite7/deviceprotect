"""
Utils service.
"""

# Fernet
from cryptography.fernet import Fernet

# Utilities
from pathlib import Path
import os
import sys


def create_key():
    """
    Create and returns the master
    key.
    """

    return Fernet.generate_key()


def output(db_manager, service):
    """
    Shows the output to the user.
    """

    dir_home = str(Path.home())

    if sys.platform.startswith('linux'):
        user_path = '{}/deviceprotect/summary.txt'.format(dir_home)
    elif sys.platform.startswith('win32'):
        user_path = '{}\\deviceprotect\\summary.txt'.format(dir_home)

    if service == 'encrypt':
        fields = db_manager.get(table='keys')
        message = ''

        for field in fields:
            message += (
                'ID: {} | KEY: {} | '
                'PATH: {} | CRETATED AT: {}\n'
            ).format(field[0], field[1], field[2], field[3])

        with open(user_path, 'w') as raw_file:
            raw_file.write(message)

        return print(
            'Encrypting ends up successfully\n',
            'The info can be found: {}'.format(user_path)
        )
    elif service == 'decrypt':
        return print('Decrypting ends up successfully.')
