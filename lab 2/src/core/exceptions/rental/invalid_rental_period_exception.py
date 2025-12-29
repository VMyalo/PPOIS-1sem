"""
Исключение, возникающее при недействительном периоде аренды.
"""

from datetime import datetime
from typing import Optional

from ..base_exception import RentalSystemException


class InvalidRentalPeriodException(RentalSystemException):
    """
    Исключение, возникающее при недействительном периоде аренды.

    Выбрасывается когда указанный период аренды не соответствует
    правилам системы (слишком короткий, слишком длинный и т.д.).
    """

    def __init__(self, message: str = "Недействительный период аренды",
                 start_date: Optional[datetime] = None,
                 end_date: Optional[datetime] = None,
                 min_duration_hours: Optional[int] = None,
                 max_duration_days: Optional[int] = None):
        """
        Инициализирует исключение недействительного периода аренды.

        Args:
            message: Сообщение об ошибке
            start_date: Дата начала аренды
            end_date: Дата окончания аренды
            min_duration_hours: Минимальная длительность в часах
            max_duration_days: Максимальная длительность в днях
        """
        super().__init__(message, "INVALID_RENTAL_PERIOD",
                         {'start_date': str(start_date) if start_date else None,
                          'end_date': str(end_date) if end_date else None,
                          'min_duration_hours': min_duration_hours,
                          'max_duration_days': max_duration_days})
        self.start_date = start_date
        self.end_date = end_date
        self.min_duration_hours = min_duration_hours
        self.max_duration_days = max_duration_days
