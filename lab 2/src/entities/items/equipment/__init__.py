"""
Оборудование для аренды.

Этот модуль экспортирует все классы оборудования:
камеры, дроны, спортивное оборудование.
"""

from .base_equipment import BaseEquipment, EquipmentType, PowerSource
from .camera import Camera, CameraType, SensorSize
from .drone import Drone, DroneCategory
from .sport_equipment import SportEquipment, SportType

__all__ = [
    'BaseEquipment',
    'EquipmentType',
    'PowerSource',
    'Camera',
    'CameraType',
    'SensorSize',
    'Drone',
    'DroneCategory',
    'SportEquipment',
    'SportType'
]
