"""
Перечисление для типов одежды.
"""

from enum import Enum


class ClothingType(Enum):
    """
    Типы одежды.

    Определяет категории одежды для аренды.
    """

    CASUAL = "casual"
    FORMAL = "formal"
    SPORT = "sport"
    WINTER = "winter"
    SUMMER = "summer"
    PROTECTIVE = "protective"
