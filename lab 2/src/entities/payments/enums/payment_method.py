"""
Перечисление для методов оплаты.
"""

from enum import Enum


class PaymentMethod(Enum):
    """
    Методы оплаты.

    Определяет доступные способы оплаты.
    """

    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    WALLET = "wallet"
    BANK_TRANSFER = "bank_transfer"
