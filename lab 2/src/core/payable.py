"""
Протокол для объектов, которые можно оплачивать.
"""

from decimal import Decimal
from typing import Protocol


class Payable(Protocol):
    """
    Протокол для объектов, которые можно оплачивать.

    Определяет контракт для объектов, которые требуют финансовой оплаты.
    """

    def process_payment(self, amount: Decimal, payment_method: str) -> bool:
        """
        Обработать платеж.

        Args:
            amount: Сумма платежа
            payment_method: Метод оплаты

        Returns:
            bool: True если платеж успешен
        """
        ...

    def get_payment_status(self) -> str:
        """
        Получить статус оплаты.

        Returns:
            str: Статус оплаты
        """
        ...
