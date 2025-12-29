"""
Класс резервирования.

Этот модуль содержит реализацию резервирования предметов для аренды.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any

from src.core.base import BaseEntity
from src.utils import constants as const


@dataclass
class Reservation(BaseEntity):
    """
    Класс представляющий резервирование предмета.

    Attributes:
        customer_id: ID клиента
        item_id: ID предмета
        start_date: Дата начала резерва
        end_date: Дата окончания резерва
        status: Статус резерва
        total_cost: Общая стоимость
        deposit_amount: Сумма залога
        special_requests: Особые запросы
        confirmed_at: Время подтверждения
        expires_at: Время истечения резерва
    """

    customer_id: str = ""
    item_id: str = ""
    start_date: datetime = datetime.now()
    end_date: datetime = datetime.now()
    status: str = "pending"
    total_cost: float = 0.0
    deposit_amount: float = 0.0
    special_requests: Optional[str] = None
    confirmed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        if not self.customer_id or not self.item_id:
            raise ValueError("ID клиента и предмета обязательны")

    def confirm_reservation(self) -> None:
        """Подтверждает резервирование."""
        self.status = "confirmed"
        self.confirmed_at = datetime.now()
        self.expires_at = None
        self.update_timestamp()

    def cancel_reservation(self) -> None:
        """Отменяет резервирование."""
        self.status = "cancelled"
        self.update_timestamp()

    def expire_reservation(self) -> None:
        """Истекает резервирование."""
        self.status = "expired"
        self.update_timestamp()

    def is_active(self) -> bool:
        """
        Проверяет активно ли резервирование.

        Returns:
            bool: True если активно
        """
        return self.status == "confirmed" and self.start_date <= datetime.now() <= self.end_date

    def get_duration_days(self) -> int:
        """
        Получает длительность резервирования в днях.

        Returns:
            int: Длительность в днях
        """
        return (self.end_date - self.start_date).days + 1

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует резервирование в словарь.

        Returns:
            Dict[str, Any]: Словарь с данными резервирования
        """
        data = super().to_dict()
        data.update({
            'customer_id': self.customer_id,
            'item_id': self.item_id,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'status': self.status,
            'total_cost': self.total_cost,
            'deposit_amount': self.deposit_amount,
            'special_requests': self.special_requests,
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        })
        return data
