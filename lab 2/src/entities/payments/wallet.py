"""
Класс оплаты электронным кошельком.

Этот модуль содержит реализацию оплаты через электронный кошелек.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from .base_payment import BasePayment, PaymentMethod


@dataclass
class WalletPayment(BasePayment):
    """
    Класс представляющий оплату электронным кошельком.

    Attributes:
        wallet_id: ID кошелька
        wallet_provider: Провайдер кошелька
        user_wallet_balance: Баланс кошелька пользователя
        transaction_fee: Комиссия транзакции
    """

    wallet_id: Optional[str] = None
    wallet_provider: str = "generic"
    user_wallet_balance: float = 0.0
    transaction_fee: float = 0.0

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.payment_method = PaymentMethod.WALLET

    def check_sufficient_balance(self) -> bool:
        """
        Проверяет достаточность баланса.

        Returns:
            bool: True если баланс достаточный
        """
        return self.user_wallet_balance >= float(self.amount) + self.transaction_fee

    def deduct_from_wallet(self) -> bool:
        """
        Списывает средства с кошелька.

        Returns:
            bool: True если списание успешно
        """
        if not self.check_sufficient_balance():
            return False

        total_amount = float(self.amount) + self.transaction_fee
        self.user_wallet_balance -= total_amount
        return True

    def get_wallet_details(self) -> Dict[str, Any]:
        """
        Получает детали кошелька.

        Returns:
            Dict[str, Any]: Детали кошелька
        """
        return {
            'wallet_id': self.wallet_id,
            'wallet_provider': self.wallet_provider,
            'user_wallet_balance': self.user_wallet_balance,
            'transaction_fee': self.transaction_fee
        }
