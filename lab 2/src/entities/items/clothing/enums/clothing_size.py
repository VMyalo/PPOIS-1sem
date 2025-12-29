"""
Перечисление для размеров одежды.
"""

from enum import Enum


class ClothingSize(Enum):
    """
    Размеры одежды.

    Определяет стандартные размеры одежды.
    """

    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"
