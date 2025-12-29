"""
Базовые классы для системы аренды.

Этот модуль содержит основные базовые классы для сущностей и сервисов системы.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar, Generic
from uuid import uuid4
from decimal import Decimal

from .identifiable import Identifiable
from .validatable import Validatable
from .serializable import Serializable

T = TypeVar('T')


@dataclass
class BaseEntity(Identifiable, Validatable, Serializable):
    """
    Базовый класс для всех сущностей в системе.

    Этот класс предоставляет общую функциональность для всех объектов предметной области,
    включая уникальную идентификацию, валидацию и сериализацию.

    Attributes:
        entity_id: Уникальный идентификатор сущности
        created_at: Временная метка создания сущности
        updated_at: Временная метка последнего обновления сущности
        is_active: Флаг, указывающий, активна ли сущность
    """

    entity_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def __post_init__(self):
        """Инициализация после создания объекта."""
        pass

    @property
    def id(self) -> str:
        """Возвращает уникальный идентификатор сущности."""
        return self.entity_id

    def generate_id(self) -> str:
        """Генерирует новый уникальный идентификатор."""
        self.entity_id = str(uuid4())
        return self.entity_id

    def validate(self) -> bool:
        """
        Проверяет корректность состояния сущности.

        Returns:
            bool: True, если проверка пройдена, иначе False
        """
        return len(self.get_validation_errors()) == 0

    def get_validation_errors(self) -> List[str]:
        """
        Возвращает список ошибок валидации.

        Returns:
            List[str]: Список сообщений об ошибках валидации
        """
        errors = []

        if not self.entity_id:
            errors.append("Идентификатор сущности не может быть пустым")

        if self.created_at > datetime.now():
            errors.append("Дата создания не может быть в будущем")

        if self.updated_at < self.created_at:
            errors.append("Дата обновления не может быть раньше даты создания")

        return errors

    def update_timestamp(self) -> None:
        """Обновляет временную метку updated_at до текущего времени."""
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует сущность в словарь.

        Returns:
            Dict[str, Any]: Словарное представление сущности
        """
        return {
            'entity_id': self.entity_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseEntity':
        """
        Создаёт сущность на основе словаря.

        Args:
            data: Словарь с данными сущности

        Returns:
            BaseEntity: Новый экземпляр сущности
        """
        return cls(
            entity_id=data.get('entity_id', str(uuid4())),
            created_at=datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if 'updated_at' in data else datetime.now(),
            is_active=data.get('is_active', True)
        )


class BaseService(Generic[T], ABC):
    """
    Базовый класс для всех сервисов в системе.

    Этот абстрактный класс предоставляет общую функциональность для сервисов,
    включая операции CRUD и валидацию.

    Attributes:
        repository: Репозиторий для сохранения данных
    """

    def __init__(self, repository: Optional['Repository[T]'] = None):
        """
        Инициализирует сервис.

        Args:
            repository: Репозиторий для операций с данными
        """
        self.repository = repository

    @abstractmethod
    def create(self, entity: T) -> T:
        """
        Создаёт новую сущность.

        Args:
            entity: Сущность для создания

        Returns:
            T: Созданная сущность
        """
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Получает сущность по её идентификатору.

        Args:
            entity_id: Уникальный идентификатор сущности

        Returns:
            Optional[T]: Сущность, если найдена, иначе None
        """
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """
        Обновляет существующую сущность.

        Args:
            entity: Сущность для обновления

        Returns:
            T: Обновлённая сущность
        """
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Удаляет сущность по её идентификатору.

        Args:
            entity_id: Уникальный идентификатор сущности

        Returns:
            bool: True, если удаление прошло успешно, иначе False
        """
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """
        Получает все сущности.

        Returns:
            List[T]: Список всех сущностей
        """
        pass


class Repository(Generic[T], ABC):
    """
    Абстрактный интерфейс репозитория для хранения данных.

    Этот интерфейс определяет контракт для операций доступа к данным,
    которые могут быть реализованы различными хранилищами данных.
    """

    @abstractmethod
    def save(self, entity: T) -> T:
        """
        Сохраняет сущность в репозитории.

        Args:
            entity: Сущность для сохранения

        Returns:
            T: Сохранённая сущность
        """
        pass

    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[T]:
        """
        Находит сущность по её идентификатору.

        Args:
            entity_id: Уникальный идентификатор

        Returns:
            Optional[T]: Сущность, если найдена, иначе None
        """
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        """
        Находит все сущности в репозитории.

        Returns:
            List[T]: Список всех сущностей
        """
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Удаляет сущность по её идентификатору.

        Args:
            entity_id: Уникальный идентификатор

        Returns:
            bool: True, если удалено, иначе False
        """
        pass

    @abstractmethod
    def exists(self, entity_id: str) -> bool:
        """
        Проверяет, существует ли сущность с указанным идентификатором.

        Args:
            entity_id: Уникальный идентификатор

        Returns:
            bool: True, если существует, иначе False
        """
        pass