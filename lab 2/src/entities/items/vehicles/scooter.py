"""
Класс скутера.

Этот модуль содержит реализацию скутера для аренды.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from .base_vehicle import BaseVehicle, VehicleType


@dataclass
class Scooter(BaseVehicle):
    """
    Класс представляющий скутер.

    Attributes:
        engine_cc: Объем двигателя в куб.см
        foldable: Складной
        max_load_kg: Максимальная нагрузка
        battery_range_km: Запас хода на батарее
    """

    engine_cc: int = 50
    foldable: bool = False
    max_load_kg: float = 100.0
    battery_range_km: Optional[float] = None

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.vehicle_type = VehicleType.SCOOTER
        self.license_required = False
        self.passenger_capacity = 1

    def get_scooter_specs(self) -> Dict[str, Any]:
        """
        Получает спецификации скутера.

        Returns:
            Dict[str, Any]: Спецификации скутера
        """
        return {
            'engine_cc': self.engine_cc,
            'foldable': self.foldable,
            'max_load_kg': self.max_load_kg,
            'battery_range_km': self.battery_range_km
        }
