"""
Исключение, возникающее при ошибках валидации.
"""

from typing import Optional, Any

from ..base_exception import RentalSystemException


class ValidationException(RentalSystemException):
    """
    Исключение, возникающее при ошибках валидации.

    Выбрасывается когда входные данные не проходят валидацию
    согласно бизнес-правилам или техническим ограничениям.
    """

    def __init__(self, message: str = "Ошибка валидации данных",
                 field_name: Optional[str] = None, field_value: Optional[Any] = None):
        """
        Инициализирует исключение валидации.

        Args:
            message: Сообщение об ошибке
            field_name: Название поля с ошибкой
            field_value: Значение поля с ошибкой
        """
        super().__init__(message, "VALIDATION_ERROR",
                         {'field_name': field_name, 'field_value': str(field_value) if field_value else None})
        self.field_name = field_name
        self.field_value = field_value
