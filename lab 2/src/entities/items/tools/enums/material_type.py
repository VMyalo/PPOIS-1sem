"""
Перечисление для типов материалов.
"""

from enum import Enum


class MaterialType(Enum):
    """
    Типы материалов инструментов.

    Определяет материалы, из которых изготовлены инструменты.
    """

    STEEL = "steel"
    ALUMINUM = "aluminum"
    PLASTIC = "plastic"
    COMPOSITE = "composite"
    CARBON_FIBER = "carbon_fiber"
