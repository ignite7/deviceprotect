"""Services."""

# Click
from click.exceptions import UsageError

# Fernet
from cryptography.fernet import Fernet

# Modules
from .utils import create_key, output

# Utilities
from os import path, walk


class Services:
    """Service class."""

    def __init__(self, **kwargs):
        """Init method."""

        self.service = kwargs['service']
        self.key = kwargs.get('key') or create_key()
        self.user_path = list(kwargs['files_path']) or kwargs['device_path']
        self.fernet = Fernet(self.key)
        self.kind()

    def kind(self):
        """
        Choose the type depending
        `user_path` value.
        """

        if isinstance(self.user_path, list):
            for files_path in self.user_path:
                self.encryption(files_path)
        elif path.isdir(self.user_path) or path.ismount(self.user_path):
            for dirs_path, dirs, files in walk(self.user_path):
                for name in files:
                    self.encryption(path.join(dirs_path, name))

        return output(self.key, self.user_path)

    def encryption(self, path):
        """
        Encrypt or decrypt the files
        depending of the service.
        """

        try:
            with open(path, 'rb') as raw_file:
                file_data = raw_file.read()

            if self.service == 'encrypt':
                new_data = self.fernet.encrypt(file_data)
            elif self.service == 'decrypt':
                new_data = self.fernet.decrypt(file_data)

            with open(path, 'wb') as raw_file:
                raw_file.write(new_data)
        except OSError:
            raise UsageError(
                message=(
                    'You must grant permission to the script, '
                    'if you are in Linux try `sudo` or '
                    '`Run as administator` in Windows.'
                )
            )
