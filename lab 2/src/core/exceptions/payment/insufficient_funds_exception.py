"""
Исключение, возникающее при недостатке средств.
"""

from typing import Optional
from decimal import Decimal

from ..base_exception import RentalSystemException


class InsufficientFundsException(RentalSystemException):
    """
    Исключение, возникающее при недостатке средств.

    Выбрасывается когда на счете недостаточно средств
    для выполнения платежа.
    """

    def __init__(self, message: str = "Недостаточно средств для оплаты",
                 required_amount: Optional[Decimal] = None,
                 available_balance: Optional[Decimal] = None):
        """
        Инициализирует исключение недостатка средств.

        Args:
            message: Сообщение об ошибке
            required_amount: Требуемая сумма
            available_balance: Доступный баланс
        """
        super().__init__(message, "INSUFFICIENT_FUNDS",
                         {'required_amount': str(required_amount) if required_amount else None,
                          'available_balance': str(available_balance) if available_balance else None})
        self.required_amount = required_amount
        self.available_balance = available_balance
