""" QFrame add new key """

__all__ = ['AddNewKey']

from datetime import datetime

import chime
from PyQt5.QtCore import QEvent, QRect, QSize, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLineEdit, QPushButton, QRadioButton, QVBoxLayout, QWidget

from models import QueryBuilder
from services import AnimationService
from styles import qframe_css
from tools import run_encode


class AddNewKey(QFrame):
    """ QFrame popup widget for adding new element """

    def __init__(
            self,
            secret_key: str,
            data: list | None,
            parent: QWidget
    ):
        super().__init__(parent)
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.secret_key = secret_key
        self.data = data
        self.w = self.parent.width()
        self.h = self.parent.height()
        self.setFixedSize(self.w, self.h)
        self.setObjectName("AddFrame")
        self.setStyleSheet(qframe_css.add_new_key_style)
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
            self.combo.addItems(
                ("Web Sites", "Web Accounts", "Emails", "Credit Cards", "E-commerce", "Secrets", "Software", "Forums")
            )
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
        self.animation = AnimationService(self, b"geometry", 200,
                                          QRect(0, -self.h, self.w, self.h),
                                          QRect(0, 0, self.w, self.h)
                                          ).init_animation()
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
        query = QueryBuilder.retrieve_parents(root_parent=self.combo.currentText())
        for item in query:
            r_elem = QRadioButton()
            r_elem.setObjectName("child-element")
            r_elem.setText(item.child)
            r_elem.setFixedHeight(20)
            r_elem.setCursor(Qt.PointingHandCursor)
            r_elem.clicked.connect(self.child_text_replace)
            self.cc.addWidget(r_elem)
        self.sender().blockSignals(False)

    def child_text_replace(self):
        self.child.setText(self.sender().text())

    def _save(self):
        crypt_password = run_encode(self.secret_key, self.password.text().encode("utf-8"))
        if not self.data:
            QueryBuilder.create_item(
                parent=self.combo.currentText(), child=self.child.text(), title=self.title.text(),
                login=self.name.text(), email=self.email.text(), password=crypt_password, url=self.url.text(),
                phone=self.phone.text(), created=self.created.text(), modified=self.modified.text()
            )
        else:
            QueryBuilder.update_item(
                item_id=self.data[3],
                title=self.title.text(),
                login=self.name.text(),
                email=self.email.text(),
                password=crypt_password,
                url=self.url.text(),
                phone=self.phone.text(),
                modified=self.modified.text()
            )
        self._close()
        chime.success()

    def _close(self):
        self.animation.setStartValue(QRect(0, 0, self.w, self.h))
        self.animation.setEndValue(QRect(0, -self.h, self.w, self.h))
        self.animation.start()
        self.timer.start()

    def _quit(self):
        self.close()
        self.deleteLater()
        self.parent._add = None

    def keyPressEvent(
            self,
            event: QEvent
    ) -> None:
        """ Track key press """
        if event.key() == Qt.Key_Escape:
            self._close()
