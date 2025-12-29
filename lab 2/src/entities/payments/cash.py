"""
Класс оплаты наличными.

Этот модуль содержит реализацию оплаты наличными деньгами.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from .base_payment import BasePayment, PaymentMethod


@dataclass
class CashPayment(BasePayment):
    """
    Класс представляющий оплату наличными.

    Attributes:
        received_amount: Полученная сумма
        change_amount: Сумма сдачи
        received_by: Кто принял оплату
        payment_location: Место оплаты
    """

    received_amount: float = 0.0
    change_amount: float = 0.0
    received_by: Optional[str] = None
    payment_location: Optional[str] = None

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.payment_method = PaymentMethod.CASH

    def process_payment(self, amount: float, payment_method: str) -> bool:
        """
        Обрабатывает оплату наличными.

        Args:
            amount: Сумма к оплате
            payment_method: Метод оплаты

        Returns:
            bool: True если оплата успешна
        """
        self.received_amount = amount
        self.change_amount = max(0, amount - float(self.amount))

        return super().process_payment(self.amount, payment_method)

    def get_cash_details(self) -> Dict[str, Any]:
        """
        Получает детали оплаты наличными.

        Returns:
            Dict[str, Any]: Детали оплаты
        """
        return {
            'received_amount': self.received_amount,
            'change_amount': self.change_amount,
            'received_by': self.received_by,
            'payment_location': self.payment_location
        }
