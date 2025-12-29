"""
Перечисление для статуса предмета.
"""

from enum import Enum


class ItemStatus(Enum):
    """
    Статус предмета аренды.

    Определяет текущее состояние предмета в системе аренды.
    """

    AVAILABLE = "available"
    RENTED = "rented"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"
    DAMAGED = "damaged"
    LOST = "lost"
