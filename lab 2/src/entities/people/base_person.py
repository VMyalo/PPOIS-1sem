"""
Базовый класс для людей в системе аренды.

Этот модуль содержит базовую реализацию для всех типов людей:
клиентов, сотрудников, менеджеров, администраторов.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any

from src.core.base import BaseEntity
from src.entities.people.enums.gender import Gender
from src.entities.people.enums.contact_preference import ContactPreference
from src.utils import constants as const


@dataclass
class BasePerson(BaseEntity):
    """
    Базовый класс для всех людей в системе.

    Этот класс предоставляет общую функциональность для всех типов пользователей:
    клиентов, сотрудников и администраторов системы аренды.

    Attributes:
        first_name: Имя
        last_name: Фамилия
        email: Email адрес
        phone: Номер телефона
        date_of_birth: Дата рождения
        gender: Пол
        address: Адрес проживания
        contact_preference: Предпочтительный способ связи
        is_active: Активен ли аккаунт
        last_login: Последний вход в систему
        profile_image_url: URL аватара профиля
    """

    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Gender = Gender.OTHER
    address: Optional[str] = None
    contact_preference: ContactPreference = ContactPreference.EMAIL
    is_active: bool = True
    last_login: Optional[datetime] = None
    profile_image_url: Optional[str] = None

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        if not self.first_name or not self.last_name:
            raise ValueError("Имя и фамилия обязательны")
        if not self.email:
            raise ValueError("Email обязателен")

    @property
    def full_name(self) -> str:
        """
        Полное имя человека.

        Returns:
            str: Полное имя в формате "Фамилия Имя"
        """
        return f"{self.last_name} {self.first_name}"

    @property
    def age(self) -> Optional[int]:
        """
        Возраст человека в годах.

        Returns:
            Optional[int]: Возраст или None если дата рождения не указана
        """
        if not self.date_of_birth:
            return None
        today = datetime.now()
        age = today.year - self.date_of_birth.year
        # Корректировка если день рождения еще не наступил в этом году
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

    def validate(self) -> bool:
        """
        Валидирует данные человека.

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

        if not self.first_name or len(self.first_name.strip()) == 0:
            errors.append("Имя не может быть пустым")

        if not self.last_name or len(self.last_name.strip()) == 0:
            errors.append("Фамилия не может быть пустой")

        if len(self.first_name) > const.MAXIMUM_STRING_LENGTH:
            errors.append(f"Имя не может превышать {const.MAXIMUM_STRING_LENGTH} символов")

        if len(self.last_name) > const.MAXIMUM_STRING_LENGTH:
            errors.append(f"Фамилия не может превышать {const.MAXIMUM_STRING_LENGTH} символов")

        if not self.email or len(self.email.strip()) == 0:
            errors.append("Email не может быть пустым")

        if self.email and len(self.email) > const.MAXIMUM_STRING_LENGTH:
            errors.append(f"Email не может превышать {const.MAXIMUM_STRING_LENGTH} символов")

        # Простая валидация email
        if self.email and ('@' not in self.email or '.' not in self.email):
            errors.append("Некорректный формат email")

        if self.phone and len(self.phone) > const.MAXIMUM_STRING_LENGTH:
            errors.append(f"Телефон не может превышать {const.MAXIMUM_STRING_LENGTH} символов")

        if self.address and len(self.address) > const.MAXIMUM_TEXT_LENGTH:
            errors.append(f"Адрес не может превышать {const.MAXIMUM_TEXT_LENGTH} символов")

        if self.date_of_birth and self.date_of_birth > datetime.now():
            errors.append("Дата рождения не может быть в будущем")

        if self.last_login and self.last_login > datetime.now():
            errors.append("Дата последнего входа не может быть в будущем")

        return errors

    def update_last_login(self) -> None:
        """Обновляет время последнего входа в систему."""
        self.last_login = datetime.now()
        self.update_timestamp()

    def deactivate_account(self) -> None:
        """Деактивирует аккаунт пользователя."""
        self.is_active = False
        self.update_timestamp()

    def activate_account(self) -> None:
        """Активирует аккаунт пользователя."""
        self.is_active = True
        self.update_timestamp()

    def update_contact_info(self, email: Optional[str] = None,
                          phone: Optional[str] = None,
                          address: Optional[str] = None) -> None:
        """
        Обновляет контактную информацию.

        Args:
            email: Новый email
            phone: Новый телефон
            address: Новый адрес
        """
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if address is not None:
            self.address = address
        self.update_timestamp()

    def update_personal_info(self, first_name: Optional[str] = None,
                           last_name: Optional[str] = None,
                           date_of_birth: Optional[datetime] = None,
                           gender: Optional[Gender] = None) -> None:
        """
        Обновляет личную информацию.

        Args:
            first_name: Новое имя
            last_name: Новая фамилия
            date_of_birth: Новая дата рождения
            gender: Новый пол
        """
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if date_of_birth is not None:
            self.date_of_birth = date_of_birth
        if gender is not None:
            self.gender = gender
        self.update_timestamp()

    def set_contact_preference(self, preference: ContactPreference) -> None:
        """
        Устанавливает предпочтительный способ связи.

        Args:
            preference: Предпочтение по контактам
        """
        self.contact_preference = preference
        self.update_timestamp()

    def can_receive_notifications(self) -> bool:
        """
        Проверяет может ли пользователь получать уведомления.

        Returns:
            bool: True если может получать уведомления
        """
        return self.is_active and bool(self.email or self.phone)

    def get_preferred_contact_method(self) -> str:
        """
        Получает предпочтительный метод связи.

        Returns:
            str: Предпочтительный метод связи
        """
        return self.contact_preference.value

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует человека в словарь для сериализации.

        Returns:
            Dict[str, Any]: Словарь с данными человека
        """
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender.value,
            'address': self.address,
            'contact_preference': self.contact_preference.value,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'profile_image_url': self.profile_image_url
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BasePerson':
        """
        Создает человека из словаря.

        Args:
            data: Словарь с данными человека

        Returns:
            BasePerson: Новый экземпляр человека
        """
        # Преобразуем строковые значения обратно в соответствующие типы
        if 'date_of_birth' in data and data['date_of_birth']:
            data['date_of_birth'] = datetime.fromisoformat(data['date_of_birth'])
        if 'last_login' in data and data['last_login']:
            data['last_login'] = datetime.fromisoformat(data['last_login'])
        if 'gender' in data:
            data['gender'] = Gender(data['gender'])
        if 'contact_preference' in data:
            data['contact_preference'] = ContactPreference(data['contact_preference'])

        return cls(**data)
