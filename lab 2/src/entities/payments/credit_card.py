"""
Класс оплаты кредитной картой.

Этот модуль содержит реализацию оплаты кредитной картой.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from .base_payment import BasePayment, PaymentMethod


@dataclass
class CreditCardPayment(BasePayment):
    """
    Класс представляющий оплату кредитной картой.

    Attributes:
        card_number_masked: Маскированный номер карты
        card_holder_name: Имя владельца карты
        expiry_month: Месяц истечения срока
        expiry_year: Год истечения срока
        authorization_code: Код авторизации
        card_brand: Бренд карты
    """

    card_number_masked: Optional[str] = None
    card_holder_name: Optional[str] = None
    expiry_month: Optional[int] = None
    expiry_year: Optional[int] = None
    authorization_code: Optional[str] = None
    card_brand: Optional[str] = None

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.payment_method = PaymentMethod.CREDIT_CARD

    def mask_card_number(self, full_card_number: str) -> str:
        """
        Маскирует номер карты.

        Args:
            full_card_number: Полный номер карты

        Returns:
            str: Маскированный номер карты
        """
        if len(full_card_number) >= 4:
            return f"****-****-****-{full_card_number[-4:]}"
        return "****-****-****-****"

    def validate_card(self) -> bool:
        """
        Валидирует данные карты.

        Returns:
            bool: True если данные валидны
        """
        # Простая валидация
        return (self.expiry_month and 1 <= self.expiry_month <= 12 and
                self.expiry_year and self.expiry_year >= 2024)

    def get_card_details(self) -> Dict[str, Any]:
        """
        Получает детали карты.

        Returns:
            Dict[str, Any]: Детали карты
        """
        return {
            'card_number_masked': self.card_number_masked,
            'card_holder_name': self.card_holder_name,
            'expiry_month': self.expiry_month,
            'expiry_year': self.expiry_year,
            'card_brand': self.card_brand
        }
