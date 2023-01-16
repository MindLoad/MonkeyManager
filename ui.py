""" Main window UI class """

# Created: 27.08.2019
# Changed: 16.01.2023


from PyQt5.QtWidgets import (QWidget, QLineEdit, QToolButton, QHBoxLayout, QVBoxLayout, QLabel, QTableWidget,
                             QTableWidgetItem, QAbstractItemView, QGraphicsDropShadowEffect, QCompleter)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QPixmap, QIcon
from widgets import MenuButton
from styles import qwidget_css
from models import QueryBuilder

__all__ = ['UiRootWindow']


class UiRootWindow:
    """ Root window UI class """

    def __init__(self):
        # ELEMENTS
        # ------------------------------ TOP ELEMENTS -------------------------------------
        self.logo = QLabel()
        self.add_new = QToolButton()
        self.pass_input = QLineEdit()
        # ------------------------------ MENU PANEL ELEMENTS ------------------------------
        self.b1 = MenuButton("Web Sites", ":/web", 30, 16)
        self.b2 = MenuButton("Credit Cards", ":/credit", 26, 16)
        self.b3 = MenuButton("Secrets", ":/secret", 26, 16)
        self.b4 = MenuButton("E-commerce", ":/ecommerce", 27, 16)
        self.b5 = MenuButton("Web Accounts", ":/webaccount", 30, 16)
        self.b6 = MenuButton("Emails", ":/email", 27, 16)
        self.b7 = MenuButton("Forums", ":/forum", 30, 16)
        self.b8 = MenuButton("Software", ":/software", 30, 16)
        self.export_dump = QToolButton()
        self.import_dump = QToolButton()
        # ------------------------------ TABLE PANEL ELEMENTS -----------------------------
        self.search_field = QLineEdit()
        self.completer = QCompleter(QueryBuilder.completer_values())
        # WIDGETS
        # ------------------------------ TOP WIDGETS --------------------------------------
        self.bar_top = QWidget()
        self.bar_menu = QWidget()
        self.bar_key = QWidget()
        # ------------------------------ TABLE PANEL WIDGETS ------------------------------
        self.table = QTableWidget()
        # Layouts
        self.main_layout = QVBoxLayout()
        self.first_layout = QHBoxLayout()
        self.second_layout = QHBoxLayout()
        self.second_layout_menu_bottom_extra = QHBoxLayout()
        self.second_layout_menu = QVBoxLayout()
        self.second_layout_keys = QVBoxLayout()
        self.second_layout_keys_childs = QHBoxLayout()

    def setup_ui(self, root_window) -> None:
        """ setup ui """

        root_window.setStyleSheet(qwidget_css.root_style)
        self.init_elements()
        self.init_widgets()
        self.init_layouts(root_window)
        self.table.setGraphicsEffect(self.init_effects(root_window))

    @staticmethod
    def init_effects(root_window: QWidget) -> QGraphicsDropShadowEffect:
        """
        Initialize base effects
        :return: QGraphicsDropShadowEffect
        """

        # ------------------------------ EFFECTS ------------------------------------------
        effect = QGraphicsDropShadowEffect(root_window)
        effect.setXOffset(0)
        effect.setYOffset(0)
        effect.setBlurRadius(10)
        effect.setColor(QColor("#b4b4b4"))
        return effect

    def init_elements(self) -> None:
        """
        Initialize main elements
        :return: None
        """

        # ------------------------------ TOP ELEMENTS -------------------------------------
        # LOGO with monkey face
        self.logo.setObjectName("logo")
        self.logo.setFixedSize(200, 50)
        self.logo.setPixmap(QPixmap(":/logo"))
        # ADD NEW button
        self.add_new.setObjectName("add_new")
        self.add_new.setText("+ add")
        self.add_new.setFixedHeight(50)
        self.add_new.setCursor(Qt.PointingHandCursor)
        # PASSWORD input field
        self.pass_input.setObjectName("pass_input")
        self.pass_input.setFixedHeight(50)
        self.pass_input.setPlaceholderText("secret key")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.installEventFilter(self)
        # ------------------------------ MENU PANEL ELEMENTS ------------------------------
        self.export_dump.setMinimumSize(42, 14)
        self.export_dump.setIcon(QIcon("images/json.png"))
        self.export_dump.setIconSize(QSize(44, 14))
        self.export_dump.setCursor(Qt.PointingHandCursor)
        self.export_dump.setToolTip("Export CSV")
        self.export_dump.setStyleSheet(qwidget_css.menu_extra_buttons)
        # ------------------------------ TABLE PANEL ELEMENTS -----------------------------
        # SEARCH field
        self.search_field.setMinimumHeight(46)
        self.search_field.setMaxLength(50)
        self.search_field.setPlaceholderText("Search ~ Title, Name")
        self.search_field.installEventFilter(self)
        self.search_field.setStyleSheet(qwidget_css.search_field_style)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.search_field.setCompleter(self.completer)

    def init_widgets(self) -> None:
        """
        Initialize main widgets
        :return: None
        """

        # ------------------------------ TOP WIDGETS --------------------------------------
        self.bar_top.setObjectName("bar_top")
        self.bar_top.setFixedHeight(50)
        # ------------------------------ MENU WIDGETS -------------------------------------
        self.bar_menu.setObjectName("bar_menu")
        self.bar_menu.setFixedWidth(200)
        # ------------------------------ TABLE PANEL WIDGETS ------------------------------
        self.bar_key.setObjectName("bar_key")
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
        self.table.installEventFilter(self)

    def init_layouts(self, root_window) -> None:
        """
        Initialize main layouts
        :return: None
        """

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.second_layout_keys.setSpacing(0)
        self.second_layout_keys.setContentsMargins(40, 0, 40, 0)
        self.second_layout_keys.setAlignment(Qt.AlignTop)
        self.second_layout_keys_childs.setSpacing(0)
        self.second_layout_keys_childs.setContentsMargins(0, 0, 0, 4)
        self.second_layout_keys_childs.setAlignment(Qt.AlignLeft)

        self.first_layout.setContentsMargins(0, 0, 0, 0)
        self.first_layout.addWidget(self.logo, alignment=Qt.AlignLeft)
        self.first_layout.addStretch(1)
        self.first_layout.addWidget(self.add_new, alignment=Qt.AlignCenter)
        self.first_layout.addWidget(self.pass_input, alignment=Qt.AlignCenter)
        self.bar_top.setLayout(self.first_layout)

        self.second_layout_menu_bottom_extra.setContentsMargins(10, 0, 10, 10)
        self.second_layout_menu_bottom_extra.addWidget(self.export_dump, alignment=Qt.AlignLeft)

        self.second_layout_menu.setContentsMargins(0, 0, 0, 0)
        self.second_layout_menu.setSpacing(0)
        self.second_layout_menu.addSpacing(20)
        self.second_layout_menu.addWidget(self.b1, alignment=Qt.AlignCenter)
        self.second_layout_menu.addWidget(self.b5, alignment=Qt.AlignCenter)
        self.second_layout_menu.addWidget(self.b6, alignment=Qt.AlignCenter)
        self.second_layout_menu.addWidget(self.b2, alignment=Qt.AlignCenter)
        self.second_layout_menu.addWidget(self.b4, alignment=Qt.AlignCenter)
        self.second_layout_menu.addWidget(self.b3, alignment=Qt.AlignCenter)
        self.second_layout_menu.addWidget(self.b7, alignment=Qt.AlignCenter)
        self.second_layout_menu.addWidget(self.b8, alignment=Qt.AlignCenter)
        self.second_layout_menu.addStretch(1)
        self.second_layout_menu.addLayout(self.second_layout_menu_bottom_extra)
        self.bar_menu.setLayout(self.second_layout_menu)

        self.second_layout_keys.insertSpacing(0, 20)
        self.second_layout_keys.addWidget(self.search_field, alignment=Qt.AlignBaseline)
        self.second_layout_keys.insertSpacing(2, 20)
        self.second_layout_keys.addLayout(self.second_layout_keys_childs)
        self.second_layout_keys.insertSpacing(4, 7)
        self.second_layout_keys.addWidget(self.table)
        self.second_layout_keys.insertSpacing(6, 5)
        self.bar_key.setLayout(self.second_layout_keys)

        self.second_layout.setContentsMargins(0, 0, 0, 0)
        self.second_layout.addWidget(self.bar_menu, alignment=Qt.AlignLeft)
        self.second_layout.addWidget(self.bar_key)

        self.main_layout.addWidget(self.bar_top, alignment=Qt.AlignBaseline)
        self.main_layout.addLayout(self.second_layout)

        root_window.setLayout(self.main_layout)
        self.pass_input.setFocus(True)
