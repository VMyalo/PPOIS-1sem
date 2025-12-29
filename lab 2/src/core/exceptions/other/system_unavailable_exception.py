"""
Исключение, возникающее при недоступности системы.
"""

from typing import Optional

from ..base_exception import RentalSystemException


class SystemUnavailableException(RentalSystemException):
    """
    Исключение, возникающее при недоступности системы.

    Выбрасывается когда система временно недоступна
    из-за технических проблем или обслуживания.
    """

    def __init__(self, message: str = "Система временно недоступна",
                 estimated_downtime: Optional[str] = None):
        """
        Инициализирует исключение недоступности системы.

        Args:
            message: Сообщение об ошибке
            estimated_downtime: Ожидаемое время восстановления
        """
        super().__init__(message, "SYSTEM_UNAVAILABLE",
                         {'estimated_downtime': estimated_downtime})
        self.estimated_downtime = estimated_downtime
