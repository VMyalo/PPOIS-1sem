"""
Интерфейсы системы аренды.

Этот модуль содержит основные интерфейсы, используемые в системе.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Identifiable:
    """
    Интерфейс для объектов с уникальными идентификаторами.

    Определяет контракт для объектов, которые имеют уникальный идентификатор.
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """Получить уникальный идентификатор объекта."""
        pass

    @abstractmethod
    def generate_id(self) -> str:
        """Сгенерировать новый уникальный идентификатор."""
        pass


class Validatable:
    """
    Интерфейс для объектов, которые можно валидировать.

    Определяет контракт для объектов, состояние которых можно проверить.
    """

    @abstractmethod
    def validate(self) -> bool:
        """Валидировать состояние объекта."""
        pass

    @abstractmethod
    def get_validation_errors(self) -> List[str]:
        """Получить список ошибок валидации."""
        pass


class Serializable:
    """
    Интерфейс для объектов, которые можно сериализовать.

    Определяет контракт для объектов, которые можно преобразовать
    в словарь и обратно.
    """

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать объект в словарь."""
        pass

    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> 'Serializable':
        """Создать объект из словаря."""
        pass
