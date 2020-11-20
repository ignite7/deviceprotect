"""Services."""

# Click
from click.exceptions import UsageError

# Fernet
from cryptography.fernet import Fernet, InvalidToken

# Utilities
from tqdm import tqdm
from os import path, walk
import os
import sys

# Base dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Modules
from app.utils import user_dir, output
from app.database import DataBase


class Services:
    """Service class."""

    db_manager = DataBase()

    def __init__(self, **kwargs):
        """Init method."""

        self.user_path = (
            list(kwargs.get('files_path', None))
            or list(kwargs.get('device_path', None))
        )
        self.service = kwargs.get('service', None)
        self.key = kwargs.get('key') or Fernet.generate_key()
        self.multiple_keys = kwargs.get('multiple_keys', None)
        self.backup_path = kwargs.get('backup_path', None)
        self.fernet = Fernet(self.key)

        if self.service == 'encrypt':
            self.home_dir = user_dir(kwargs.get('output_path', None))
            self.detail_id = self.db_manager.connection(
                output_path=self.home_dir,
                action=self.service
            )

        if self.backup_path:
            self.backup()
        else:
            self.kind()

    def backup(self):
        """
        Read the database for keys
        and its paths.
        """

        query = self.db_manager.backup(db_path=self.backup_path)

        for data in query:
            self.user_path = [data[1]]
            self.key = data[0]
            self.fernet = Fernet(self.key)
            self.kind()

    def kind(self):
        """
        Choose the type depending
        `user_path` value, this method
        is used for iterate files encrypted
        and files not encrypted.
        """

        for files_path in tqdm(self.user_path, desc='Progress', unit='enc'):
            if self.service == 'encrypt':
                if self.multiple_keys:
                    self.key = Fernet.generate_key()
                    self.fernet = Fernet(self.key)

                self.key_id = self.db_manager.insert_keys(
                    key=self.key.decode(),
                    path=files_path
                )

            if path.isfile(files_path):
                if self.service == 'encrypt':
                    self.db_manager.insert_routes(
                        path=files_path,
                        key_id=self.key_id,
                        detail_id=self.detail_id
                    )
                self.encryption(files_path)
            elif path.isdir(files_path) or path.ismount(files_path):
                for dirs_path, _, files in walk(files_path):
                    for name in files:
                        if self.service == 'encrypt':
                            self.db_manager.insert_routes(
                                path=path.join(dirs_path, name),
                                key_id=self.key_id,
                                detail_id=self.detail_id
                            )
                        self.encryption(path.join(dirs_path, name))

        return output(self.service, self.db_manager, self.backup_path)

    def encryption(self, path):
        """
        Encrypt or decrypt the files
        depending of the service.
        """

        try:
            with open(path, 'rb+') as f:
                old_data = f.read()

                if self.service == 'encrypt':
                    new_data = self.fernet.encrypt(old_data)
                    self.db_manager.insert_routes(is_encrypted=1, path=path)
                else:
                    new_data = self.fernet.decrypt(old_data)

                f.seek(0)
                f.write(new_data)
                f.truncate()
        except InvalidToken:
            raise UsageError(message='Invalid key.')
