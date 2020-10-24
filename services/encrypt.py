"""
Encrypt service.
"""

# Fernet
from cryptography.fernet import Fernet

# Utilities
from .utils import create_key, output, find_files
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
        
        patterns = find_files(self.kwargs)

        for pattern in patterns:
            with open(pattern, 'rb') as raw_file:
                file_data = raw_file.read()

            encrypt_data = self.fernet.encrypt(file_data)

            with open(pattern, 'wb') as raw_file:
                raw_file.write(encrypt_data)

        return output(self.key, self.kwargs)

