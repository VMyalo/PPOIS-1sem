"""
Сервисы системы.

Этот модуль экспортирует все сервисы системы.
"""

from .auth_service import AuthService
from .rental_service import RentalService

__all__ = [
    'AuthService',
    'RentalService'
]
