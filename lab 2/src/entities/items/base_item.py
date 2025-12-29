"""
Базовый класс для предметов аренды.

Этот модуль содержит базовую реализацию предметов,
доступных для аренды в системе.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Any

from src.core.base import BaseEntity
from src.core.calculable import Calculable
from src.core.reservable import Reservable
from .enums.item_status import ItemStatus
from .enums.item_condition import ItemCondition
from src.utils import constants as const


@dataclass
class BaseItem(BaseEntity, Calculable, Reservable):
    """
    Базовый класс для всех предметов аренды.

    Этот класс предоставляет общую функциональность для всех типов предметов,
    доступных для аренды: одежду, оборудование, инструменты, транспорт и т.д.

    Attributes:
        name: Название предмета
        description: Описание предмета
        category: Категория предмета
        daily_rate: Стоимость аренды за день
        status: Текущий статус предмета
        condition: Состояние предмета
        location_id: ID места хранения
        serial_number: Серийный номер
        purchase_date: Дата покупки
        last_maintenance_date: Дата последнего обслуживания
        rental_count: Количество аренд
        total_revenue: Общий доход от аренды
    """

    name: str = ""
    description: str = ""
    category: str = ""
    daily_rate: Decimal = Decimal("0.00")
    status: ItemStatus = ItemStatus.AVAILABLE
    condition: ItemCondition = ItemCondition.GOOD
    location_id: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: Optional[datetime] = None
    last_maintenance_date: Optional[datetime] = None
    rental_count: int = 0
    total_revenue: Decimal = Decimal("0.00")

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        if not self.name:
            raise ValueError("Название предмета не может быть пустым")
        if self.daily_rate < 0:
            raise ValueError("Стоимость аренды не может быть отрицательной")

    def validate(self) -> bool:
        """
        Валидирует состояние предмета.

        Returns:
            bool: True если валидация успешна
        """
        errors = self.get_validation_errors()
        return len(errors) == 0

    def get_validation_errors(self) -> List[str]:
        """
        Получает список ошибок валидации.

        Returns:
            List[str]: Список ошибок валидации
        """
        errors = super().get_validation_errors()

        if not self.name or len(self.name.strip()) == 0:
            errors.append("Название предмета не может быть пустым")

        if len(self.name) > const.MAXIMUM_STRING_LENGTH:
            errors.append(f"Название предмета не может превышать {const.MAXIMUM_STRING_LENGTH} символов")

        if self.daily_rate < 0:
            errors.append("Стоимость аренды не может быть отрицательной")

        if self.rental_count < 0:
            errors.append("Количество аренд не может быть отрицательным")

        if self.total_revenue < 0:
            errors.append("Общий доход не может быть отрицательным")

        if self.serial_number and len(self.serial_number) > const.MAXIMUM_STRING_LENGTH:
            errors.append(f"Серийный номер не может превышать {const.MAXIMUM_STRING_LENGTH} символов")

        if self.purchase_date and self.purchase_date > datetime.now():
            errors.append("Дата покупки не может быть в будущем")

        if self.last_maintenance_date and self.last_maintenance_date > datetime.now():
            errors.append("Дата обслуживания не может быть в будущем")

        return errors

    def calculate_total(self, days: int = 1) -> Decimal:
        """
        Рассчитывает стоимость аренды за указанное количество дней.

        Args:
            days: Количество дней аренды

        Returns:
            Decimal: Общая стоимость аренды
        """
        if days <= 0:
            raise ValueError("Количество дней должно быть положительным")

        base_cost = self.daily_rate * Decimal(str(days))

        # Применяем скидку за длительную аренду
        if days >= const.DISCOUNT_THRESHOLD_DAYS:
            discount = base_cost * const.DISCOUNT_PERCENTAGE
            return base_cost - discount

        return base_cost

    def reserve(self, user_id: str, start_date: datetime, end_date: datetime) -> bool:
        """
        Резервирует предмет на указанный период.

        Args:
            user_id: ID пользователя
            start_date: Дата начала резерва
            end_date: Дата окончания резерва

        Returns:
            bool: True если резервирование успешно
        """
        if self.status != ItemStatus.AVAILABLE:
            return False

        if start_date >= end_date:
            return False

        if start_date < datetime.now():
            return False

        # Здесь должна быть логика проверки конфликтов с существующими резервами
        # Для простоты предполагаем, что резервирование всегда успешно
        self.status = ItemStatus.RESERVED
        self.update_timestamp()
        return True

    def cancel_reservation(self, reservation_id: str) -> bool:
        """
        Отменяет резервирование предмета.

        Args:
            reservation_id: ID резервирования

        Returns:
            bool: True если отмена успешна
        """
        if self.status == ItemStatus.RESERVED:
            self.status = ItemStatus.AVAILABLE
            self.update_timestamp()
            return True
        return False

    def mark_as_rented(self) -> None:
        """Отмечает предмет как арендованный."""
        self.status = ItemStatus.RENTED
        self.rental_count += 1
        self.update_timestamp()

    def mark_as_returned(self, revenue: Decimal) -> None:
        """
        Отмечает предмет как возвращенный и обновляет статистику.

        Args:
            revenue: Доход от этой аренды
        """
        self.status = ItemStatus.AVAILABLE
        self.total_revenue += revenue
        self.update_timestamp()

    def mark_for_maintenance(self) -> None:
        """Отмечает предмет как требующий обслуживания."""
        self.status = ItemStatus.MAINTENANCE
        self.last_maintenance_date = datetime.now()
        self.update_timestamp()

    def mark_as_damaged(self) -> None:
        """Отмечает предмет как поврежденный."""
        self.status = ItemStatus.DAMAGED
        self.update_timestamp()

    def mark_as_lost(self) -> None:
        """Отмечает предмет как утерянный."""
        self.status = ItemStatus.LOST
        self.update_timestamp()

    def update_condition(self, new_condition: ItemCondition) -> None:
        """
        Обновляет состояние предмета.

        Args:
            new_condition: Новое состояние предмета
        """
        self.condition = new_condition
        self.update_timestamp()

    def is_available_for_rental(self) -> bool:
        """
        Проверяет доступен ли предмет для аренды.

        Returns:
            bool: True если доступен
        """
        return self.status == ItemStatus.AVAILABLE and self.condition != ItemCondition.DAMAGED

    def needs_maintenance(self) -> bool:
        """
        Проверяет требуется ли предмету обслуживание.

        Returns:
            bool: True если требуется обслуживание
        """
        if not self.last_maintenance_date:
            return True

        days_since_maintenance = (datetime.now() - self.last_maintenance_date).days
        return days_since_maintenance >= const.MAINTENANCE_CHECK_INTERVAL_DAYS

    def get_age_in_days(self) -> int:
        """
        Получает возраст предмета в днях.

        Returns:
            int: Возраст в днях
        """
        if not self.purchase_date:
            return 0
        return (datetime.now() - self.purchase_date).days

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует предмет в словарь для сериализации.

        Returns:
            Dict[str, Any]: Словарь с данными предмета
        """
        data = super().to_dict()
        data.update({
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'daily_rate': str(self.daily_rate),
            'status': self.status.value,
            'condition': self.condition.value,
            'location_id': self.location_id,
            'serial_number': self.serial_number,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'last_maintenance_date': self.last_maintenance_date.isoformat() if self.last_maintenance_date else None,
            'rental_count': self.rental_count,
            'total_revenue': str(self.total_revenue)
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseItem':
        """
        Создает предмет из словаря.

        Args:
            data: Словарь с данными предмета

        Returns:
            BaseItem: Новый экземпляр предмета
        """
        # Преобразуем строковые значения обратно в соответствующие типы
        if 'daily_rate' in data:
            data['daily_rate'] = Decimal(data['daily_rate'])
        if 'total_revenue' in data:
            data['total_revenue'] = Decimal(data['total_revenue'])
        if 'status' in data:
            data['status'] = ItemStatus(data['status'])
        if 'condition' in data:
            data['condition'] = ItemCondition(data['condition'])
        if 'purchase_date' in data and data['purchase_date']:
            data['purchase_date'] = datetime.fromisoformat(data['purchase_date'])
        if 'last_maintenance_date' in data and data['last_maintenance_date']:
            data['last_maintenance_date'] = datetime.fromisoformat(data['last_maintenance_date'])

        return cls(**data)
