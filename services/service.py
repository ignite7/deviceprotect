"""
Services.
"""

# Fernet
from cryptography.fernet import Fernet

# Utilities
from .utils import create_key, output
import os


class Services:
    """
    Service class.
    """

    def __init__(self, **kwargs):
        """
        Init method.
        """

        self.service = kwargs['service']
        self.key = kwargs.get('key') or create_key()
        self.user_path = kwargs['file_path'] or kwargs['device_path']
        self.fernet = Fernet(self.key)
        self.kind()

    def kind(self):
        """
        Choose the type depending
        `user_path` value.
        """

        if os.path.isfile(self.user_path):
            self.encryption(self.user_path)

        elif os.path.isdir(self.user_path):
            for dirs_path, dirs, files in os.walk(self.user_path):
                for name in files:
                    self.encryption(os.path.join(dirs_path, name))

        return output(self.key, self.user_path)

    def encryption(self, path):
        """
        Encrypt or decrypt the files
        depending of the service.
        """

        with open(path, 'rb') as raw_file:
            file_data = raw_file.read()

        if self.service == 'encrypt':
            new_file_data = self.fernet.encrypt(file_data)

        elif self.service == 'decrypt':
            new_file_data = self.fernet.decrypt(file_data)

        with open(path, 'wb') as raw_file:
            raw_file.write(new_file_data)

