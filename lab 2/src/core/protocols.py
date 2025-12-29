"""
Протоколы системы аренды.

Этот модуль содержит протоколы (интерфейсы с поведением),
используемые в системе.
"""

from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Any, Protocol


class Calculable(Protocol):
    """
    Протокол для объектов, стоимость которых можно рассчитать.

    Определяет контракт для объектов, которые могут вычислить свою стоимость.
    """

    def calculate_total(self) -> Decimal:
        """
        Рассчитать общую стоимость.

        Returns:
            Decimal: Общая стоимость
        """
        ...


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


class Payable(Protocol):
    """
    Протокол для объектов, которые можно оплачивать.

    Определяет контракт для объектов, которые требуют финансовой оплаты.
    """

    def process_payment(self, amount: Decimal, payment_method: str) -> bool:
        """
        Обработать платеж.

        Args:
            amount: Сумма платежа
            payment_method: Метод оплаты

        Returns:
            bool: True если платеж успешен
        """
        ...

    def get_payment_status(self) -> str:
        """
        Получить статус оплаты.

        Returns:
            str: Статус оплаты
        """
        ...


class Notifiable(Protocol):
    """
    Протокол для объектов, которые могут отправлять уведомления.

    Определяет контракт для объектов, которые могут уведомлять пользователей.
    """

    def send_notification(self, recipient: str, message: str, notification_type: str) -> bool:
        """
        Отправить уведомление.

        Args:
            recipient: Получатель уведомления
            message: Текст уведомления
            notification_type: Тип уведомления

        Returns:
            bool: True если уведомление отправлено
        """
        ...

    def get_notification_history(self) -> List[Dict[str, Any]]:
        """
        Получить историю уведомлений.

        Returns:
            List[Dict[str, Any]]: История уведомлений
        """
        ...


class Trackable(Protocol):
    """
    Протокол для объектов, которые можно отслеживать.

    Определяет контракт для объектов, состояние которых можно отслеживать.
    """

    def get_current_location(self) -> Optional[Dict[str, float]]:
        """
        Получить текущее местоположение.

        Returns:
            Optional[Dict[str, float]]: Координаты местоположения
        """
        ...

    def update_location(self, latitude: float, longitude: float) -> None:
        """
        Обновить местоположение.

        Args:
            latitude: Широта
            longitude: Долгота
        """
        ...

    def get_tracking_history(self) -> List[Dict[str, Any]]:
        """
        Получить историю отслеживания.

        Returns:
            List[Dict[str, Any]]: История перемещений
        """
        ...
