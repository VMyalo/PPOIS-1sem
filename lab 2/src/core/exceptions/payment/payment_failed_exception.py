"""
Исключение, возникающее при неудачной оплате.
"""

from typing import Optional

from ..base_exception import RentalSystemException


class PaymentFailedException(RentalSystemException):
    """
    Исключение, возникающее при неудачной оплате.

    Выбрасывается когда платеж не может быть обработан
    по техническим или финансовым причинам.
    """

    def __init__(self, message: str = "Оплата не удалась",
                 payment_id: Optional[str] = None, reason: Optional[str] = None):
        """
        Инициализирует исключение неудачной оплаты.

        Args:
            message: Сообщение об ошибке
            payment_id: Идентификатор платежа
            reason: Причина неудачи оплаты
        """
        super().__init__(message, "PAYMENT_FAILED",
                         {'payment_id': payment_id, 'reason': reason})
        self.payment_id = payment_id
        self.reason = reason
