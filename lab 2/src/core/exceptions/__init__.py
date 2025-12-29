"""
Исключения системы аренды.

Этот модуль экспортирует все исключения системы для удобного импорта.
"""

from .base_exception import RentalSystemException
from .auth.invalid_credentials_exception import InvalidCredentialsException
from .auth.account_locked_exception import AccountLockedException
from .auth.insufficient_permissions_exception import InsufficientPermissionsException
from .inventory.item_not_available_exception import ItemNotAvailableException
from .inventory.item_already_rented_exception import ItemAlreadyRentedException
from .inventory.insufficient_stock_exception import InsufficientStockException
from .payment.payment_failed_exception import PaymentFailedException
from .payment.insufficient_funds_exception import InsufficientFundsException
from .payment.invalid_card_exception import InvalidCardException
from .rental.rental_not_found_exception import RentalNotFoundException
from .rental.invalid_rental_period_exception import InvalidRentalPeriodException
from .rental.overdue_return_exception import OverdueReturnException
from .other.validation_exception import ValidationException
from .other.business_rule_violation_exception import BusinessRuleViolationException
from .other.system_unavailable_exception import SystemUnavailableException

__all__ = [
    # Базовое исключение
    'RentalSystemException',

    # Исключения аутентификации
    'InvalidCredentialsException',
    'AccountLockedException',
    'InsufficientPermissionsException',

    # Исключения инвентаря
    'ItemNotAvailableException',
    'ItemAlreadyRentedException',
    'InsufficientStockException',

    # Исключения платежей
    'PaymentFailedException',
    'InsufficientFundsException',
    'InvalidCardException',

    # Исключения аренды
    'RentalNotFoundException',
    'InvalidRentalPeriodException',
    'OverdueReturnException',

    # Прочие исключения
    'ValidationException',
    'BusinessRuleViolationException',
    'SystemUnavailableException'
]
