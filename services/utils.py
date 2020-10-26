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


def output(key, file_path):
    """
    Shows the output to the user.
    """

    if sys.platform.startswith('linux'):
        user_path = '/home/{}/deviceprotect.txt'.format(USER)

    elif sys.platform.startswith('win32'):
        user_path = 'C:\\User\\{}/deviceprotect.txt'.format(USER)

    message = (
        'IMPORTANT DATA.\nKEY: {}\nPATH: {}\n'
    ).format(key.decode(), file_path)

    with open(user_path, 'w') as raw_file:
        raw_file.write(message)

    return print(
        'Encrypting ends up successfully\n',
        'The info can be found: {}'.format(user_path)
    )
