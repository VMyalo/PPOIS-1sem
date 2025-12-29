"""
Перечисление для типов спорта.
"""

from enum import Enum


class SportType(Enum):
    """
    Типы спорта.

    Определяет категории спортивного оборудования.
    """

    WINTER_SPORTS = "winter_sports"
    WATER_SPORTS = "water_sports"
    TEAM_SPORTS = "team_sports"
    INDIVIDUAL_SPORTS = "individual_sports"
    EXTREME_SPORTS = "extreme_sports"
