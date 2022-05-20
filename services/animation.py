""" Animation service logic """

__all__ = ['AnimationService']

import typing
from dataclasses import dataclass
from PyQt5.QtCore import QRect, QPropertyAnimation


@dataclass
class AnimationService:
    """
    Animation service dataclass
    """

    element: typing.Any
    property_name: typing.ByteString
    duration: int
    start_value: QRect
    end_value: QRect

    def init_animation(self) -> QPropertyAnimation:
        """
        Prepare animation instance
        :return: QPropertyAnimation
        """

        animation = QPropertyAnimation(self.element, self.property_name)
        animation.setDuration(self.duration)
        animation.setStartValue(self.start_value)
        animation.setEndValue(self.end_value)
        return animation
