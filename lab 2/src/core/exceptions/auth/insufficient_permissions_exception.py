"""
Исключение, возникающее при недостаточных правах доступа.
"""

from typing import Optional

from ..base_exception import RentalSystemException


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
