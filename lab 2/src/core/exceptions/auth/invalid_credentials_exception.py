"""
Исключение, возникающее при неверных учетных данных.
"""

from typing import Optional

from ..base_exception import RentalSystemException


class InvalidCredentialsException(RentalSystemException):
    """
    Исключение, возникающее при неверных учетных данных.

    Выбрасывается когда пользователь вводит неправильный логин или пароль.
    """

    def __init__(self, message: str = "Неверные учетные данные", username: Optional[str] = None):
        """
        Инициализирует исключение неверных учетных данных.

        Args:
            message: Сообщение об ошибке
            username: Имя пользователя, которое вызвало ошибку
        """
        super().__init__(message, "INVALID_CREDENTIALS", {'username': username})
        self.username = username
