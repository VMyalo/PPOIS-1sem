"""
Сервис аутентификации.

Этот модуль содержит логику аутентификации и авторизации пользователей.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from hashlib import sha256

from ..core.base import BaseService
from ..entities.people import Customer, BaseEmployee, Manager, Administrator
from ..core.exceptions import (
    InvalidCredentialsException,
    AccountLockedException,
    InsufficientPermissionsException
)
from ..utils import constants as const


@dataclass
class AuthService(BaseService):
    """
    Сервис для аутентификации и авторизации пользователей.

    Attributes:
        user_repository: Репозиторий пользователей
        session_timeout_minutes: Таймаут сессии в минутах
        max_login_attempts: Максимальное количество попыток входа
    """

    user_repository: Optional[Any] = None
    session_timeout_minutes: int = 60
    max_login_attempts: int = const.MAXIMUM_LOGIN_ATTEMPTS

    def authenticate_user(self, email: str, password: str) -> Tuple[bool, Optional[Any], str]:
        """
        Аутентифицирует пользователя.

        Args:
            email: Email пользователя
            password: Пароль пользователя

        Returns:
            Tuple[bool, Optional[Any], str]: (успех, пользователь, сообщение)
        """
        try:
            # Поиск пользователя по email
            user = self._find_user_by_email(email)
            if not user:
                raise InvalidCredentialsException(f"Пользователь с email {email} не найден")

            # Проверка блокировки аккаунта
            if self._is_account_locked(user):
                raise AccountLockedException(
                    f"Аккаунт заблокирован до {self._get_lockout_end_time(user)}",
                    const.ACCOUNT_LOCKOUT_DURATION_MINUTES
                )

            # Проверка пароля
            if not self._verify_password(password, user):
                self._increment_failed_attempts(user)
                raise InvalidCredentialsException("Неверный пароль")

            # Сброс счетчика неудачных попыток
            self._reset_failed_attempts(user)

            # Обновление времени последнего входа
            user.update_last_login()

            return True, user, "Аутентификация успешна"

        except InvalidCredentialsException as e:
            return False, None, str(e)
        except AccountLockedException as e:
            return False, None, str(e)
        except Exception as e:
            return False, None, f"Ошибка аутентификации: {str(e)}"

    def authorize_action(self, user: Any, required_role: str, action: str) -> bool:
        """
        Проверяет права пользователя на выполнение действия.

        Args:
            user: Пользователь
            required_role: Требуемая роль
            action: Действие

        Returns:
            bool: True если авторизовано

        Raises:
            InsufficientPermissionsException: Если прав недостаточно
        """
        user_role = self._get_user_role(user)

        if not self._has_required_role(user_role, required_role):
            raise InsufficientPermissionsException(
                f"Недостаточно прав для выполнения действия '{action}'",
                required_role,
                user_role
            )

        return True

    def create_session(self, user: Any) -> str:
        """
        Создает сессию для пользователя.

        Args:
            user: Пользователь

        Returns:
            str: ID сессии
        """
        session_id = self._generate_session_id(user)
        # В реальном приложении сессия сохранялась бы в хранилище
        return session_id

    def validate_session(self, session_id: str) -> Optional[Any]:
        """
        Валидирует сессию.

        Args:
            session_id: ID сессии

        Returns:
            Optional[Any]: Пользователь если сессия валидна
        """
        # В реальном приложении проверка в хранилище сессий
        return None  # Заглушка

    def logout_user(self, user: Any) -> None:
        """
        Выход пользователя из системы.

        Args:
            user: Пользователь
        """
        # В реальном приложении удаление сессии
        pass

    def register_customer(self, customer_data: Dict[str, Any]) -> Customer:
        """
        Регистрирует нового клиента.

        Args:
            customer_data: Данные клиента

        Returns:
            Customer: Созданный клиент
        """
        # Валидация данных
        self._validate_registration_data(customer_data)

        # Создание клиента
        customer = Customer(**customer_data)
        customer.generate_id()

        # Хэширование пароля
        if 'password' in customer_data:
            customer.password_hash = self._hash_password(customer_data['password'])

        return customer

    def change_password(self, user: Any, old_password: str, new_password: str) -> bool:
        """
        Изменяет пароль пользователя.

        Args:
            user: Пользователь
            old_password: Старый пароль
            new_password: Новый пароль

        Returns:
            bool: True если пароль изменен
        """
        if not self._verify_password(old_password, user):
            raise InvalidCredentialsException("Неверный старый пароль")

        if not self._validate_password_strength(new_password):
            raise ValueError("Пароль не соответствует требованиям безопасности")

        user.password_hash = self._hash_password(new_password)
        return True

    def reset_password(self, email: str) -> str:
        """
        Сбрасывает пароль пользователя.

        Args:
            email: Email пользователя

        Returns:
            str: Токен сброса пароля
        """
        user = self._find_user_by_email(email)
        if not user:
            raise ValueError("Пользователь не найден")

        reset_token = self._generate_reset_token()
        # В реальном приложении токен сохранялся бы в хранилище
        return reset_token

    def _find_user_by_email(self, email: str) -> Optional[Any]:
        """
        Находит пользователя по email.

        Args:
            email: Email пользователя

        Returns:
            Optional[Any]: Пользователь или None
        """
        # Заглушка - в реальном приложении поиск в репозитории
        return None

    def _verify_password(self, password: str, user: Any) -> bool:
        """
        Проверяет пароль пользователя.

        Args:
            password: Пароль для проверки
            user: Пользователь

        Returns:
            bool: True если пароль верный
        """
        if not hasattr(user, 'password_hash'):
            return False

        hashed_password = self._hash_password(password)
        return hashed_password == user.password_hash

    def _hash_password(self, password: str) -> str:
        """
        Хэширует пароль.

        Args:
            password: Пароль

        Returns:
            str: Хэш пароля
        """
        return sha256(password.encode()).hexdigest()

    def _is_account_locked(self, user: Any) -> bool:
        """
        Проверяет заблокирован ли аккаунт.

        Args:
            user: Пользователь

        Returns:
            bool: True если заблокирован
        """
        if not hasattr(user, 'failed_login_attempts'):
            return False

        return user.failed_login_attempts >= self.max_login_attempts

    def _get_lockout_end_time(self, user: Any) -> datetime:
        """
        Получает время окончания блокировки.

        Args:
            user: Пользователь

        Returns:
            datetime: Время окончания блокировки
        """
        if not hasattr(user, 'last_failed_login'):
            return datetime.now()

        return user.last_failed_login + timedelta(minutes=const.ACCOUNT_LOCKOUT_DURATION_MINUTES)

    def _increment_failed_attempts(self, user: Any) -> None:
        """
        Увеличивает счетчик неудачных попыток входа.

        Args:
            user: Пользователь
        """
        if not hasattr(user, 'failed_login_attempts'):
            user.failed_login_attempts = 0
        if not hasattr(user, 'last_failed_login'):
            user.last_failed_login = datetime.now()

        user.failed_login_attempts += 1
        user.last_failed_login = datetime.now()

    def _reset_failed_attempts(self, user: Any) -> None:
        """
        Сбрасывает счетчик неудачных попыток входа.

        Args:
            user: Пользователь
        """
        user.failed_login_attempts = 0
        user.last_failed_login = None

    def _get_user_role(self, user: Any) -> str:
        """
        Получает роль пользователя.

        Args:
            user: Пользователь

        Returns:
            str: Роль пользователя
        """
        if isinstance(user, Administrator):
            return const.ROLE_ADMINISTRATOR
        elif isinstance(user, Manager):
            return const.ROLE_MANAGER
        elif isinstance(user, BaseEmployee):
            return const.ROLE_EMPLOYEE
        elif isinstance(user, Customer):
            return const.ROLE_CUSTOMER
        else:
            return "unknown"

    def _has_required_role(self, user_role: str, required_role: str) -> bool:
        """
        Проверяет имеет ли пользователь требуемую роль.

        Args:
            user_role: Роль пользователя
            required_role: Требуемая роль

        Returns:
            bool: True если роль подходит
        """
        role_hierarchy = {
            const.ROLE_ADMINISTRATOR: 4,
            const.ROLE_MANAGER: 3,
            const.ROLE_EMPLOYEE: 2,
            const.ROLE_CUSTOMER: 1
        }

        user_level = role_hierarchy.get(user_role, 0)
        required_level = role_hierarchy.get(required_role, 0)

        return user_level >= required_level

    def _validate_registration_data(self, data: Dict[str, Any]) -> None:
        """
        Валидирует данные регистрации.

        Args:
            data: Данные для валидации

        Raises:
            ValueError: Если данные невалидны
        """
        required_fields = ['first_name', 'last_name', 'email', 'password']

        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Поле {field} обязательно")

        if not self._validate_password_strength(data['password']):
            raise ValueError("Пароль не соответствует требованиям безопасности")

    def _validate_password_strength(self, password: str) -> bool:
        """
        Проверяет надежность пароля.

        Args:
            password: Пароль

        Returns:
            bool: True если пароль надежный
        """
        if len(password) < const.MINIMUM_PASSWORD_LENGTH:
            return False

        if len(password) > const.MAXIMUM_PASSWORD_LENGTH:
            return False

        # Проверка наличия цифр, букв верхнего и нижнего регистра
        has_digit = any(c.isdigit() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)

        return has_digit and has_upper and has_lower

    def _generate_session_id(self, user: Any) -> str:
        """
        Генерирует ID сессии.

        Args:
            user: Пользователь

        Returns:
            str: ID сессии
        """
        timestamp = str(datetime.now().timestamp())
        user_id = user.entity_id
        return sha256(f"{user_id}_{timestamp}".encode()).hexdigest()[:32]

    def _generate_reset_token(self) -> str:
        """
        Генерирует токен сброса пароля.

        Returns:
            str: Токен сброса
        """
        timestamp = str(datetime.now().timestamp())
        return sha256(f"reset_{timestamp}".encode()).hexdigest()[:16]

    # Реализация абстрактных методов BaseService
    def create(self, entity: Any) -> Any:
        """Создает сущность (заглушка для BaseService)."""
        return entity

    def get_by_id(self, entity_id: str) -> Optional[Any]:
        """Получает сущность по ID (заглушка для BaseService)."""
        return None

    def update(self, entity: Any) -> Any:
        """Обновляет сущность (заглушка для BaseService)."""
        return entity

    def delete(self, entity_id: str) -> bool:
        """Удаляет сущность (заглушка для BaseService)."""
        return False

    def get_all(self) -> List[Any]:
        """Получает все сущности (заглушка для BaseService)."""
        return []
