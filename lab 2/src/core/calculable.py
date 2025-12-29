"""
Протокол для объектов, стоимость которых можно рассчитать.
"""

from decimal import Decimal
from typing import Protocol


class Calculable(Protocol):
    """
    Протокол для объектов, стоимость которых можно рассчитать.

    Определяет контракт для объектов, которые могут вычислить свою стоимость.
    """

    def calculate_total(self) -> Decimal:
        """
        Рассчитать общую стоимость.

        Returns:
            Decimal: Общая стоимость
        """
        ...
