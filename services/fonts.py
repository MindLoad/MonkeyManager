""" Font service logic """

__all__ = ['FontService']

from attrs import define, field
from PyQt5.QtGui import QFont


@define
class FontService:
    """ Font service dataclass """

    family: str = field(factory=str)
    size: int = field(factory=int)
    bold: bool = field(factory=bool)

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
