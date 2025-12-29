"""
Исключение, возникающее когда предмет недоступен для аренды.
"""

from typing import Optional

from ..base_exception import RentalSystemException


class ItemNotAvailableException(RentalSystemException):
    """
    Исключение, возникающее когда предмет недоступен для аренды.

    Выбрасывается когда пользователь пытается арендовать предмет,
    который в данный момент недоступен.
    """

    def __init__(self, message: str = "Предмет недоступен для аренды",
                 item_id: Optional[str] = None, reason: Optional[str] = None):
        """
        Инициализирует исключение недоступности предмета.

        Args:
            message: Сообщение об ошибке
            item_id: Идентификатор недоступного предмета
            reason: Причина недоступности
        """
        super().__init__(message, "ITEM_NOT_AVAILABLE",
                         {'item_id': item_id, 'reason': reason})
        self.item_id = item_id
        self.reason = reason
