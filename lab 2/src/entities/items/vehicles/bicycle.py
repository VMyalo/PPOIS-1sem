"""
Класс велосипеда.

Этот модуль содержит реализацию велосипеда для аренды.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from .base_vehicle import BaseVehicle, VehicleType, FuelType


@dataclass
class Bicycle(BaseVehicle):
    """
    Класс представляющий велосипед.

    Attributes:
        frame_size: Размер рамы
        gear_count: Количество передач
        has_basket: Есть ли корзина
        has_lights: Есть ли фары
        tire_size: Размер шин
        brake_type: Тип тормозов
    """

    frame_size: str = "M"
    gear_count: int = 1
    has_basket: bool = False
    has_lights: bool = True
    tire_size: str = "26\""
    brake_type: str = "rim"

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.vehicle_type = VehicleType.BICYCLE
        self.fuel_type = FuelType.ELECTRIC  # велосипеду топливо не нужно
        self.license_required = False
        self.max_speed_kmh = 25

    def get_bike_specs(self) -> Dict[str, Any]:
        """
        Получает спецификации велосипеда.

        Returns:
            Dict[str, Any]: Спецификации велосипеда
        """
        return {
            'frame_size': self.frame_size,
            'gear_count': self.gear_count,
            'has_basket': self.has_basket,
            'has_lights': self.has_lights,
            'tire_size': self.tire_size,
            'brake_type': self.brake_type
        }
