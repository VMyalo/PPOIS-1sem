"""
Исключение, возникающее при недостатке запасов.
"""

from typing import Optional

from ..base_exception import RentalSystemException


class InsufficientStockException(RentalSystemException):
    """
    Исключение, возникающее при недостатке запасов.

    Выбрасывается когда запрашиваемое количество предметов
    превышает доступное количество на складе.
    """

    def __init__(self, message: str = "Недостаточно товара на складе",
                 item_id: Optional[str] = None, requested_quantity: int = 0,
                 available_quantity: int = 0):
        """
        Инициализирует исключение недостатка запасов.

        Args:
            message: Сообщение об ошибке
            item_id: Идентификатор предмета
            requested_quantity: Запрашиваемое количество
            available_quantity: Доступное количество
        """
        super().__init__(message, "INSUFFICIENT_STOCK",
                         {'item_id': item_id, 'requested_quantity': requested_quantity,
                          'available_quantity': available_quantity})
        self.item_id = item_id
        self.requested_quantity = requested_quantity
        self.available_quantity = available_quantity
