"""
Перечисление для источников питания.
"""

from enum import Enum


class PowerSource(Enum):
    """
    Источники питания.

    Определяет типы источников питания для оборудования.
    """

    BATTERY = "battery"
    ELECTRIC = "electric"
    MANUAL = "manual"
    SOLAR = "solar"
