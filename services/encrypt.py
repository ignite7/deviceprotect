"""
Encrypt service.
"""

# Fernet
from cryptography.fernet import Fernet

# Utilities
from .utils import create_key, output
import os


class EncryptService:
    """
    Class encrypt service.
    """

    def __init__(self, **kwargs):
        """
        Init method.
        """

        self.key = create_key()
        self.kwargs = kwargs['file'] or kwargs['device']
        self.fernet = Fernet(self.key)
        self.encrypt()

    def encrypt(self):
        """
        Encrypting files.
        """

        if os.path.isfile(self.kwargs):
            self.iter_encrypt(self.kwargs)

        elif os.path.isdir(self.kwargs):
            for dirs_path, dirs, files in os.walk(self.kwargs):
                for name in files:
                    self.iter_encrypt(os.path.join(dirs_path, name))

        return output(self.key, self.kwargs)

    def iter_encrypt(self, path):
        """
        Iterate by the path, encrypting
        one by one.
        """

        with open(path, 'rb') as raw_file:
            file_data = raw_file.read()

        encrypt_data = self.fernet.encrypt(file_data)

        with open(path, 'wb') as raw_file:
            raw_file.write(encrypt_data)


