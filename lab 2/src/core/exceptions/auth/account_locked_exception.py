"""
Исключение, возникающее при блокировке учетной записи.
"""

from ..base_exception import RentalSystemException


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
