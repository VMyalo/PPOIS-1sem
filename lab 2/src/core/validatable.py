"""
Интерфейс для объектов, которые можно валидировать.
"""

from abc import ABC, abstractmethod
from typing import List


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
