"""
Базовый класс для транспортных средств.

Этот модуль содержит базовую реализацию для различных
транспортных средств, доступных для аренды в системе.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from ..base_item import BaseItem, ItemStatus, ItemCondition
from .enums.vehicle_type import VehicleType
from .enums.fuel_type import FuelType
from src.utils import constants as const


@dataclass
class BaseVehicle(BaseItem):
    """
    Базовый класс для всех транспортных средств.

    Attributes:
        vehicle_type: Тип транспортного средства
        fuel_type: Тип топлива
        fuel_capacity_liters: Объем топливного бака
        fuel_efficiency_kml: Расход топлива км/л
        max_speed_kmh: Максимальная скорость
        passenger_capacity: Вместимость пассажиров
        cargo_capacity_kg: Грузоподъемность
        license_required: Требуется ли лицензия
        insurance_required: Требуется ли страховка
        mileage_km: Пробег
        registration_number: Регистрационный номер
        vin: VIN номер
    """

    vehicle_type: VehicleType = VehicleType.BICYCLE
    fuel_type: FuelType = FuelType.PETROL
    fuel_capacity_liters: Optional[float] = None
    fuel_efficiency_kml: Optional[float] = None
    max_speed_kmh: int = 50
    passenger_capacity: int = 1
    cargo_capacity_kg: Optional[float] = None
    license_required: bool = False
    insurance_required: bool = True
    mileage_km: float = 0.0
    registration_number: Optional[str] = None
    vin: Optional[str] = None

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.category = const.CATEGORY_VEHICLES

    def requires_drivers_license(self) -> bool:
        """
        Проверяет требуется ли водительские права.

        Returns:
            bool: True если требуется лицензия
        """
        return self.license_required

    def calculate_fuel_cost(self, distance_km: float, fuel_price_per_liter: float) -> float:
        """
        Рассчитывает стоимость топлива.

        Args:
            distance_km: Расстояние в км
            fuel_price_per_liter: Цена топлива за литр

        Returns:
            float: Стоимость топлива
        """
        if not self.fuel_efficiency_kml or self.fuel_type == FuelType.ELECTRIC:
            return 0.0

        fuel_needed = distance_km / self.fuel_efficiency_kml
        return fuel_needed * fuel_price_per_liter

    def get_vehicle_specs(self) -> Dict[str, Any]:
        """
        Получает спецификации транспортного средства.

        Returns:
            Dict[str, Any]: Спецификации
        """
        return {
            'vehicle_type': self.vehicle_type.value,
            'fuel_type': self.fuel_type.value,
            'max_speed_kmh': self.max_speed_kmh,
            'passenger_capacity': self.passenger_capacity,
            'cargo_capacity_kg': self.cargo_capacity_kg,
            'license_required': self.license_required,
            'insurance_required': self.insurance_required
        }
