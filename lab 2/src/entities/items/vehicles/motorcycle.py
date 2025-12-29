"""
Класс мотоцикла.

Этот модуль содержит реализацию мотоцикла для аренды.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from .base_vehicle import BaseVehicle, VehicleType


@dataclass
class Motorcycle(BaseVehicle):
    """
    Класс представляющий мотоцикл.

    Attributes:
        engine_cc: Объем двигателя в куб.см
        has_sidecar: Есть ли коляска
        helmet_required: Требуется ли шлем
        bike_type: Тип мотоцикла
    """

    engine_cc: int = 250
    has_sidecar: bool = False
    helmet_required: bool = True
    bike_type: str = "standard"

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.vehicle_type = VehicleType.MOTORCYCLE
        self.license_required = True
        self.passenger_capacity = 2

    def get_motorcycle_specs(self) -> Dict[str, Any]:
        """
        Получает спецификации мотоцикла.

        Returns:
            Dict[str, Any]: Спецификации мотоцикла
        """
        return {
            'engine_cc': self.engine_cc,
            'has_sidecar': self.has_sidecar,
            'helmet_required': self.helmet_required,
            'bike_type': self.bike_type
        }
