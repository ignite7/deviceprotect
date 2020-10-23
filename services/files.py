"""
Files service.
"""

# Fernet
from cryptography.fernet import Fernet

# Utilities
from .utils import create_key, output

class FileService:
    """
    Class file service.
    """

    def __init__(self, **kwargs):
        """
        Init method.
        """
        
        self.key = create_key()
        self.kwargs = kwargs
        self.fernet = Fernet(self.key)

        if self.kwargs['encrypt']:
            self.encrypt()

        elif self.kwargs['decrypt']:
            pass

    def encrypt(self):
        """
        Encrypt files.
        """

        with open(self.kwargs['encrypt'], 'rb') as raw_file:
            file_data = raw_file.read()

        encrypt_data = self.fernet.encrypt(file_data)
        
        with open(self.kwargs['encrypt'], 'wb') as raw_file:
            raw_file.write(encrypt_data)

        return output(self.key, self.kwargs['encrypt'])

