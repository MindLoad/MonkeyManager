# -*- coding: utf-8 -*-
# Created: 15.11.2019
# Changed: 17.11.2019

"""
Database dump service
"""

__all__ = [
    'DumpService',
]

import typing
import sqlite3

from PyQt5.QtWidgets import QFileDialog, QWidget


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
                f.write(f"{line}\n")

    @staticmethod
    def read_from_file(
            file_name: str
    ) -> None:
        """
        Import dump with SQL statements to main database
        :return: None
        """

        _file = open(file_name, 'r')
        _sql = _file.read()
        print(_sql)
        # self.cursor.executescript(_sql)

    @staticmethod
    def open_dump_file_dialog(
            root_widget: QWidget
    ) -> typing.Union[str, None]:
        """
        Open file dialog for selecting dump
        :return: None
        """

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
