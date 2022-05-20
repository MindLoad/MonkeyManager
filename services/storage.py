""" Database dump service """

__all__ = [
    'ConnectionService',
    'DumpService',
]

import typing
import sqlite3
from pathlib import Path
import attr
from PyQt5.QtWidgets import QFileDialog, QWidget


@attr.s(slots=True)
class ConnectionService:
    """ Connect to database """

    __connect = attr.ib(
        validator=attr.validators.instance_of(sqlite3.Connection),
        default=sqlite3.connect(Path(__file__).cwd() / 'crypt.db')
    )

    @property
    def connection(self) -> sqlite3.Connection:
        """ Current connection instance """
        return self.__connect


@attr.s(slots=True)
class DumpService:
    """ Dump service """

    connection = attr.ib(validator=attr.validators.instance_of(sqlite3.Connection))
    cursor = attr.ib(validator=attr.validators.instance_of(sqlite3.Cursor))

    def write_to_file(self) -> None:
        """ Export sqlite3 database to file with SQL statements """

        with open('dump.sql', 'w') as f:
            for line in self.connection.iterdump():
                f.write(f"{line}\n")

    @staticmethod
    def read_from_file(file_name: str) -> None:
        """ Import dump with SQL statements to main database """

        _file = open(file_name, 'r')
        _sql = _file.read()
        print(_sql)
        # self.cursor.executescript(_sql)

    @staticmethod
    def open_dump_file_dialog(
            root_widget: QWidget
    ) -> typing.Optional[str]:
        """ Open file dialog for selecting dump """

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            root_widget,
            "Open sql dump file",
            "",
            "All files (*);;SQL Dump Files (*.sql)",
            options=options
        )
        if file_name:
            return file_name
        return None
