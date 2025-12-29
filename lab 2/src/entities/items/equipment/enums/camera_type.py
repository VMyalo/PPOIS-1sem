"""
Перечисление для типов камер.
"""

from enum import Enum


class CameraType(Enum):
    """
    Типы камер.

    Определяет различные типы камер для фото и видеосъемки.
    """

    DSLR = "dslr"
    MIRRORLESS = "mirrorless"
    COMPACT = "compact"
    ACTION = "action"
    CINEMA = "cinema"
