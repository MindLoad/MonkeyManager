# -*- coding: utf-8 -*-
# Created: 27.08.2019
# Changed: 28.08.2019

"""
Main window UI class
"""


from PyQt5.QtWidgets import (QWidget, QLineEdit, QToolButton, QHBoxLayout, QVBoxLayout, QLabel, QTableWidget,
                             QTableWidgetItem, QAbstractItemView, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap

from widgets import MenuButton
from styles import qwidget_css

__all__ = [
    'UiRootWindow',
]


class UiRootWindow:
    """ Root window ui class """

    def setup_ui(self, RootWindow):
        """ setup ui """

        RootWindow.setStyleSheet(qwidget_css.root_style)
        # Effects
        effect = QGraphicsDropShadowEffect(RootWindow)
        effect.setXOffset(0)
        effect.setYOffset(0)
        effect.setBlurRadius(10)
        effect.setColor(QColor("#b4b4b4"))
        # Top Elements
        # bar_top: QWidget which include first_layout as basic layout. First element of main_layout
        bar_top = QWidget()
        bar_top.setObjectName("bar_top")
        bar_top.setFixedHeight(50)
        logo = QLabel()
        logo.setObjectName("logo")
        logo.setFixedSize(200, 50)
        logo.setPixmap(QPixmap(":/logo"))
        self.add_new = QToolButton()
        self.add_new.setObjectName("add_new")
        self.add_new.setText("+ add")
        self.add_new.setFixedHeight(50)
        self.add_new.setCursor(Qt.PointingHandCursor)
        # add_new.clicked.connect(lambda: self.add_form(None))
        self.pass_input = QLineEdit()
        self.pass_input.setObjectName("pass_input")
        self.pass_input.setFixedHeight(50)
        self.pass_input.setPlaceholderText("secret key")
        self.pass_input.setEchoMode(QLineEdit.Password)
        # Second Elements menu
        # bar_menu: QWidget which include second_layout_menu as basic layout. First element of second_layout
        bar_menu = QWidget()
        bar_menu.setObjectName("bar_menu")
        bar_menu.setFixedWidth(200)
        self.b1 = MenuButton("Web Sites", ":/web", 30, 16)
        self.b2 = MenuButton("Credit Cards", ":/credit", 26, 16)
        self.b3 = MenuButton("Secrets", ":/secret", 26, 16)
        self.b4 = MenuButton("E-commerce", ":/ecommerce", 27, 16)
        self.b5 = MenuButton("Web Accounts", ":/webaccount", 30, 16)
        self.b6 = MenuButton("Emails", ":/email", 27, 16)
        self.b7 = MenuButton("Forums", ":/forum", 30, 16)
        self.b8 = MenuButton("Software", ":/software", 30, 16)
        # Keys Elements
        # bar_key: QWidget which include second_layout_keys as basic layout. Second element of second_layout
        bar_key = QWidget()
        bar_key.setObjectName("bar_key")
        self.search_field = QLineEdit()
        self.search_field.setMinimumHeight(46)
        self.search_field.setMaxLength(50)
        self.search_field.setPlaceholderText("Search: [title, name, email, url]")
        # self.search_field.returnPressed.connect(self.go_search)
        self.search_field.setStyleSheet(qwidget_css.search_field_style)
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
        # self.table.cellDoubleClicked.connect(self.click_item)
        self.table.installEventFilter(self)
        self.table.setGraphicsEffect(effect)
        # Layers
        # main_layout: includes bar_top, second_layout. Main app layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # first_layout: includes monkey logo, add button, secret input. Main layout for bar_top widget
        first_layout = QHBoxLayout()
        first_layout.setContentsMargins(0, 0, 0, 0)
        # second_layout: includes widgets with menus and keys. Second element of main_layout
        second_layout = QHBoxLayout()
        second_layout.setContentsMargins(0, 0, 0, 0)
        # second_layout_meny: Includes menu buttons. Main layout for bar_menu
        second_layout_menu = QVBoxLayout()
        second_layout_menu.setContentsMargins(0, 0, 0, 0)
        second_layout_menu.setSpacing(0)
        # second_layout_keys: includes search field, second_layout_keys_child, table widget. Main layout for second_layout_keys
        self.second_layout_keys = QVBoxLayout()
        self.second_layout_keys.setSpacing(0)
        self.second_layout_keys.setContentsMargins(40, 0, 40, 0)
        self.second_layout_keys.setAlignment(Qt.AlignTop)
        # second_layout_keys_childs. Includes sub keys and search result string. Placed under search field
        self.second_layout_keys_childs = QHBoxLayout()
        self.second_layout_keys_childs.setSpacing(0)
        self.second_layout_keys_childs.setContentsMargins(0, 0, 0, 4)
        self.second_layout_keys_childs.setAlignment(Qt.AlignLeft)
        # insert into Layouts
        # insert into top layout
        first_layout.addWidget(logo)
        first_layout.addStretch(1)
        first_layout.addWidget(self.add_new)
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
        second_layout_menu.addWidget(self.b8)
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
        RootWindow.setLayout(main_layout)
        self.pass_input.setFocus(True)
