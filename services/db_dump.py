"""
Database dump service
"""

__all__ = [
    'DumpService',
]

import sqlite3


class DumpService:
    """
    Dump service
    """

    def __init__(
            self,
            connection: sqlite3.Connection,
            cursor: sqlite3.Cursor,
    ):
        self.connection = connection
        self.cursor = cursor

    def write_to_file(self) -> None:
        """
        Export sqlite3 database to file with SQL statements
        :return: None
        """

        with open('dump.sql', 'w') as f:
            for line in self.connection.iterdump():
                print(line)
                f.write(f"{line}\n")

    def read_from_file(self) -> None:
        """
        Import dump with SQL statements to main database
        :return: None
        """

        _file = open('dump.sql', 'r')
        _sql = _file.read()
        print(_sql)
        # self.cursor.executescript(_sql)
