"""
Исключение, возникающее при просроченном возврате.
"""

from datetime import datetime
from typing import Optional
from decimal import Decimal

from ..base_exception import RentalSystemException


class OverdueReturnException(RentalSystemException):
    """
    Исключение, возникающее при просроченном возврате.

    Выбрасывается когда предмет не возвращен вовремя
    и требуется оплата штрафа.
    """

    def __init__(self, message: str = "Просрочен возврат предмета",
                 rental_id: Optional[str] = None,
                 due_date: Optional[datetime] = None,
                 days_overdue: int = 0,
                 penalty_amount: Optional[float] = None):
        """
        Инициализирует исключение просроченного возврата.

        Args:
            message: Сообщение об ошибке
            rental_id: Идентификатор аренды
            due_date: Срок возврата
            days_overdue: Количество дней просрочки
            penalty_amount: Сумма штрафа
        """
        super().__init__(message, "OVERDUE_RETURN",
                         {'rental_id': rental_id,
                          'due_date': str(due_date) if due_date else None,
                          'days_overdue': days_overdue,
                          'penalty_amount': penalty_amount})
        self.rental_id = rental_id
        self.due_date = due_date
        self.days_overdue = days_overdue
        self.penalty_amount = penalty_amount
