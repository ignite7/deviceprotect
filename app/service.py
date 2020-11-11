"""Services."""

# Click
from click.exceptions import UsageError

# Fernet
from cryptography.fernet import Fernet, InvalidToken

# Modules
from .utils import (
    create_key,
    handler_dir_app,
    encrypt_output,
    decrypt_output
)
from .database import DataBase

# Utilities
from os import path, walk


class Services:
    """Service class."""

    db_manager = DataBase()

    def __init__(self, **kwargs):
        """Init method."""

        self.service = kwargs.get('service', None)
        self.user_path = list(kwargs.get('files_path', None)) \
            or list(kwargs.get('device_path', None))
        self.key = kwargs.get('key') or create_key()
        self.multiple_keys = kwargs.get('multiple_keys', None)
        self.backup_path = kwargs.get('backup_path', None)
        self.fernet = Fernet(self.key)

        if self.service == 'encrypt':
            self.dir_home = handler_dir_app(kwargs.get('save_path', None))
            self.detail_id = self.db_manager.connection(
                save_path=self.dir_home,
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

        for files_path in self.user_path:
            if self.service == 'encrypt':
                if self.multiple_keys:
                    self.key = create_key()
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
                    for dirs_path, dirs, files in walk(files_path):
                        for name in files:
                            if self.service == 'encrypt':
                                self.db_manager.insert_routes(
                                    path=path.join(dirs_path, name),
                                    key_id=self.key_id,
                                    detail_id=self.detail_id
                                )
                            self.encryption(path.join(dirs_path, name))

        if self.service == 'encrypt':
            return encrypt_output(self.db_manager)
        else:
            return decrypt_output()

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
                if self.service == 'encrypt':
                    self.db_manager.insert_routes(
                        is_encrypted=1,
                        path=path
                    )

                raw_file.write(new_data)
        except OSError:
            raise UsageError(
                message=(
                    'You must grant permission to the script, '
                    'if you are in Linux try `sudo` or '
                    '`Run as administator` in Windows.'
                )
            )
        except InvalidToken:
            raise UsageError(message='Invalid key.')
