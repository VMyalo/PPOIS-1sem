"""
Перечисление для типов топлива.
"""

from enum import Enum


class FuelType(Enum):
    """
    Типы топлива.

    Определяет виды топлива для транспортных средств.
    """

    PETROL = "petrol"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"
