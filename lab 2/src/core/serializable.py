"""
Интерфейс для объектов, которые можно сериализовать.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


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
