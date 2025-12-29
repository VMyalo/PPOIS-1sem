"""
Исключение, возникающее когда аренда не найдена.
"""

from typing import Optional

from ..base_exception import RentalSystemException


class RentalNotFoundException(RentalSystemException):
    """
    Исключение, возникающее когда аренда не найдена.

    Выбрасывается когда пытаются выполнить операцию с арендой,
    которая не существует в системе.
    """

    def __init__(self, message: str = "Аренда не найдена",
                 rental_id: Optional[str] = None):
        """
        Инициализирует исключение ненайденной аренды.

        Args:
            message: Сообщение об ошибке
            rental_id: Идентификатор аренды
        """
        super().__init__(message, "RENTAL_NOT_FOUND", {'rental_id': rental_id})
        self.rental_id = rental_id
