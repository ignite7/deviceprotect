"""
Utils service.
"""

# Fernet
from cryptography.fernet import Fernet

# Utilities
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


def find_files(user_path):
    """
    Iterate for the path the
    user gave and find all
    files.
    """

    if os.path.isfile(user_path):
        patterns = [user_path]

    elif os.path.isdir(user_path):
        accumulate = []
        patterns = user_path.rstrip('/') + \
            '/{}'.format(next(os.walk(user_path))[1])

        for pattern in patterns:
            if os.path.isfile(pattern):
                accumulate.append(pattern)

            else:
                #TODO: Improve idea
                pass

    return patterns or accumulate


def output(key, file_path):
    """
    Shows the output to the user.
    """

    if sys.platform.startswith('linux'):
        user_path = '/home/{}/deviceprotect.txt'.format(USER)
 
    elif sys.platform.startswith('win32'):
        user_path = 'C\\Users\\{}/deviceprotect.txt'.format(USER)
  
    message = (
        'IMPORTANT DATA.\nKEY: {}\nPATH: {}\n'
    ).format(key, file_path)

    with open(user_path, 'w') as raw_file:
        raw_file.write(message)

    return print(
        'Encrypting ends up successfully\n',
        'The info can be found: {}'.format(user_path)
    )
