"""
Исключение, возникающее когда предмет уже арендован.
"""

from typing import Optional
from datetime import datetime

from ..base_exception import RentalSystemException


class ItemAlreadyRentedException(RentalSystemException):
    """
    Исключение, возникающее когда предмет уже арендован.

    Выбрасывается когда пользователь пытается арендовать предмет,
    который уже находится в аренде у другого пользователя.
    """

    def __init__(self, message: str = "Предмет уже арендован другим пользователем",
                 item_id: Optional[str] = None, return_date: Optional[str] = None):
        """
        Инициализирует исключение уже арендованного предмета.

        Args:
            message: Сообщение об ошибке
            item_id: Идентификатор арендованного предмета
            return_date: Дата возврата предмета
        """
        super().__init__(message, "ITEM_ALREADY_RENTED",
                         {'item_id': item_id, 'return_date': return_date})
        self.item_id = item_id
        self.return_date = return_date
