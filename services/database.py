"""Database."""

# Sqlite
import sqlite3

# Click
from click.exceptions import UsageError

# Utilities
from pathlib import Path
import os
import sys
import shutil


class DataBase:
    """Data base class."""

    dir_home = str(Path.home())

    def __init__(self):
        """Init method."""

        try:
            if sys.platform.startswith('linux'):
                os.mkdir('{}/deviceprotect'.format(self.dir_home))
            elif sys.platform.startswith('win32'):
                os.mkdir('{}\\deviceprotect'.format(self.dir_home))
        except OSError:
            pass

        self.sum_dir = '{}/deviceprotect'.format(self.dir_home)
        self.conn = sqlite3.connect('{}/backup.db'.format(self.sum_dir))
        self.cursor = self.conn.cursor()

    def create(self):
        """Create operation."""

        try:
            self.cursor.execute('''
                CREATE TABLE routes
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                PATH TEXT NOT NULL UNIQUE,
                IS_ENCRYPTED BOOLEAN DEFAULT 0,
                CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP)
            ''')
            self.cursor.execute('''
               CREATE TABLE keys
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                KEY TEXT NOT NULL,
                PATH TEXT NOT NULL UNIQUE,
                CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP)
            ''')
        except sqlite3.OperationalError:
            pass

    def insert_routes(self, **kwargs):
        """Insert routes operation."""

        try:
            self.cursor.execute(
                'INSERT INTO routes (PATH) VALUES ("{}")'.format(
                    kwargs['path']
                )
            )
        except sqlite3.IntegrityError:
            pass
        except sqlite3.OperationalError:
            raise UsageError(message='Something was wrong.')

        self.conn.commit()

    def insert_keys(self, **kwargs):
        """Inser keys operation."""

        try:
            self.cursor.execute(
                'INSERT INTO keys (KEY, PATH) VALUES ("{}", "{}")'.format(
                    kwargs['key'],
                    kwargs['path']
                )
            )
        except sqlite3.IntegrityError:
            self.cursor.execute(
                'UPDATE keys SET KEY="{}" WHERE PATH="{}"'.format(
                    kwargs['key'],
                    kwargs['path']
                )
            )
        except sqlite3.OperationalError:
            raise UsageError(message='Something was wrong.')

        self.conn.commit()

    def update_routes(self, **kwargs):
        """Update operation."""

        try:
            self.cursor.execute(
                'UPDATE routes SET IS_ENCRYPTED={} WHERE PATH="{}"'.format(
                    kwargs['is_encrypted'],
                    kwargs['path']
                )
            )
        except sqlite3.IntegrityError:
            pass
        except sqlite3.OperationalError:
            raise UsageError(message='Something was wrong.')

        self.conn.commit()

    def get(self, **kwargs):
        """Get operation."""

        try:
            data = self.cursor.execute('SELECT * FROM {}'.format(
                kwargs['table']
            ))
        except sqlite3.OperationalError:
            raise UsageError(message='Database not found.')

        return data

    def backup(self, **kwargs):
        """Get backup operation."""

        try:
            data = self.cursor.execute('SELECT KEY, PATH FROM keys')
        except sqlite3.OperationalError:
            raise UsageError(message='Invalid keys path.')

        return data
