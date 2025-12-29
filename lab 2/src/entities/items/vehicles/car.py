"""
Класс автомобиля.

Этот модуль содержит реализацию автомобиля для аренды.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from .base_vehicle import BaseVehicle, VehicleType, FuelType


@dataclass
class Car(BaseVehicle):
    """
    Класс представляющий автомобиль.

    Attributes:
        transmission: Тип трансмиссии
        drive_type: Тип привода
        engine_size: Объем двигателя
        doors_count: Количество дверей
        has_gps: Есть ли GPS
        has_ac: Есть ли кондиционер
        fuel_level_percent: Уровень топлива в процентах
    """

    transmission: str = "manual"
    drive_type: str = "fwd"
    engine_size: Optional[float] = None  # литры
    doors_count: int = 4
    has_gps: bool = True
    has_ac: bool = True
    fuel_level_percent: float = 100.0

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.vehicle_type = VehicleType.CAR
        self.license_required = True
        self.passenger_capacity = 5
        self.cargo_capacity_kg = 500.0

    def get_car_specs(self) -> Dict[str, Any]:
        """
        Получает спецификации автомобиля.

        Returns:
            Dict[str, Any]: Спецификации автомобиля
        """
        return {
            'transmission': self.transmission,
            'drive_type': self.drive_type,
            'engine_size': self.engine_size,
            'doors_count': self.doors_count,
            'has_gps': self.has_gps,
            'has_ac': self.has_ac,
            'fuel_level_percent': self.fuel_level_percent
        }
