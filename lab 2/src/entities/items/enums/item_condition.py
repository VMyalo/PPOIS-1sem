"""
Перечисление для состояния предмета.
"""

from enum import Enum


class ItemCondition(Enum):
    """
    Состояние предмета.

    Определяет физическое состояние предмета аренды.
    """

    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    DAMAGED = "damaged"
