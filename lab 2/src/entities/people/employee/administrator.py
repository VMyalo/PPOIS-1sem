"""
Класс администратора системы аренды.

Этот модуль содержит реализацию администратора - сотрудника
с максимальными правами доступа и управления системой.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Any, Set

from .manager import Manager
from src.utils import constants as const


@dataclass
class Administrator(Manager):
    """
    Класс представляющий администратора системы аренды.

    Администратор - это сотрудник с максимальными правами доступа,
    включая управление пользователями, настройками системы и аудитом.

    Attributes:
        system_access_level: Уровень доступа к системе
        last_security_audit: Дата последнего аудита безопасности
        configurations_changed: Количество измененных конфигураций
        users_created: Количество созданных пользователей
        emergency_access_enabled: Экстренный доступ включен
        audit_logs_reviewed: Количество просмотренных логов аудита
        system_alerts_handled: Количество обработанных системных алертов
        backup_operations_performed: Количество выполненных операций резервного копирования
    """

    system_access_level: str = "full"
    last_security_audit: Optional[datetime] = None
    configurations_changed: int = 0
    users_created: int = 0
    emergency_access_enabled: bool = False
    audit_logs_reviewed: int = 0
    system_alerts_handled: int = 0
    backup_operations_performed: int = 0

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        # Автоматически устанавливаем должность как администратор
        if 'admin' not in self.position.lower():
            self.position = f"System Administrator"
        # Устанавливаем максимальные лимиты для администратора
        self.budget_limit = Decimal("100000.00")
        self.approval_limit = Decimal("50000.00")

    def validate(self) -> bool:
        """
        Валидирует данные администратора.

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

        if self.system_access_level not in ['read_only', 'limited', 'full']:
            errors.append("Некорректный уровень доступа к системе")

        if self.configurations_changed < 0:
            errors.append("Количество изменений конфигурации не может быть отрицательным")

        if self.users_created < 0:
            errors.append("Количество созданных пользователей не может быть отрицательным")

        if self.audit_logs_reviewed < 0:
            errors.append("Количество просмотренных логов не может быть отрицательным")

        if self.system_alerts_handled < 0:
            errors.append("Количество обработанных алертов не может быть отрицательным")

        if self.backup_operations_performed < 0:
            errors.append("Количество операций резервного копирования не может быть отрицательным")

        return errors

    def perform_security_audit(self) -> None:
        """Выполняет аудит безопасности системы."""
        self.last_security_audit = datetime.now()
        self.update_timestamp()

    def increment_configurations_changed(self) -> None:
        """Увеличивает счетчик измененных конфигураций."""
        self.configurations_changed += 1
        self.update_timestamp()

    def increment_users_created(self) -> None:
        """Увеличивает счетчик созданных пользователей."""
        self.users_created += 1
        self.update_timestamp()

    def toggle_emergency_access(self) -> None:
        """Переключает экстренный доступ."""
        self.emergency_access_enabled = not self.emergency_access_enabled
        self.update_timestamp()

    def increment_audit_logs_reviewed(self) -> None:
        """Увеличивает счетчик просмотренных логов аудита."""
        self.audit_logs_reviewed += 1
        self.update_timestamp()

    def increment_system_alerts_handled(self) -> None:
        """Увеличивает счетчик обработанных системных алертов."""
        self.system_alerts_handled += 1
        self.update_timestamp()

    def increment_backup_operations(self) -> None:
        """Увеличивает счетчик операций резервного копирования."""
        self.backup_operations_performed += 1
        self.update_timestamp()

    def can_access_system_settings(self) -> bool:
        """
        Проверяет может ли администратор получить доступ к настройкам системы.

        Returns:
            bool: True если может получить доступ
        """
        return self.system_access_level == "full" and self.status.name == "ACTIVE"

    def can_manage_users(self) -> bool:
        """
        Проверяет может ли администратор управлять пользователями.

        Returns:
            bool: True если может управлять
        """
        return self.system_access_level in ["limited", "full"] and self.status.name == "ACTIVE"

    def can_view_audit_logs(self) -> bool:
        """
        Проверяет может ли администратор просматривать логи аудита.

        Returns:
            bool: True если может просматривать
        """
        return self.system_access_level in ["limited", "full"] and self.status.name == "ACTIVE"

    def reset_user_password(self, user_id: str) -> bool:
        """
        Сбрасывает пароль пользователя.

        Args:
            user_id: ID пользователя

        Returns:
            bool: True если пароль сброшен
        """
        if self.can_manage_users():
            # Здесь должна быть логика сброса пароля
            # Для простоты возвращаем True
            self.update_timestamp()
            return True
        return False

    def disable_user_account(self, user_id: str, reason: str) -> bool:
        """
        Отключает учетную запись пользователя.

        Args:
            user_id: ID пользователя
            reason: Причина отключения

        Returns:
            bool: True если учетная запись отключена
        """
        if self.can_manage_users():
            # Здесь должна быть логика отключения учетной записи
            # Для простоты возвращаем True
            self.update_timestamp()
            return True
        return False

    def enable_user_account(self, user_id: str) -> bool:
        """
        Включает учетную запись пользователя.

        Args:
            user_id: ID пользователя

        Returns:
            bool: True если учетная запись включена
        """
        if self.can_manage_users():
            # Здесь должна быть логика включения учетной записи
            # Для простоты возвращаем True
            self.update_timestamp()
            return True
        return False

    def change_system_access_level(self, new_level: str) -> None:
        """
        Изменяет уровень доступа к системе.

        Args:
            new_level: Новый уровень доступа
        """
        if new_level not in ['read_only', 'limited', 'full']:
            raise ValueError("Некорректный уровень доступа")

        self.system_access_level = new_level
        self.update_timestamp()

    def perform_system_backup(self) -> bool:
        """
        Выполняет резервное копирование системы.

        Returns:
            bool: True если резервное копирование выполнено
        """
        if self.can_access_system_settings():
            self.increment_backup_operations()
            return True
        return False

    def get_admin_summary(self) -> Dict[str, Any]:
        """
        Получает сводную информацию об администраторе.

        Returns:
            Dict[str, Any]: Сводная информация
        """
        return {
            'administrator_id': self.employee_id,
            'full_name': self.full_name,
            'system_access_level': self.system_access_level,
            'last_security_audit': self.last_security_audit.isoformat() if self.last_security_audit else None,
            'configurations_changed': self.configurations_changed,
            'users_created': self.users_created,
            'emergency_access_enabled': self.emergency_access_enabled,
            'audit_logs_reviewed': self.audit_logs_reviewed,
            'system_alerts_handled': self.system_alerts_handled,
            'backup_operations_performed': self.backup_operations_performed
        }

    def has_emergency_access(self) -> bool:
        """
        Проверяет включен ли экстренный доступ.

        Returns:
            bool: True если экстренный доступ включен
        """
        return self.emergency_access_enabled

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует администратора в словарь для сериализации.

        Returns:
            Dict[str, Any]: Словарь с данными администратора
        """
        data = super().to_dict()
        data.update({
            'system_access_level': self.system_access_level,
            'last_security_audit': self.last_security_audit.isoformat() if self.last_security_audit else None,
            'configurations_changed': self.configurations_changed,
            'users_created': self.users_created,
            'emergency_access_enabled': self.emergency_access_enabled,
            'audit_logs_reviewed': self.audit_logs_reviewed,
            'system_alerts_handled': self.system_alerts_handled,
            'backup_operations_performed': self.backup_operations_performed
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Administrator':
        """
        Создает администратора из словаря.

        Args:
            data: Словарь с данными администратора

        Returns:
            Administrator: Новый экземпляр администратора
        """
        # Преобразуем строковые значения обратно в соответствующие типы
        if 'last_security_audit' in data and data['last_security_audit']:
            data['last_security_audit'] = datetime.fromisoformat(data['last_security_audit'])

        return cls(**data)
