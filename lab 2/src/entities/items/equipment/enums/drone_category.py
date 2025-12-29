"""
Перечисление для категорий дронов.
"""

from enum import Enum


class DroneCategory(Enum):
    """
    Категории дронов.

    Определяет размер и назначение дронов.
    """

    NANO = "nano"
    MINI = "mini"
    STANDARD = "standard"
    PROFESSIONAL = "professional"
    INDUSTRIAL = "industrial"
