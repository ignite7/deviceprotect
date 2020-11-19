"""Database."""

# Sqlite
import sqlite3

# Click
from click.exceptions import UsageError

# Utilities
from os import path


class DataBase:
    """Data base class."""

    def connection(self, **kwargs):
        """Connection database."""

        self.conn = sqlite3.connect(
            path.join(kwargs['save_path'], 'backup.db')
        )
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute('''
                CREATE TABLE details
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                SAVE_PATH TEXT NOT NULL,
                ACTION TEXT NOT NULL,
                CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP)
            ''')
            self.cursor.execute('''
                CREATE TABLE routes
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                PATH TEXT NOT NULL UNIQUE,
                IS_ENCRYPTED BOOLEAN DEFAULT 0,
                ID_KEY INTEGER NOT NULL,
                ID_DETAIL INTERGER NOT NULL,
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

        self.cursor.execute('''
            INSERT INTO details (SAVE_PATH, ACTION)
            VALUES("{}", "{}")
        '''.format(kwargs['save_path'], kwargs['action']))
        query = self.cursor.execute('SELECT ID FROM details')

        for data in query:
            return data[0]

    def insert_routes(self, **kwargs):
        """Insert routes operation."""

        try:
            self.cursor.execute(
                '''INSERT INTO routes (PATH, ID_KEY, ID_DETAIL)
                VALUES ("{}", {}, {})'''.format(
                    kwargs['path'],
                    kwargs['key_id'],
                    kwargs['detail_id']
                )
            )
        except (KeyError, sqlite3.IntegrityError):
            self.cursor.execute(
                'UPDATE routes SET IS_ENCRYPTED={} WHERE PATH="{}"'.format(
                    kwargs['is_encrypted'],
                    kwargs['path']
                )
            )
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
        query = self.cursor.execute(
            'SELECT ID FROM keys WHERE PATH="{}"'.format(kwargs['path'])
        )

        for data in query:
            return data[0]

    def get(self):
        """Get operation."""

        try:
            query = self.cursor.execute('''
                SELECT d.SAVE_PATH, k.PATH, k.KEY,
                d.ACTION, r.PATH, r.IS_ENCRYPTED, r.CREATED_AT
                FROM routes AS r
                INNER JOIN keys AS k ON r.ID_KEY=k.ID
                INNER JOIN details AS d ON r.ID_DETAIL=d.ID
            ''')
        except sqlite3.OperationalError:
            raise UsageError(message='Database not found.')

        return query

    def backup(self, **kwargs):
        """Get backup operation."""

        try:
            conn = sqlite3.connect(kwargs['db_path'])
            cursor = conn.cursor()
            query = cursor.execute('SELECT KEY, PATH FROM keys')
        except sqlite3.OperationalError:
            raise UsageError(message='Invalid database [PATH].')

        return query
