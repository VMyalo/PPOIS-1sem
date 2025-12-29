"""
Протокол для объектов, которые можно отслеживать.
"""

from typing import Dict, List, Any, Optional, Protocol


class Trackable(Protocol):
    """
    Протокол для объектов, которые можно отслеживать.

    Определяет контракт для объектов, состояние которых можно отслеживать.
    """

    def get_current_location(self) -> Optional[Dict[str, float]]:
        """
        Получить текущее местоположение.

        Returns:
            Optional[Dict[str, float]]: Координаты местоположения
        """
        ...

    def update_location(self, latitude: float, longitude: float) -> None:
        """
        Обновить местоположение.

        Args:
            latitude: Широта
            longitude: Долгота
        """
        ...

    def get_tracking_history(self) -> List[Dict[str, Any]]:
        """
        Получить историю отслеживания.

        Returns:
            List[Dict[str, Any]]: История перемещений
        """
        ...
