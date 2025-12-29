"""
Сотрудники системы аренды.

Этот модуль экспортирует все классы сотрудников:
базовых сотрудников, менеджеров и администраторов.
"""

from .base_employee import BaseEmployee, EmployeeStatus, Department
from .manager import Manager
from .administrator import Administrator

__all__ = [
    'BaseEmployee',
    'EmployeeStatus',
    'Department',
    'Manager',
    'Administrator'
]
