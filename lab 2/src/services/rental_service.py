"""
Сервис аренды.

Этот модуль содержит логику управления арендой предметов.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from decimal import Decimal

from ..core.base import BaseService
from ..entities.items import BaseItem
from ..entities.people import Customer
from ..entities.payments import BasePayment
from ..entities.rentals import Reservation
from ..core.exceptions import (
    ItemNotAvailableException,
    InvalidRentalPeriodException,
    InsufficientPermissionsException
)
from ..utils import constants as const


@dataclass
class RentalService(BaseService):
    """
    Сервис для управления арендой предметов.

    Attributes:
        item_repository: Репозиторий предметов
        customer_repository: Репозиторий клиентов
        payment_service: Сервис платежей
    """

    item_repository: Optional[Any] = None
    customer_repository: Optional[Any] = None
    payment_service: Optional[Any] = None

    def create_reservation(self, customer_id: str, item_id: str,
                          start_date: datetime, end_date: datetime) -> Reservation:
        """
        Создает резервирование предмета.

        Args:
            customer_id: ID клиента
            item_id: ID предмета
            start_date: Дата начала
            end_date: Дата окончания

        Returns:
            Reservation: Созданное резервирование
        """
        # Валидация периода
        if not self._validate_rental_period(start_date, end_date):
            raise InvalidRentalPeriodException()

        # Проверка доступности предмета
        item = self._get_item_by_id(item_id)
        if not item.is_available_for_rental():
            raise ItemNotAvailableException(item_id=item_id)

        # Проверка конфликтов с существующими резервами
        if not self._check_availability(item_id, start_date, end_date):
            raise ItemNotAvailableException(item_id=item_id)

        # Создание резервирования
        reservation = Reservation(
            customer_id=customer_id,
            item_id=item_id,
            start_date=start_date,
            end_date=end_date,
            status="confirmed"
        )

        return reservation

    def start_rental(self, reservation_id: str):
        """
        Начинает аренду на основе резервирования.

        Args:
            reservation_id: ID резервирования

        Returns:
            None: Метод пока не реализован
        """
        # Заглушка - класс Rental еще не реализован
        pass

    def end_rental(self, rental_id: str, return_condition: str) -> Decimal:
        """
        Завершает аренду.

        Args:
            rental_id: ID аренды
            return_condition: Состояние при возврате

        Returns:
            Decimal: Итоговая стоимость
        """
        # Заглушка - класс Rental еще не реализован
        return Decimal("0.00")

    def calculate_rental_cost(self, item_id: str, start_date: datetime,
                            end_date: datetime, customer_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Рассчитывает стоимость аренды.

        Args:
            item_id: ID предмета
            start_date: Дата начала
            end_date: Дата окончания
            customer_id: ID клиента (опционально)

        Returns:
            Dict[str, Any]: Детализация стоимости
        """
        item = self._get_item_by_id(item_id)
        days = (end_date - start_date).days + 1

        base_cost = item.calculate_total(days)

        # Скидки для постоянных клиентов
        discount = Decimal("0.00")
        if customer_id:
            customer = self._get_customer_by_id(customer_id)
            discount = customer.get_membership_discount() * base_cost

        # Страховка
        insurance_cost = days * Decimal("2.00")

        total = base_cost - discount + insurance_cost

        return {
            'base_cost': float(base_cost),
            'discount': float(discount),
            'insurance': float(insurance_cost),
            'total': float(total),
            'currency': const.DEFAULT_CURRENCY
        }

    def get_available_items(self, category: Optional[str] = None,
                          date_from: Optional[datetime] = None,
                          date_to: Optional[datetime] = None) -> List[BaseItem]:
        """
        Получает доступные для аренды предметы.

        Args:
            category: Категория предметов
            date_from: Дата начала аренды
            date_to: Дата окончания аренды

        Returns:
            List[BaseItem]: Список доступных предметов
        """
        # В реальном приложении фильтрация по репозиторию
        return []

    def _validate_rental_period(self, start_date: datetime, end_date: datetime) -> bool:
        """
        Валидирует период аренды.

        Args:
            start_date: Дата начала
            end_date: Дата окончания

        Returns:
            bool: True если период валиден
        """
        if start_date >= end_date:
            return False

        days = (end_date - start_date).days
        return (const.MINIMUM_RENTAL_DURATION_HOURS / 24) <= days <= const.MAXIMUM_RENTAL_DURATION_DAYS

    def _check_availability(self, item_id: str, start_date: datetime, end_date: datetime) -> bool:
        """
        Проверяет доступность предмета на заданный период.

        Args:
            item_id: ID предмета
            start_date: Дата начала
            end_date: Дата окончания

        Returns:
            bool: True если доступен
        """
        # Заглушка - в реальном приложении проверка в репозитории
        return True

    def _calculate_penalties(self, rental, return_condition: str) -> Decimal:
        """
        Рассчитывает штрафы за аренду.

        Args:
            rental: Аренда
            return_condition: Состояние при возврате

        Returns:
            Decimal: Сумма штрафов
        """
        penalty = Decimal("0.00")

        # Штраф за просрочку
        if datetime.now() > rental.end_date:
            overdue_days = (datetime.now() - rental.end_date).days
            penalty += overdue_days * Decimal("5.00")

        # Штраф за повреждения
        if return_condition == "damaged":
            penalty += Decimal("50.00")

        return penalty

    def _get_item_by_id(self, item_id: str) -> BaseItem:
        """Получает предмет по ID."""
        # Заглушка
        raise NotImplementedError()

    def _get_customer_by_id(self, customer_id: str) -> Customer:
        """Получает клиента по ID."""
        # Заглушка
        raise NotImplementedError()

    def _get_reservation_by_id(self, reservation_id: str) -> Reservation:
        """Получает резервирование по ID."""
        # Заглушка
        raise NotImplementedError()

    def _get_rental_by_id(self, rental_id: str):
        """Получает аренду по ID."""
        # Заглушка - класс Rental еще не реализован
        raise NotImplementedError("Класс Rental еще не реализован")

    # Реализация абстрактных методов BaseService
    def create(self, entity: Any) -> Any:
        """Создает сущность (заглушка для BaseService)."""
        return entity

    def get_by_id(self, entity_id: str) -> Optional[Any]:
        """Получает сущность по ID (заглушка для BaseService)."""
        return None

    def update(self, entity: Any) -> Any:
        """Обновляет сущность (заглушка для BaseService)."""
        return entity

    def delete(self, entity_id: str) -> bool:
        """Удаляет сущность (заглушка для BaseService)."""
        return False

    def get_all(self) -> List[Any]:
        """Получает все сущности (заглушка для BaseService)."""
        return []
