"""
Перечисление для статуса сотрудника.
"""

from enum import Enum


class EmployeeStatus(Enum):
    """
    Статус сотрудника.

    Определяет текущее состояние сотрудника в системе.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"
    ON_LEAVE = "on_leave"
