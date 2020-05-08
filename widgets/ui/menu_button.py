# -*- coding: utf-8 -*-
# Created: 27.08.2019
# Changed: 28.08.2019

"""
Menu button UI class
"""

__all__ = [
    'UiMenuButton',
]

from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtCore import Qt, QRect

from services import FontService, AnimationService
from styles import qlabel_css


class UiMenuButton:
    """ Menu button ui class """

    def __init__(self):
        self.hide_animation = self.show_animation = self.check_mark = self.font = self.count_label = None
        self.enter = False

    def setup_ui(
            self,
            MenuButtonWidget: QPushButton
    ) -> None:
        """ setup left menu button ui """

        MenuButtonWidget.setFixedSize(200, 45)
        MenuButtonWidget.setCursor(Qt.PointingHandCursor)
        MenuButtonWidget.setObjectName("menu_button")
        self.font = FontService("Verdana", 11, True).get_font()
        self.count_label = QLabel(self)
        self.count_label.setText('test')
        self.count_label.setFont(self.font)
        self.count_label.setStyleSheet(qlabel_css.menu_button_count_style)
        self.count_label.setGeometry(200, 0, 30, 45)
        MenuButtonWidget.installEventFilter(self)
        # Animation
        self.show_animation = AnimationService(
            self.count_label,
            b"geometry",
            150,
            QRect(
                self.count_label.x(),
                self.count_label.y(),
                self.count_label.width(),
                self.count_label.height()
                ),
            QRect(
                self.count_label.x() - 30,
                self.count_label.y(),
                self.count_label.width(),
                self.count_label.height()
                )
        ).init_animation()
