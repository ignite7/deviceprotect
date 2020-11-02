"""Database."""

# Sqlite
import sqlite3

# Click
from click.exceptions import UsageError

# Utilities
import os


class DataBase:
    """Data base class."""

    def create(self):
        """Create operation."""

        conn = sqlite3.connect('backup.db')

        try:
            conn.execute('''
                CREATE TABLE routes
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                PATH TEXT NOT NULL,
                IS_ENCRYPTED BOOLEAN DEFAULT 0,
                CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP)
            ''')
            conn.execute('''
                CREATE TABLE keys
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                KEY TEXT NOT NULL,
                PATH TEXT NOT NULL,
                CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP)
            ''')
            conn.close()
        except sqlite3.OperationalError:
            pass

    def insert_routes(self, **kwargs):
        """Insert routes operation."""

        conn = sqlite3.connect('backup.db')
        conn.execute(
            'INSERT INTO routes (PATH) VALUES ("{}")'.format(
                kwargs['path']
            )
        )
        conn.commit()
        conn.close()

    def insert_keys(self, **kwargs):
        """Inser keys operation."""

        conn = sqlite3.connect('backup.db')
        conn.execute(
            'INSERT INTO keys (KEY, PATH) VALUES ("{}", "{}")'.format(
                kwargs['key'],
                kwargs['path']
            )
        )
        conn.commit()
        conn.close()

    def update_routes(self, **kwargs):
        """Update operation."""

        conn = sqlite3.connect('backup.db')
        conn.execute(
            'UPDATE routes SET IS_ENCRYPTED={} WHERE PATH="{}"'.format(
                kwargs['is_encrypted'],
                kwargs['path']
            )
        )
        conn.commit()
        conn.close()

    def get(self, **kwargs):
        """Get operation."""

        conn = sqlite3.connect('backup.db')
        data = conn.execute('SELECT * FROM {}'.format(kwargs['table']))

        return data

    def get_keys(self, **kwargs):
        """Get key operation."""

        try:
            conn = sqlite3.connect('{}'.format(kwargs['keys_path']))
        except sqlite3.OperationalError:
            raise UsageError(message='Invalid keys path.')

        data = conn.execute('SELECT KEY FROM keys')

        return data
