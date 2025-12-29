"""
Интерфейс для объектов с уникальными идентификаторами.
"""

from abc import ABC, abstractmethod


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
