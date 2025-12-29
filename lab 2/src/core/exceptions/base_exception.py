"""
Базовые исключения для системы аренды.

Этот модуль содержит базовые классы исключений,
используемые во всей системе.
"""


class RentalSystemException(Exception):
    """
    Базовое исключение для системы аренды.

    Все исключения системы должны наследоваться от этого класса.

    Attributes:
        message: Сообщение об ошибке
        error_code: Код ошибки для систематизации
        details: Дополнительная информация об ошибке
    """

    def __init__(self, message: str, error_code: str = None, details: dict = None):
        """
        Инициализирует исключение.

        Args:
            message: Сообщение об ошибке
            error_code: Код ошибки
            details: Дополнительная информация
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.details = details or {}

    def __str__(self) -> str:
        """Возвращает строковое представление исключения."""
        if self.error_code != "UNKNOWN_ERROR":
            return f"[{self.error_code}] {self.message}"
        return self.message

    def to_dict(self) -> dict:
        """
        Преобразует исключение в словарь для сериализации.

        Returns:
            dict: Словарь с информацией об исключении
        """
        return {
            'error_code': self.error_code,
            'message': self.message,
            'details': self.details
        }
