"""
Протокол для объектов, которые можно резервировать.
"""

from datetime import datetime
from typing import Protocol


class Reservable(Protocol):
    """
    Протокол для объектов, которые можно резервировать.

    Определяет контракт для объектов, которые можно временно зарезервировать.
    """

    def reserve(self, user_id: str, start_date: datetime, end_date: datetime) -> bool:
        """
        Зарезервировать объект на указанный период.

        Args:
            user_id: ID пользователя
            start_date: Дата начала резерва
            end_date: Дата окончания резерва

        Returns:
            bool: True если резервирование успешно
        """
        ...

    def cancel_reservation(self, reservation_id: str) -> bool:
        """
        Отменить резервирование.

        Args:
            reservation_id: ID резервирования

        Returns:
            bool: True если отмена успешна
        """
        ...
