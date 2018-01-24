# -*- coding: utf-8 -*-
# Created: 13.09.2017
# Changed: 24.01.2018

import sys
import os
import sqlite3
import encrypt_m
import source

from datetime import datetime

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QToolButton, QHBoxLayout, QVBoxLayout, QLabel,\
    QTableWidget, QTableWidgetItem, QAbstractItemView, QRadioButton, QPushButton, QFrame, QComboBox, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QRect, QTimer, QEvent
from PyQt5.QtGui import QIcon, QPainter, QColor, QPixmap, QFont, QResizeEvent


class Root(QWidget):
    def __init__(self, parent=None):
        super(Root, self).__init__(parent)
        self.c = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "/crypt.db")
        self.conn = self.c.cursor()
        self.setStyleSheet("""
            QWidget#bar_top {background:#fff;border-bottom:1px solid #c6c6c6;}
            QLabel#logo {background:#4797ce;border-bottom:1px solid #00365c;}
            QWidget#bar_menu {background:#00365c;}
            QWidget#bar_key {background:#eaeaea;}
            QLineEdit#pass_input {border:none;font:bold 12px Arial;color:#636363;border-left:1px solid #c6c6c6;border-bottom:1px solid #c6c6c6;padding:0 30px;}
            QToolButton#add_new {font:bold 12px Arial;color:#6089a6;border:none;padding:0 30px;border-left:1px solid #c6c6c6;}
            QPushButton#menu_button {background:#00365c;color:#9bb0bf;border:none;font:bold 13px Arial;}
            QRadioButton#child-element {font:bold 10px Arial;color:#757575;padding:2px 8px 2px 4px;}
            QRadioButton#child-element::checked {background:#4797ce;border-radius:10px;color:#fff;}
            QRadioButton#child-element::indicator {width:0;}
            QToolButton#refresh {border:none;}
            QTableWidget {border: 1px solid #c6c6c6; font:bold 11px Arial; color: #8e8e8e;}
            QHeaderView::section {border-top: 0px solid #8a8a8a; border-left: 0px solid #8a8a8a;
                border-right: 0px solid #d9d9d9; border-bottom: 1px solid #ccc; font: bold 12px Arial; background:#fff;
                height:45px; color:#325d7c;padding-left:20px;}
            QHeaderView::up-arrow {image: url(:/header-up);width:18px;height:18px;}
            QHeaderView::down-arrow {image: url(:/header-down);width:18px;height:18px;}
            QTableView::item {border-bottom: 1px solid #ccc;padding-left:20px;}
            QTableView::item:selected {background:#f2faff; color:#578dc9;}
            QScrollBar:horizontal {border: none; background: #a5c8ed; height: 3px;}
            QScrollBar::handle:horizontal {max-width: 0; background: #4797ce;}
            QScrollBar:vertical {border: none; background: #a5c8ed; width: 4px;}
            QScrollBar::handle:vertical {max-height: 0; background: #4797ce;}
            QLabel#search_result {font:12px Arial;color:#646464;}
        """)
        # Static variables
        self.current_parent = self._add = None
        # Effects
        effect = QGraphicsDropShadowEffect(self)
        effect.setXOffset(0)
        effect.setYOffset(0)
        effect.setBlurRadius(10)
        effect.setColor(QColor("#b4b4b4"))
        # Top Elements
        bar_top = QWidget()
        bar_top.setObjectName("bar_top")
        bar_top.setFixedHeight(50)
        logo = QLabel()
        logo.setObjectName("logo")
        logo.setFixedSize(200, 50)
        logo.setPixmap(QPixmap(":/logo"))
        add_new = QToolButton()
        add_new.setObjectName("add_new")
        add_new.setText("+ add")
        add_new.setFixedHeight(50)
        add_new.setCursor(Qt.PointingHandCursor)
        add_new.clicked.connect(lambda: self.add_form(None))
        self.pass_input = QLineEdit()
        self.pass_input.setObjectName("pass_input")
        self.pass_input.setFixedHeight(50)
        self.pass_input.setPlaceholderText("secret key")
        self.pass_input.setEchoMode(QLineEdit.Password)
        # Second Elements menu
        bar_menu = QWidget()
        bar_menu.setObjectName("bar_menu")
        bar_menu.setFixedWidth(200)
        self.b1 = MenuButton("Web Sites")
        self.b2 = MenuButton("Credit Cards")
        self.b3 = MenuButton("Secrets")
        self.b4 = MenuButton("E-commerce")
        self.b5 = MenuButton("Web Accounts")
        self.b6 = MenuButton("Emails")
        self.b7 = MenuButton("Forums")
        # Keys Elements
        bar_key = QWidget()
        bar_key.setObjectName("bar_key")
        self.search_field = QLineEdit()
        self.search_field.setMinimumHeight(46)
        self.search_field.setMaxLength(50)
        self.search_field.setPlaceholderText("search field")
        self.search_field.returnPressed.connect(self.go_search)
        self.search_field.setStyleSheet("border-radius:23px; background:#fff; border:1px solid #c6c6c6; padding:0 30px;"
                                   "font:13px Arial;"
                                   "color:#636363;"
                                   "background-image: url(:/search);"
                                   "background-repeat: no-repeat;"
                                   "background-position: left;")
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setColumnWidth(0, 160)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 160)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 180)
        self.table.setColumnWidth(5, 150)
        self.table.setColumnWidth(6, 150)
        self.table.setColumnWidth(7, 150)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("TITLE"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("NAME"))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("EMAIL"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("PASSWORD"))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem("URL"))
        self.table.setHorizontalHeaderItem(5, QTableWidgetItem("PHONE"))
        self.table.setHorizontalHeaderItem(6, QTableWidgetItem("CREATED"))
        self.table.setHorizontalHeaderItem(7, QTableWidgetItem("MODIFIED"))
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.click_item)
        self.table.installEventFilter(self)
        self.table.setGraphicsEffect(effect)
        # Layers
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        first_layout = QHBoxLayout()
        first_layout.setContentsMargins(0, 0, 0, 0)
        second_layout = QHBoxLayout()
        second_layout.setContentsMargins(0, 0, 0, 0)
        second_layout_menu = QVBoxLayout()
        second_layout_menu.setContentsMargins(0, 0, 0, 0)
        second_layout_menu.setSpacing(0)
        self.second_layout_keys = QVBoxLayout()
        self.second_layout_keys.setSpacing(0)
        self.second_layout_keys.setContentsMargins(40, 0, 40, 0)
        self.second_layout_keys.setAlignment(Qt.AlignTop)
        self.second_layout_keys_childs = QHBoxLayout()
        self.second_layout_keys_childs.setSpacing(0)
        self.second_layout_keys_childs.setContentsMargins(0, 0, 0, 4)
        self.second_layout_keys_childs.setAlignment(Qt.AlignLeft)
        # insert into Layouts
        # insert into top layout
        first_layout.addWidget(logo)
        first_layout.addStretch(1)
        first_layout.addWidget(add_new)
        first_layout.addWidget(self.pass_input)
        bar_top.setLayout(first_layout)
        # insert into second menu layout
        second_layout_menu.addSpacing(20)
        second_layout_menu.addWidget(self.b1)
        second_layout_menu.addWidget(self.b5)
        second_layout_menu.addWidget(self.b6)
        second_layout_menu.addWidget(self.b2)
        second_layout_menu.addWidget(self.b4)
        second_layout_menu.addWidget(self.b3)
        second_layout_menu.addWidget(self.b7)
        second_layout_menu.addStretch(1)
        bar_menu.setLayout(second_layout_menu)
        self.second_layout_keys.insertSpacing(0, 20)
        self.second_layout_keys.addWidget(self.search_field)
        self.second_layout_keys.insertSpacing(2, 20)
        self.second_layout_keys.addLayout(self.second_layout_keys_childs)
        self.second_layout_keys.insertSpacing(4, 7)
        self.second_layout_keys.addWidget(self.table)
        self.second_layout_keys.insertSpacing(6, 5)
        bar_key.setLayout(self.second_layout_keys)
        second_layout.addWidget(bar_menu)
        second_layout.addWidget(bar_key)
        # set Main Layout
        main_layout.addWidget(bar_top)
        main_layout.addLayout(second_layout)
        self.setLayout(main_layout)
        self.pass_input.setFocus(True)
        # QTimer
        self.bg_timeout = QTimer(self)
        self.bg_timeout.setInterval(3000)
        self.bg_timeout.timeout.connect(self.back_to_white)

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Delete and self.table.currentRow() >= 0:
                row = self.table.currentRow()
                row_id = self.table.item(row, 3).statusTip()
                self.conn.execute("DELETE FROM passwords WHERE id=?", (row_id,))
                self.c.commit()
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
        self._add = AddNewKey(self.c, self.conn, self.pass_input.text(), arg)
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
        query = self.conn.execute("SELECT DISTINCT child FROM passwords WHERE parent=? ORDER BY child ASC", (sender,))
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
        query = self.conn.execute(
            "SELECT id, title, login, email, url, phone, created, modified FROM passwords WHERE child=? ORDER BY title ASC",
            (sender,))
        self.build_table_rows(query)
        self.table.setSortingEnabled(True)
        self.refresh_element.setEnabled(True)
        self.refresh_element.setStatusTip(sender)

    def click_item(self, row, column):
        if column == 3:
            if len(self.pass_input.text().strip()) == 0:
                self.secret_key_filter()
                return
            self.table.blockSignals(True)
            query = self.conn.execute("SELECT password FROM passwords WHERE id=?", (self.table.currentItem().statusTip(),))
            fetch = query.fetchone()[0]
            if fetch:
                result = encrypt_m.run_decode(self.pass_input.text(), fetch)
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
        search_line = self.search_field.text().strip()
        if search_line:
            result_t = []
            query = self.conn.execute("SELECT id, title, login, email, url FROM passwords ORDER BY id ASC")
            for items in query.fetchall():
                for item in items[1:]:
                    if search_line in item:
                        result_t.append(items[0])
                        break
            if result_t:
                self.current_parent = None
                self.clear_child_table()
                if len(result_t) == 1:
                    result_t = f"({result_t[0]})"
                else:
                    result_t = f"{tuple(result_t)}"
                query = self.conn.execute(
                    f"SELECT id, title, login, email, url, phone, created, modified FROM passwords WHERE id IN {result_t} ORDER BY id ASC")
                self.build_table_rows(query)
            else:
                self.clear_child_table()
                self.s_result = QLabel()
                self.s_result.setObjectName("search_result")
                self.s_result.setText("No results found!")
                self.second_layout_keys_childs.addWidget(self.s_result)
        else:
            self.clear_child_table()
            self.s_result = QLabel()
            self.s_result.setObjectName("search_result")
            self.s_result.setText("Empty search line")
            self.second_layout_keys_childs.addWidget(self.s_result)


class MenuButton(QPushButton):
    def __init__(self, title, parent=None):
        super(MenuButton, self).__init__(parent)
        self.setFixedSize(200, 45)
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("menu_button")
        self.title = title
        self.check_mark = None
        self.font = QFont()
        self.font.setFamily("Arial")
        self.font.setPixelSize(11)
        self.font.setBold(True)
        self.enter = False
        self.installEventFilter(self)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.check_mark:
            painter.setBrush(QColor("#0d4871"))
        else:
            painter.setBrush(QColor("#00365c"))
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, self.width(), 45)
        if self.title == "Web Sites":
            painter.drawPixmap(30, 16, QPixmap(":/web"))
        elif self.title == "Credit Cards":
            painter.drawPixmap(26, 16, QPixmap(":/credit"))
        elif self.title == "Secrets":
            painter.drawPixmap(26, 16, QPixmap(":/secret"))
        elif self.title == "E-commerce":
            painter.drawPixmap(27, 16, QPixmap(":/ecommerce"))
        elif self.title == "Web Accounts":
            painter.drawPixmap(30, 16, QPixmap(":/webaccount"))
        elif self.title == "Emails":
            painter.drawPixmap(27, 16, QPixmap(":/email"))
        else:
            painter.drawPixmap(30, 16, QPixmap(":/forum"))
        painter.setPen(QColor("#9bb0bf")) if not self.enter and not self.check_mark else painter.setPen(QColor("#cadfee"))
        painter.drawText(70, 15, 140, 14, Qt.AlignLeft, self.title)
        if self.check_mark:
            painter.setBrush(QColor("#4797ce"))
            painter.drawRect(0, 0, 3, 45)
            painter.setFont(self.font)
            painter.setPen(QColor("#7e8c96"))
            painter.drawText(175, 15, 10, 14, Qt.AlignCenter, self.check_mark)

    def mousePressEvent(self, event):
        for element in (main.b1, main.b2, main.b3, main.b4, main.b5, main.b6, main.b7):
            if element.check_mark:
                element.check_mark = None
                element.repaint()
        query = main.conn.execute("SELECT COUNT(id) FROM passwords WHERE parent=?", (self.title,))
        self.check_mark = f"{query.fetchone()[0]}"
        main.get_childs(self.title)

    def eventFilter(self, source, event):
        if event.type() == 10:
            self.enter = True
            self.update()
        elif event.type() == 11:
            self.enter = False
            self.update()
        return QPushButton.eventFilter(self, source, event)


class AddNewKey(QFrame):
    def __init__(self, c, conn, secret_key, data):
        super(AddNewKey, self).__init__(main)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.c = c
        self.conn = conn
        self.secret_key = secret_key
        self.data = data
        self.w = main.width()
        self.h = main.height()
        self.setFixedSize(self.w, self.h)
        self.setObjectName("AddFrame")
        self.setStyleSheet("""
            QFrame#AddFrame {background:#eaeaea;}
            QPushButton#close {border:none;}
            QLineEdit#field {border-radius:20px;background:#fff;border:1px solid #b7b7b7;padding:0 30px;font:13px Arial;color:#808080;}
            QPushButton#save {font: 14px Arial;color:#fff;background:#4797ce;border:none;}
            QComboBox {font: 15px Arial;color:#808080;padding-left:10px;border: 1px solid #b7b7b7;background:#fff;height:28px;}
            QComboBox::drop-down {subcontrol-origin:padding;subcontrol-position: top right;width:20px;border-top-right-radius:3px;border-bottom-right-radius:3px;}
            QComboBox::down-arrow {image: url(:/down);padding-right:8px;}
            QComboBox QAbstractItemView {background:#fff;padding:7px 5px 7px 5px;font:15px Arial;color:#808080;}
            QComboBox QAbstractItemView::item {padding:4px;}
            QRadioButton#child-element {font:bold 10px Arial;color:#646464;padding:2px 6px 3px 0;}
            QRadioButton#child-element::checked {background:#4797ce;border-radius:10px;color:#fff;}
            QRadioButton#child-element::indicator {width:0;}
        """)
        # Elements
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        close_button = QPushButton()
        close_button.setObjectName("close")
        close_button.setFixedSize(QSize(13, 13))
        close_button.setCursor(Qt.PointingHandCursor)
        close_button.setIcon(QIcon(":/quit"))
        close_button.clicked.connect(self._close)
        if not self.data:
            self.combo = QComboBox()
            self.combo.setObjectName("combo")
            self.combo.addItems(("Web Sites", "Web Accounts", "Emails", "Credit Cards", "E-commerce", "Secrets", "Forums"))
            self.combo.currentTextChanged.connect(self.generate_child_list)
            self.child = QLineEdit()
            self.child.setPlaceholderText("Branch *")
        self.title = QLineEdit()
        self.title.setPlaceholderText("Title *")
        self.name = QLineEdit()
        self.name.setPlaceholderText("Login")
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password *")
        self.password.setEchoMode(QLineEdit.Password)
        self.url = QLineEdit()
        self.url.setPlaceholderText("Url")
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Phone")
        self.created = QLineEdit()
        self.created.setPlaceholderText("Create Date *")
        if not self.data:
            self.created.setText(current_time)
        else:
            self.created.setText(self.data[6])
        self.created.setEnabled(False)
        self.modified = QLineEdit()
        self.modified.setPlaceholderText("Modified Date *")
        self.modified.setText(current_time)
        self.modified.setEnabled(False)
        if not self.data:
            for elements in (self.combo, self.child):
                elements.setFixedSize(400, 40)
                elements.setObjectName("field")
        for elements in (self.title, self.name, self.email, self.password, self.url, self.phone,
                         self.created, self.modified):
            elements.setFixedSize(400, 40)
            elements.setObjectName("field")
        save_button = QPushButton()
        save_button.setObjectName("save")
        save_button.setText("Сохранить")
        save_button.setFixedSize(300, 40)
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.clicked.connect(self._save)
        # Animation
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setStartValue(QRect(0, -self.h, self.w, self.h))
        self.animation.setEndValue(QRect(0, 0, self.w, self.h))
        self.animation.start()
        # Timer
        self.timer = QTimer(self)
        self.timer.setInterval(210)
        self.timer.timeout.connect(self._quit)
        # LAYOUTS
        if not self.data:
            self.cc = QHBoxLayout()
            self.cc.setContentsMargins(0, 6, 0, 4)
            self.cc.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(close_button, alignment=Qt.AlignRight)
        layout.addSpacing(10)
        if not self.data:
            layout.addWidget(self.combo, alignment=Qt.AlignCenter)
            layout.addLayout(self.cc)
            layout.addWidget(self.child, alignment=Qt.AlignCenter)
            layout.addSpacing(10)
        layout.addWidget(self.title, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.name, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.email, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.password, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.url, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.phone, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.created, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.modified, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(save_button, alignment=Qt.AlignCenter)
        layout.addStretch(1)
        self.setLayout(layout)
        self.title.setFocus(True)
        if not self.data:
            self.generate_child_list()
        else:
            self.title.setText(self.data[0])
            self.name.setText(self.data[1])
            self.email.setText(self.data[2])
            self.url.setText(self.data[4])
            self.phone.setText(self.data[5])

    def generate_child_list(self):
        self.sender().blockSignals(True)
        for pos in reversed(range(self.cc.count())):
            curr_item = self.cc.takeAt(pos).widget()
            if curr_item is not None:
                curr_item.deleteLater()
        query = self.conn.execute("SELECT DISTINCT child FROM passwords WHERE parent=? ORDER BY child ASC", (self.combo.currentText(),))
        for item in query.fetchall():
            r_elem = QRadioButton()
            r_elem.setObjectName("child-element")
            r_elem.setText(item[0])
            r_elem.setFixedHeight(20)
            r_elem.setCursor(Qt.PointingHandCursor)
            r_elem.clicked.connect(self.child_text_replace)
            self.cc.addWidget(r_elem)
        self.sender().blockSignals(False)

    def child_text_replace(self):
        self.child.setText(self.sender().text())

    def _save(self):
        crypt_password = encrypt_m.run_encode(self.secret_key, self.password.text().encode("utf-8"))
        if not self.data:
            self.conn.execute("INSERT INTO passwords (parent, child, title, login, email, password, url, phone, created, modified) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                              (self.combo.currentText(), self.child.text(), self.title.text(), self.name.text(), self.email.text(),
                               crypt_password, self.url.text(), self.phone.text(), self.created.text(), self.modified.text()))
        else:
            self.conn.execute("UPDATE passwords SET title=?, login=?, email=?, password=?, url=?, phone=?, modified=? WHERE id=?",
                              (self.title.text(), self.name.text(), self.email.text(), crypt_password, self.url.text(),
                               self.phone.text(), self.modified.text(), self.data[3]))
        self.c.commit()
        self._close()

    def _close(self):
        self.animation.setStartValue(QRect(0, 0, self.w, self.h))
        self.animation.setEndValue(QRect(0, -self.h, self.w, self.h))
        self.animation.start()
        self.timer.start()

    def _quit(self):
        self.close()
        self.deleteLater()
        main._add = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self._close()


if __name__ == "__main__":
    __author__ = 'MindLoad'
    __version__ = "1.0.1"
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/icon"))
    main = Root()
    main.setWindowTitle("Monkey manager")
    main.setMinimumSize(1200, 700)
    main.setObjectName("Root")
    main.show()
    sys.exit(app.exec_())
