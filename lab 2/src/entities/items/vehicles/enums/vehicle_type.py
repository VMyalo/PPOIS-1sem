"""
Перечисление для типов транспортных средств.
"""

from enum import Enum


class VehicleType(Enum):
    """
    Типы транспортных средств.

    Определяет категории транспортных средств для аренды.
    """

    BICYCLE = "bicycle"
    MOTORCYCLE = "motorcycle"
    SCOOTER = "scooter"
    CAR = "car"
    VAN = "van"
