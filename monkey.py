# -*- coding: utf-8 -*-
# Created: 13.09.2017
# Changed: 28.08.2019

import sys
import os
import sqlite3
import source
import ui

from PyQt5.QtWidgets import QApplication, QWidget, QToolButton, QLabel, QTableWidgetItem, QRadioButton
from PyQt5.QtCore import Qt, QSize, QTimer, QEvent
from PyQt5.QtGui import QIcon, QResizeEvent

from tools import run_decode
from services import SearchService
from widgets import AddNewKey


class Root(QWidget, ui.UiRootWindow):
    """
    Root application widget
    """

    def __init__(self):
        super().__init__(flags=Qt.WindowTitleHint)
        # Establish connection to db
        self.connection, self.cursor = self.get_connection()
        # Setup main window UI
        self.setup_ui(self)
        # Static variables
        self.current_parent = self._add = self.search_result = self.refresh_element = self.search_service = None
        # Widget element logic
        self.add_new.clicked.connect(lambda: self.add_form(None))
        self.search_field.returnPressed.connect(self.go_search)

        self.table.cellDoubleClicked.connect(self.click_item)

        # QTimer
        self.bg_timeout = QTimer(self)
        self.bg_timeout.setInterval(3000)
        self.bg_timeout.timeout.connect(self.back_to_white)
        # Build extra elements
        self.build_extra_elements()
        # Init extra services
        self.init_extra_services()

    @property
    def currently_checked_menu_button(self):
        """ return menu button that was clicked last """

        for button in (self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8):
            if button.check_mark is not None:
                return button
        return None

    @staticmethod
    def get_connection() -> [sqlite3.Connection, sqlite3.Cursor]:
        """
        Connect to Sqlite source
        :return: sqlite connection, cursor
        """

        c = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "/crypt.db")
        return c, c.cursor()

    def build_extra_elements(self):
        """
        Build extra UI elements
        """

        self.search_result = QLabel()
        self.search_result.setObjectName("search_result")
        self.second_layout_keys_childs.addWidget(self.search_result)

    def init_extra_services(self):
        """
        Initialize additional extra services
        get_connection should start before
        """

        self.search_service = SearchService(self.cursor)

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Delete and self.table.currentRow() >= 0:
                row = self.table.currentRow()
                row_id = self.table.item(row, 3).statusTip()
                sql = "DELETE FROM passwords " \
                      "WHERE id=?"
                self.cursor.execute(sql, (row_id,))
                self.connection.commit()
                self.table.removeRow(row)
            elif event.key() == Qt.Key_F4 and self.table.currentRow() >= 0:
                if not self.pass_input.text().strip():
                    self.secret_key_filter()
                    return QWidget.eventFilter(self, source, event)
                row = self.table.currentRow()
                data = (self.table.item(row, 0).text(), self.table.item(row, 1).text(), self.table.item(row, 2).text(),
                        self.table.item(row, 3).statusTip(), self.table.item(row, 4).text(),
                        self.table.item(row, 5).text(), self.table.item(row, 6).text(), self.table.item(row, 7).text())
                self.add_form(data)
            elif event.key() == Qt.Key_Tab and self.pass_input.hasFocus():
                self.search_field.setFocus(True)
                return True
            elif event.key() == Qt.Key_Tab and self.search_field.hasFocus():
                self.pass_input.setFocus(True)
                return True
        return QWidget.eventFilter(self, source, event)

    def resizeEvent(self, a0: QResizeEvent):
        if self._add:
            self._add.setFixedSize(self.size())

    def secret_key_filter(self):
        self.pass_input.setStyleSheet("background:#f3a7a7;")
        self.pass_input.setFocus(True)
        self.bg_timeout.start()

    def back_to_white(self):
        self.pass_input.setStyleSheet("background:#fff;")
        self.bg_timeout.stop()

    def add_form(self, arg):
        if not self.pass_input.text().strip():
            self.secret_key_filter()
            return
        self._add = AddNewKey(self.connection, self.cursor, self.pass_input.text(), arg, parent=main)
        self._add.show()

    def clear_child_table(self):
        for pos in reversed(range(self.second_layout_keys_childs.count())):
            curr_item = self.second_layout_keys_childs.takeAt(pos).widget()
            if curr_item is not None:
                curr_item.deleteLater()
        self.table.setRowCount(0)

    def build_table_rows(self, query):
        items = query.fetchall()
        rows = len(items)
        if not rows:
            self.clear_child_table()
            self.search_result = QLabel()
            self.search_result.setObjectName("search_result")
            self.search_result.setText("No results ...")
            self.second_layout_keys_childs.addWidget(self.search_result)
            return
        self.table.setRowCount(rows)
        for pos, item in enumerate(items):
            cell_title = QTableWidgetItem(item[1])
            cell_title.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            cell_title.setToolTip(item[1])
            cell_login = QTableWidgetItem(item[2])
            cell_login.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            cell_login.setToolTip(item[2])
            cell_email = QTableWidgetItem(item[3])
            cell_email.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            cell_email.setToolTip(item[3])
            cell_password = QTableWidgetItem("********")
            cell_password.setStatusTip(f"{item[0]}")
            cell_password.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            cell_url = QTableWidgetItem(item[4])
            cell_url.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            cell_url.setToolTip(item[4])
            cell_phone = QTableWidgetItem(item[5])
            cell_phone.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            cell_created = QTableWidgetItem(item[6])
            cell_created.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            cell_modified = QTableWidgetItem(item[7])
            cell_modified.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(pos, 0, cell_title)
            self.table.setItem(pos, 1, cell_login)
            self.table.setItem(pos, 2, cell_email)
            self.table.setItem(pos, 3, cell_password)
            self.table.setItem(pos, 4, cell_url)
            self.table.setItem(pos, 5, cell_phone)
            self.table.setItem(pos, 6, cell_created)
            self.table.setItem(pos, 7, cell_modified)
        for row in range(rows):
            self.table.setRowHeight(row, 45)

    def get_childs(self, sender):
        """ Generate sub dirs relevant to main menu element """

        self.clear_child_table()
        self.current_parent = sender
        # Create Childs
        self.refresh_element = QToolButton()
        self.refresh_element.setObjectName('refresh')
        self.refresh_element.setIcon(QIcon(':/refresh'))
        self.refresh_element.setIconSize(QSize(22, 22))
        self.refresh_element.setCursor(Qt.PointingHandCursor)
        self.refresh_element.clicked.connect(lambda: self.get_keys(True, refresh=self.refresh_element.statusTip()))
        self.refresh_element.setEnabled(False)
        self.second_layout_keys_childs.addWidget(self.refresh_element)
        self.second_layout_keys_childs.addSpacing(5)
        sql = "SELECT DISTINCT child " \
              "FROM passwords " \
              "WHERE parent=? " \
              "ORDER BY child ASC"
        query = self.cursor.execute(sql, (sender,))
        for item in query.fetchall():
            child_element = QRadioButton()
            child_element.setObjectName("child-element")
            child_element.setText(item[0])
            child_element.setMinimumHeight(22)
            child_element.setCursor(Qt.PointingHandCursor)
            child_element.clicked.connect(self.get_keys)
            self.second_layout_keys_childs.addWidget(child_element)
            self.second_layout_keys_childs.addSpacing(5)

    def get_keys(self, status, refresh=None):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        sender = self.sender().text() if not refresh else refresh
        sql = "SELECT id, title, login, email, url, phone, created, modified " \
              "FROM passwords " \
              "WHERE child=? " \
              "ORDER BY title ASC"
        query = self.cursor.execute(
            sql,
            (sender,))
        self.build_table_rows(query)
        self.table.setSortingEnabled(True)
        self.refresh_element.setEnabled(True)
        self.refresh_element.setStatusTip(sender)

    def click_item(self, row, column, decode_res="unknown error"):
        if column == 3:
            if len(self.pass_input.text().strip()) == 0:
                self.secret_key_filter()
                return
            self.table.blockSignals(True)
            sql = "SELECT password " \
                  "FROM passwords " \
                  "WHERE id=?"
            query = self.cursor.execute(sql, (self.table.currentItem().statusTip(),))
            fetch = query.fetchone()[0]
            if fetch:
                result = run_decode(self.pass_input.text(), fetch)
                try:
                    decode_res = result.decode("utf-8")
                except UnicodeDecodeError:
                    decode_res = "error key"
                finally:
                    self.table.item(row, 3).setText(decode_res)
            else:
                print("No Password in DB!")
            self.table.blockSignals(False)

    def go_search(self):
        """ Search for relevant key in db """

        results = self.search_service.search(phrase=self.search_field.text())
        if results is not None:
            self.build_table_rows(results)


if __name__ == "__main__":
    __author__ = 'MindLoad'
    __version__ = "2.0.0"
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/icon"))
    main = Root()
    main.setWindowTitle("Monkey manager")
    main.setMinimumSize(1200, 700)
    main.setObjectName("Root")
    main.show()
    sys.exit(app.exec_())
