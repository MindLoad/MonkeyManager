""" Monkey manager - simple password keeper application """

import sys

import chime
from PyQt5.QtCore import QEvent, QSize, Qt, QTimer
from PyQt5.QtGui import QIcon, QResizeEvent
from PyQt5.QtWidgets import QApplication, QLabel, QRadioButton, QTableWidgetItem, QToolButton, QWidget

import ui
import source
from models.query_builder import QueryBuilder
from services import ExportService, SearchService
from tools import run_decode
from widgets import AddNewKey


class Root(QWidget, ui.UiRootWindow):
    """ Root application widget """

    def __init__(self):
        super().__init__(flags=Qt.WindowTitleHint)
        # Setup main window UI
        self.setup_ui(self)
        # Static variables
        self.current_parent = self._add = self.search_result = self.refresh_element = None
        # Widget element logic
        self.add_new.clicked.connect(lambda: self.add_form(None))
        self.search_field.returnPressed.connect(self._search)

        self.table.cellDoubleClicked.connect(self.click_item)

        self.export_dump.clicked.connect(lambda: ExportService.make_export(key=self.pass_input.text()))

        # QTimer
        self.bg_timeout = QTimer(self)
        self.bg_timeout.setInterval(3000)
        self.bg_timeout.timeout.connect(self.back_to_white)
        # Build extra elements
        self.build_extra_elements()
        chime.notify_exceptions()

    @property
    def currently_checked_menu_button(self):
        """ return menu button that was clicked last """
        for button in (self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8):
            if button.check_mark is not None:
                return button
        return None

    def build_extra_elements(self) -> None:
        """ Build extra UI elements """

        self.search_result = QLabel()
        self.search_result.setObjectName("search_result")
        self.second_layout_keys_childs.addWidget(self.search_result)

    def eventFilter(self, *args) -> QWidget.eventFilter:
        event = args[1]
        if event.type() == QEvent.KeyPress:
            match event.key():
                case Qt.Key_Delete if self.table.currentRow() >= 0:
                    row = self.table.currentRow()
                    row_id = self.table.item(row, 3).statusTip()
                    QueryBuilder.delete_obj(row_id=row_id)
                    self.table.removeRow(row)
                case Qt.Key_F4 if self.table.currentRow() >= 0:
                    if not self.pass_input.text().strip():
                        self.secret_key_filter()
                        chime.error()
                        return QWidget.eventFilter(self, *args)
                    row = self.table.currentRow()
                    data = (
                        self.table.item(row, 0).text(), self.table.item(row, 1).text(), self.table.item(row, 2).text(),
                        self.table.item(row, 3).statusTip(), self.table.item(row, 4).text(),
                        self.table.item(row, 5).text(), self.table.item(row, 6).text(), self.table.item(row, 7).text())
                    self.add_form(data)
                case Qt.Key_Tab if self.pass_input.hasFocus():
                    self.search_field.setFocus(True)
                    return True
                case Qt.Key_Tab if self.search_field.hasFocus():
                    self.pass_input.setFocus(True)
                    return True
        return QWidget.eventFilter(self, *args)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        if self._add:
            self._add.setFixedSize(self.size())

    def secret_key_filter(self) -> None:
        self.pass_input.setStyleSheet("background:#f3a7a7;")
        self.pass_input.setFocus(True)
        self.bg_timeout.start()

    def back_to_white(self) -> None:
        self.pass_input.setStyleSheet("background:#fff;")
        self.bg_timeout.stop()

    def add_form(self, arg) -> None:
        if not self.pass_input.text().strip():
            self.secret_key_filter()
            chime.error()
            return
        self._add = AddNewKey(self.pass_input.text(), arg, parent=self)
        self._add.show()

    def clear_child_table(self) -> None:
        for pos in reversed(range(self.second_layout_keys_childs.count())):
            curr_item = self.second_layout_keys_childs.takeAt(pos).widget()
            if curr_item is not None:
                curr_item.deleteLater()
        self.table.setRowCount(0)

    def build_table_rows(self, data: list | tuple) -> None:
        rows = len(data)
        if not rows:
            self.clear_child_table()
            self.search_result = QLabel()
            self.search_result.setObjectName("search_result")
            self.search_result.setText("No results ...")
            self.second_layout_keys_childs.addWidget(self.search_result)
            return
        self.table.setRowCount(rows)
        for pos, item in enumerate(data):
            cell_title = QTableWidgetItem(item.title)
            cell_title.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            cell_title.setToolTip(f"{item.parent} ➔ {item.child} ➔ {item.title}")
            cell_login = QTableWidgetItem(item.login)
            cell_login.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            cell_login.setToolTip(item.login)
            cell_email = QTableWidgetItem(item.email)
            cell_email.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            cell_email.setToolTip(item.email)
            cell_password = QTableWidgetItem("********")
            cell_password.setStatusTip(f"{item.id}")
            cell_password.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            cell_url = QTableWidgetItem(item.url)
            cell_url.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            cell_url.setToolTip(item.url)
            cell_phone = QTableWidgetItem(item.phone)
            cell_phone.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            cell_created = QTableWidgetItem(item.created.__str__())
            cell_created.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            cell_modified = QTableWidgetItem(item.modified.__str__())
            cell_modified.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            for index, cell in enumerate(
                (cell_title, cell_login, cell_email, cell_password, cell_url, cell_phone, cell_created, cell_modified)
            ):
                self.table.setItem(pos, index, cell)
        for row in range(rows):
            self.table.setRowHeight(row, 45)

    def get_children(self, sender: str) -> None:
        """ Generate sub dirs relevant to main menu element """

        self.clear_child_table()
        self.current_parent = sender
        # Create Child
        self.refresh_element = QToolButton()
        self.refresh_element.setObjectName('refresh')
        self.refresh_element.setIcon(QIcon(':/refresh'))
        self.refresh_element.setIconSize(QSize(22, 22))
        self.refresh_element.setCursor(Qt.PointingHandCursor)
        self.refresh_element.clicked.connect(lambda: self.get_keys(True, refresh=self.refresh_element.statusTip()))
        self.refresh_element.setEnabled(False)
        self.second_layout_keys_childs.addWidget(self.refresh_element)
        self.second_layout_keys_childs.addSpacing(5)
        query = QueryBuilder.retrieve_parents(root_parent=sender)
        for item in query:
            child_element = QRadioButton()
            child_element.setObjectName("child-element")
            child_element.setText(item.child)
            child_element.setMinimumHeight(22)
            child_element.setCursor(Qt.PointingHandCursor)
            child_element.clicked.connect(self.get_keys)
            self.second_layout_keys_childs.addWidget(child_element)
            self.second_layout_keys_childs.addSpacing(5)

    def get_keys(self, status, refresh=None) -> None:
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        sender = refresh if refresh else self.sender().text()
        query = QueryBuilder.retrieve_children(parent=sender)
        self.build_table_rows(query)
        self.table.setSortingEnabled(True)
        self.refresh_element.setEnabled(True)
        self.refresh_element.setStatusTip(sender)

    def click_item(self, row, column, decode_res="unknown error") -> None:
        if column == 3:
            if len(self.pass_input.text().strip()) == 0:
                self.secret_key_filter()
                chime.error()
                return
            self.table.blockSignals(True)
            query = QueryBuilder.retrieve_item_password(item_id=self.table.currentItem().statusTip())
            try:
                decode_res = run_decode(self.pass_input.text(), query.password).decode("utf-8")
            except UnicodeDecodeError:
                decode_res = "error key"
                chime.error()
            finally:
                self.table.item(row, 3).setText(decode_res)
            self.table.blockSignals(False)

    def _search(self) -> None:
        """ Search for relevant key in db """
        phrase = self.search_field.text()
        if not phrase.strip():
            chime.warning()
            return
        results = SearchService.completer_search(phrase=phrase)
        chime.success()
        self.build_table_rows(results)


if __name__ == "__main__":
    __author__ = 'MindLoad'
    __version__ = "2.1.1"
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/icon"))
    main = Root()
    main.setWindowTitle("Monkey manager")
    main.setMinimumSize(1200, 750)
    main.setObjectName("Root")
    main.show()
    sys.exit(app.exec_())
