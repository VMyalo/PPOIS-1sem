"""
Перечисление для статусов платежа.
"""

from enum import Enum


class PaymentStatus(Enum):
    """
    Статусы платежа.

    Определяет состояния платежной транзакции.
    """

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
