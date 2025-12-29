"""
Исключения, связанные с аутентификацией и авторизацией.

Этот модуль содержит исключения для обработки ошибок
в системах аутентификации и авторизации.
"""

from .base_exception import RentalSystemException
from typing import Optional


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


class AccountLockedException(RentalSystemException):
    """
    Исключение, возникающее при блокировке учетной записи.

    Выбрасывается когда учетная запись заблокирована из-за
    превышения количества неудачных попыток входа.
    """

    def __init__(self, message: str = "Учетная запись заблокирована", lockout_duration_minutes: int = 30):
        """
        Инициализирует исключение блокировки учетной записи.

        Args:
            message: Сообщение об ошибке
            lockout_duration_minutes: Длительность блокировки в минутах
        """
        super().__init__(message, "ACCOUNT_LOCKED",
                         {'lockout_duration_minutes': lockout_duration_minutes})
        self.lockout_duration_minutes = lockout_duration_minutes


class InsufficientPermissionsException(RentalSystemException):
    """
    Исключение, возникающее при недостаточных правах доступа.

    Выбрасывается когда пользователь пытается выполнить действие,
    на которое у него нет прав.
    """

    def __init__(self, message: str = "Недостаточно прав для выполнения действия",
                 required_role: Optional[str] = None, user_role: Optional[str] = None):
        """
        Инициализирует исключение недостаточных прав.

        Args:
            message: Сообщение об ошибке
            required_role: Требуемая роль для действия
            user_role: Текущая роль пользователя
        """
        super().__init__(message, "INSUFFICIENT_PERMISSIONS",
                         {'required_role': required_role, 'user_role': user_role})
        self.required_role = required_role
        self.user_role = user_role
