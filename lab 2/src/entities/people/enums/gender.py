"""
Перечисление для пола человека.
"""

from enum import Enum


class Gender(Enum):
    """
    Пол человека.

    Определяет возможные значения пола для пользователей системы.
    """

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
