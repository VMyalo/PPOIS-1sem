"""
Транспортные средства для аренды.

Этот модуль экспортирует все классы транспортных средств:
автомобили, велосипеды, мотоциклы, скутеры.
"""

from .base_vehicle import BaseVehicle, VehicleType, FuelType
from .car import Car
from .bicycle import Bicycle
from .motorcycle import Motorcycle
from .scooter import Scooter

__all__ = [
    'BaseVehicle',
    'VehicleType',
    'FuelType',
    'Car',
    'Bicycle',
    'Motorcycle',
    'Scooter'
]
