"""
Исключение, возникающее при недействительной карте.
"""

from typing import Optional

from ..base_exception import RentalSystemException


class InvalidCardException(RentalSystemException):
    """
    Исключение, возникающее при недействительной карте.

    Выбрасывается когда данные кредитной карты недействительны
    или карта отклонена платежной системой.
    """

    def __init__(self, message: str = "Недействительная карта",
                 card_last_four: Optional[str] = None, reason: Optional[str] = None):
        """
        Инициализирует исключение недействительной карты.

        Args:
            message: Сообщение об ошибке
            card_last_four: Последние четыре цифры карты
            reason: Причина отклонения карты
        """
        super().__init__(message, "INVALID_CARD",
                         {'card_last_four': card_last_four, 'reason': reason})
        self.card_last_four = card_last_four
        self.reason = reason
