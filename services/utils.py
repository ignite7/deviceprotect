"""
Utils service.
"""

# Fernet
from cryptography.fernet import Fernet

# Utilities
import os
import sys
import getpass

# OS user
USER = getpass.getuser()


def create_key():
    """
    Create and returns the master
    key.
    """

    return Fernet.generate_key()


def output(db_manager):
    """
    Shows the output to the user.
    """

    if sys.platform.startswith('linux'):
        user_path = '/home/{}/deviceprotect.txt'.format(USER)

    elif sys.platform.startswith('win32'):
        user_path = 'C:\\User\\{}/deviceprotect.txt'.format(USER)

    fields = db_manager.get(table='keys')
    message = ''

    for field in fields:
        message += (
            'ID: {} | KEY: {} | '
            'PATH: {} | CRETATED AT: {}\n'
        ).format(field[0], field[1].decode(), field[2], field[3])

    with open(user_path, 'w') as raw_file:
        raw_file.write(message)

    return print(
        'Encrypting ends up successfully\n',
        'The info can be found: {}'.format(user_path)
    )
