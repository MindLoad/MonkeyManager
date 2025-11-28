""" Left menu button widget """

__all__ = ['MenuButton']

from PyQt5.QtCore import QEvent, QRect, Qt
from PyQt5.QtGui import QColor, QMouseEvent, QPainter, QPixmap
from PyQt5.QtWidgets import QPushButton, QLabel

from models import QueryBuilder
from services import AnimationService, FontService
from styles import qlabel_css


class UiMenuButton:
    """ Menu button ui class """

    def __init__(self):
        self.hide_animation = self.show_animation = self.check_mark = self.font = self.count_label = None
        self.enter = False

    def setup_ui(self, MenuButtonWidget: QPushButton) -> None:
        """ setup left menu button ui """

        MenuButtonWidget.setFixedSize(200, 45)
        MenuButtonWidget.setCursor(Qt.PointingHandCursor)
        MenuButtonWidget.setObjectName("menu_button")
        self.font = FontService("Verdana", 11, True).get_font()
        self.count_label = QLabel(self)
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

    def mousePressEvent(self, event: QMouseEvent) -> None:
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
