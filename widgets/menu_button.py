""" Left menu button widget """

# Created: 27.08.2019
# Changed: 15.01.2023

__all__ = ['MenuButton']

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QRect, QEvent
from PyQt5.QtGui import QPainter, QColor, QPixmap, QMouseEvent
from services import AnimationService
from .ui import UiMenuButton
from models import QueryBuilder


class MenuButton(QPushButton, UiMenuButton):
    """ Menu button class """

    def __init__(
            self,
            title: str,
            icon_alias: str,
            position_x: int,
            position_y: int,
            parent=None):
        super().__init__(parent)
        self.title = title
        self.icon_alias = icon_alias
        self.position_x = position_x
        self.position_y = position_y
        # Out-init elements
        self.check_mark = self.hide_animation = self.enter = None
        self.setup_ui(self)

    @staticmethod
    def _parent(obj):
        return obj.parent().parent()

    def paintEvent(self, event):
        """ Override built-in paintEvent """

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.check_mark:
            painter.setBrush(QColor("#0d4871"))
        else:
            painter.setBrush(QColor("#00365c"))
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, self.width(), 45)
        painter.drawPixmap(self.position_x, self.position_y, QPixmap(self.icon_alias))
        painter.setPen(QColor("#9bb0bf")) if not self.enter and not self.check_mark else \
            painter.setPen(QColor("#cadfee"))
        painter.drawText(70, 15, 140, 14, Qt.AlignLeft, self.title)
        if self.check_mark:
            painter.setBrush(QColor("#4797ce"))
            painter.drawRect(0, 0, 3, 45)

    def mousePressEvent(
            self,
            event: QMouseEvent
    ) -> None:
        """ Override some mouse click events """

        parent = self._parent(self)
        previous_active = parent.currently_checked_menu_button
        if self == previous_active:
            return
        if previous_active is not None:
            previous_active.check_mark = None
            self.hide_animation = AnimationService(
                previous_active.count_label,
                b"geometry",
                200,
                QRect(
                    previous_active.count_label.x(),
                    previous_active.count_label.y(),
                    previous_active.count_label.width(),
                    previous_active.count_label.height()
                    ),
                QRect(
                    previous_active.count_label.x() + 30,
                    previous_active.count_label.y(),
                    previous_active.count_label.width(),
                    previous_active.count_label.height()
                    )
            ).init_animation()
            self.hide_animation.start()
            previous_active.repaint()
        query = QueryBuilder.count_parents(title=self.title)
        self.check_mark = f"{query}"
        parent.get_children(self.title)
        self.count_label.setText(self.check_mark)
        self.show_animation.start()

    def eventFilter(
            self,
            source: QPushButton,
            event: QEvent
    ) -> QPushButton:
        """
        Override event logic
        FocusIn, FocusOut
        """

        states = {10: True, 11: False}
        if event.type() in states:
            self.enter = states[event.type()]
            self.update()
        return QPushButton.eventFilter(self, source, event)
