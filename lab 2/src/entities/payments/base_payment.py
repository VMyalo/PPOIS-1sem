"""
Базовый класс для платежей.

Этот модуль содержит базовую реализацию для различных
методов оплаты в системе аренды.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Any

from src.core.base import BaseEntity
from src.core.payable import Payable
from .enums.payment_status import PaymentStatus
from .enums.payment_method import PaymentMethod
from src.utils import constants as const


@dataclass
class BasePayment(BaseEntity, Payable):
    """
    Базовый класс для всех платежей.

    Этот класс предоставляет общую функциональность для различных
    методов оплаты: наличные, карты, электронные кошельки и т.д.

    Attributes:
        amount: Сумма платежа
        currency: Валюта
        payment_method: Метод оплаты
        status: Статус платежа
        transaction_id: ID транзакции
        payment_date: Дата платежа
        description: Описание платежа
        customer_id: ID клиента
        rental_id: ID аренды
        fees: Сборы и комиссии
        refund_amount: Сумма возврата
        refund_reason: Причина возврата
    """

    amount: Decimal = Decimal("0.00")
    currency: str = const.DEFAULT_CURRENCY
    payment_method: PaymentMethod = PaymentMethod.CASH
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_id: Optional[str] = None
    payment_date: Optional[datetime] = None
    description: Optional[str] = None
    customer_id: Optional[str] = None
    rental_id: Optional[str] = None
    fees: Decimal = Decimal("0.00")
    refund_amount: Decimal = Decimal("0.00")
    refund_reason: Optional[str] = None

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        if self.amount < 0:
            raise ValueError("Сумма платежа не может быть отрицательной")

    def validate(self) -> bool:
        """
        Валидирует платеж.

        Returns:
            bool: True если валидация успешна
        """
        errors = self.get_validation_errors()
        return len(errors) == 0

    def get_validation_errors(self) -> List[str]:
        """
        Получает список ошибок валидации.

        Returns:
            List[str]: Список ошибок валидации
        """
        errors = super().get_validation_errors()

        if self.amount < const.MINIMUM_PAYMENT_AMOUNT:
            errors.append(f"Сумма платежа должна быть не менее {const.MINIMUM_PAYMENT_AMOUNT}")

        if self.amount > const.MAXIMUM_PAYMENT_AMOUNT:
            errors.append(f"Сумма платежа не может превышать {const.MAXIMUM_PAYMENT_AMOUNT}")

        if self.fees < 0:
            errors.append("Сборы не могут быть отрицательными")

        if self.refund_amount < 0:
            errors.append("Сумма возврата не может быть отрицательной")

        if self.refund_amount > self.amount:
            errors.append("Сумма возврата не может превышать сумму платежа")

        return errors

    def process_payment(self, amount: Decimal, payment_method: str) -> bool:
        """
        Обрабатывает платеж.

        Args:
            amount: Сумма платежа
            payment_method: Метод оплаты

        Returns:
            bool: True если платеж успешен
        """
        if amount != self.amount:
            return False

        self.status = PaymentStatus.PROCESSING
        self.payment_date = datetime.now()
        self.transaction_id = f"TXN_{self.entity_id}_{int(datetime.now().timestamp())}"
        self.update_timestamp()

        # Имитация обработки платежа
        self.status = PaymentStatus.COMPLETED
        return True

    def get_payment_status(self) -> str:
        """
        Получает статус оплаты.

        Returns:
            str: Статус оплаты
        """
        return self.status.value

    def calculate_total_amount(self) -> Decimal:
        """
        Рассчитывает общую сумму с учетом сборов.

        Returns:
            Decimal: Общая сумма
        """
        return self.amount + self.fees

    def refund_payment(self, amount: Decimal, reason: str) -> bool:
        """
        Возвращает платеж.

        Args:
            amount: Сумма возврата
            reason: Причина возврата

        Returns:
            bool: True если возврат успешен
        """
        if self.status != PaymentStatus.COMPLETED:
            return False

        if amount > self.amount - self.refund_amount:
            return False

        self.refund_amount += amount
        self.refund_reason = reason
        self.status = PaymentStatus.REFUNDED if self.refund_amount == self.amount else PaymentStatus.COMPLETED
        self.update_timestamp()

        return True

    def cancel_payment(self) -> None:
        """Отменяет платеж."""
        if self.status in [PaymentStatus.PENDING, PaymentStatus.PROCESSING]:
            self.status = PaymentStatus.CANCELLED
            self.update_timestamp()

    def get_payment_summary(self) -> Dict[str, Any]:
        """
        Получает сводку платежа.

        Returns:
            Dict[str, Any]: Сводка платежа
        """
        return {
            'payment_id': self.entity_id,
            'amount': float(self.amount),
            'currency': self.currency,
            'method': self.payment_method.value,
            'status': self.status.value,
            'transaction_id': self.transaction_id,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'fees': float(self.fees),
            'total': float(self.calculate_total_amount()),
            'refund_amount': float(self.refund_amount)
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует платеж в словарь для сериализации.

        Returns:
            Dict[str, Any]: Словарь с данными платежа
        """
        data = super().to_dict()
        data.update({
            'amount': str(self.amount),
            'currency': self.currency,
            'payment_method': self.payment_method.value,
            'status': self.status.value,
            'transaction_id': self.transaction_id,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'description': self.description,
            'customer_id': self.customer_id,
            'rental_id': self.rental_id,
            'fees': str(self.fees),
            'refund_amount': str(self.refund_amount),
            'refund_reason': self.refund_reason
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BasePayment':
        """
        Создает платеж из словаря.

        Args:
            data: Словарь с данными платежа

        Returns:
            BasePayment: Новый экземпляр платежа
        """
        # Преобразуем строковые значения обратно в соответствующие типы
        if 'amount' in data:
            data['amount'] = Decimal(data['amount'])
        if 'fees' in data:
            data['fees'] = Decimal(data['fees'])
        if 'refund_amount' in data:
            data['refund_amount'] = Decimal(data['refund_amount'])
        if 'payment_date' in data and data['payment_date']:
            data['payment_date'] = datetime.fromisoformat(data['payment_date'])
        if 'payment_method' in data:
            data['payment_method'] = PaymentMethod(data['payment_method'])
        if 'status' in data:
            data['status'] = PaymentStatus(data['status'])

        return cls(**data)
