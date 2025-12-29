"""
Класс клиента системы аренды.

Этот модуль содержит реализацию клиента - основного пользователя
системы аренды предметов.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Any, Set

from .base_person import BasePerson
from src.utils import constants as const


@dataclass
class Customer(BasePerson):
    """
    Класс представляющий клиента системы аренды.

    Клиент - это пользователь, который арендует предметы в системе.
    Класс содержит информацию о клиенте, его истории аренд,
    лояльности и платежной информации.

    Attributes:
        loyalty_points: Количество баллов лояльности
        total_spent: Общая сумма потраченная на аренду
        rental_count: Количество совершенных аренд
        average_rating: Средний рейтинг клиента
        preferred_categories: Предпочитаемые категории предметов
        payment_methods: Сохраненные методы оплаты
        is_vip: VIP статус клиента
        referral_code: Реферальный код для приглашения друзей
        referred_by: Кто пригласил этого клиента
        last_rental_date: Дата последней аренды
        membership_level: Уровень членства
    """

    loyalty_points: int = 0
    total_spent: Decimal = Decimal("0.00")
    rental_count: int = 0
    average_rating: float = 0.0
    preferred_categories: Set[str] = field(default_factory=set)
    payment_methods: List[str] = field(default_factory=list)
    is_vip: bool = False
    referral_code: Optional[str] = None
    referred_by: Optional[str] = None
    last_rental_date: Optional[datetime] = None
    membership_level: str = "standard"

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        if self.loyalty_points < 0:
            raise ValueError("Баллы лояльности не могут быть отрицательными")
        if self.total_spent < 0:
            raise ValueError("Общая сумма не может быть отрицательной")
        if self.rental_count < 0:
            raise ValueError("Количество аренд не может быть отрицательным")
        if not (0.0 <= self.average_rating <= 5.0):
            raise ValueError("Рейтинг должен быть от 0.0 до 5.0")

    def validate(self) -> bool:
        """
        Валидирует данные клиента.

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

        if self.loyalty_points < 0:
            errors.append("Баллы лояльности не могут быть отрицательными")

        if self.total_spent < 0:
            errors.append("Общая сумма не может быть отрицательной")

        if self.rental_count < 0:
            errors.append("Количество аренд не может быть отрицательным")

        if not (0.0 <= self.average_rating <= 5.0):
            errors.append("Рейтинг должен быть от 0.0 до 5.0")

        if self.membership_level not in ['standard', 'premium', 'vip']:
            errors.append("Некорректный уровень членства")

        if self.last_rental_date and self.last_rental_date > datetime.now():
            errors.append("Дата последней аренды не может быть в будущем")

        return errors

    def add_rental(self, amount: Decimal, rating: Optional[float] = None) -> None:
        """
        Добавляет информацию об аренде.

        Args:
            amount: Сумма аренды
            rating: Рейтинг аренды (опционально)
        """
        if amount < 0:
            raise ValueError("Сумма аренды не может быть отрицательной")

        self.total_spent += amount
        self.rental_count += 1
        self.last_rental_date = datetime.now()

        # Начисляем баллы лояльности
        points_earned = int(amount * const.LOYALTY_POINTS_PER_DOLLAR)
        self.loyalty_points += points_earned

        # Обновляем средний рейтинг
        if rating is not None:
            if not (0.0 <= rating <= 5.0):
                raise ValueError("Рейтинг должен быть от 0.0 до 5.0")
            # Простая формула обновления среднего рейтинга
            total_rating_points = self.average_rating * (self.rental_count - 1)
            self.average_rating = (total_rating_points + rating) / self.rental_count

        # Проверяем VIP статус
        self._update_vip_status()

        self.update_timestamp()

    def redeem_loyalty_points(self, points_to_redeem: int) -> Decimal:
        """
        Использует баллы лояльности для получения скидки.

        Args:
            points_to_redeem: Количество баллов для использования

        Returns:
            Decimal: Сумма скидки в долларах

        Raises:
            ValueError: Если недостаточно баллов
        """
        if points_to_redeem < const.MINIMUM_POINTS_FOR_REDEMPTION:
            raise ValueError(f"Минимальное количество баллов для использования: {const.MINIMUM_POINTS_FOR_REDEMPTION}")

        if points_to_redeem > self.loyalty_points:
            raise ValueError("Недостаточно баллов лояльности")

        # Конвертируем баллы в скидку
        discount_amount = Decimal(str(points_to_redeem)) * const.LOYALTY_POINTS_REDEMPTION_RATE

        self.loyalty_points -= points_to_redeem
        self.update_timestamp()

        return discount_amount

    def add_preferred_category(self, category: str) -> None:
        """
        Добавляет предпочтительную категорию.

        Args:
            category: Название категории
        """
        if category and category.strip():
            self.preferred_categories.add(category.strip())
            self.update_timestamp()

    def remove_preferred_category(self, category: str) -> None:
        """
        Удаляет предпочтительную категорию.

        Args:
            category: Название категории
        """
        if category in self.preferred_categories:
            self.preferred_categories.remove(category)
            self.update_timestamp()

    def add_payment_method(self, payment_method_id: str) -> None:
        """
        Добавляет метод оплаты.

        Args:
            payment_method_id: ID метода оплаты
        """
        if payment_method_id not in self.payment_methods:
            self.payment_methods.append(payment_method_id)
            self.update_timestamp()

    def remove_payment_method(self, payment_method_id: str) -> None:
        """
        Удаляет метод оплаты.

        Args:
            payment_method_id: ID метода оплаты
        """
        if payment_method_id in self.payment_methods:
            self.payment_methods.remove(payment_method_id)
            self.update_timestamp()

    def generate_referral_code(self) -> str:
        """
        Генерирует реферальный код для клиента.

        Returns:
            str: Реферальный код
        """
        if not self.referral_code:
            # Простая генерация кода на основе ID и имени
            code_base = f"{self.entity_id[:8]}_{self.first_name[:3].upper()}"
            self.referral_code = code_base
            self.update_timestamp()
        return self.referral_code

    def apply_referral_bonus(self, referrer: 'Customer') -> None:
        """
        Применяет бонус за приглашение друга.

        Args:
            referrer: Клиент, который пригласил этого клиента
        """
        # Начисляем бонусные баллы обоим клиентам
        referral_bonus = 100  # баллы за приглашение

        self.loyalty_points += referral_bonus
        referrer.loyalty_points += referral_bonus

        self.referred_by = referrer.entity_id
        self.update_timestamp()
        referrer.update_timestamp()

    def _update_vip_status(self) -> None:
        """Обновляет VIP статус на основе активности клиента."""
        # Логика определения VIP статуса
        if (self.total_spent >= Decimal("1000.00") or
            self.rental_count >= 50 or
            self.membership_level == 'vip'):
            self.is_vip = True
        else:
            self.is_vip = False

    def upgrade_membership(self, new_level: str) -> None:
        """
        Обновляет уровень членства.

        Args:
            new_level: Новый уровень членства
        """
        if new_level not in ['standard', 'premium', 'vip']:
            raise ValueError("Некорректный уровень членства")

        self.membership_level = new_level
        self._update_vip_status()
        self.update_timestamp()

    def get_membership_discount(self) -> Decimal:
        """
        Получает скидку по уровню членства.

        Returns:
            Decimal: Процент скидки
        """
        discounts = {
            'standard': Decimal("0.00"),
            'premium': Decimal("0.05"),  # 5% скидка
            'vip': Decimal("0.10")  # 10% скидка
        }
        return discounts.get(self.membership_level, Decimal("0.00"))

    def can_redeem_points(self, points: int) -> bool:
        """
        Проверяет можно ли использовать указанное количество баллов.

        Args:
            points: Количество баллов

        Returns:
            bool: True если можно использовать
        """
        return (points >= const.MINIMUM_POINTS_FOR_REDEMPTION and
                points <= self.loyalty_points)

    def get_customer_summary(self) -> Dict[str, Any]:
        """
        Получает сводную информацию о клиенте.

        Returns:
            Dict[str, Any]: Сводная информация
        """
        return {
            'customer_id': self.entity_id,
            'full_name': self.full_name,
            'email': self.email,
            'membership_level': self.membership_level,
            'is_vip': self.is_vip,
            'loyalty_points': self.loyalty_points,
            'total_spent': float(self.total_spent),
            'rental_count': self.rental_count,
            'average_rating': round(self.average_rating, 2),
            'preferred_categories': list(self.preferred_categories),
            'last_rental_date': self.last_rental_date.isoformat() if self.last_rental_date else None
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует клиента в словарь для сериализации.

        Returns:
            Dict[str, Any]: Словарь с данными клиента
        """
        data = super().to_dict()
        data.update({
            'loyalty_points': self.loyalty_points,
            'total_spent': str(self.total_spent),
            'rental_count': self.rental_count,
            'average_rating': self.average_rating,
            'preferred_categories': list(self.preferred_categories),
            'payment_methods': self.payment_methods,
            'is_vip': self.is_vip,
            'referral_code': self.referral_code,
            'referred_by': self.referred_by,
            'last_rental_date': self.last_rental_date.isoformat() if self.last_rental_date else None,
            'membership_level': self.membership_level
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Customer':
        """
        Создает клиента из словаря.

        Args:
            data: Словарь с данными клиента

        Returns:
            Customer: Новый экземпляр клиента
        """
        # Преобразуем строковые значения обратно в соответствующие типы
        if 'total_spent' in data:
            data['total_spent'] = Decimal(data['total_spent'])
        if 'preferred_categories' in data:
            data['preferred_categories'] = set(data['preferred_categories'])
        if 'last_rental_date' in data and data['last_rental_date']:
            data['last_rental_date'] = datetime.fromisoformat(data['last_rental_date'])

        return cls(**data)
