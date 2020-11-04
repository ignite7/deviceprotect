"""Services."""

# Click
from click.exceptions import UsageError

# Fernet
from cryptography.fernet import Fernet

# Modules
from .utils import create_key, output, handler_dir_app
from .database import DataBase

# Utilities
from os import path, walk


class Services:
    """Service class."""

    db_manager = DataBase()

    def __init__(self, **kwargs):
        """Init method."""

        self.service = kwargs['service']
        self.user_path = list(kwargs['files_path']) \
            or list(kwargs['device_path'])
        self.key = kwargs.get('key') or create_key()
        self.fernet = Fernet(self.key)
        self.multiple_keys = kwargs.get('multiple_keys')
        self.db_path = kwargs.get('backup', None)
        self.dir_home = None

        if self.service == 'encrypt':
            self.dir_home = handler_dir_app(kwargs.get('save_path', None))
            self.db_manager.connection(self.dir_home)
            self.db_manager.create()

        if self.db_path:
            self.backup()
        else:
            self.kind()

    def backup(self):
        """
        Read the database for keys
        and its paths.
        """

        data = self.db_manager.backup(db_path=self.db_path)

        for path in data:
            self.user_path = [path[1]]
            self.key = path[0]
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
            if self.multiple_keys:
                if self.service == 'encrypt':
                    self.key = create_key()
                    self.fernet = Fernet(self.key)

            if self.service == 'encrypt':
                self.db_manager.insert_keys(
                    key=self.key.decode(),
                    path=files_path
                )

            if path.isfile(files_path):
                if self.service == 'encrypt':
                    self.db_manager.insert_routes(
                        path=files_path
                    )
                self.encryption(files_path)
            elif path.isdir(files_path) or path.ismount(files_path):
                    for dirs_path, dirs, files in walk(files_path):
                        for name in files:
                            if self.service == 'encrypt':
                                self.db_manager.insert_routes(
                                    path=path.join(dirs_path, name)
                                )
                            self.encryption(path.join(dirs_path, name))

        return output(self.db_manager, self.service, self.dir_home)

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

                if self.service == 'encrypt':
                    self.db_manager.update_routes(
                        is_encrypted=1,
                        path=path
                    )
        except OSError:
            raise UsageError(
                message=(
                    'You must grant permission to the script, '
                    'if you are in Linux try `sudo` or '
                    '`Run as administator` in Windows.'
                )
            )
