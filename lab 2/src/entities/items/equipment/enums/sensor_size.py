"""
Перечисление для размеров сенсора.
"""

from enum import Enum


class SensorSize(Enum):
    """
    Размеры сенсора камеры.

    Определяет стандартные размеры сенсоров в камерах.
    """

    FULL_FRAME = "full_frame"
    APS_C = "aps_c"
    MICRO_FOUR_THIRDS = "micro_four_thirds"
    ONE_INCH = "one_inch"
