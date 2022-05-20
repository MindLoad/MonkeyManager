""" Font service logic """

__all__ = ['FontService']

from dataclasses import dataclass
from PyQt5.QtGui import QFont


@dataclass
class FontService:
    """
    Font service dataclass
    """

    family: str
    size: int
    bold: bool

    def get_font(self) -> QFont:
        """
        Return font after initializing class
        :return: font
        """

        font = QFont()
        font.setFamily(self.family)
        font.setPixelSize(self.size)
        font.setBold(self.bold)
        return font
