"""
Люди в системе аренды.

Этот модуль экспортирует все классы, связанные с людьми:
клиентами, сотрудниками, менеджерами и администраторами.
"""

from .base_person import BasePerson, Gender, ContactPreference
from .customer import Customer
from .employee.base_employee import BaseEmployee, EmployeeStatus, Department
from .employee.manager import Manager
from .employee.administrator import Administrator

__all__ = [
    # Базовые классы и перечисления
    'BasePerson',
    'Gender',
    'ContactPreference',

    # Клиент
    'Customer',

    # Иерархия сотрудников
    'BaseEmployee',
    'EmployeeStatus',
    'Department',
    'Manager',
    'Administrator'
]
