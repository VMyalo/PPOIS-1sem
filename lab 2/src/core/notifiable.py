"""
Протокол для объектов, которые могут отправлять уведомления.
"""

from typing import Dict, List, Any, Protocol


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
