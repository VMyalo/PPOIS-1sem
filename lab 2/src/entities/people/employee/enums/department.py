"""
Перечисление для отделов сотрудников.
"""

from enum import Enum


class Department(Enum):
    """
    Отдел сотрудника.

    Определяет отделы компании, в которых работают сотрудники.
    """

    MANAGEMENT = "management"
    SALES = "sales"
    CUSTOMER_SERVICE = "customer_service"
    MAINTENANCE = "maintenance"
    LOGISTICS = "logistics"
    ADMINISTRATION = "administration"
