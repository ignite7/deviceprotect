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
        Encrypt files.
        """

        if os.path.isfile(self.kwargs):
            with open(self.kwargs, 'rb') as raw_file:
                file_data = raw_file.read()

            encrypt_data = self.fernet.encrypt(file_data)

            with open(self.kwargs, 'wb') as raw_file:
                raw_file.write(encrypt_data)

        elif os.path.isdir(self.kwargs):
            for dirs_path, dirs, files in os.walk(self.kwargs):
                for name in files:
                    rel_path = os.path.join(dirs_path, name)

                    with open(rel_path, 'rb') as raw_file:
                        file_data = raw_file.read()

                    encrypt_data = self.fernet.encrypt(file_data)

                    with open(rel_path, 'wb') as raw_file:
                        raw_file.write(encrypt_data)

        return output(self.key, self.kwargs)
